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
    n = instance.n
    k = len(assignment)

    assigned_cost = 0
    for i in range(k):
        for j in range(k):
            if i != j:
                assigned_cost += instance.flow[i][j] * instance.distance[assignment[i]][assignment[j]]

    if k == n:
        return assigned_cost

    unassigned_facilities = range(k, n)
    unassigned_locations = [loc for loc in range(n) if loc not in assignment]

    cross_cost = 0
    for i in range(k):
        loc_i = assignment[i]
        min_dist_from_i = min(instance.distance[loc_i][l] for l in unassigned_locations)
        min_dist_to_i = min(instance.distance[l][loc_i] for l in unassigned_locations)

        for u in unassigned_facilities:
            cross_cost += instance.flow[i][u] * min_dist_from_i
            cross_cost += instance.flow[u][i] * min_dist_to_i

    min_flows = []
    for u in unassigned_facilities:
        flows = [instance.flow[u][v] for v in unassigned_facilities if u != v]
        min_flows.append(min(flows) if flows else 0)

    min_distances = []
    for loc in unassigned_locations:
        distances = [instance.distance[loc][l] for l in unassigned_locations if loc != l]
        min_distances.append(min(distances) if distances else 0)

    min_flows.sort(reverse=True)
    min_distances.sort()

    unassigned_cost = sum(f * d for f, d in zip(min_flows, min_distances))

    return assigned_cost + cross_cost + unassigned_cost