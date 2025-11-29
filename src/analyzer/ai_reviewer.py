import logging
import os
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyAmAFvqu13MnqegONw1tvgFepmq-PZa2Zw"
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")
else:
    logger.warning("GEMINI_API_KEY environment variable not set. AI review will use fallback.")

def review_code_with_ai(code: str, model_name: str = "gemini-pro") -> dict:
    """Provides AI-driven code review using Google Gemini or other models.

    Args:
        code (str): The code string to review.
        model_name (str): The name of the AI model to use.

    Returns:
        dict: A dictionary containing AI review result or fallback if API not available.
    """
    
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