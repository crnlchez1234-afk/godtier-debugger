import time

def slow_sum_squares(n: int) -> int:
    """
    Calculates the sum of squares up to n.
    """
    print(f"Calculando suma de cuadrados para {n}...")
    # Simulación de lentitud
    time.sleep(0.1) 
    res = 0
    for i in range(n):
        res += i * i
    return res

def main():
    print("--- Programa Lento v2.0 ---")
    val = 10
    res = slow_sum_squares(val)
    print(f"Resultado final: {res}")

if __name__ == "__main__":
    main()
