import time

def slow_sum_squares(n: int) ->int:
    """
    Calculates the sum of squares up to n.
    """
    return sum(i * i for i in range(n))

def main():
    print("--- Programa Lento v2.0 ---")
    val = 10
    res = slow_sum_squares(val)
    print(f"Resultado final: {res}")

if __name__ == "__main__":
    main()
