import time
from .instance import QAPInstance
from .solver_base import Node, SolverResult, evaluate, partial_cost


def solve(instance: QAPInstance, beam_width: int) -> SolverResult:
    start = time.perf_counter()
    n = instance.n

    root = Node(assignment=(), lower_bound=0)
    current_level: list[Node] = [root]

    nodes_visited = 0
    nodes_pruned = 0

    for _ in range(n):
        next_level: list[Node] = []
        for node in current_level:
            for loc in range(n):
                if loc in node.assignment:
                    continue

                nodes_visited += 1
                child_assignment = node.assignment + (loc,)
                lb = partial_cost(child_assignment, instance)

                next_level.append(Node(
                    assignment=child_assignment,
                    lower_bound=lb,
                ))

        next_level.sort(key=lambda c: c.lower_bound)

        if len(next_level) > beam_width:
            nodes_pruned += len(next_level) - beam_width
            next_level = next_level[:beam_width]

        current_level = next_level

    best = min(current_level, key=lambda node: evaluate(node.assignment, instance))
    best_cost = evaluate(best.assignment, instance)

    return SolverResult(
        best_assignment=best.assignment,
        best_cost=best_cost,
        nodes_visited=nodes_visited,
        nodes_pruned=nodes_pruned,
        elapsed_seconds=time.perf_counter() - start,
        algorithm=f"beam_search(k={beam_width})",
    )