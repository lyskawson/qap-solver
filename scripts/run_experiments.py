"""Run benchmark experiments and save results to results/benchmark.csv."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.benchmark import run_all, save_csv

SIZES = [4, 5, 6, 7, 8, 9, 10]
SEEDS = [42, 123, 50, 7, 2024]
BEAM_WIDTHS = [2, 5, 10]
OUTPUT = Path("results/benchmark.csv")


def main() -> None:
    print("Running experiments...")
    print(f"  sizes: {SIZES}")
    print(f"  seeds: {SEEDS}")
    print(f"  beam_widths: {BEAM_WIDTHS}")
    print()

    rows = run_all(
        sizes=SIZES,
        seeds=SEEDS,
        beam_widths=BEAM_WIDTHS,
        brute_force_max_n=8,
    )

    save_csv(rows, OUTPUT)
    print(f"Saved {len(rows)} rows to {OUTPUT}")

    print("\nSample results (n=6, seed=42):")
    for row in rows:
        if row.n == 6 and row.seed == 42:
            err_str = f"{row.relative_error:.2%}" if row.relative_error is not None else "N/A"
            print(f"  {row.algorithm:<25} cost={row.cost:6d}  time={row.elapsed_seconds:.4f}s  "
                  f"visited={row.nodes_visited:6d}  rel_err={err_str}")


if __name__ == "__main__":
    main()
