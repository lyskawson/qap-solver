"""Demo: run all three algorithms on a single QAP instance."""
from src.instance import generate_instance
from src.solver_base import SolverResult
from src import brute_force, branch_and_bound, beam_search

DEMO_N = 6
DEMO_SEED = 42
BEAM_WIDTH = 3


def fmt_result(r: SolverResult) -> None:
    print(f"  {r.algorithm:<25} cost={r.best_cost:6d}  time={r.elapsed_seconds:.4f}s  "
          f"visited={r.nodes_visited:6d}  pruned={r.nodes_pruned:6d}")
    print(f"  {'':25} assignment={list(r.best_assignment)}")


def main() -> None:
    print(f"QAP Demo — n={DEMO_N}, seed={DEMO_SEED}")
    print("=" * 65)

    instance = generate_instance(DEMO_N, DEMO_SEED)

    print("\nFlow matrix:")
    for row in instance.flow:
        print("  " + " ".join(f"{v:3d}" for v in row))

    print("\nDistance matrix:")
    for row in instance.distance:
        print("  " + " ".join(f"{v:3d}" for v in row))

    print(f"\n{'Algorithm':<25} {'Cost':>6}  {'Time':>8}  {'Visited':>8}  {'Pruned':>8}")
    print("-" * 65)

    bf = brute_force.solve(instance)
    fmt_result(bf)

    bb = branch_and_bound.solve(instance)
    fmt_result(bb)

    bs = beam_search.solve(instance, beam_width=BEAM_WIDTH)
    fmt_result(bs)

    print()
    if bb.best_cost == bf.best_cost:
        print("B&B found the exact optimum.")
    rel_err = (bs.best_cost - bf.best_cost) / bf.best_cost
    print(f"Beam Search (k={BEAM_WIDTH}) relative error: {rel_err:.2%}")


if __name__ == "__main__":
    main()
