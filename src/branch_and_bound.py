import random
import time
from .instance import QAPInstance
from .solver_base import Node, SolverResult, evaluate, partial_cost


def _random_initial_solution(instance: QAPInstance) -> tuple[int, ...]:
    assignment = list(range(instance.n))
    random.shuffle(assignment)
    return tuple(assignment)


def solve(instance: QAPInstance, initial_upper_bound: int | None = None) -> SolverResult:
    start = time.perf_counter()
    n = instance.n

    initial_sol = _random_initial_solution(instance)

    if initial_upper_bound is not None:
        upper_bound = initial_upper_bound
    else:
        upper_bound = evaluate(initial_sol, instance)

    best_assignment = initial_sol

    root = Node(assignment=(), lower_bound=0)
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
            if loc in node.assignment:
                continue

            child_assignment = node.assignment + (loc,)
            lb = partial_cost(child_assignment, instance)

            if lb < upper_bound:
                children.append(Node(
                    assignment=child_assignment,
                    lower_bound=lb,
                ))
            else:
                nodes_pruned += 1

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