"""
Master Test Runner for GapFinder AI
Executes all unit and integration test suites, returning exit code 0 if all pass.
"""

import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def run_all():
    print("=" * 70)
    print("🧪 Running GapFinder AI Automated Test Suite...")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(BASE_DIR, "tests"), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print(f"🎉 SUCCESS: All {result.testsRun} test cases passed!")
        print("=" * 70)
        return 0
    else:
        print(f"❌ FAILURE: {len(result.failures)} failures, {len(result.errors)} errors out of {result.testsRun} tests.")
        print("=" * 70)
        return 1

if __name__ == '__main__':
    exit_code = run_all()
    sys.exit(exit_code)

