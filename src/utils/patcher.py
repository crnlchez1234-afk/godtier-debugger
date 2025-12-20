import ast
from pathlib import Path
from typing import Optional

class FuzzyPatcher:
    """
    Robustly patches source files using AST location data instead of string matching.
    Handles indentation and exact line replacement.
    """
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.content = self.file_path.read_text(encoding='utf-8')
        self.lines = self.content.splitlines(keepends=True)
        try:
            self.tree = ast.parse(self.content)
        except SyntaxError:
            self.tree = None

    def replace_function(self, func_name: str, new_code: str) -> bool:
        """
        Replaces a function in the file with new code, preserving indentation.
        Returns True if successful.
        """
        if not self.tree:
            return False

        target_node = None
        # Recursive search for the function definition
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
                target_node = node
                break
        
        if not target_node:
            return False

        # Get line range (1-based to 0-based)
        # start_line is the index of the first line
        # end_line is the index AFTER the last line (for slicing)
        start_line = target_node.lineno - 1
        end_line = target_node.end_lineno
        
        # Determine indentation from the first line of the function
        # (This captures the indentation of the 'def' or the first decorator)
        original_first_line = self.lines[start_line]
        indentation = original_first_line[:len(original_first_line) - len(original_first_line.lstrip())]
        
        # Prepare new code
        new_lines_list = new_code.strip().splitlines()
        
        indented_new_lines = []
        for line in new_lines_list:
            if line.strip():
                indented_new_lines.append(indentation + line + '\n')
            else:
                indented_new_lines.append('\n')
                
        # Replace the lines in the original file content
        self.lines[start_line:end_line] = indented_new_lines
        
        # Write back to disk
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.writelines(self.lines)
            return True
        except Exception as e:
            print(f"   ❌ Patcher Error: {e}")
            return False
