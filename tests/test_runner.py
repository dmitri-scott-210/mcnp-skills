"""
Main test runner script
Executes all tests and generates coverage report
"""
import pytest
import sys
from pathlib import Path

def run_all_tests():
    """Run complete test suite"""
    
    test_dir = Path(__file__).parent
    
    # Run pytest with coverage
    args = [
        str(test_dir),
        '-v',  # Verbose
        '--tb=short',  # Short traceback
        '-x',  # Stop on first failure (optional)
        '--color=yes',
        f'--cov={test_dir.parent}',  # Coverage for entire project
        '--cov-report=html',
        '--cov-report=term-missing'
    ]
    
    return pytest.main(args)

def run_category_tests(category):
    """Run tests for specific category"""
    test_dir = Path(__file__).parent
    
    category_map = {
        'parsers': 'parsers',
        'utils': 'utils',
        'input_creation': 'skills/test_input_creation.py',
        'input_editing': 'skills/test_input_editing.py',
        'validation': 'skills/test_validation.py',
        'output_analysis': 'skills/test_output_analysis.py',
        'advanced': 'skills/test_advanced.py',
        'utilities': 'skills/test_utilities.py',
        'integration': 'integration'
    }
    
    if category not in category_map:
        print(f"Unknown category: {category}")
        print(f"Available: {list(category_map.keys())}")
        return 1
    
    test_path = test_dir / category_map[category]
    
    args = [
        str(test_path),
        '-v',
        '--tb=short',
        '--color=yes'
    ]
    
    return pytest.main(args)

def quick_smoke_test():
    """Quick smoke test - run subset of fast tests"""
    test_dir = Path(__file__).parent
    
    args = [
        str(test_dir),
        '-v',
        '-k', 'test_parse_simple or test_identity or test_generate_simple',
        '--tb=short',
        '--color=yes'
    ]
    
    return pytest.main(args)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'quick':
            print("Running quick smoke tests...")
            exit_code = quick_smoke_test()
        elif sys.argv[1] == 'category' and len(sys.argv) > 2:
            print(f"Running {sys.argv[2]} tests...")
            exit_code = run_category_tests(sys.argv[2])
        else:
            print("Usage: python test_runner.py [quick|category <name>]")
            exit_code = 1
    else:
        print("Running all tests...")
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
