# HexRaysPyTools Test Suite

## Overview

This directory contains unit tests for HexRaysPyTools plugin, focusing on IDA Pro version compatibility.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── test_ida_compat.py       # Compatibility layer tests
└── README.md                # This file
```

## Running Tests

### Using unittest (Python standard library)

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run specific test file
python -m unittest tests.test_ida_compat

# Run specific test class
python -m unittest tests.test_ida_compat.TestIdaCompatIDA7

# Run specific test method
python -m unittest tests.test_ida_compat.TestIdaCompatIDA7.test_get_idati_ida7
```

### Using pytest (recommended)

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=HexRaysPyTools --cov-report=html tests/

# Run specific test file
pytest tests/test_ida_compat.py

# Run with verbose output
pytest -v tests/
```

## Test Coverage

### ida_compat.py
- ✅ `get_idati()` - IDA 7.x fallback
- ✅ `get_idati()` - IDA 9.x+ behavior
- ✅ `inf_is_64bit()` - IDA 7.x fallback
- ✅ `inf_is_64bit()` - IDA 9.x+ behavior
- ✅ `inf_get_procname()` - IDA 7.x fallback
- ✅ `inf_get_procname()` - IDA 9.x+ behavior
- ✅ Return type validation

## Test Categories

### 1. TestIdaCompatIDA7
Tests compatibility layer behavior when IDA 7.x APIs are present.

### 2. TestIdaCompatIDA9
Tests compatibility layer behavior when IDA 9.x+ APIs are present.

### 3. TestIdaCompatReturnTypes
Tests that all compatibility functions return correct types.

## Mocking Strategy

Since IDA Pro APIs are not available in a standard Python environment, tests use:
- `unittest.mock` for mocking IDA modules (`idaapi`, `ida_ida`)
- Dynamic module patching to simulate different IDA versions
- Return type validation to ensure API compatibility

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install pytest pytest-cov
    pytest tests/ --cov=HexRaysPyTools --cov-report=xml
```

## Future Test Additions

Planned test coverage expansion:
- [ ] Integration tests for core modules (const.py, helper.py)
- [ ] Mock-based tests for callbacks
- [ ] Type annotation validation
- [ ] Performance benchmarks
