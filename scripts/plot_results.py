"""Generate plots from benchmark.csv."""
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib.pyplot as plt

CSV_PATH = Path("results/benchmark.csv")
RESULTS_DIR = Path("results")


def load_csv(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def group_by(rows: list[dict], key: str) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row[key]].append(row)
    return groups


def avg_by_n(rows: list[dict], field: str) -> dict[int, float]:
    by_n: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        val = row[field]
        if val != "":
            by_n[int(row["n"])].append(float(val))
    return {n: sum(vs) / len(vs) for n, vs in sorted(by_n.items())}


def plot_time_vs_n(rows: list[dict]) -> None:
    algorithms = {
        "brute_force": "Brute Force",
        "branch_and_bound": "Branch & Bound",
        "beam_search(k=2)": "Beam Search k=2",
        "beam_search(k=5)": "Beam Search k=5",
        "beam_search(k=10)": "Beam Search k=10",
    }

    fig, ax = plt.subplots()
    for algo, label in algorithms.items():
        algo_rows = [r for r in rows if r["algorithm"] == algo]
        if not algo_rows:
            continue
        data = avg_by_n(algo_rows, "elapsed_seconds")
        ns = sorted(data.keys())
        times = [data[n] for n in ns]
        ax.semilogy(ns, times, marker="o", label=label)

    ax.set_xlabel("Problem size n")
    ax.set_ylabel("Time (seconds, log scale)")
    ax.set_title("Computation time vs problem size")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    fig.savefig(RESULTS_DIR / "time_vs_n.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved results/time_vs_n.png")


def plot_nodes_vs_n(rows: list[dict]) -> None:
    algorithms = {
        "brute_force": "Brute Force",
        "branch_and_bound": "Branch & Bound",
        "beam_search(k=2)": "Beam Search k=2",
        "beam_search(k=5)": "Beam Search k=5",
        "beam_search(k=10)": "Beam Search k=10",
    }

    fig, ax = plt.subplots()
    for algo, label in algorithms.items():
        algo_rows = [r for r in rows if r["algorithm"] == algo]
        if not algo_rows:
            continue
        data = avg_by_n(algo_rows, "nodes_visited")
        ns = sorted(data.keys())
        counts = [data[n] for n in ns]
        ax.semilogy(ns, counts, marker="o", label=label)

    ax.set_xlabel("Problem size n")
    ax.set_ylabel("Nodes visited (log scale)")
    ax.set_title("Nodes visited vs problem size")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    fig.savefig(RESULTS_DIR / "nodes_vs_n.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved results/nodes_vs_n.png")


def plot_relative_error_vs_beam_width(rows: list[dict], target_n: int = 8) -> None:
    beam_rows = [
        r for r in rows
        if r["algorithm"].startswith("beam_search") and int(r["n"]) == target_n
        and r["relative_error"] != ""
    ]

    by_bw: dict[int, list[float]] = defaultdict(list)
    for row in beam_rows:
        bw = int(row["beam_width"])
        by_bw[bw].append(float(row["relative_error"]))

    if not by_bw:
        print(f"No beam search data for n={target_n}, skipping relative error plot.")
        return

    bws = sorted(by_bw.keys())
    avg_errors = [sum(by_bw[bw]) / len(by_bw[bw]) for bw in bws]

    fig, ax = plt.subplots()
    ax.plot(bws, avg_errors, marker="o")
    ax.set_xlabel("Beam width k")
    ax.set_ylabel("Average relative error")
    ax.set_title(f"Beam Search relative error vs beam width (n={target_n})")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.savefig(RESULTS_DIR / "error_vs_beam_width.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved results/error_vs_beam_width.png")


def main() -> None:
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found. Run scripts/run_experiments.py first.")
        sys.exit(1)

    rows = load_csv(CSV_PATH)
    print(f"Loaded {len(rows)} rows from {CSV_PATH}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    plot_time_vs_n(rows)
    plot_nodes_vs_n(rows)
    plot_relative_error_vs_beam_width(rows, target_n=8)


if __name__ == "__main__":
    main()
