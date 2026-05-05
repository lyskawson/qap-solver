import time
from .instance import QAPInstance
from .solver_base import Node, SolverResult, evaluate, partial_cost


def _greedy_initial_solution(instance: QAPInstance) -> tuple[int, ...]:
    """Greedy heuristic: assign each facility to the location with minimum marginal cost."""
    n = instance.n
    assignment: list[int] = []
    available = list(range(n))

    for i in range(n):
        best_loc: int = -1
        best_marginal = float("inf")
        for loc in available:
            marginal = 0
            for j in range(i):
                marginal += instance.flow[i][j] * instance.distance[loc][assignment[j]]
                marginal += instance.flow[j][i] * instance.distance[assignment[j]][loc]
            if marginal < best_marginal:
                best_marginal = marginal
                best_loc = loc
        assignment.append(best_loc)
        available.remove(best_loc)

    return tuple(assignment)


def solve(instance: QAPInstance, initial_upper_bound: int | None = None) -> SolverResult:
    """Branch and Bound with iterative DFS (LIFO stack) and simple partial-cost LB."""
    start = time.perf_counter()
    n = instance.n

    greedy = _greedy_initial_solution(instance)
    upper_bound = initial_upper_bound if initial_upper_bound is not None else evaluate(greedy, instance)
    best_assignment = greedy

    root = Node(assignment=(), used_locations=frozenset(), lower_bound=0)
    stack: list[Node] = [root]

    nodes_visited = 0
    nodes_pruned = 0

    while stack:
        node = stack.pop()
        nodes_visited += 1

        if node.lower_bound >= upper_bound:
            nodes_pruned += 1
            continue

        depth = len(node.assignment)

        if depth == n:
            cost = evaluate(node.assignment, instance)
            if cost < upper_bound:
                upper_bound = cost
                best_assignment = node.assignment
            continue

        children: list[Node] = []
        for loc in range(n):
            if loc in node.used_locations:
                continue
            child_assignment = node.assignment + (loc,)
            lb = partial_cost(child_assignment, instance)
            if lb < upper_bound:
                children.append(Node(
                    assignment=child_assignment,
                    used_locations=node.used_locations | {loc},
                    lower_bound=lb,
                ))
            else:
                nodes_pruned += 1

        # Sort descending by LB so stack pops smallest-LB first (DFS, best-first within level)
        children.sort(key=lambda c: c.lower_bound, reverse=True)
        stack.extend(children)

    return SolverResult(
        best_assignment=best_assignment,
        best_cost=upper_bound,
        nodes_visited=nodes_visited,
        nodes_pruned=nodes_pruned,
        elapsed_seconds=time.perf_counter() - start,
        algorithm="branch_and_bound",
    )
