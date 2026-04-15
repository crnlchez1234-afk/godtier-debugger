#!/usr/bin/env python3
"""Script de prueba con errores intencionados"""

def dividir(a, b):
    # Bug: división por cero
    return a / b

def procesar_lista(items):
    # Bug: acceso a índice inexistente
    primero = items[0]
    ultimo = items[999]  # Error si la lista es pequeña
    return primero + ultimo

def main():
    # Test 1: División por cero
    resultado1 = dividir(10, 0)
    print(f"Resultado 1: {resultado1}")
    
    # Test 2: Lista pequeña
    numeros = [1, 2, 3]
    resultado2 = procesar_lista(numeros)
    print(f"Resultado 2: {resultado2}")

if __name__ == "__main__":
    main()
