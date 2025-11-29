import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


class BestPracticesChecker:
    """Checks code against Python and software engineering best practices."""

    def check(self, code: str, model: Optional[str] = None) -> dict:
        """Run all best practices checks.

        Args:
            code: source code to analyze
            model: optional model identifier (e.g. 'gemini-pro', 'custom-codebert')

        Returns:
            dict with checks and model recommendation
        """
        practices = {
            'pep8_violations': self._check_pep8(code),
            'performance_issues': self._check_performance(code),
            'security_issues': self._check_security(code),
            'maintainability': self._check_maintainability(code),
        }

        # Model-aware recommendations
        if model:
            selected = model
            if model.startswith('custom-'):
                model_recommendation = f"Using provided custom model: {model.replace('custom-', '')}"
            else:
                model_recommendation = f"Using selected model: {model}"
        else:
            selected = None
            model_recommendation = (
                "No model selected. For in-depth code embeddings and custom checks, "
                "consider using a trained CodeBERT or a local model (custom-codebert)."
            )

        practices['selected_model'] = selected
        practices['model_recommendation'] = model_recommendation

        logger.info("Best practices check complete")
        return practices

    def _check_pep8(self, code: str) -> list:
        """Check PEP 8 style violations."""
        issues = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 79:
                issues.append({
                    'line': i,
                    'issue': f'Line too long ({len(line)} > 79 characters)',
                    'suggestion': 'Break long lines for readability'
                })

            # Check trailing whitespace
            if line != line.rstrip():
                issues.append({
                    'line': i,
                    'issue': 'Trailing whitespace',
                    'suggestion': 'Remove trailing whitespace'
                })

            # Check multiple statements per line
            if ';' in line and not line.strip().startswith('#'):
                issues.append({
                    'line': i,
                    'issue': 'Multiple statements on one line',
                    'suggestion': 'Put each statement on its own line'
                })

            # Check spacing around operators
            if re.search(r'\w\s{2,}=\s*\w', line):
                issues.append({
                    'line': i,
                    'issue': 'Inconsistent spacing around operators',
                    'suggestion': 'Use single spaces around operators'
                })

        return issues

    def _check_performance(self, code: str) -> list:
        """Check for performance issues."""
        issues = []

        # Check for inefficient operations
        if 'for ' in code and '.append(' in code:
            if 'list(' not in code:
                issues.append({
                    'issue': 'Consider using list comprehension',
                    'suggestion': 'Replace loop with list comprehension for better performance'
                })

        # Check for repeated function calls in loops
        if 'for ' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if 'len(' in line and 'range(len(' in line:
                    issues.append({
                        'line': i + 1,
                        'issue': 'Inefficient range(len()) usage',
                        'suggestion': 'Use enumerate() or direct iteration'
                    })

        # Check for N+1 query patterns
        if 'for ' in code and 'if ' in code:
            issues.append({
                'issue': 'Potential N+1 query pattern',
                'suggestion': 'Consider batching operations outside loops'
            })

        return issues

    def _check_security(self, code: str) -> list:
        """Check for security vulnerabilities."""
        issues = []

        # Check for SQL injection risk
        if 'query' in code.lower() and '+' in code:
            issues.append({
                'issue': 'Potential SQL injection risk',
                'suggestion': 'Use parameterized queries instead of string concatenation'
            })

        # Check for hardcoded credentials
        if re.search(r'(password|api_key|secret)\s*=\s*["\']', code, re.IGNORECASE):
            issues.append({
                'issue': 'Hardcoded credentials found',
                'severity': 'Critical',
                'suggestion': 'Use environment variables for sensitive data'
            })

        # Check for eval usage
        if 'eval(' in code or 'exec(' in code:
            issues.append({
                'issue': 'Dangerous eval() or exec() usage',
                'severity': 'Critical',
                'suggestion': 'Avoid eval/exec. Use safer alternatives like ast.literal_eval()'
            })

        # Check for insecure file permissions
        if 'chmod' in code and '0777' in code:
            issues.append({
                'issue': 'Insecure file permissions',
                'suggestion': 'Use restrictive permissions like 0755 or 0644'
            })

        return issues

    def _check_maintainability(self, code: str) -> list:
        """Check code maintainability."""
        issues = []

        lines = code.split('\n')

        # Check for overly complex conditions
        complex_conditions = [line for line in lines if line.count(' and ') > 3 or line.count(' or ') > 3]
        if complex_conditions:
            issues.append({
                'issue': 'Complex conditional expressions',
                'suggestion': 'Break complex conditions into variables or helper functions'
            })

        # Check for large functions
        if 'def ' in code:
            func_lines = 0
            in_func = False
            for line in lines:
                if line.strip().startswith('def '):
                    in_func = True
                    func_lines = 0
                elif in_func and (line and not line[0].isspace()):
                    if func_lines > 50:
                        issues.append({
                            'issue': 'Large function detected',
                            'suggestion': 'Consider breaking large functions into smaller, focused functions'
                        })
                    in_func = False
                elif in_func:
                    func_lines += 1

        # Check for magic strings
        if re.search(r'["\'][a-zA-Z]{10,}["\']', code):
            issues.append({
                'issue': 'Magic strings found',
                'suggestion': 'Define string constants at module level'
            })

        return issues
