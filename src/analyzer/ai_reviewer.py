import logging
import os
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY environment variable not set. AI review will use fallback.")

def review_code_with_ai(code: str, model_name: str = "gemini-pro") -> dict:
    """Provides AI-driven code review using Google Gemini or other models.

    Args:
        code (str): The code string to review.
        model_name (str): The name of the AI model to use.

    Returns:
        dict: A dictionary containing AI review result or fallback if API not available.
    """
    
    # Route to local / unified analyzers when requested
    if model_name in ("local", "unified", "codebert"):
        try:
            # import here to avoid circular import at module load
            from src.analyzer.model_integration import get_custom_model_integration

            integration = get_custom_model_integration()
            # Map requested model to integration ids
            if model_name == "codebert":
                res = integration.analyze_with_model(code, "codebert")
            elif model_name == "local":
                res = integration.analyze_with_model(code, "local")
            else:
                res = integration.analyze_with_model(code, "unified")

            # If integration produced an error, fallback
            if not res or res.get("status") != "success":
                logger.info("Integration review unavailable or returned error, using fallback")
                return _fallback_review(code, model_name)

            # Normalize integration result into review-like structure
            # Build a better summary and extract readable suggestions/issues
            result_obj = res.get("result", {}) or {}

            # If the unified analyzer returns a wrapper, unwrap it
            if isinstance(result_obj, dict) and "unified_analysis" in result_obj:
                inner = result_obj.get("unified_analysis")
                if isinstance(inner, dict):
                    # prefer the inner unified_analysis dict
                    result_obj = inner

            # Try common summary fields
            summary_text = (
                result_obj.get("code_snippet")
                or result_obj.get("analysis")
                or result_obj.get("summary")
                or ", ".join(result_obj.get("models_used", []))
                or "Local model analysis"
            )

            suggestions = []
            issues_map = {}
            analyses = result_obj.get("analyses", {}) or {}

            # If analyses is empty but result_obj itself contains an 'analysis' string
            # (e.g., local model returned a single text blob), treat that as a single analysis
            if not analyses and isinstance(result_obj.get("analysis"), str):
                analyses = {res.get("model", "local"): {"analysis": result_obj.get("analysis")}}

            def _extract_from_text(text: str):
                """Heuristic extraction: split analysis text into summary, suggestions, issues."""
                s_list = []
                i_list = []
                if not text:
                    return s_list, i_list

                # Normalize
                text = text.strip()

                # If text contains explicit sections, try to parse them
                # Look for lines starting with SUGGESTIONS:, ISSUES:, SUMMARY:
                lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
                current = None
                for ln in lines:
                    up = ln.upper()
                    if up.startswith('SUGGESTIONS:'):
                        current = 'suggestions'
                        continue
                    if up.startswith('ISSUES:'):
                        current = 'issues'
                        continue
                    if up.startswith('SUMMARY:'):
                        current = 'summary'
                        continue

                    if ln.startswith('- ') or ln.startswith('• '):
                        val = ln[2:].strip()
                        if current == 'issues':
                            i_list.append(val)
                        else:
                            s_list.append(val)
                    else:
                        # If no explicit sections, treat short lines as suggestions
                        if current == 'issues':
                            i_list.append(ln)
                        elif current == 'suggestions':
                            s_list.append(ln)
                        else:
                            # fallback: split by sentence punctuation for longer blobs
                            if len(ln) < 300 and (ln.endswith('.') or ln.endswith('!') or ln.endswith('?')):
                                s_list.append(ln)
                            else:
                                # long paragraph: take first sentence as summary, subsequent sentences as suggestions
                                import re
                                parts = re.split(r'(?<=[\.\!\?])\s+', ln)
                                for p in parts:
                                    p = p.strip()
                                    if not p:
                                        continue
                                    if len(s_list) < 5:
                                        s_list.append(p)
                # Heuristic: find lines mentioning 'error', 'bug', 'vulnerab', 'exception'
                for ln in lines:
                    low = ln.lower()
                    if any(k in low for k in ('error', 'bug', 'vulnerab', 'exception', 'issue', 'undefined')):
                        if ln not in i_list:
                            i_list.append(ln)

                return s_list, i_list

            for model_key, model_res in analyses.items():
                # If the model returned a dict with 'insights' or 'analysis', extract them
                if isinstance(model_res, dict):
                    # explicit insights list
                    if "insights" in model_res and isinstance(model_res.get("insights"), (list, tuple)):
                        for it in model_res.get("insights"):
                            if isinstance(it, str) and it:
                                suggestions.append(it)

                    # free-text analysis
                    if "analysis" in model_res and isinstance(model_res.get("analysis"), str):
                        s, i = _extract_from_text(model_res.get("analysis"))
                        suggestions.extend(s)
                        if i:
                            issues_map[model_key] = i

                    # suggestions as list
                    if "suggestions" in model_res and isinstance(model_res.get("suggestions"), (list, tuple)):
                        for it in model_res.get("suggestions"):
                            if isinstance(it, str):
                                suggestions.append(it)

                    # Capture any explicit issues structure
                    if "issues" in model_res:
                        issues_map[model_key] = model_res.get("issues")
                else:
                    # model_res is likely a plain string analysis
                    try:
                        s, i = _extract_from_text(str(model_res))
                        suggestions.extend(s)
                        if i:
                            issues_map[model_key] = i
                    except Exception:
                        suggestions.append("Analysis available")

            # Deduplicate and trim suggestions
            seen = set()
            compact_suggestions = []
            for s in suggestions:
                s_str = (s or "").strip()
                if not s_str:
                    continue
                if s_str in seen:
                    continue
                seen.add(s_str)
                compact_suggestions.append(s_str)
                if len(compact_suggestions) >= 8:
                    break

            quality = result_obj.get("quality_rating") or "N/A"

            return {
                "summary": summary_text,
                "suggestions": compact_suggestions,
                "issues": issues_map,
                "quality_rating": quality,
                "recommendation": f"Results from {res.get('model', model_name)}",
                "model_used": res.get("model", model_name)
            }
        except Exception as e:
            logger.warning(f"Local/unified integration error: {e}")
            return _fallback_review(code, model_name)

    # Use Gemini if API key is available
    if GEMINI_API_KEY and model_name == "gemini-pro":
        return _review_with_gemini(code)
    elif model_name == "gpt-4":
        return _review_with_openai(code)
    elif model_name == "claude":
        return _review_with_claude(code)
    else:
        return _fallback_review(code, model_name)


def _review_with_gemini(code: str) -> dict:
    """Use Google Gemini API for code review."""
    try:
        logger.info("Requesting AI review from Gemini...")
        try:
            import google.generativeai as genai
            # configure if key available
            if GEMINI_API_KEY:
                try:
                    genai.configure(api_key=GEMINI_API_KEY)
                except Exception:
                    logger.debug("Could not configure Gemini client with provided key")
        except Exception as e:
            logger.warning(f"Gemini client not available: {e}")
            return _fallback_review(code, "gemini-pro")
        
        # Use the latest available Gemini model
        model_names = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash', 'gemini-pro']
        model = None
        used_model = None
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                used_model = model_name
                logger.info(f"Using model: {model_name}")
                break
            except Exception as e:
                logger.debug(f"Model {model_name} not available: {e}")
                continue
        
        if not model:
            logger.warning("No Gemini model available, using fallback")
            return _fallback_review(code, "gemini-pro")
        
        prompt = f"""Please review this Python code and provide:
1. A brief summary of what the code does
2. 3-5 specific improvement suggestions (be concise)
3. Any potential bugs or issues
4. Code quality rating (1-10)
5. Overall recommendation

Code to review:
```python
{code}
```

Format your response as follows:
SUMMARY: [brief summary]
SUGGESTIONS: [bullet points]
ISSUES: [potential bugs or concerns]
QUALITY_RATING: [1-10]
RECOMMENDATION: [brief recommendation]"""

        response = model.generate_content(prompt)
        review_text = response.text
        
        # Parse the response
        review_dict = _parse_gemini_response(review_text)
        review_dict["model_used"] = f"Gemini {used_model.split('-')[-1].title()}"
        
        logger.info("Gemini review completed successfully")
        return review_dict
        
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return _fallback_review(code, "gemini-pro")


def _parse_gemini_response(text: str) -> dict:
    """Parse Gemini response into structured format."""
    sections = {
        'summary': '',
        'suggestions': [],
        'issues': '',
        'quality_rating': 'N/A',
        'recommendation': '',
    }
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('SUMMARY:'):
            sections['summary'] = line.replace('SUMMARY:', '').strip()
        elif line.startswith('SUGGESTIONS:'):
            current_section = 'suggestions'
        elif line.startswith('ISSUES:'):
            current_section = 'issues'
            sections['issues'] = line.replace('ISSUES:', '').strip()
        elif line.startswith('QUALITY_RATING:'):
            sections['quality_rating'] = line.replace('QUALITY_RATING:', '').strip()
        elif line.startswith('RECOMMENDATION:'):
            sections['recommendation'] = line.replace('RECOMMENDATION:', '').strip()
        elif line.startswith('- ') or line.startswith('• '):
            if current_section == 'suggestions':
                sections['suggestions'].append(line[2:].strip())
    
    return sections


def _review_with_openai(code: str) -> dict:
    """Use OpenAI GPT-4 API for code review."""
    try:
        from openai import OpenAI
        
        logger.info("Requesting AI review from OpenAI...")
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not set, using fallback")
            return _fallback_review(code, "gpt-4")
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"""Review this Python code and provide:
1. Summary of what it does
2. 3-5 improvement suggestions
3. Any bugs or issues
4. Code quality rating (1-10)

Code:
```python
{code}
```"""
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        review_text = response.choices[0].message.content
        sections = _parse_gemini_response(review_text)
        sections['model_used'] = 'GPT-4'
        
        logger.info("OpenAI review completed successfully")
        return sections
        
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return _fallback_review(code, "gpt-4")


def _review_with_claude(code: str) -> dict:
    """Use Anthropic Claude API for code review."""
    try:
        import anthropic
        
        logger.info("Requesting AI review from Claude...")
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not set, using fallback")
            return _fallback_review(code, "claude")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""Review this Python code and provide:
1. Summary of what it does
2. 3-5 improvement suggestions
3. Any bugs or issues
4. Code quality rating (1-10)

Code:
```python
{code}
```"""
                }
            ]
        )
        
        review_text = message.content[0].text
        sections = _parse_gemini_response(review_text)
        sections['model_used'] = 'Claude 3 Opus'
        
        logger.info("Claude review completed successfully")
        return sections
        
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return _fallback_review(code, "claude")


def _fallback_review(code: str, model_name: str) -> dict:
    """Fallback review when API is not available."""
    logger.info(f"Using fallback review (API not available for {model_name})")
    
    return {
        "summary": "AI review unavailable. Please set up your API key to get real AI-powered code review.",
        "suggestions": [
            "Set up GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY environment variable",
            "Add comprehensive docstrings to functions and classes",
            "Implement robust error handling and validation",
            "Consider adding type hints for better code clarity",
            "Break down complex functions into smaller, focused units"
        ],
        "issues": "API not configured",
        "quality_rating": "Unable to rate",
        "recommendation": "Configure API keys to enable real AI review",
        "model_used": f"{model_name} (Fallback)"
    }
