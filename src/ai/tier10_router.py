"""
🧠 TIER 10 ROUTER — Task Complexity Router
Routes tasks between 'light' and 'beast' categories
based on prompt heuristics. Pure logic, no LLM dependency.
"""


class Tier10Router:
    """
    Routes tasks by complexity.
    'light' = simple fixes, short prompts.
    'beast' = refactors, rewrites, long context.
    """

    def __init__(self):
        self.current_model_type = None

    def decide_model(self, prompt: str, complexity_hint: str = "auto") -> str:
        if complexity_hint != "auto":
            return complexity_hint

        if len(prompt) > 2000:
            return "beast"
        if "architect" in prompt.lower() or "refactor" in prompt.lower() or "rewrite" in prompt.lower():
            return "beast"
        if "complex" in prompt.lower() or "algorithm" in prompt.lower():
            return "beast"

        return "light"

    def load_model(self, model_type: str):
        """No-op. Kept for API compatibility."""
        self.current_model_type = model_type

    def generate(self, prompt: str, complexity: str = "auto", **kwargs) -> str:
        """
        Returns a heuristic-based analysis instead of LLM output.
        """
        target = self.decide_model(prompt, complexity)
        return f"[Tier10Router] Routed to '{target}'. LLM not available — use symbolic analysis."
