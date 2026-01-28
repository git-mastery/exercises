# test-module.md

## Overview
Testing utilities for exercise validation.

See [exercise_utils/test.py](../../../exercise_utils/test.py) for implementation.

## Core Classes
- `GitAutograderTestLoader(exercise_name, grade_func)` - Test runner factory
- `GitMasteryHelper` - Repo-smith helper with `create_start_tag()` method
- `assert_output(output, expected_status, expected_comments=[])` - Assertion helper

## Usage Examples
See test files:
- [amateur_detective/test_verify.py](../../../amateur_detective/test_verify.py)
- [grocery_shopping/test_verify.py](../../../grocery_shopping/test_verify.py)

## Loader Pattern
See [amateur_detective/test_verify.py](../../../amateur_detective/test_verify.py) and [grocery_shopping/test_verify.py](../../../grocery_shopping/test_verify.py) for complete examples.
