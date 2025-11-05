"""
Pytest configuration and shared fixtures
"""
import pytest
import os
from pathlib import Path

@pytest.fixture
def test_data_dir():
    """Path to test data directory"""
    return Path(__file__).parent.parent / "example_files"

@pytest.fixture
def simple_input():
    """Simple MCNP input file content"""
    return """simple - simplest MCNP input
10  0    -1   imp:n=1
20  0     1   imp:n=0

1 so    1.0

sdef
"""

@pytest.fixture
def src1_input(test_data_dir):
    """Load src1.txt example"""
    with open(test_data_dir / "basic_examples" / "src1.txt", 'r') as f:
        return f.read()

@pytest.fixture
def tal01_input(test_data_dir):
    """Load tal01.txt example"""
    with open(test_data_dir / "basic_examples" / "tal01.txt", 'r') as f:
        return f.read()

@pytest.fixture
def all_example_files(test_data_dir):
    """Generator yielding all MCNP example files"""
    for root, dirs, files in os.walk(test_data_dir):
        for file in files:
            if file.endswith(('.txt', '.i', '.inp', '')):
                yield Path(root) / file
