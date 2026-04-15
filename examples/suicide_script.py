
def risky_function(x):
    print(f"Calculando inverso de {x}...")
    return 100 / x

def main():
    print("Inicio del programa suicida...")
    for i in [5, 2, 0, 10]:
        res = risky_function(i)
        print(f"Resultado: {res}")
    print("Fin del programa.")

if __name__ == "__main__":
    main()
