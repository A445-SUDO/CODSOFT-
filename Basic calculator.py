# ====================================================================
# PROJECT: BASIC ARITHMETIC CALCULATOR
# PURPOSE: A continuous command-line application that performs basic 
#          math operations with built-in error handling.
# ====================================================================

# --- STEP 1: Define Modular Arithmetic Functions ---
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

# --- STEP 2: Main Application Loop ---
while True:
    print("\n" + "="*30)
    print("      ARITHMETIC CALCULATOR   ")
    print("="*30)
    print("Available Operations:")
    print("  + : Addition")
    print("  - : Subtraction")
    print("  * : Multiplication")
    print("  / : Division")
    print("  q : Quit Program")
    print("="*30)

    # 1. Ask user for operation first or check if they want to exit
    op = input("Choose an operation (+, -, *, /) or 'q' to quit: ").strip()

    if op.lower() == 'q':
        print("\nThank you for using the calculator. Goodbye!")
        break

    # Check if the entered operator is valid before asking for numbers
    if op not in ['+', '-', '*', '/']:
        print("Error: Invalid operator chosen! Please try again.")
        continue

    # 2. Use try-except block to handle input errors safely
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        print("-" * 30)
        
        # 3. Decision-making structure to execute corresponding functions
        if op == '+':
            result = add(num1, num2)
            print(f"Result: {num1} + {num2} = {result}")
            
        elif op == '-':
            result = subtract(num1, num2)
            print(f"Result: {num1} - {num2} = {result}")
            
        elif op == '*':
            result = multiply(num1, num2)
            print(f"Result: {num1} * {num2} = {result}")
            
        elif op == '/':
            # Custom error check: prevent division by zero crash
            if num2 == 0:
                print("Error: Division by zero is undefined and not allowed!")
            else:
                result = divide(num1, num2)
                print(f"Result: {num1} / {num2} = {result}")

    except ValueError:
        # Executes if a user inputs alphabetical text instead of numbers
        print("Error: Invalid input! Please enter numbers only.")
