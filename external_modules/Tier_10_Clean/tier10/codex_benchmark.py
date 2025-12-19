import time
import sys
import os
import importlib.util
from typing import Optional, Tuple, Any

def run_benchmark(file_path: str, function_name: str, test_arg: int = 30) -> Tuple[Optional[float], Any, Optional[str]]:
    """
    Ejecuta una función específica de un archivo y mide su tiempo de ejecución.
    Retorna (tiempo_en_segundos, resultado_funcion, error).
    """
    try:
        # Obtener nombre del módulo desde el path
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            return None, None, "No se pudo cargar el módulo"
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Buscar la función
        if not hasattr(module, function_name):
            return None, None, f"Función '{function_name}' no encontrada en {module_name}"
        
        func = getattr(module, function_name)
        
        # Medir tiempo
        print(f"   [BENCHMARK DEBUG] Ejecutando {function_name}({test_arg}) en {module_name}...")
        start_time = time.perf_counter()
        try:
            # Intentamos ejecutar con el argumento
            result = func(test_arg)
            print(f"   [BENCHMARK DEBUG] Resultado: {result}")
        except TypeError:
            # Si falla con argumento, intentamos sin argumentos (por si acaso)
            print(f"   [BENCHMARK DEBUG] Falló con argumento, intentando sin argumentos...")
            start_time = time.perf_counter()
            result = func()
        except Exception as e:
            print(f"   [BENCHMARK DEBUG] Excepción: {e}")
            return None, None, f"Error al ejecutar la función: {e}"
            
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"   [BENCHMARK DEBUG] Duración: {duration:.6f}s")
        
        return duration, result, None

    except Exception as e:
        return None, None, f"Error general en benchmark: {e}"
