import pytest
from pathlib import Path
from src.utils.code_upgrade_system import (
    DebugPatternAnalyzer,
    CodeUpgrader,
    AutoCodeUpgradeSystem
)


@pytest.fixture
def analyzer():
    return DebugPatternAnalyzer()


@pytest.fixture
def upgrader(tmp_path):
    return CodeUpgrader(target_dir=tmp_path)


@pytest.fixture
def upgrade_system(tmp_path):
    return AutoCodeUpgradeSystem(code_base_path=tmp_path)


def test_pattern_analyzer_detects_error_handling(analyzer):
    code = """
    try:
        risky_operation()
    except Exception as e:
        handle_error(e)
    """
    result = analyzer.analyze_code_pattern(code)
    
    assert len(result['patterns']) > 0
    pattern_names = [p['name'] for p in result['patterns']]
    assert 'error_handling' in pattern_names


def test_pattern_analyzer_detects_lazarus(analyzer):
    code = """
    from src.lazarus.engine import lazarus_protect
    
    @lazarus_protect
    def auto_healing_function():
        pass
    """
    result = analyzer.analyze_code_pattern(code)
    
    pattern_names = [p['name'] for p in result['patterns']]
    assert 'lazarus_protection' in pattern_names


def test_pattern_analyzer_detects_darwin(analyzer):
    code = """
    from src.darwin.evolver import DarwinEvolver
    
    evolver = DarwinEvolver()
    evolved = evolver.evolve(code)
    """
    result = analyzer.analyze_code_pattern(code)
    
    pattern_names = [p['name'] for p in result['patterns']]
    assert 'darwin_evolution' in pattern_names


def test_upgrader_suggests_improvements(upgrader):
    patterns = [
        {
            'name': 'error_handling',
            'category': 'safety',
            'implementation': 'try-except',
            'source': 'test',
            'relevance': 0.8
        }
    ]
    
    suggestions = upgrader.suggest_upgrades(patterns)
    
    assert len(suggestions) > 0
    assert suggestions[0]['pattern'] == 'error_handling'
    # Priority is 'medium' for relevance 0.8 (needs > 0.8 for 'high')
    assert suggestions[0]['priority'] in ['medium', 'high']


def test_upgrader_dry_run(upgrader):
    suggestion = {
        'pattern': 'error_handling',
        'action': 'add_safety_layer',
        'code_template': '# test code',
        'target_files': ['test.py'],
        'priority': 'high',
        'description': 'Test upgrade'
    }
    
    result = upgrader.apply_upgrade(suggestion, dry_run=True)
    
    assert result['success'] is True
    assert result['dry_run'] is True
    assert len(result['changes']) > 0


def test_upgrade_system_generates_plan(upgrade_system, tmp_path):
    # Create a test Python file
    test_file = tmp_path / "src" / "test.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("""
try:
    something()
except:
    pass
    """)
    
    plan = upgrade_system.generate_upgrade_plan()
    
    assert 'timestamp' in plan
    assert 'patterns_found' in plan
    assert 'suggestions' in plan
    assert isinstance(plan['suggestions'], list)


def test_upgrade_system_estimates_improvements(upgrade_system):
    suggestions = [
        {'pattern': 'error_handling', 'action': 'add'},
        {'pattern': 'unit_testing', 'action': 'add'}
    ]
    
    improvements = upgrade_system._estimate_improvements(suggestions)
    
    assert 'reliability' in improvements
    assert 'test_coverage' in improvements
    assert improvements['reliability'] != '0%'
    assert improvements['test_coverage'] != '0%'


def test_code_template_generation(upgrader):
    template = upgrader._get_code_template('error_handling')
    
    assert 'try:' in template
    assert 'except' in template
    
    template_lazarus = upgrader._get_code_template('lazarus_protection')
    assert 'lazarus_protect' in template_lazarus


def test_full_auto_upgrade_dry_run(upgrade_system, tmp_path):
    # Create test file
    test_file = tmp_path / "src" / "sample.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("""
import logging
logger = logging.getLogger(__name__)

def process():
    logger.debug("Processing")
    """)
    
    summary = upgrade_system.auto_upgrade(dry_run=True)
    
    assert summary['dry_run'] is True
    assert 'plan' in summary
    assert 'results' in summary
    assert summary['total_upgrades'] >= 0
