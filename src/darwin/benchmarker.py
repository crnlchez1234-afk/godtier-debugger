import time
import timeit
import tracemalloc
import statistics
from typing import Callable, Dict, Any, List

class ArenaBenchmarker:
    """
    The Arena: Measures performance of code gladiators.
    """
    
    @staticmethod
    def measure_performance(func: Callable, args=(), kwargs={}, iterations: int = 100) -> Dict[str, float]:
        """
        Runs a function multiple times and measures time and memory.
        """
        # Warmup & Result Capture
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e), "valid": False}

        # Time Measurement
        times = []
        for _ in range(iterations):
            start = time.perf_counter_ns()
            func(*args, **kwargs)
            end = time.perf_counter_ns()
            times.append(end - start)
        
        avg_time_ns = statistics.mean(times)
        median_time_ns = statistics.median(times)
        stdev_time_ns = statistics.stdev(times) if len(times) > 1 else 0

        # Memory Measurement
        tracemalloc.start()
        func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "valid": True,
            "result": result,
            "avg_time_ns": avg_time_ns,
            "median_time_ns": median_time_ns,
            "stdev_time_ns": stdev_time_ns,
            "peak_memory_bytes": peak,
            "score": (1 / (avg_time_ns + 1)) * 1e9  # Higher is better (ops/sec approx)
        }

    @staticmethod
    def compare_gladiators(original_stats: Dict, mutant_stats: Dict) -> Dict[str, Any]:
        """
        Compares two sets of stats and determines the winner.
        """
        if not mutant_stats.get("valid", False):
            return {"winner": "original", "reason": "Mutant failed execution"}
            
        time_diff = original_stats["avg_time_ns"] - mutant_stats["avg_time_ns"]
        time_improvement_pct = (time_diff / original_stats["avg_time_ns"]) * 100
        
        mem_diff = original_stats["peak_memory_bytes"] - mutant_stats["peak_memory_bytes"]
        
        # Criteria for evolution:
        # 1. Must be valid
        # 2. Must be at least 10% faster OR use 20% less memory (without being slower)
        
        is_faster = time_improvement_pct > 10
        is_lighter = (mem_diff > 0) and (time_improvement_pct > -5) # Lighter and not significantly slower
        
        if is_faster:
            return {
                "winner": "mutant", 
                "reason": f"🚀 {time_improvement_pct:.2f}% Faster",
                "improvement_pct": time_improvement_pct
            }
        elif is_lighter:
            return {
                "winner": "mutant", 
                "reason": f"🪶 {mem_diff} bytes less memory",
                "improvement_pct": 0 # Memory focused
            }
        else:
            return {
                "winner": "original", 
                "reason": "Mutant not significantly better",
                "improvement_pct": time_improvement_pct
            }
