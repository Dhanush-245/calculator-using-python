"""A simple command-line calculator."""


def add(left, right):
    return left + right


def subtract(left, right):
    return left - right


def multiply(left, right):
    return left * right


def divide(left, right):
    if right == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return left / right


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def read_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def read_operation():
    choices = ", ".join(OPERATIONS)
    while True:
        operation = input(f"Choose an operation ({choices}): ").strip()
        if operation in OPERATIONS:
            return operation
        print("Please choose one of the listed operations.")


def calculate():
    print("Python Calculator")
    print("Enter two numbers and choose an operation.")

    while True:
        first_number = read_number("First number: ")
        operation = read_operation()
        second_number = read_number("Second number: ")

        try:
            result = OPERATIONS[operation](first_number, second_number)
        except ZeroDivisionError as error:
            print(error)
        else:
            print(f"Result: {result}")

        again = input("Calculate again? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    calculate()
