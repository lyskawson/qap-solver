import csv
import time
from dataclasses import dataclass
from pathlib import Path

from .instance import generate_instance, QAPInstance
from .solver_base import SolverResult
from . import brute_force, branch_and_bound, beam_search


@dataclass
class BenchmarkRow:
    n: int
    seed: int
    algorithm: str
    beam_width: int | None
    cost: int
    optimum: int | None
    relative_error: float | None
    nodes_visited: int
    nodes_pruned: int
    elapsed_seconds: float


def run_all(
    sizes: list[int],
    seeds: list[int],
    beam_widths: list[int],
    brute_force_max_n: int = 8,
) -> list[BenchmarkRow]:
    rows: list[BenchmarkRow] = []

    for n in sizes:
        for seed in seeds:
            instance = generate_instance(n, seed)

            optimum: int | None = None
            if n <= brute_force_max_n:
                bf = brute_force.solve(instance)
                optimum = bf.best_cost
                rows.append(_make_row(n, seed, bf, None, optimum))

            bb = branch_and_bound.solve(instance)
            rows.append(_make_row(n, seed, bb, None, optimum))

            for bw in beam_widths:
                bs = beam_search.solve(instance, beam_width=bw)
                rows.append(_make_row(n, seed, bs, bw, optimum))

    return rows


def _make_row(
    n: int,
    seed: int,
    result: SolverResult,
    beam_width: int | None,
    optimum: int | None,
) -> BenchmarkRow:
    rel_err: float | None = None
    if optimum is not None and optimum > 0:
        rel_err = (result.best_cost - optimum) / optimum

    return BenchmarkRow(
        n=n,
        seed=seed,
        algorithm=result.algorithm,
        beam_width=beam_width,
        cost=result.best_cost,
        optimum=optimum,
        relative_error=rel_err,
        nodes_visited=result.nodes_visited,
        nodes_pruned=result.nodes_pruned,
        elapsed_seconds=result.elapsed_seconds,
    )


def save_csv(rows: list[BenchmarkRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "n", "seed", "algorithm", "beam_width", "cost", "optimum",
            "relative_error", "nodes_visited", "nodes_pruned", "elapsed_seconds",
        ])
        for row in rows:
            writer.writerow([
                row.n, row.seed, row.algorithm, row.beam_width,
                row.cost, row.optimum,
                f"{row.relative_error:.6f}" if row.relative_error is not None else "",
                row.nodes_visited, row.nodes_pruned,
                f"{row.elapsed_seconds:.6f}",
            ])
