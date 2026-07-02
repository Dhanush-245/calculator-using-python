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


def read_number(prompt, allow_end=False):
    while True:
        value = input(prompt).strip()
        if allow_end and value.lower() == "end":
            return None
        try:
            return float(value)
        except ValueError:
            if allow_end:
                print("Please enter a valid number, or type 'end' to finish.")
            else:
                print("Please enter a valid number.")


def read_operation(allow_end=False):
    choices = ", ".join(OPERATIONS)
    while True:
        operation = input(f"Choose an operation ({choices}): ").strip()
        if allow_end and operation.lower() == "end":
            return None
        if operation in OPERATIONS:
            return operation
        if allow_end:
            print("Please choose one of the listed operations, or type 'end' to finish.")
        else:
            print("Please choose one of the listed operations.")


def calculate():
    print("Python Calculator")
    print("Start with a number, then keep adding operations and numbers.")
    print("Type 'end' when you are finished.")

    result = read_number("First number: ")

    while True:
        operation = read_operation(allow_end=True)
        if operation is None:
            break

        next_number = read_number("Next number: ", allow_end=True)
        if next_number is None:
            break

        try:
            result = OPERATIONS[operation](result, next_number)
        except ZeroDivisionError as error:
            print(error)
        else:
            print(f"Current result: {result}")

    print(f"Final result: {result}")
    print("Goodbye!")


if __name__ == "__main__":
    calculate()
