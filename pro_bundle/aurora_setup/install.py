"""
Aurora LLM Setup for GodTier Debugger PRO
==========================================
Installs and configures the Aurora LLM bridge for local AI inference.
"""

import subprocess
import sys
from pathlib import Path


def check_gpu():
    """Check if NVIDIA GPU is available."""
    try:
        import torch
        if torch.cuda.is_available():
            name = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"  GPU: {name} ({vram:.0f} GB VRAM)")
            return True
        else:
            print("  WARNING: No CUDA GPU detected. Aurora LLM requires an NVIDIA GPU.")
            return False
    except ImportError:
        print("  PyTorch not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                             "torch", "--index-url", "https://download.pytorch.org/whl/cu128"])
        return check_gpu()


def install_dependencies():
    """Install HuggingFace stack for Aurora LLM."""
    deps = ["transformers", "peft", "accelerate", "bitsandbytes"]
    print(f"  Installing: {', '.join(deps)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + deps,
                         stdout=subprocess.DEVNULL)
    print("  Dependencies installed.")


def verify():
    """Verify Aurora LLM bridge works."""
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ai"))
        from neurosys_debugger_wrapper import NeurosysDebuggerAI
        ai = NeurosysDebuggerAI()
        if ai.llm_ready:
            print("  Aurora LLM: CONNECTED")
        elif ai.ready:
            print("  Symbolic Core: OK (Aurora loading in background...)")
        else:
            print("  WARNING: Core not ready. Check installation.")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    print("=" * 50)
    print("GodTier Debugger PRO - Aurora LLM Setup")
    print("=" * 50)

    print("\n[1/3] Checking GPU...")
    has_gpu = check_gpu()

    if has_gpu:
        print("\n[2/3] Installing LLM dependencies...")
        install_dependencies()
    else:
        print("\n[2/3] Skipping LLM deps (no GPU)")

    print("\n[3/3] Verifying installation...")
    verify()

    print("\n" + "=" * 50)
    print("Setup complete! Use: godtier analyze <file>")
    print("=" * 50)


if __name__ == "__main__":
    main()
