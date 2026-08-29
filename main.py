import tkinter as tk


# --------------------------------
# COLOR THEME
# --------------------------------

COLOR_BG = "#1e1f29"
COLOR_DISPLAY_BG = "#282a3a"
COLOR_DISPLAY_FG = "#ffffff"
COLOR_TEXT_MUTED = "#8b8fa3"

COLOR_NUMBER_BG = "#323548"
COLOR_NUMBER_HOVER = "#3d4160"
COLOR_NUMBER_FG = "#ffffff"

COLOR_OPERATOR_BG = "#ff9f43"
COLOR_OPERATOR_HOVER = "#ffb976"
COLOR_OPERATOR_FG = "#1e1f29"

COLOR_FUNCTION_BG = "#4a4e69"
COLOR_FUNCTION_HOVER = "#5c6088"
COLOR_FUNCTION_FG = "#ffffff"

COLOR_EQUALS_BG = "#00c896"
COLOR_EQUALS_HOVER = "#33d6ac"
COLOR_EQUALS_FG = "#1e1f29"


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
# BUTTON STYLE HELPERS
# --------------------------------

def style_for(value):
    """Return (bg, hover_bg, fg) colors depending on button type."""

    if value in ("C", "⌫", "%", "( )"):
        return COLOR_FUNCTION_BG, COLOR_FUNCTION_HOVER, COLOR_FUNCTION_FG

    if value in ("÷", "×", "−", "+"):
        return COLOR_OPERATOR_BG, COLOR_OPERATOR_HOVER, COLOR_OPERATOR_FG

    if value == "=":
        return COLOR_EQUALS_BG, COLOR_EQUALS_HOVER, COLOR_EQUALS_FG

    return COLOR_NUMBER_BG, COLOR_NUMBER_HOVER, COLOR_NUMBER_FG


def on_enter(event, hover_color):
    event.widget.configure(bg=hover_color)


def on_leave(event, base_color):
    event.widget.configure(bg=base_color)


# --------------------------------
# MAIN WINDOW
# --------------------------------

root = tk.Tk()

root.title("Calculator")
root.geometry("400x600")
root.minsize(340, 520)
root.configure(bg=COLOR_BG)


# --------------------------------
# DISPLAY AREA
# --------------------------------

display_frame = tk.Frame(root, bg=COLOR_DISPLAY_BG)
display_frame.pack(fill="x", padx=0, pady=0)

mode_label = tk.Label(
    display_frame,
    text="STANDARD",
    font=("Segoe UI", 10, "bold"),
    bg=COLOR_DISPLAY_BG,
    fg=COLOR_TEXT_MUTED,
    anchor="e"
)
mode_label.pack(fill="x", padx=20, pady=(18, 0))

display_var = tk.StringVar()

display = tk.Entry(
    display_frame,
    textvariable=display_var,
    font=("Consolas", 40, "bold"),
    justify="right",
    bd=0,
    relief="flat",
    bg=COLOR_DISPLAY_BG,
    fg=COLOR_DISPLAY_FG,
    insertbackground=COLOR_DISPLAY_FG,
    highlightthickness=0
)

display.pack(
    fill="x",
    padx=20,
    pady=(5, 25),
    ipady=10
)

display.focus_set()


# --------------------------------
# BUTTON FRAME
# --------------------------------

button_frame = tk.Frame(root, bg=COLOR_BG)

button_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=12
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

        base_color, hover_color, fg_color = style_for(value)

        button = tk.Button(
            button_frame,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg=base_color,
            fg=fg_color,
            activebackground=hover_color,
            activeforeground=fg_color,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda value=value: button_click(value)
        )

        button.grid(
            row=row_index,
            column=column_index,
            padx=6,
            pady=6,
            sticky="nsew"
        )

        button.bind("<Enter>", lambda e, h=hover_color: on_enter(e, h))
        button.bind("<Leave>", lambda e, b=base_color: on_leave(e, b))


# --------------------------------
# BIND KEYBOARD
# --------------------------------

root.bind("<Key>", keyboard_input)


# --------------------------------
# RUN APPLICATION
# --------------------------------

root.mainloop()
