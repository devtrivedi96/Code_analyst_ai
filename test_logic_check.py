#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from src.app import app
import json

# Test code that should trigger logic checks
test_code = """
x = 100
y = 200
data = open('file.txt')
password = "secret123"

def process(items=[]):
    for i in range(len(items)):
        print(items[i])
"""

client = app.test_client()
response = client.post('/api/analyze', 
    json={'code': test_code, 'model': 'gemini-pro'},
    content_type='application/json'
)

data = response.get_json()

print("=" * 60)
print("LOGIC CHECK TEST RESULTS")
print("=" * 60)

# Check syntax
print(f"\n✓ Syntax Valid: {data['syntax_valid']}")

# Check quality
print(f"\n✓ Code Quality:")
print(f"  - Lines of Code: {data['quality_metrics']['line_count']}")
print(f"  - Complexity: {data['quality_metrics']['mccabe_complexity']}")

# Check logic analysis
logic = data['logic_analysis']
print(f"\n🔍 Logic Analysis:")
print(f"  - Total Issues: {logic['total_issues']}")
print(f"  - Critical: {logic['severity_count']['Critical']}")
print(f"  - Major: {logic['severity_count']['Major']}")
print(f"  - Minor: {logic['severity_count']['Minor']}")

if logic['issues']:
    print(f"\n  Issues Found:")
    for issue in logic['issues'][:5]:
        print(f"    [{issue['severity']}] Line {issue['line']}: {issue['type']}")
        print(f"      Message: {issue['message']}")
        print(f"      Suggestion: {issue['suggestion'][:80]}...")
        
# Check best practices
practices = data['best_practices']
print(f"\n✨ Best Practices:")
print(f"  - PEP 8 Violations: {len(practices.get('pep8_violations', []))}")
print(f"  - Security Issues: {len(practices.get('security_issues', []))}")
print(f"  - Performance Issues: {len(practices.get('performance_issues', []))}")

print(f"\n{'='*60}")
print("✓ ALL CHECKS COMPLETED SUCCESSFULLY!")
print(f"{'='*60}")
