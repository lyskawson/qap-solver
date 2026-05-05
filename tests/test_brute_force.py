import pytest
from itertools import permutations
from src.instance import generate_instance
from src.solver_base import evaluate
from src import brute_force


def test_brute_force_n4_finds_optimum():
    inst = generate_instance(4, 42)
    result = brute_force.solve(inst)

    all_costs = [evaluate(p, inst) for p in permutations(range(4))]
    assert result.best_cost == min(all_costs)


def test_brute_force_visits_n_factorial_nodes():
    import math
    for n in (3, 4, 5):
        inst = generate_instance(n, seed=7)
        result = brute_force.solve(inst)
        assert result.nodes_visited == math.factorial(n)


def test_brute_force_result_is_valid_permutation():
    inst = generate_instance(4, 123)
    result = brute_force.solve(inst)
    assert sorted(result.best_assignment) == list(range(inst.n))


def test_brute_force_cost_matches_assignment():
    inst = generate_instance(4, 50)
    result = brute_force.solve(inst)
    assert result.best_cost == evaluate(result.best_assignment, inst)
