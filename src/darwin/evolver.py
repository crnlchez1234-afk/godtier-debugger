import sys
import inspect
import textwrap
import re
from pathlib import Path
from typing import Callable, Optional, Dict, Any, Tuple

# Import NeuroSys
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI
from src.darwin.benchmarker import ArenaBenchmarker
from src.darwin.memory import GeneMemory
from src.darwin.safety import validate_mutant_safety

class DarwinEvolver:
    def __init__(self):
        self.ai = NeurosysDebuggerAI()
        self.benchmarker = ArenaBenchmarker()
        self.memory = GeneMemory()

    def evolve_function(self, func_name: str, func: Callable, test_args=(), test_kwargs={}, source_code_override: str = None) -> Tuple[Optional[Callable], Optional[str]]:
        """
        Intent to evolve a specific function.
        Returns: (Best Function, Best Source Code)
        """
        print(f"\n🧬 PROJECT DARWIN: Initiating Evolution for '{func_name}'")
        
        # 0. Resolve Source Code (Needed for Memory Lookup)
        source_code = source_code_override
        if not source_code:
            try:
                source_code = inspect.getsource(func)
                source_code = textwrap.dedent(source_code)
            except OSError:
                print("   ❌ Cannot access source code via inspect.")
                return None, None
        
        if not source_code:
             print("   ❌ No source code available.")
             return None, None

        # 1. Check Gene Memory
        cached = self.memory.recall_optimization(func_name, source_code)
        if cached:
            opt_code, speedup = cached
            print(f"   🧠 Gene Memory Recall: Found optimized version (Speedup: {speedup:.2f}x)")
            return None, opt_code

        # 2. Baseline
        print("   📊 Establishing Baseline (Original)...")
        baseline_stats = self.benchmarker.measure_performance(func, test_args, test_kwargs)
        if not baseline_stats["valid"]:
            print(f"   ❌ Original function failed: {baseline_stats.get('error')}")
            return None, None
            
        print(f"      Time: {baseline_stats['avg_time_ns']:.2f} ns | Mem: {baseline_stats['peak_memory_bytes']} bytes")

        # 3. Generate Mutant (Tier 10 Specialist)
        print("   🧪 Generating Mutant (Tier 10 Specialist)...")
        # source_code is already resolved above

        mutant_code = self._generate_mutant_code(source_code)
        if not mutant_code:
            print("   ❌ Failed to generate mutant code.")
            return None, None

        # 3.1 SAFETY CHECK (New Phase 1)
        print("   🛡️ Security Scan: Analyzing Mutant DNA...")
        is_safe, safety_errors = validate_mutant_safety(mutant_code)
        if not is_safe:
            print(f"   ☣️  SECURITY ALERT: Mutant contained dangerous code!")
            for err in safety_errors:
                print(f"      - {err}")
            print("   🔥 Incinerating dangerous mutant.")
            return None, None
        print("   ✅ Scan Passed: No malicious code detected.")

        # 3.2 Compile Mutant
        print("   🏗️ Compiling Mutant...")
        mutant_func = self._compile_mutant(mutant_code, func.__name__, func)
        if not mutant_func:
            print("   ❌ Mutant compilation failed.")
            return None, None

        # 4. Battle Arena (Benchmark)
        print("   ⚔️  ENTERING THE ARENA...")
        mutant_stats = self.benchmarker.measure_performance(mutant_func, test_args, test_kwargs)
        
        if not mutant_stats["valid"]:
            print(f"   ❌ Mutant died in the arena: {mutant_stats.get('error')}")
            return None, None

        # Check Correctness
        if mutant_stats.get('result') != baseline_stats.get('result'):
             print(f"   ⚠️ Mutant produced WRONG result! (Expected: {baseline_stats.get('result')}, Got: {mutant_stats.get('result')})")
             print("   ⚰️ Disqualified for incorrectness.")
             return None, None

        print(f"      Mutant Time: {mutant_stats['avg_time_ns']:.2f} ns | Mem: {mutant_stats['peak_memory_bytes']} bytes")

        # 5. Decision
        # Simple logic: if faster, wins.
        if mutant_stats['avg_time_ns'] < baseline_stats['avg_time_ns']:
            improvement = ((baseline_stats['avg_time_ns'] - mutant_stats['avg_time_ns']) / baseline_stats['avg_time_ns']) * 100
            print(f"   🏆 MUTANT WINS! (🚀 {improvement:.2f}% Faster)")
            print("   🧬 Evolution Successful.")
            
            # Save to Gene Memory
            speedup_factor = baseline_stats['avg_time_ns'] / mutant_stats['avg_time_ns']
            self.memory.save_optimization(func_name, source_code, mutant_code, speedup_factor)
            print("   💾 Saved to Gene Memory.")

            return mutant_func, mutant_code
        else:
            print("   ⚰️ Mutant was weaker. Natural Selection discarded it.")
            return None, None

    def _generate_mutant_code(self, original_code: str) -> Optional[str]:
        """Uses Tier 10 Specialist to optimize code."""
        try:
            if not self.ai.llm_ready:
                print("   ⚠️ AI not ready. Using Mock Mutation (for testing).")
                # Mock optimization: replace sleep or inefficient loops if found
                if "time.sleep" in original_code:
                    return original_code.replace("time.sleep", "# time.sleep optimized out\n    pass #")
                return None

            # --- STYLE LEARNING INJECTION ---
            from src.ai.style_analyzer import StyleAnalyzer
            style_prompt = StyleAnalyzer().get_style_prompt(original_code)
            # --------------------------------

            # Prompt estilo "Completion" para Phi-2
            prompt = f"""{original_code}

# Optimized version of the function above (faster, no sleeps).
{style_prompt}
# IMPORTANT: Return ONLY the function definition. NO usage examples. NO benchmarks.
def"""
            
            # Usamos raw_mode=True para evitar el formato "Instruct:"
            response = self.ai.consult_specialist(prompt, raw_mode=True)
            
            # Si la respuesta empieza con el nombre de la función, le agregamos el def que quitamos/o no
            if not response.strip().startswith("def "):
                 response = "def " + response
                 
            print(f"   🧬 [DEBUG] Raw Mutant DNA: {response[:100]}...") # Debug log
            return self._extract_code(response)
        except Exception as e:
            print(f"   ❌ Error generating mutant code: {e}")
            return None
             
        print(f"   🧬 [DEBUG] Raw Mutant DNA: {response[:100]}...") # Debug log
        return self._extract_code(response)

    def _extract_code(self, text: str) -> Optional[str]:
        """Clean LLM output."""
        code = text
        
        # If it starts with def, it's likely the code we want (Completion mode)
        if text.strip().startswith("def "):
            code = text
        # Otherwise look for markdown
        elif "```python" in text:
            code = text.split("```python")[1].split("```")[0]
        elif "```" in text:
            code = text.split("```")[1].split("```")[0]
            
        # Basic cleanup
        lines = []
        for l in code.split('\n'):
            stripped = l.strip()
            if stripped.startswith('Instruct:') or stripped.startswith('Output:'):
                continue
            if stripped.startswith('Code:'):
                continue
            lines.append(l)
            
        final_code = "\n".join(lines).strip()
        
        # Fallback: If empty, try to find 'def'
        if not final_code and "def " in text:
            final_code = text[text.find("def "):]

        # --- NEW: Truncate until valid AST AND remove top-level calls ---
        import ast
        try:
            tree = ast.parse(final_code)
            # Filter out top-level expressions that are NOT function definitions or imports
            new_body = []
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Import, ast.ImportFrom, ast.ClassDef)):
                    new_body.append(node)
            
            if not new_body:
                # If we filtered everything, maybe it was just a function body without def?
                # Fallback to original truncation logic
                raise SyntaxError("No function definition found")
                
            # Reconstruct code from filtered AST
            import astor
            return astor.to_source(ast.Module(body=new_body, type_ignores=[]))
            
        except (SyntaxError, ImportError):
            # Fallback: Try removing lines from the end (original logic)
            lines = final_code.split('\n')
            for i in range(len(lines) - 1, 0, -1):
                subset = "\n".join(lines[:i])
                try:
                    tree = ast.parse(subset)
                    print(f"   ✂️ [DEBUG] Truncated to {i} lines to fix syntax.")
                    
                    # NOW: Apply the same AST filtering to the truncated subset
                    new_body = []
                    for node in tree.body:
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Import, ast.ImportFrom, ast.ClassDef)):
                            new_body.append(node)
                    
                    if new_body:
                        import astor
                        return astor.to_source(ast.Module(body=new_body, type_ignores=[]))
                    else:
                        return subset # Return subset if filtering fails (better than nothing)
                        
                except (SyntaxError, ImportError):
                    continue
            
        return final_code

    def _compile_mutant(self, code: str, func_name: str, original_func: Callable) -> Optional[Callable]:
        """Compiles string code into a function object."""
        print(f"   🏗️ Compiling Mutant Code:\n---\n{code}\n---")
        try:
            # Create a new namespace
            module_name = getattr(original_func, '__module__', None)
            if module_name and module_name in sys.modules:
                module_dict = sys.modules[module_name].__dict__
            else:
                # Fallback for dynamically created functions (exec)
                module_dict = globals().copy()

            local_scope = {}
            
            # Inject common libraries to avoid ImportErrors
            import numpy as np
            import math
            local_scope['np'] = np
            local_scope['numpy'] = np
            local_scope['math'] = math
            
            # Execute in the original module's context to keep imports
            # WARNING: This executes the code. If the code has top-level calls (like benchmarks), they run NOW.
            exec(code, module_dict, local_scope)
            
            # Try to find the function
            # 1. Look for the original name (if the LLM respected it)
            if func_name in local_scope:
                return local_scope[func_name]
            
            # 2. Look for ANY new callable that wasn't there before
            for key, val in local_scope.items():
                if callable(val) and key not in ['np', 'numpy', 'math']:
                    # Heuristic: It's likely the mutant function
                    return val
            
            return None
        except Exception as e:
            print(f"   ❌ Compilation Error: {e}")
            return None

    def generate_commit_analysis(self, func_name: str, original_code: str, mutant_code: str, speedup: float) -> str:
        """Generates a technical analysis for the git commit message."""
        if not self.ai.llm_ready:
            return f"⚡ Darwin: Optimized '{func_name}' (🚀 {speedup:.2f}% Speedup)\n\nAutomated optimization by Darwin Protocol."

        prompt = f"""
Analyze the following code optimization for function '{func_name}'.

Original:
{original_code}

Optimized:
{mutant_code}

Speedup: {speedup:.2f}%

Task: Generate a Git Commit Message.
Format:
Subject: <Subject Line>
Body: <Technical Explanation>

Commit Message:
Subject:"""
        try:
            analysis = self.ai.consult_specialist(prompt, raw_mode=True)
            # Clean up potential markdown code blocks if the LLM wraps the message
            analysis = analysis.replace("```", "").strip()
            
            # If analysis is empty or error, fallback
            if not analysis or "Error:" in analysis:
                 return f"⚡ Darwin: Optimized '{func_name}' (🚀 {speedup:.2f}% Speedup)\n\nAutomated optimization."
                 
            # Re-attach "Subject:" if it was stripped or not generated
            if not analysis.startswith("Subject:") and not analysis.startswith("feat"):
                analysis = "Subject: " + analysis
                
            return analysis
        except Exception:
            return f"⚡ Darwin: Optimized '{func_name}' (🚀 {speedup:.2f}% Speedup)\n\nAutomated optimization."
