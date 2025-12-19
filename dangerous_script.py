import os

def slow_dangerous_function(n):
    print("I am a dangerous function")
    # This should be caught by the safety scanner
    os.system("echo 'Deleting system32...'") 
    return n * n

def main():
    print("--- Dangerous Script ---")
    res = slow_dangerous_function(10)
    print(res)

if __name__ == "__main__":
    main()