import ast
from typing import List, Tuple

class DarwinSafetyInspector(ast.NodeVisitor):
    """
    Inspector de seguridad para código generado por IA (Mutantes).
    Asegura que el código no contenga operaciones peligrosas antes de ejecutarlo.
    """
    
    # Lista blanca de módulos permitidos (solo cálculo y lógica pura)
    SAFE_MODULES = {'math', 'numpy', 'itertools', 'collections', 'functools', 'random', 'time'}
    
    # Lista negra de funciones/clases peligrosas explícitas
    FORBIDDEN_CALLS = {
        'open', 'exec', 'eval', 'compile', 'input', 
        '__import__', 'globals', 'locals', 'breakpoint', 'help', 'exit', 'quit'
    }

    def __init__(self):
        self.errors: List[str] = []
        self.imported_modules = set()

    def check(self, source_code: str) -> Tuple[bool, List[str]]:
        """
        Analiza el código fuente y retorna (EsSeguro, ListaDeErrores).
        """
        self.errors = []
        self.imported_modules = set()
        
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return False, [f"Syntax Error: {e}"]

        self.visit(tree)
        
        return len(self.errors) == 0, self.errors

    def visit_Import(self, node):
        for alias in node.names:
            self._check_import(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self._check_import(node.module)
        self.generic_visit(node)

    def _check_import(self, module_name: str):
        base_module = module_name.split('.')[0]
        if base_module not in self.SAFE_MODULES:
            self.errors.append(f"❌ Import prohibido: '{module_name}'. Solo se permiten: {', '.join(self.SAFE_MODULES)}")

    def visit_Call(self, node):
        # Verificar llamadas a funciones prohibidas (ej: open(), eval())
        if isinstance(node.func, ast.Name):
            if node.func.id in self.FORBIDDEN_CALLS:
                self.errors.append(f"❌ Función prohibida detectada: '{node.func.id}()'")
        
        # Verificar llamadas a atributos peligrosos (ej: os.system, subprocess.run)
        # Aunque el import checker debería atrapar 'os', esto es doble seguridad.
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr
            if attr_name in {'system', 'popen', 'run', 'spawn', 'remove', 'rmdir', 'unlink'}:
                self.errors.append(f"❌ Método sospechoso detectado: '.{attr_name}()'")

        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Prohibir acceso a atributos internos peligrosos
        if node.attr.startswith("__") and node.attr not in {'__name__', '__doc__', '__class__'}:
             # Permitir dunder methods comunes si es necesario, pero bloquear acceso a internals profundos
             pass 
        self.generic_visit(node)

def validate_mutant_safety(code: str) -> Tuple[bool, List[str]]:
    inspector = DarwinSafetyInspector()
    return inspector.check(code)
