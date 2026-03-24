import os
from langchain.tools import tool


@tool
def write_file(input: str) -> str:
    """
    Write content to a file. 
    Input MUST be formatted as: "filename.txt|content to write"
    The filename and content are separated by a pipe character (|).
    Use this tool when you need to save text, results, or any data to a file.
    Example input: "output.txt|Hello, this is the file content."
    """
    try:
        if "|" not in input:
            return (
                "Error: Input must be formatted as 'filename|content'. "
                "Please provide filename and content separated by a pipe '|' character."
            )

        # Split only on the first pipe so content can contain pipes
        filename, content = input.split("|", 1)
        filename = filename.strip()
        content = content.strip()

        if not filename:
            return "Error: Filename cannot be empty."

        # Basic path safety — no directory traversal
        safe_name = os.path.basename(filename)
        if safe_name != filename:
            return (
                f"Error: Filename must not contain directory paths. "
                f"Use '{safe_name}' instead."
            )

        with open(safe_name, "w", encoding="utf-8") as f:
            f.write(content)

        char_count = len(content)
        return (
            f"Successfully wrote {char_count} characters to '{safe_name}'."
        )

    except PermissionError:
        return f"Error: Permission denied when writing to '{filename}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def read_file(filename: str) -> str:
    """
    Read and return the contents of a file.
    Input should be just the filename (e.g., "notes.txt").
    Use this tool when you need to retrieve previously saved information
    or inspect the contents of a file.
    """
    try:
        filename = filename.strip()

        if not filename:
            return "Error: Filename cannot be empty."

        safe_name = os.path.basename(filename)

        if not os.path.exists(safe_name):
            return f"Error: File '{safe_name}' does not exist."

        with open(safe_name, "r", encoding="utf-8") as f:
            content = f.read()

        if not content:
            return f"File '{safe_name}' exists but is empty."

        return f"Contents of '{safe_name}':\n\n{content}"

    except PermissionError:
        return f"Error: Permission denied when reading '{filename}'."
    except Exception as e:
        return f"Error reading file: {str(e)}"
