import tkinter as tk
import math


class Calculator:
    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title("Python Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        self.expression = ""
        self.display = tk.StringVar(value="0")

        self.create_display()
        self.create_buttons()

        # Keyboard support
        self.root.bind("<Key>", self.keyboard_input)

    # -----------------------------
    # DISPLAY
    # -----------------------------
    def create_display(self):

        display_frame = tk.Frame(
            self.root,
            bg="#202124"
        )

        display_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        screen = tk.Entry(
            display_frame,
            textvariable=self.display,
            font=("Arial", 30),
            justify="right",
            bg="#202124",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        screen.pack(
            fill="both",
            ipady=25,
            padx=10
        )

    # -----------------------------
    # BUTTONS
    # -----------------------------
    def create_buttons(self):

        button_frame = tk.Frame(
            self.root,
            bg="#171717"
        )

        button_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        buttons = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["√", "x²", "0", "."],
            ["(", ")", "^", "="]
        ]

        for row in range(6):
            button_frame.rowconfigure(row, weight=1)

        for column in range(4):
            button_frame.columnconfigure(column, weight=1)

        for row in range(6):

            for column in range(4):

                value = buttons[row][column]

                button = tk.Button(
                    button_frame,
                    text=value,
                    font=("Arial", 18, "bold"),
                    command=lambda v=value: self.button_click(v)
                )

                button.grid(
                    row=row,
                    column=column,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )

    # -----------------------------
    # BUTTON CLICK
    # -----------------------------
    def button_click(self, value):

        if value == "C":
            self.clear()

        elif value == "⌫":
            self.backspace()

        elif value == "=":
            self.calculate()

        elif value == "√":
            self.square_root()

        elif value == "x²":
            self.square()

        elif value == "%":
            self.percentage()

        else:
            self.add_value(value)

    # -----------------------------
    # ADD VALUE
    # -----------------------------
    def add_value(self, value):

        if self.expression == "Error":
            self.expression = ""

        symbols = {
            "×": "*",
            "÷": "/",
            "−": "-",
            "^": "**"
        }

        value = symbols.get(value, value)

        self.expression += value

        self.display.set(self.expression)

    # -----------------------------
    # CLEAR
    # -----------------------------
    def clear(self):

        self.expression = ""
        self.display.set("0")

    # -----------------------------
    # BACKSPACE
    # -----------------------------
    def backspace(self):

        if self.expression:
            self.expression = self.expression[:-1]

        if self.expression:
            self.display.set(self.expression)
        else:
            self.display.set("0")

    # -----------------------------
    # CALCULATE
    # -----------------------------
    def calculate(self):

        if not self.expression:
            return

        try:

            allowed = "0123456789+-*/(). "

            if not all(char in allowed for char in self.expression):
                raise ValueError

            result = eval(
                self.expression,
                {"__builtins__": None},
                {}
            )

            if isinstance(result, float):

                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            self.expression = str(result)
            self.display.set(self.expression)

        except ZeroDivisionError:

            self.expression = "Error"
            self.display.set("Cannot divide by zero")

        except Exception:

            self.expression = "Error"
            self.display.set("Invalid expression")

    # -----------------------------
    # SQUARE ROOT
    # -----------------------------
    def square_root(self):

        try:

            number = float(self.expression)

            if number < 0:
                raise ValueError

            result = math.sqrt(number)

            self.expression = str(
                int(result) if result.is_integer() else result
            )

            self.display.set(self.expression)

        except Exception:

            self.expression = "Error"
            self.display.set("Invalid input")

    # -----------------------------
    # SQUARE
    # -----------------------------
    def square(self):

        try:

            number = float(self.expression)
            result = number ** 2

            self.expression = str(
                int(result) if result.is_integer() else result
            )

            self.display.set(self.expression)

        except Exception:

            self.expression = "Error"
            self.display.set("Invalid input")

    # -----------------------------
    # PERCENTAGE
    # -----------------------------
    def percentage(self):

        try:

            number = float(self.expression)
            result = number / 100

            self.expression = str(result)
            self.display.set(self.expression)

        except Exception:

            self.expression = "Error"
            self.display.set("Invalid input")

    # -----------------------------
    # KEYBOARD
    # -----------------------------
    def keyboard_input(self, event):

        key = event.char

        if key in "0123456789":
            self.add_value(key)

        elif key in "+-*/().":
            self.add_value(key)

        elif key == "^":
            self.add_value("^")

        elif event.keysym == "Return":
            self.calculate()

        elif event.keysym == "BackSpace":
            self.backspace()

        elif event.keysym == "Escape":
            self.clear()


# =================================
# START PROGRAM
# =================================

if __name__ == "__main__":

    root = tk.Tk()

    app = Calculator(root)

    root.mainloop()