import os

def load_code_from_file(filepath: str) -> str:
    """Loads code content from a specified file path."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found at: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Error reading file {filepath}: {e}")