import os
import sys
import logging
from flask import Flask, render_template, request, jsonify

# Add the project root to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.analyzer.syntax_checker import check_syntax
from src.analyzer.quality_analyzer import analyze_quality
from src.analyzer.ai_reviewer import review_code_with_ai
from src.analyzer.logic_analyzer import LogicAnalyzer
from src.analyzer.best_practices import BestPracticesChecker
from src.analyzer.model_integration import get_custom_model_integration

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/models', methods=['GET'])
def list_models():
    """Return available cloud + custom models for the frontend selector."""
    try:
        # Cloud models offered by the app
        cloud_models = [
            {"id": "gemini-pro", "name": "Gemini Pro", "type": "cloud"},
            {"id": "gpt-4", "name": "GPT-4", "type": "cloud"},
            {"id": "claude", "name": "Claude", "type": "cloud"}
        ]

        # Custom/local models from integration (lazy init)
        custom = []
        try:
            integration = get_custom_model_integration()
            custom = integration.get_available_models()
        except Exception as e:
            # If integration fails, return cloud-only but log
            logging.getLogger(__name__).warning(f"Custom model integration error: {e}")

        response = {
            "cloud_models": cloud_models,
            "custom_models": custom
        }
        return jsonify(response), 200
    except Exception as e:
        logging.getLogger(__name__).error(f"Error listing models: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze code provided in request"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        # Normalize escaped newlines if the client sent literal "\\n" sequences
        if isinstance(code, str) and "\\n" in code:
            try:
                # Replace literal backslash-n with an actual newline for parsing
                code = code.replace('\\n', "\n")
            except Exception:
                pass
        model = data.get('model', 'gemini-pro')

        if not code.strip():
            return jsonify({'error': 'No code provided'}), 400

        # 1. Syntax Check
        syntax_valid = check_syntax(code)
        syntax_error = None
        if not syntax_valid:
            try:
                compile(code, '<string>', 'exec')
            except SyntaxError as e:
                syntax_error = str(e)

        # 2. Quality Analysis
        quality_metrics = analyze_quality(code)

        # 3. Logic Analysis
        logic_analyzer = LogicAnalyzer()
        logic_issues = logic_analyzer.analyze(code)
        
        # Convert list to proper response format
        logic_analysis = {
            'total_issues': len(logic_issues),
            'issues': logic_issues,
            'severity_count': {
                'Critical': sum(1 for i in logic_issues if i.get('severity') == 'Critical'),
                'Major': sum(1 for i in logic_issues if i.get('severity') == 'Major'),
                'Minor': sum(1 for i in logic_issues if i.get('severity') == 'Minor')
            }
        }

        # 4. Best Practices Check (pass selected model for recommendations)
        practices_checker = BestPracticesChecker()
        try:
            best_practices = practices_checker.check(code, model=model)
        except TypeError:
            # Fallback if older signature: call without model
            best_practices = practices_checker.check(code)

        # 5. AI Review
        ai_review = review_code_with_ai(code, model_name=model)

        # Prepare response
        analysis_results = {
            'syntax_valid': syntax_valid,
            'syntax_error': syntax_error,
            'quality_metrics': quality_metrics,
            'logic_analysis': logic_analysis,
            'best_practices': best_practices,
            'ai_review': ai_review
        }

        logger.info("Code analysis completed successfully")
        return jsonify(analysis_results), 200

    except Exception as e:
        logger.error(f"Error during code analysis: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Only run locally, not on Vercel
    app.run(debug=True, host='0.0.0.0', port=5000)
