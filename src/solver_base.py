from dataclasses import dataclass, field
from .instance import QAPInstance


@dataclass(frozen=True)
class Node:
    assignment: tuple[int, ...]
    lower_bound: int


@dataclass
class SolverResult:
    best_assignment: tuple[int, ...]
    best_cost: int
    nodes_visited: int
    nodes_pruned: int
    elapsed_seconds: float
    algorithm: str


def evaluate(assignment: tuple[int, ...], instance: QAPInstance) -> int:
    n = len(assignment)
    total = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                total += instance.flow[i][j] * instance.distance[assignment[i]][assignment[j]]
    return total


def partial_cost(assignment: tuple[int, ...], instance: QAPInstance) -> int:
    """
    Cost of already assigned pairs — used as lower bound.
    """
    k = len(assignment)
    total = 0
    for i in range(k):
        for j in range(k):
            if i != j:
                total += instance.flow[i][j] * instance.distance[assignment[i]][assignment[j]]
    return total
