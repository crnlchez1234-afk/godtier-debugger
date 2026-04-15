import pytest
from src.ai.neurosymbolic_agi_core import SymbolicParser

@pytest.fixture
def parser():
    return SymbolicParser()

def test_parse_logical_expression_rule(parser):
    expr = "IF x > 0 THEN y = 1"
    result = parser.parse_logical_expression(expr)
    assert result['type'] == 'rule'
    assert 'antecedent' in result
    assert 'consequent' in result
    # Note: exact content depends on implementation, checking structure

def test_parse_logical_expression_fact(parser):
    expr = "The sky is blue"
    result = parser.parse_logical_expression(expr)
    assert result['type'] == 'fact'
    assert result['subject'] == 'The sky'
    assert result['predicate'] == 'is blue'

def test_parse_logical_expression_negation(parser):
    expr = "NOT valid"
    result = parser.parse_logical_expression(expr)
    assert result['type'] == 'negation'
    assert 'target' in result

def test_parse_logical_expression_conjunction(parser):
    expr = "A AND B"
    result = parser.parse_logical_expression(expr)
    assert result['type'] == 'conjunction'
    assert len(result['operands']) == 2
