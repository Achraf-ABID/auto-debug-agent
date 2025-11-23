from src.tools.patcher import Patcher


def test_create_diff():
    original = "a = 1"
    fixed = "a = 2"
    diff = Patcher.create_diff(original, fixed, "test.py")
    assert "--- a/test.py" in diff
    assert "-a = 1" in diff
    assert "+a = 2" in diff
