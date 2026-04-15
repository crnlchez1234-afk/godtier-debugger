import pytest
from unittest.mock import MagicMock, patch
from src.lazarus.engine import lazarus_protect, LazarusEngine

# Mock the global engine instance in the module
@pytest.fixture
def mock_lazarus_engine():
    with patch('src.lazarus.engine._engine') as mock_engine:
        yield mock_engine

def test_lazarus_protect_success(mock_lazarus_engine):
    @lazarus_protect
    def safe_func(x):
        return x * 2
    
    assert safe_func(5) == 10
    mock_lazarus_engine.heal_and_retry.assert_not_called()

def test_lazarus_protect_failure_triggers_heal(mock_lazarus_engine):
    # Setup mock to return a fixed value when healing
    mock_lazarus_engine.heal_and_retry.return_value = 42
    
    @lazarus_protect
    def risky_func():
        raise ValueError("Boom")
    
    result = risky_func()
    
    assert result == 42
    mock_lazarus_engine.heal_and_retry.assert_called_once()
    # Check arguments passed to heal_and_retry
    args = mock_lazarus_engine.heal_and_retry.call_args
    # args[0] is (func, args, kwargs, exception)
    # The function passed to heal_and_retry is the original function, not the wrapper
    assert args[0][0] == risky_func.__wrapped__
    assert isinstance(args[0][3], ValueError)
