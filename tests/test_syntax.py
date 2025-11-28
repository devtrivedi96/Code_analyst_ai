import pytest
import os
import sys

# Add the project root to the sys.path to allow absolute imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.analyzer.syntax_checker import check_syntax

def test_valid_syntax():
    """Test with valid Python code."""
    valid_code = """
def my_function():
    x = 10
    if x > 5:
        print("Hello")
"""
    assert check_syntax(valid_code) is True

def test_invalid_syntax():
    """Test with invalid Python code."""
    invalid_code = """
def my_function():
    x = 10
    if x > 5
        print("Hello") # Missing colon here
"""
    assert check_syntax(invalid_code) is False

def test_empty_code():
    """Test with empty code string."""
    empty_code = """
"""
    assert check_syntax(empty_code) is True

def test_syntax_with_comments():
    """Test with code containing comments."""
    code_with_comments = """
# This is a comment
def another_function():
    # Another comment
    pass
"""
    assert check_syntax(code_with_comments) is True