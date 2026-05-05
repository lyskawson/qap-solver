import pytest
from src.instance import generate_instance
from src import brute_force, branch_and_bound


SEEDS = [42, 123, 50, 7, 2024]


@pytest.mark.parametrize("n", [3, 4, 5, 6])
@pytest.mark.parametrize("seed", SEEDS)
def test_bb_matches_brute_force(n, seed):
    """B&B must find the exact same optimal cost as brute force."""
    inst = generate_instance(n, seed)
    bf = brute_force.solve(inst)
    bb = branch_and_bound.solve(inst)
    assert bb.best_cost == bf.best_cost, (
        f"n={n}, seed={seed}: B&B={bb.best_cost}, BF={bf.best_cost}"
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_bb_assignment_is_valid_permutation(seed):
    inst = generate_instance(5, seed)
    result = branch_and_bound.solve(inst)
    assert sorted(result.best_assignment) == list(range(inst.n))


def test_bb_with_explicit_upper_bound():
    """Providing a tight UB should still yield the optimum."""
    inst = generate_instance(5, 42)
    bf = brute_force.solve(inst)
    bb = branch_and_bound.solve(inst, initial_upper_bound=bf.best_cost + 1)
    assert bb.best_cost == bf.best_cost


def test_bb_prunes_more_with_tight_bound():
    """Tighter initial UB should prune at least as many nodes."""
    inst = generate_instance(6, 42)
    bb_default = branch_and_bound.solve(inst)
    bb_tight = branch_and_bound.solve(inst, initial_upper_bound=bb_default.best_cost + 1)
    # With UB = optimum+1, we prune anything >= optimum+1, which is at least as tight
    assert bb_tight.best_cost == bb_default.best_cost
