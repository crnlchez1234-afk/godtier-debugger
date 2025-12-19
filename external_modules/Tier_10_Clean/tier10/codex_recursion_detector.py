import ast
from typing import List, Dict, Any

class RecursionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.recursive_functions = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.has_recursion = False
        self.has_cache = False
        
        # Check decorators
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id in ['lru_cache', 'cache']:
                self.has_cache = True
            elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id in ['lru_cache', 'cache']:
                self.has_cache = True
            elif isinstance(decorator, ast.Attribute) and decorator.attr in ['lru_cache', 'cache']:
                self.has_cache = True

        # Visit body to find self-calls
        self.generic_visit(node)

        if self.has_recursion:
            self.recursive_functions.append({
                'name': node.name,
                'lineno': node.lineno,
                'has_cache': self.has_cache
            })
        
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name) and node.func.id == self.current_function:
                self.has_recursion = True
        self.generic_visit(node)

def detect_recursion(source_code: str) -> List[Dict[str, Any]]:
    tree = ast.parse(source_code)
    visitor = RecursionVisitor()
    visitor.visit(tree)
    return visitor.recursive_functions
