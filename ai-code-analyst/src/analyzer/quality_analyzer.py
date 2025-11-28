import logging
from radon.complexity import cc_visit

logger = logging.getLogger(__name__)

def analyze_quality(code: str) -> dict:
    """Analyzes code quality metrics like line count and McCabe complexity.

    Args:
        code (str): The Python code string to analyze.

    Returns:
        dict: A dictionary containing 'line_count' and 'mccabe_complexity'.
    """
    line_count = len(code.splitlines())
    
    mccabe_complexity = 0.0
    try:
        complexity_results = cc_visit(code)
        if complexity_results:
            total_complexity = sum(c.complexity for c in complexity_results)
            mccabe_complexity = total_complexity / len(complexity_results)
        else:
            logger.info("No functions or classes found for McCabe complexity calculation.")
    except Exception as e:
        logger.warning(f"Could not calculate McCabe complexity: {e}")

    logger.info(f"Code Quality Analysis: Line Count={line_count}, McCabe Complexity={mccabe_complexity:.2f}")
    
    return {
        "line_count": line_count,
        "mccabe_complexity": round(mccabe_complexity, 2)
    }