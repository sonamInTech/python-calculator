import tkinter as tk


# --------------------------------
# CALCULATOR FUNCTIONS
# --------------------------------

def format_result(result):
    """Remove .0 from whole number results."""

    if isinstance(result, float) and result.is_integer():
        return str(int(result))

    return str(result)


def button_click(value):
    """Handle calculator button clicks."""

    current = display_var.get()

    # Clear everything
    if value == "C":
        display_var.set("")

    # Delete last character
    elif value == "⌫":
        display_var.set(current[:-1])

    # Percentage
    elif value == "%":
        try:
            if current:
                result = eval_expression(current) / 100
                display_var.set(format_result(result))
        except Exception:
            display_var.set("Error")

    # Parentheses
    elif value == "( )":

        open_count = current.count("(")
        close_count = current.count(")")

        if open_count == close_count:
            display_var.set(current + "(")
        else:
            display_var.set(current + ")")

    # Calculate result
    elif value == "=":
        calculate()

    # Normal numbers and operators
    else:
        display_var.set(current + value)

    # Keep cursor at the end
    display.focus_set()
    display.icursor(tk.END)


def eval_expression(expression):
    """Convert calculator symbols and evaluate expression."""

    expression = expression.replace("÷", "/")
    expression = expression.replace("×", "*")
    expression = expression.replace("−", "-")

    return eval(expression)


def calculate():
    """Calculate and display the result."""

    try:
        expression = display_var.get()

        if expression:
            result = eval_expression(expression)
            display_var.set(format_result(result))

    except ZeroDivisionError:
        display_var.set("Cannot divide by zero")

    except Exception:
        display_var.set("Error")

    display.focus_set()
    display.icursor(tk.END)


# --------------------------------
# KEYBOARD SUPPORT
# --------------------------------

def keyboard_input(event):
    """Handle keyboard input."""

    key = event.keysym

    if key == "Return":
        calculate()

    elif key == "Escape":
        display_var.set("")

    elif key == "BackSpace":
        current = display_var.get()
        display_var.set(current[:-1])

    else:
        character = event.char

        allowed_characters = "0123456789+-*/()."

        if character in allowed_characters:
            current = display_var.get()

            # Convert keyboard operators to calculator symbols
            if character == "*":
                character = "×"
            elif character == "/":
                character = "÷"
            elif character == "-":
                character = "−"

            display_var.set(current + character)

    display.icursor(tk.END)


# --------------------------------
# MAIN WINDOW
# --------------------------------

root = tk.Tk()

root.title("My Calculator")
root.geometry("500x700")
root.minsize(400, 600)


# --------------------------------
# DISPLAY
# --------------------------------

display_var = tk.StringVar()

display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Consolas", 32),
    justify="right"
)

display.pack(
    fill="x",
    padx=15,
    pady=20,
    ipady=20
)

display.focus_set()


# --------------------------------
# BUTTON FRAME
# --------------------------------

button_frame = tk.Frame(root)

button_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# --------------------------------
# BUTTON LAYOUT
# --------------------------------

buttons = [

    ["C", "⌫", "%", "÷"],

    ["7", "8", "9", "×"],

    ["4", "5", "6", "−"],

    ["1", "2", "3", "+"],

    ["( )", "0", ".", "="]
]


# --------------------------------
# MAKE GRID RESPONSIVE
# --------------------------------

for column in range(4):
    button_frame.grid_columnconfigure(
        column,
        weight=1
    )


for row in range(5):
    button_frame.grid_rowconfigure(
        row,
        weight=1
    )


# --------------------------------
# CREATE BUTTONS
# --------------------------------

for row_index, row in enumerate(buttons):

    for column_index, value in enumerate(row):

        button = tk.Button(
            button_frame,
            text=value,
            font=("Consolas", 20),
            command=lambda value=value: button_click(value)
        )

        button.grid(
            row=row_index,
            column=column_index,
            padx=5,
            pady=5,
            sticky="nsew"
        )


# --------------------------------
# BIND KEYBOARD
# --------------------------------

root.bind("<Key>", keyboard_input)


# --------------------------------
# RUN APPLICATION
# --------------------------------

root.mainloop()