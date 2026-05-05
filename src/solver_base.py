from dataclasses import dataclass, field
from .instance import QAPInstance


@dataclass(frozen=True)
class Node:
    """Decision tree node.

    assignment[i] = location assigned to facility i.
    len(assignment) equals the current depth (number of assigned facilities).
    """
    assignment: tuple[int, ...]
    used_locations: frozenset[int]
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
    """Full cost for a complete assignment (len == n)."""
    n = len(assignment)
    total = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                total += instance.flow[i][j] * instance.distance[assignment[i]][assignment[j]]
    return total


def partial_cost(assignment: tuple[int, ...], instance: QAPInstance) -> int:
    """Cost of already-assigned pairs — used as lower bound.

    Sums w(i,j)*d(assignment[i], assignment[j]) for all pairs i,j < len(assignment).
    Valid LB because all weights/distances are non-negative, so additional
    assignments can only increase total cost.
    """
    k = len(assignment)
    total = 0
    for i in range(k):
        for j in range(k):
            if i != j:
                total += instance.flow[i][j] * instance.distance[assignment[i]][assignment[j]]
    return total
