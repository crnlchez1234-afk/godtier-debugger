import ollama
import re
from tier10.config_loader import ConfigLoader

class CodexCortex:
    """
    Corteza Cerebral Real basada en LLM (Ollama).
    Reemplaza las reglas estáticas con razonamiento real.
    """
    def __init__(self, config=None):
        self.config = config or ConfigLoader.load_config()
        self.model = self.config.get('llm', {}).get('model', "llama3.1:8b")
        self.provider = self.config.get('llm', {}).get('provider', "ollama")

    def analyze_and_optimize(self, code: str) -> str:
        """
        Envía el código al LLM para análisis y optimización profunda.
        """
        prompt = f"""
        You are an expert Python Software Engineer focused on performance and logic optimization.
        Analyze the following Python code. Look for:
        1. Algorithmic inefficiencies (e.g., O(n) loops that can be O(1) math).
        2. Missing optimizations (e.g., recursion without memoization).
        3. Security vulnerabilities.

        GOVERNANCE RULES (CRITICAL):
        - RESPECT INTENT: If you see comments like '# Intentional', '# Pausa', or logic that simulates real-world constraints (like time.sleep), DO NOT optimize them away. Preserving business logic is more important than raw speed.
        - VALID SYNTAX: Return ONLY valid, executable Python code. Do not use pseudocode like '...' or placeholders.
        - NO HALLUCINATIONS: Do not invent libraries or syntax that doesn't exist.

        If you find issues, rewrite the code to be optimal. If the code is already optimal or contains intentional delays, return it AS IS.
        
        IMPORTANT:
        - Return ONLY the valid Python code. 
        - Do not add markdown backticks (```).
        - Do not add explanations or text before/after the code.
        - Keep imports if they are needed.
        
        Code to analyze:
        {code}
        """

        try:
            print(f"   🧠 Cortex: Thinking with {self.model} ({self.provider})...")
            
            if self.provider == "ollama":
                response = ollama.chat(model=self.model, messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ])
                optimized_code = response['message']['content']
            
            elif self.provider == "transformers":
                # Lazy import to avoid heavy dependencies if not used
                try:
                    from transformers import AutoModelForCausalLM, AutoTokenizer
                    from peft import PeftModel
                    import torch
                    import json
                    import os
                except ImportError:
                    print("⚠️ Transformers/Torch/Peft not installed. Please run: pip install transformers torch accelerate peft")
                    return code

                # Load model only once
                if not hasattr(self, '_hf_model'):
                    print(f"   ⚙️ Loading local model {self.model}...")
                    try:
                        # Check if it is an adapter
                        is_adapter = os.path.exists(os.path.join(self.model, 'adapter_config.json'))
                        
                        if is_adapter:
                            print(f"   🧩 Detected LoRA Adapter at {self.model}")
                            # Read base model from adapter config
                            with open(os.path.join(self.model, 'adapter_config.json'), 'r') as f:
                                adapter_conf = json.load(f)
                            base_model_id = adapter_conf.get('base_model_name_or_path', 'microsoft/phi-2')
                            
                            print(f"   🏗️ Loading base model: {base_model_id}")
                            self._hf_tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
                            base_model = AutoModelForCausalLM.from_pretrained(
                                base_model_id, 
                                torch_dtype="auto", 
                                trust_remote_code=True,
                                device_map="auto"
                            )
                            print(f"   🔗 Merging adapter...")
                            self._hf_model = PeftModel.from_pretrained(base_model, self.model)
                        else:
                            self._hf_tokenizer = AutoTokenizer.from_pretrained(self.model, trust_remote_code=True)
                            self._hf_model = AutoModelForCausalLM.from_pretrained(
                                self.model, 
                                torch_dtype="auto", 
                                trust_remote_code=True,
                                device_map="auto"
                            )
                    except Exception as load_err:
                        print(f"   ❌ Failed to load model: {load_err}")
                        return code

                # Generate
                inputs = self._hf_tokenizer(prompt, return_tensors="pt", return_attention_mask=False)
                if hasattr(self._hf_model, "device"):
                    inputs = inputs.to(self._hf_model.device)
                
                outputs = self._hf_model.generate(
                    **inputs, 
                    max_new_tokens=512,
                    do_sample=True, 
                    temperature=0.1,
                    top_p=0.9
                )
                full_output = self._hf_tokenizer.batch_decode(outputs)[0]
                
                # Strip the prompt from the output if present
                # Phi-2 and others often include the prompt
                if prompt in full_output:
                    optimized_code = full_output.split(prompt)[-1]
                else:
                    optimized_code = full_output

            else:
                # Placeholder for future providers (OpenAI, Anthropic, etc.)
                print(f"⚠️ Provider {self.provider} not implemented yet. Returning original code.")
                return code
            
            # Clean up potential markdown formatting from LLM
            # Robust extraction of code block
            if "```" in optimized_code:
                match = re.search(r'```(?:python)?\s*(.*?)```', optimized_code, re.DOTALL)
                if match:
                    optimized_code = match.group(1)
            else:
                # Fallback for simple stripping if no blocks found but maybe just backticks
                optimized_code = re.sub(r'^```python\s*', '', optimized_code)
                optimized_code = re.sub(r'^```\s*', '', optimized_code)
                optimized_code = re.sub(r'\s*```$', '', optimized_code)
            
            return optimized_code.strip()

        except Exception as e:
            print(f"   🧠 Cortex Error: {e}")
            return code
