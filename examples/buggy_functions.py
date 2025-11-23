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
