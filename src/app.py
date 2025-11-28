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


@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze code provided in request"""
    try:
        data = request.get_json()
        code = data.get('code', '')
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

        # 3. AI Review
        ai_review = review_code_with_ai(code, model_name=model)

        # Prepare response
        analysis_results = {
            'syntax_valid': syntax_valid,
            'syntax_error': syntax_error,
            'quality_metrics': quality_metrics,
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
