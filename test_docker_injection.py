"""Test pour vérifier l'injection de code dans Docker."""

import base64
import docker

# Code corrigé
fixed_code = """def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

def is_even(n):
    return n % 2 == 0
"""

# Test
test_code = """import pytest

def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

def is_even(n):
    return n % 2 == 0

def test_is_even():
    assert is_even(2) is True
    assert is_even(3) is False
"""

# Encodage
b64_src = base64.b64encode(fixed_code.encode("utf-8")).decode("utf-8")
b64_test = base64.b64encode(test_code.encode("utf-8")).decode("utf-8")

print("Source Base64:", b64_src[:50], "...")
print("Test Base64:", b64_test[:50], "...")

# Commande Docker
cmd = (
    f"/bin/sh -c '"
    f"mkdir -p /app && "
    f"echo {b64_src} | base64 -d > /app/buggy_math.py && "
    f"echo {b64_test} | base64 -d > /app/test_buggy_math.py && "
    f"cat /app/buggy_math.py && "
    f"echo '---TEST---' && "
    f"cat /app/test_buggy_math.py && "
    f"pip install pytest -q > /dev/null && "
    f"cd /app && pytest test_buggy_math.py -v'"
)

print("\nCommande:", cmd[:200], "...")


client = docker.from_env()
container = client.containers.run(
    "python:3.10-slim",
    command=cmd,
    working_dir="/app",
    detach=True,
    mem_limit="512m",
)

container.wait(timeout=45)
logs = container.logs().decode("utf-8")
print("\n=== LOGS ===")
print(logs)
container.remove(force=True)
