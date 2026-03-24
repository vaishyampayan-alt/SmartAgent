from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Safely evaluate a mathematical expression and return the result.
    Use this tool for any arithmetic, algebra, or numerical calculations.
    Input should be a valid Python math expression string.
    Examples: "2 + 2", "100 * 0.15", "(3 ** 2) + (4 ** 2)", "1000 / 12"
    Supports: +, -, *, /, **, //, %, parentheses, and numeric literals.
    Do NOT use for non-mathematical operations.
    """
    try:
        expression = expression.strip()

        if not expression:
            return "Error: Expression cannot be empty."

        # Allow only safe characters: digits, operators, whitespace, parentheses, dot
        allowed_chars = set("0123456789+-*/().% \t\n")
        for char in expression:
            if char not in allowed_chars:
                return (
                    f"Error: Character '{char}' is not allowed in mathematical "
                    f"expressions. Only numbers and operators (+, -, *, /, **, //, %) "
                    f"are permitted."
                )

        # Evaluate with no builtins and no globals for safety
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307

        # Format: remove trailing zeros for floats that are whole numbers
        if isinstance(result, float) and result.is_integer():
            return f"{expression} = {int(result)}"

        return f"{expression} = {result}"

    except ZeroDivisionError:
        return "Error: Division by zero is undefined."
    except SyntaxError:
        return f"Error: '{expression}' is not a valid mathematical expression."
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
