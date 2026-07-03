"""A Tkinter scientific calculator.

Run with:
    python "scientific calculator.py"
"""

import math
import ast
import operator
import tkinter as tk
from tkinter import messagebox


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.resizable(False, False)

        self.expression = ""
        self.angle_mode = tk.StringVar(value="DEG")

        self.display = tk.Entry(
            root,
            font=("Arial", 22),
            borderwidth=8,
            relief=tk.RIDGE,
            justify="right",
            width=24,
        )
        self.display.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

        self.mode_label = tk.Label(root, textvariable=self.angle_mode, font=("Arial", 10, "bold"))
        self.mode_label.grid(row=1, column=0, sticky="ew", padx=5)

        buttons = [
            ("DEG/RAD", self.toggle_angle_mode), ("C", self.clear), ("⌫", self.backspace),
            ("(", lambda: self.add("(")), (")", lambda: self.add(")")), ("/", lambda: self.add("/")),
            ("sin", lambda: self.add_function("sin")), ("cos", lambda: self.add_function("cos")),
            ("tan", lambda: self.add_function("tan")), ("7", lambda: self.add("7")),
            ("8", lambda: self.add("8")), ("9", lambda: self.add("9")),
            ("asin", lambda: self.add_function("asin")), ("acos", lambda: self.add_function("acos")),
            ("atan", lambda: self.add_function("atan")), ("4", lambda: self.add("4")),
            ("5", lambda: self.add("5")), ("6", lambda: self.add("6")),
            ("log", lambda: self.add_function("log10")), ("ln", lambda: self.add_function("log")),
            ("√", lambda: self.add_function("sqrt")), ("1", lambda: self.add("1")),
            ("2", lambda: self.add("2")), ("3", lambda: self.add("3")),
            ("x²", lambda: self.add("**2")), ("xʸ", lambda: self.add("**")),
            ("π", lambda: self.add("pi")), ("0", lambda: self.add("0")),
            (".", lambda: self.add(".")), ("*", lambda: self.add("*")),
            ("e", lambda: self.add("e")), ("!", self.factorial),
            ("%", lambda: self.add("/100")), ("+", lambda: self.add("+")),
            ("-", lambda: self.add("-")), ("=", self.calculate),
        ]

        row = 2
        col = 0
        for text, command in buttons:
            button = tk.Button(
                root,
                text=text,
                command=command,
                font=("Arial", 14),
                width=7,
                height=2,
            )
            button.grid(row=row, column=col, padx=4, pady=4)
            col += 1
            if col == 6:
                col = 0
                row += 1

    def add(self, value):
        self.expression += value
        self.update_display()

    def add_function(self, function_name):
        self.expression += f"{function_name}("
        self.update_display()

    def clear(self):
        self.expression = ""
        self.update_display()

    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def toggle_angle_mode(self):
        self.angle_mode.set("RAD" if self.angle_mode.get() == "DEG" else "DEG")

    def factorial(self):
        try:
            value = self.safe_eval(self.expression)
            if value < 0 or int(value) != value:
                raise ValueError
            self.expression = str(math.factorial(int(value)))
            self.update_display()
        except (ValueError, OverflowError):
            messagebox.showerror("Invalid input", "Factorial only works with non-negative whole numbers.")

    def calculate(self):
        try:
            result = self.safe_eval(self.expression)
            self.expression = str(result)
            self.update_display()
        except ZeroDivisionError:
            messagebox.showerror("Math error", "Cannot divide by zero.")
        except Exception:
            messagebox.showerror("Invalid input", "Please check the expression and try again.")

    def safe_eval(self, expression):
        def to_angle(value):
            return math.radians(value) if self.angle_mode.get() == "DEG" else value

        def from_angle(value):
            return math.degrees(value) if self.angle_mode.get() == "DEG" else value

        allowed_names = {
            "pi": math.pi,
            "e": math.e,
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "sin": lambda x: math.sin(to_angle(x)),
            "cos": lambda x: math.cos(to_angle(x)),
            "tan": lambda x: math.tan(to_angle(x)),
            "asin": lambda x: from_angle(math.asin(x)),
            "acos": lambda x: from_angle(math.acos(x)),
            "atan": lambda x: from_angle(math.atan(x)),
            "abs": abs,
            "round": round,
        }

        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.Name) and node.id in allowed_names:
                value = allowed_names[node.id]
                if callable(value):
                    raise ValueError(f"{node.id} requires parentheses")
                return value
            if isinstance(node, ast.BinOp) and type(node.op) in operators:
                return operators[type(node.op)](evaluate(node.left), evaluate(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
                return operators[type(node.op)](evaluate(node.operand))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                function = allowed_names.get(node.func.id)
                if not callable(function):
                    raise ValueError(f"Unknown function: {node.func.id}")
                if node.keywords:
                    raise ValueError("Keyword arguments are not supported")
                return function(*(evaluate(argument) for argument in node.args))
            raise ValueError("Unsupported expression")

        parsed = ast.parse(expression, mode="eval")
        return evaluate(parsed)


if __name__ == "__main__":
    window = tk.Tk()
    ScientificCalculator(window)
    window.mainloop()
