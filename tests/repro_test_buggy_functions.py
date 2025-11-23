def factorial(n):
    """Calcule la factorielle de n."""
    if n == 0:
        return 1
    # Bug: devrait être n * factorial(n-1)
    return n + factorial(n - 1)


def fibonacci(n):
    """Retourne le n-ième nombre de Fibonacci."""
    if n <= 1:
        return n
    # Bug: devrait additionner, pas multiplier
    return fibonacci(n - 1) * fibonacci(n - 2)


def max_of_three(a, b, c):
    """Retourne le maximum de trois nombres."""
    # Bug: logique incorrecte
    if a > b:
        return a
    else:
        return c


def reverse_string(s):
    """Inverse une chaîne de caractères."""
    # Bug: ne fait rien
    return s


def count_vowels(text):
    """Compte le nombre de voyelles dans un texte."""
    vowels = "aeiou"
    count = 0
    for char in text.lower():
        # Bug: vérifie si char n'est PAS une voyelle
        if char not in vowels:
            count += 1
    return count


# Test for factorial bug (should fail, 3! is 6, not 7)
def test_factorial_bug():
    assert factorial(3) == 6


# Test for fibonacci bug (should fail, fib(3) is 2, not 0)
def test_fibonacci_bug():
    assert fibonacci(3) == 2


# Test for max_of_three bug (should fail, max of 5, 1, 10 is 10, not 5)
def test_max_of_three_bug_case_one():
    assert max_of_three(5, 1, 10) == 10


# Test for max_of_three bug (should fail, max of 1, 10, 5 is 10, not 5)
def test_max_of_three_bug_case_two():
    assert max_of_three(1, 10, 5) == 10


# Test for reverse_string bug (should fail, 'hello' reversed is 'olleh', not 'hello')
def test_reverse_string_bug():
    assert reverse_string("hello") == "olleh"


# Test for count_vowels bug (should fail, 'hello' has 2 vowels, not 3)
def test_count_vowels_bug_hello():
    assert count_vowels("hello") == 2


# Test for count_vowels bug (should fail, 'AEIOU' has 5 vowels, not 0)
def test_count_vowels_bug_all_vowels():
    assert count_vowels("AEIOU") == 5
