"""
GodTier Debugger PRO Configuration
===================================
Optimized settings for GPU-accelerated debugging with Aurora LLM.
"""

PRO_CONFIG = {
    "version": "1.0.0-PRO",
    "license": "PRO",

    # Aurora LLM Settings
    "aurora": {
        "enabled": True,
        "model": "Qwen2.5-14B-Instruct",
        "adapter": "Aurora_V2_Qwen14B",
        "quantization": "nf4",          # 4-bit for 8GB+ GPUs
        "max_new_tokens": 512,
        "temperature": 0.3,             # Low for precise debugging
        "auto_detect_gpu": True,
        "warmup_on_start": False,       # Load on first query (saves VRAM)
    },

    # Analysis Settings
    "analysis": {
        "use_llm": True,                # Use Aurora for deep analysis
        "fallback_to_heuristic": True,  # If GPU busy, use symbolic
        "max_file_size_kb": 500,        # Skip huge files
        "parallel_analysis": False,     # One file at a time (GPU memory)
    },

    # Dashboard Settings
    "dashboard": {
        "enabled": True,
        "port": 8080,
        "websocket_port": 8081,
        "auto_refresh_seconds": 5,
        "save_html_reports": True,
    },

    # Performance
    "performance": {
        "cache_ast_trees": True,
        "max_workers": 4,
        "gpu_memory_fraction": 0.8,     # Leave 20% for OS
    },
}
