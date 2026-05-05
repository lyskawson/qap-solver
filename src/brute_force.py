import time
from itertools import permutations
from .instance import QAPInstance
from .solver_base import SolverResult, evaluate


def solve(instance: QAPInstance) -> SolverResult:
    """Exhaustive search over all n! permutations. Reference baseline only."""
    start = time.perf_counter()

    best_cost = float("inf")
    best_assignment: tuple[int, ...] = ()
    nodes_visited = 0

    for perm in permutations(range(instance.n)):
        nodes_visited += 1
        cost = evaluate(perm, instance)
        if cost < best_cost:
            best_cost = cost
            best_assignment = perm

    return SolverResult(
        best_assignment=best_assignment,
        best_cost=best_cost,
        nodes_visited=nodes_visited,
        nodes_pruned=0,
        elapsed_seconds=time.perf_counter() - start,
        algorithm="brute_force",
    )
