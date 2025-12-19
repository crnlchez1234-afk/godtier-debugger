import sys
import argparse
from tier10_engine import EvolutionEngine
from tier10.config_loader import ConfigLoader

def main():
    parser = argparse.ArgumentParser(description="Tier 10 Evolution Engine")
    parser.add_argument("--target", nargs="+", help="Specific files to target for evolution")
    parser.add_argument("--generations", type=int, help="Number of generations to run")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to configuration file")
    
    args = parser.parse_args()

    # Load config to get defaults if not provided via CLI
    config = ConfigLoader.load_config(args.config)
    
    # Initialize Engine
    engine = EvolutionEngine()
    
    # Determine targets
    targets = args.target
    if not targets:
        # If no targets specified, maybe look for a default list in config or scan directory?
        # For now, let's just default to a demo file if nothing is passed, or exit.
        print("⚠️ No target files specified. Usage: python main.py --target file1.py file2.py")
        # For backward compatibility/demo, we could target the samples
        print("   Running on default demo samples...")
        targets = ["evolution_samples/slow_calculations.py"]

    # Determine generations
    generations = args.generations or config.get('evolution', {}).get('max_generations', 5)
    
    # Run Evolution
    engine.evolve(
        target_files=targets,
        max_generations=generations,
        improvement_threshold=config.get('evolution', {}).get('improvement_threshold', 0.05),
        auto_approve_threshold=config.get('evolution', {}).get('auto_approve_threshold', 0.3)
    )

if __name__ == "__main__":
    main()
