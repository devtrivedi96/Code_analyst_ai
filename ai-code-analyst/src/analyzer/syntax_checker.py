import ast
import logging

logger = logging.getLogger(__name__)

def check_syntax(code: str) -> bool:
    """Checks the syntax of the given Python code string.

    Args:
        code (str): The Python code string to check.

    Returns:
        bool: True if syntax is valid, False otherwise.
    """
    try:
        ast.parse(code)
        logger.info("Syntax check passed.")
        return True
    except SyntaxError as e:
        logger.error(f"Syntax error found: {e}")
        return False