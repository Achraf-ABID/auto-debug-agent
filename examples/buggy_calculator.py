def add(a, b):
    """Additionne deux nombres."""
    return a + b


def subtract(a, b):
    """Soustrait b de a."""
    # Bug: ordre inversé
    return b - a


def multiply(a, b):
    """Multiplie deux nombres."""
    return a * b


def divide(a, b):
    """Divise a par b."""
    # Bug: pas de gestion de division par zéro
    return a / b


def power(base, exponent):
    """Calcule base à la puissance exponent."""
    # Bug: utilise multiplication au lieu de puissance
    return base * exponent


def is_positive(n):
    """Vérifie si un nombre est positif."""
    # Bug: >= au lieu de >
    return n >= 0
