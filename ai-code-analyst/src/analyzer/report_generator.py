
import logging
import json

logger = logging.getLogger(__name__)

def generate_report(analysis_results: dict, output_file: str):
    """Generates a comprehensive report from analysis results and saves it to a file.

    Args:
        analysis_results (dict): A dictionary containing all analysis results.
        output_file (str): The path to the file where the report will be saved.
    """
    report_content = []
    report_content.append('# AI Code Analysis Report\n')
    report_content.append('## Overview\n')

    # Add Syntax Check Results
    syntax_status = 'Passed' if analysis_results.get('syntax_valid', False) else 'Failed'
    report_content.append(f'- **Syntax Check**: {syntax_status}\n')
    if not analysis_results.get('syntax_valid', False) and analysis_results.get('syntax_error'):
        report_content.append(f"  * Error: {analysis_results['syntax_error']}\n")

    # Add Quality Analysis Results
    quality_metrics = analysis_results.get('quality_metrics', {})
    report_content.append('\n## Code Quality Analysis\n')
    report_content.append(f"- **Lines of Code**: {quality_metrics.get('line_count', 'N/A')}\n")
    report_content.append(f"- **McCabe Complexity**: {quality_metrics.get('mccabe_complexity', 'N/A')}\n")

    # Add AI Review Results
    ai_review = analysis_results.get('ai_review', {})
    report_content.append('\n## AI Review\n')
    report_content.append(f"- **Summary**: {ai_review.get('summary', 'No AI review summary available.')}\n")
    if ai_review.get('suggestions'):
        report_content.append('- **Suggestions**:\n')
        for suggestion in ai_review['suggestions']:
            report_content.append(f"  * {suggestion}\n")
    report_content.append(f"- **Severity**: {ai_review.get('severity', 'N/A')}\n")
    report_content.append(f"- **Model Used**: {ai_review.get('model_used', 'N/A')}\n")

    # Add Raw JSON for debugging/completeness
    report_content.append('\n## Raw Analysis Data (JSON)\n')
    report_content.append('```json\n')
    report_content.append(json.dumps(analysis_results, indent=2))
    report_content.append('\n```\n')

    final_report = "".join(report_content)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_report)
        logger.info(f"Analysis report successfully generated and saved to {output_file}")
    except IOError as e:
        logger.error(f"Error writing report to {output_file}: {e}")
