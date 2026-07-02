"""A simple command-line calculator."""

from operator import add, mul, sub, truediv


END_COMMAND = "end"

OPERATIONS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
}


def read_value(prompt, parser, valid_values=None):
    while True:
        value = input(prompt).strip()
        if value.lower() == END_COMMAND:
            return None

        if valid_values is not None and value not in valid_values:
            choices = ", ".join(valid_values)
            print(f"Please choose one of these options: {choices}, or type '{END_COMMAND}'.")
            continue

        try:
            return parser(value)
        except ValueError:
            print(f"Please enter a valid number, or type '{END_COMMAND}'.")


def read_number(prompt):
    return read_value(prompt, float)


def read_operation():
    choices = ", ".join(OPERATIONS)
    return read_value(f"Choose an operation ({choices}): ", str, OPERATIONS)


def calculate():
    print("Python Calculator")
    print("Start with a number, then keep adding operations and numbers.")
    print(f"Type '{END_COMMAND}' when you are finished.")

    result = read_number("First number: ")
    if result is None:
        print("Goodbye!")
        return

    while True:
        operation = read_operation()
        if operation is None:
            break

        next_number = read_number("Next number: ")
        if next_number is None:
            break

        if operation == "/" and next_number == 0:
            print("Cannot divide by zero.")
            continue

        result = OPERATIONS[operation](result, next_number)
        print(f"Current result: {result}")

    print(f"Final result: {result}")
    print("Goodbye!")


if __name__ == "__main__":
    calculate()
