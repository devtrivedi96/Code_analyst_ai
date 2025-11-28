import os
import sys
import argparse
import logging

# Add the project root to the sys.path to allow absolute imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.utils.logger import setup_logging, logger
from src.utils.file_loader import load_code_from_file
from src.utils.constants import DEFAULT_MODEL, REPORT_DIR

from src.analyzer.syntax_checker import check_syntax
from src.analyzer.quality_analyzer import analyze_quality
from src.analyzer.ai_reviewer import review_code_with_ai
from src.analyzer.report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description="AI Code Analyst application.")
    parser.add_argument(
        "code_file",
        type=str,
        help="Path to the Python code file to analyze."
    )
    parser.add_argument(
        "--output_report",
        type=str,
        default=None,
        help="Optional path to save the analysis report. Defaults to 'report_<filename>.md' in a 'reports' directory."
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"AI model to use for review (default: {DEFAULT_MODEL})."
    )

    args = parser.parse_args()

    setup_logging()
    logger.info(f"Starting AI Code Analysis for {args.code_file}")

    analysis_results = {
        "code_file": args.code_file,
        "syntax_valid": False,
        "syntax_error": None,
        "quality_metrics": {},
        "ai_review": {}
    }

    code_content = None
    try:
        code_content = load_code_from_file(args.code_file)
        logger.info("Code loaded successfully.")
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Failed to load code file: {e}")
        sys.exit(1)

    # 1. Syntax Check
    logger.info("Performing syntax check...")
    try:
        is_valid = check_syntax(code_content)
        analysis_results["syntax_valid"] = is_valid
        if not is_valid:
            # The check_syntax function logs the error, no need to duplicate
            logger.error("Syntax check failed.")
            # For simplicity, if syntax fails, we might stop or flag prominently.
            # For now, we'll continue to show other analysis results.
    except Exception as e:
        logger.error(f"Error during syntax check: {e}")
        analysis_results["syntax_valid"] = False
        analysis_results["syntax_error"] = str(e)

    # 2. Quality Analysis
    logger.info("Performing code quality analysis...")
    try:
        quality_metrics = analyze_quality(code_content)
        analysis_results["quality_metrics"] = quality_metrics
        logger.info("Code quality analysis complete.")
    except Exception as e:
        logger.error(f"Error during code quality analysis: {e}")

    # 3. AI Review
    logger.info(f"Performing AI code review using model: {args.model}...")
    try:
        ai_review_results = review_code_with_ai(code_content, model_name=args.model)
        analysis_results["ai_review"] = ai_review_results
        logger.info("AI code review complete.")
    except Exception as e:
        logger.error(f"Error during AI code review: {e}")

    # 4. Generate Report
    logger.info("Generating analysis report...")
    if args.output_report:
        output_file_path = args.output_report
    else:
        # Default report path: reports/report_filename.md
        report_dir = os.path.join(os.getcwd(), REPORT_DIR)
        os.makedirs(report_dir, exist_ok=True)
        filename_without_ext = os.path.splitext(os.path.basename(args.code_file))[0]
        output_file_path = os.path.join(report_dir, f"report_{filename_without_ext}.md")

    try:
        generate_report(analysis_results, output_file_path)
        logger.info(f"Report saved to: {output_file_path}")
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        sys.exit(1)

    logger.info("AI Code Analysis complete.")

if __name__ == "__main__":
    main()