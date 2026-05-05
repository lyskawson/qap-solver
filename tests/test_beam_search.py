import math
import pytest
from src.instance import generate_instance
from src import brute_force, beam_search


SEEDS = [42, 123, 50]


@pytest.mark.parametrize("n", [3, 4, 5])
@pytest.mark.parametrize("seed", SEEDS)
def test_large_beam_matches_brute_force(n, seed):
    """beam_width >= n! degenerates to exhaustive BFS — same cost as brute force."""
    inst = generate_instance(n, seed)
    bf = brute_force.solve(inst)
    bs = beam_search.solve(inst, beam_width=math.factorial(n))
    assert bs.best_cost == bf.best_cost, (
        f"n={n}, seed={seed}: BS={bs.best_cost}, BF={bf.best_cost}"
    )


@pytest.mark.parametrize("n", [4, 5, 6])
@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("beam_width", [1, 2, 3])
def test_beam_search_never_beats_optimum(n, seed, beam_width):
    """Beam search result must be >= optimal cost."""
    inst = generate_instance(n, seed)
    bf = brute_force.solve(inst)
    bs = beam_search.solve(inst, beam_width=beam_width)
    assert bs.best_cost >= bf.best_cost, (
        f"n={n}, seed={seed}, k={beam_width}: BS={bs.best_cost} < optimal={bf.best_cost}"
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_beam_search_assignment_is_valid_permutation(seed):
    inst = generate_instance(5, seed)
    result = beam_search.solve(inst, beam_width=5)
    assert sorted(result.best_assignment) == list(range(inst.n))


def test_wider_beam_no_worse():
    """Wider beam should not produce a worse result than narrower beam."""
    inst = generate_instance(6, 42)
    costs = [beam_search.solve(inst, beam_width=k).best_cost for k in [1, 2, 5, 10]]
    # Not strictly monotone, but cost[wide] <= cost[narrow] on average — at minimum,
    # the widest beam should not exceed the narrowest.
    assert costs[-1] <= costs[0]
