def calculate_average(numbers):
    total = sum(numbers)
    # Bug: Division par zéro potentielle si la liste est vide
    return total / len(numbers)

def is_even(n):
    # Bug: Retourne l'inverse de ce qui est attendu pour les nombres négatifs ou autre logique floue
    return n % 2 == 1  # Devrait être == 0