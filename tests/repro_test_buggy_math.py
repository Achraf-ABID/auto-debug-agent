import pytest


def calculate_average(numbers):
    total = sum(numbers)
    # Bug: Division par zéro potentielle si la liste est vide
    return total / len(numbers)


def is_even(n):
    # Bug: Retourne l'inverse de ce qui est attendu pour les nombres négatifs ou autre logique floue
    return n % 2 == 1  # Devrait être == 0


def test_calculate_average_empty_list_raises_error():
    """Test that calculate_average raises ZeroDivisionError for an empty list."""
    with pytest.raises(ZeroDivisionError):
        calculate_average([])


def test_is_even_positive_even_fails():
    """Test that is_even incorrectly identifies a positive even number as odd/false."""
    # Expected: True, Actual: False
    assert is_even(4)  # This assertion will fail


def test_is_even_positive_odd_fails():
    """Test that is_even incorrectly identifies a positive odd number as even/true."""
    # Expected: False, Actual: True
    assert not is_even(3)  # This assertion will fail


def test_is_even_zero_fails():
    """Test that is_even incorrectly identifies zero as odd/false."""
    # Expected: True, Actual: False
    assert is_even(0)  # This assertion will fail


def test_is_even_negative_even_fails():
    """Test that is_even incorrectly identifies a negative even number as odd/false."""
    # Expected: True, Actual: False
    assert is_even(-2)  # This assertion will fail
