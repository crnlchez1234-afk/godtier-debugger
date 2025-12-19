from functools import lru_cache
from typing import Any

@lru_cache(maxsize=None)
def fibonacci(n: Any) -> Any:
    if n <= 1:
        return n
    return n * (fibonacci(n-1)) / math.factorial(n-1)

import math 

@lru_cache(maxsize=1024)
def is_prime(n: Any) -> int:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True