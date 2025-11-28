import pytest
import os
import sys

# Add the project root to the sys.path to allow absolute imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.analyzer.ai_reviewer import review_code_with_ai

def test_ai_review_placeholder():
    """Tests the AI reviewer with sample code and checks for expected output structure."""
    sample_code = 'print("hello")'
    model_name = "test-model"
    review_result = review_code_with_ai(sample_code, model_name=model_name)

    assert isinstance(review_result, dict)
    assert 'summary' in review_result
    assert 'suggestions' in review_result
    assert isinstance(review_result['suggestions'], list)
    assert review_result['model_used'] == model_name