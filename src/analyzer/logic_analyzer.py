import logging
import re
import ast
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class LogicAnalyzer:
    """Analyzes code logic for actual bugs and issues."""

    def __init__(self):
        self.issues = []
        self.suggestions = []

    def analyze(self, code: str) -> List[Dict]:
        """Perform comprehensive logic analysis."""
        self.issues = []
        self.suggestions = []

        # Run ONLY logic-critical checks
        self._check_division_by_zero(code)
        self._check_infinite_loops(code)
        self._check_undefined_variables(code)
        self._check_logic_errors(code)
        self._check_error_handling(code)
        self._check_unreachable_code(code)
        self._check_type_mismatches(code)

        logger.info(f"Logic analysis complete: {len(self.issues)} issues found")

        return self.issues

    def _check_division_by_zero(self, code: str):
        """Check for potential division by zero."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Look for division operations with zero
            if re.search(r'/\s*0(?![0-9])', line) or re.search(r'/\s*0\.0', line):
                self.issues.append({
                    'line': i,
                    'type': 'Division by Zero',
                    'severity': 'Critical',
                    'message': f"Potential division by zero: {line.strip()}",
                    'suggestion': "Check that the divisor is not zero before dividing. Use: if divisor != 0: result = a / divisor"
                })
            
            # Look for variable division that might be zero
            if '/ ' in line and not '/ 0' in line:
                # Check if variable could be zero
                var_match = re.search(r'/\s*(\w+)', line)
                if var_match:
                    var_name = var_match.group(1)
                    # Check if this variable is set to 0 anywhere
                    for check_line in lines:
                        if re.search(rf'{var_name}\s*=\s*0(?![0-9])', check_line):
                            self.issues.append({
                                'line': i,
                                'type': 'Division by Zero Risk',
                                'severity': 'Major',
                                'message': f"Variable '{var_name}' may be zero when dividing: {line.strip()}",
                                'suggestion': f"Add validation: if {var_name} != 0: before division"
                            })
                            break

    def _check_infinite_loops(self, code: str):
        """Check for potential infinite loops."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for 'while True:' without break
            if 'while True:' in line or 'while 1:' in line:
                # Look ahead for break statement
                has_break = False
                for j in range(i, min(i + 20, len(lines))):
                    if 'break' in lines[j]:
                        has_break = True
                        break
                    if lines[j].strip() and not lines[j][0].isspace() and j > i:
                        break
                
                if not has_break:
                    self.issues.append({
                        'line': i,
                        'type': 'Infinite Loop',
                        'severity': 'Critical',
                        'message': f"Infinite loop detected: while True without break",
                        'suggestion': "Add a break condition: while True: ... if condition: break"
                    })
            
            # Check for incrementing loop variable
            if 'for ' in line and 'range(' in line:
                # Check if range(0) or range(-n)
                range_match = re.search(r'range\((-?\d+)\)', line)
                if range_match:
                    range_val = int(range_match.group(1))
                    if range_val <= 0:
                        self.issues.append({
                            'line': i,
                            'type': 'Infinite Loop Risk',
                            'severity': 'Major',
                            'message': f"Loop range is {range_val} - will not execute or loop forever",
                            'suggestion': f"Ensure range has positive value: range({abs(range_val) if range_val < 0 else 1})"
                        })

    def _check_undefined_variables(self, code: str):
        """Check for potentially undefined variables."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return
        
        defined_vars = set()
        used_vars = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_vars.add(target.id)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)
        
        undefined = used_vars - defined_vars - {'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'open', 'True', 'False', 'None'}
        
        for var in undefined:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if var in line and 'def ' not in line:
                    self.issues.append({
                        'line': i,
                        'type': 'Undefined Variable',
                        'severity': 'Critical',
                        'message': f"Variable '{var}' may be undefined: {line.strip()}",
                        'suggestion': f"Define '{var}' before using it: {var} = ..."
                    })
                    break

    def _check_logic_errors(self, code: str):
        """Check for logic errors and faulty conditions."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for always True/False conditions
            if 'if True:' in line or 'if 1:' in line:
                self.issues.append({
                    'line': i,
                    'type': 'Logic Error',
                    'severity': 'Minor',
                    'message': "Condition is always True",
                    'suggestion': "Replace with actual condition or remove if statement"
                })
            
            if 'if False:' in line or 'if 0:' in line or 'if None:' in line:
                self.issues.append({
                    'line': i,
                    'type': 'Logic Error',
                    'severity': 'Minor',
                    'message': "Condition is always False - this code will never execute",
                    'suggestion': "Remove this if block or fix the condition"
                })
            
            # Check for assignment in condition
            if re.search(r'if\s+\w+\s*=\s+', line):
                self.issues.append({
                    'line': i,
                    'type': 'Logic Error',
                    'severity': 'Major',
                    'message': "Assignment '=' used instead of comparison '==' in condition",
                    'suggestion': "Use '==' for comparison: if variable == value:"
                })
            
            # Check for unreachable code after return
            if stripped.startswith('return'):
                if i < len(lines):
                    next_line = lines[i].strip()
                    if next_line and not next_line.startswith('#') and not next_line.startswith('def') and not next_line.startswith('class'):
                        self.issues.append({
                            'line': i + 1,
                            'type': 'Unreachable Code',
                            'severity': 'Major',
                            'message': f"Unreachable code after return: {next_line}",
                            'suggestion': "Move this code before the return statement or remove it"
                        })

    def _check_error_handling(self, code: str):
        """Check for missing error handling on risky operations."""
        lines = code.split('\n')
        dangerous_ops = [
            ('open(', 'file operations'),
            ('json.load', 'JSON parsing'),
            ('requests.', 'network requests'),
            ('int(', 'type conversion'),
            ('float(', 'type conversion'),
            ('[', 'list indexing'),
        ]
        
        for i, line in enumerate(lines, 1):
            if '#' in line:
                line = line[:line.index('#')]
            
            for op, desc in dangerous_ops:
                if op in line:
                    # Check if in try block
                    if i > 1 and 'try:' not in lines[i-2] and 'try:' not in lines[i-1]:
                        if op == 'open(' or op == 'requests.' or op == 'json.load':
                            self.issues.append({
                                'line': i,
                                'type': 'Missing Error Handling',
                                'severity': 'Major',
                                'message': f"Missing error handling for {desc}: {line.strip()}",
                                'suggestion': f"Wrap in try-except:\ntry:\n    {line.strip()}\nexcept Exception as e:\n    logger.error(f'Error: {{e}}')"
                            })

    def _check_unreachable_code(self, code: str):
        """Check for unreachable code."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('return') or stripped.startswith('raise') or stripped == 'break' or stripped == 'continue':
                # Check following lines for code
                for j in range(i, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('#'):
                        if not (next_line.startswith('def ') or next_line.startswith('class ') or next_line.startswith('else') or next_line.startswith('except') or next_line.startswith('finally')):
                            # Check indentation
                            if len(lines[j]) - len(lines[j].lstrip()) <= len(line) - len(line.lstrip()):
                                self.issues.append({
                                    'line': j + 1,
                                    'type': 'Unreachable Code',
                                    'severity': 'Major',
                                    'message': f"Unreachable code: {next_line}",
                                    'suggestion': "Move this code before the return/break statement or remove it"
                                })
                                break

    def _check_type_mismatches(self, code: str):
        """Check for potential type mismatches in operations."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Check for string + number operations
            # Pattern: variable + number or "string" + number
            if '+' in line or '-' in line:
                # Look for string literals being used with numbers
                if re.search(r'["\'].*["\']?\s*[\+\-]\s*\d', line):
                    self.issues.append({
                        'line': i,
                        'type': 'Type Mismatch',
                        'severity': 'Critical',
                        'message': f"Type mismatch: String and number operation: {line.strip()}",
                        'suggestion': "Convert string to number first: int(age) + 5 or use f-strings: f'{age} is the age'"
                    })
                
                # Look for variable that is assigned as string being used with numbers
                var_match = re.search(r'(\w+)\s*\+\s*\d', line)
                if var_match:
                    var_name = var_match.group(1)
                    # Check if this variable was assigned a string
                    for check_line in lines:
                        if re.search(rf'{var_name}\s*=\s*["\']', check_line):
                            self.issues.append({
                                'line': i,
                                'type': 'Type Mismatch',
                                'severity': 'Critical',
                                'message': f"Type mismatch: '{var_name}' is a string but used in numeric operation: {line.strip()}",
                                'suggestion': f"Convert to number: int({var_name}) + 5 or str(5) + {var_name}"
                            })
                            break

    def _count_severities(self) -> Dict[str, int]:

        """Count issues by severity."""
        counts = {'Critical': 0, 'Major': 0, 'Minor': 0}
        for issue in self.issues:
            severity = issue.get('severity', 'Minor')
            if severity in counts:
                counts[severity] += 1
        return counts
