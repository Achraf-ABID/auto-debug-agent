from src.tools.analyzer import StaticAnalyzer


def test_valid_syntax():
    code = "def hello():\n    print('world')"
    assert StaticAnalyzer.check_syntax(code) is True


def test_invalid_syntax():
    code = "def hello()\n    print('oops')"  # Manque ':'
    assert StaticAnalyzer.check_syntax(code) is False
