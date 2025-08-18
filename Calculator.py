operations = ['+', '-', '*', '/', '%', '**', '//']

while True:
    while True:
        try:
            x = float(input("Enter first number: "))
            y = float(input("Enter second number: "))
            print(f"\nYour operands are: {x}, {y}")
            break  
        except ValueError:
            print("Invalid input. Please enter numbers only.\n")
    print(f"Available operations: {operations}")
    while True:
        op = input("Enter an arithmetic operation: ").strip()
        if op not in operations:
            print("Invalid operation. Try again.")
            continue
        else:
            break
    print(f"\nOperating '{op}' on {x} and {y}...")
    try:
        result = None
        if op == '+':
            result = x + y
        elif op == '-':
            result = x - y
        elif op == '*':
            result = x * y
        elif op == '/':
            result = x / y
        elif op == '//':
            result = x // y
        elif op == '%':
            result = x % y
        elif op == '**':
            result = x ** y

        print(f"Result: {x} {op} {y} = {result:.2f}")
    
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")

    choice = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
    if choice not in ['y', 'yes']:
        print("Exiting calculator. Goodbye!")
        break
    print("-----------------------------")