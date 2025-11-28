import logging
import re
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class LogicAnalyzer:
    """Analyzes code logic, best practices, and provides improvement suggestions."""

    def __init__(self):
        self.issues = []
        self.suggestions = []

    def analyze(self, code: str) -> Dict:
        """Perform comprehensive logic analysis."""
        self.issues = []
        self.suggestions = []

        # Run all analysis checks
        self._check_variable_naming(code)
        self._check_magic_numbers(code)
        self._check_error_handling(code)
        self._check_code_repetition(code)
        self._check_imports(code)
        self._check_best_practices(code)
        self._check_type_hints(code)
        self._check_docstrings(code)

        logger.info(f"Logic analysis complete: {len(self.issues)} issues found")

        return {
            "total_issues": len(self.issues),
            "issues": self.issues,
            "suggestions": self.suggestions,
            "severity_count": self._count_severities()
        }

    def _check_variable_naming(self, code: str):
        """Check for poor variable naming conventions."""
        lines = code.split('\n')
        
        # Check for single-letter variables (except loops)
        patterns = [
            (r'\b[a-z]\s*=\s*(?!range|len)', 'Single-letter variable (except loop counters)'),
            (r'\b(x|y|z|a|b|c)\s*=\s*\w', 'Unclear variable name'),
        ]
        
        for i, line in enumerate(lines, 1):
            # Skip comments and strings
            if '#' in line:
                line = line[:line.index('#')]
            if '"""' in line or "'''" in line:
                continue
                
            for pattern, message in patterns:
                if re.search(pattern, line):
                    # Exclude loop variables
                    if 'for ' not in line:
                        self.issues.append({
                            'line': i,
                            'type': 'Variable Naming',
                            'severity': 'Minor',
                            'message': f"{message}: {line.strip()}",
                            'suggestion': 'Use descriptive variable names (e.g., user_count instead of x)'
                        })

    def _check_magic_numbers(self, code: str):
        """Check for magic numbers that should be constants."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Skip comments and strings
            if '#' in line:
                line = line[:line.index('#')]
            
            # Find numbers in assignments or comparisons (not in function calls)
            magic_nums = re.findall(r'(?<![a-zA-Z_])(\d{2,})(?![a-zA-Z_])', line)
            
            for num in magic_nums:
                if num not in ['24', '60', '100']:  # Common constants
                    self.issues.append({
                        'line': i,
                        'type': 'Magic Number',
                        'severity': 'Minor',
                        'message': f"Magic number '{num}' found: {line.strip()}",
                        'suggestion': f"Define as constant: {num.upper()}_VALUE = {num}"
                    })

    def _check_error_handling(self, code: str):
        """Check for missing error handling."""
        lines = code.split('\n')
        dangerous_functions = ['open', 'json.load', 'requests.get', 'int(', 'float(']
        
        has_try_except = 'try:' in code and 'except' in code
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            if '#' in line:
                line = line[:line.index('#')]
            
            for func in dangerous_functions:
                if func in line and not any(x in code[max(0, code.find(line)-100):] for x in ['try:', 'except']):
                    self.issues.append({
                        'line': i,
                        'type': 'Error Handling',
                        'severity': 'Major',
                        'message': f"Missing error handling for '{func}': {line.strip()}",
                        'suggestion': f"Wrap in try-except block:\ntry:\n    {line.strip()}\nexcept Exception as e:\n    logger.error(f'Error: {{e}}')"
                    })
                    break

    def _check_code_repetition(self, code: str):
        """Check for repeated code patterns."""
        lines = code.split('\n')
        code_blocks = {}
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                if line in code_blocks:
                    code_blocks[line].append(i)
                else:
                    code_blocks[line] = [i]
        
        for line, occurrences in code_blocks.items():
            if len(occurrences) >= 3 and len(line) > 20:
                self.issues.append({
                    'line': occurrences[0],
                    'type': 'Code Repetition',
                    'severity': 'Major',
                    'message': f"Code repeated {len(occurrences)} times (lines: {', '.join(map(str, occurrences))})",
                    'suggestion': "Extract repeated code into a function to follow DRY principle"
                })

    def _check_imports(self, code: str):
        """Check for unused or problematic imports."""
        lines = code.split('\n')
        imports = []
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                # Extract module name
                parts = line.split()
                if 'import' in parts:
                    idx = parts.index('import')
                    if idx + 1 < len(parts):
                        imports.append((parts[idx+1], i))
        
        # Check for wildcard imports
        if 'import *' in code:
            self.issues.append({
                'line': -1,
                'type': 'Imports',
                'severity': 'Major',
                'message': "Wildcard import found (from module import *)",
                'suggestion': "Import specific items: from module import specific_function, AnotherClass"
            })

    def _check_best_practices(self, code: str):
        """Check for general Python best practices."""
        issues_found = []
        
        # Check for print statements (should use logging)
        if 'print(' in code and 'logging' not in code:
            issues_found.append({
                'type': 'Logging',
                'severity': 'Minor',
                'suggestion': 'Use logging module instead of print() for better control'
            })
        
        # Check for bare except
        if 'except:' in code:
            issues_found.append({
                'type': 'Exception Handling',
                'severity': 'Major',
                'suggestion': 'Avoid bare except clauses. Use except SpecificException: instead'
            })
        
        # Check for mutable default arguments
        if 'def ' in code and '=[]' in code or '={}' in code:
            issues_found.append({
                'type': 'Mutable Defaults',
                'severity': 'Major',
                'suggestion': 'Avoid mutable default arguments. Use None and initialize inside function'
            })
        
        for issue in issues_found:
            self.issues.append({
                'line': -1,
                'type': issue['type'],
                'severity': issue['severity'],
                'message': issue['type'],
                'suggestion': issue['suggestion']
            })

    def _check_type_hints(self, code: str):
        """Check for missing type hints."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Check for function definitions without type hints
            if stripped.startswith('def ') and '->' not in line and 'test' not in line.lower():
                # Extract function params
                if '(' in line and ')' in line:
                    params = line[line.index('(')+1:line.index(')')]
                    if params and ':' not in params:
                        self.issues.append({
                            'line': i,
                            'type': 'Type Hints',
                            'severity': 'Minor',
                            'message': f"Missing type hints in function: {stripped[:50]}...",
                            'suggestion': "Add type hints: def func(param: str) -> int:"
                        })

    def _check_docstrings(self, code: str):
        """Check for missing docstrings."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('def ') and 'test' not in line.lower():
                # Check if next line has docstring
                if i < len(lines):
                    next_line = lines[i].strip() if i < len(lines) else ''
                    if not (next_line.startswith('"""') or next_line.startswith("'''")):
                        self.issues.append({
                            'line': i,
                            'type': 'Documentation',
                            'severity': 'Minor',
                            'message': f"Missing docstring for function: {stripped[:40]}...",
                            'suggestion': 'Add docstring:\n    """Brief description.\n    \n    Args:\n        param: description\n    Returns:\n        description\n    """'
                        })

    def _count_severities(self) -> Dict[str, int]:
        """Count issues by severity."""
        counts = {'Critical': 0, 'Major': 0, 'Minor': 0}
        for issue in self.issues:
            severity = issue.get('severity', 'Minor')
            if severity in counts:
                counts[severity] += 1
        return counts
