import pytest
from src.instance import QAPInstance
from src.solver_base import evaluate, partial_cost


# n=2 instance: hand-computed
# flow: [[0,3],[5,0]], distance: [[0,2],[4,0]]
# assignment (0,1): w(0,1)*d(0,1) + w(1,0)*d(1,0) = 3*2 + 5*4 = 6 + 20 = 26
# assignment (1,0): w(0,1)*d(1,0) + w(1,0)*d(0,1) = 3*4 + 5*2 = 12 + 10 = 22
N2_INSTANCE = QAPInstance(
    n=2,
    flow=((0, 3), (5, 0)),
    distance=((0, 2), (4, 0)),
    seed=0,
)


def test_evaluate_n2_identity():
    assert evaluate((0, 1), N2_INSTANCE) == 26


def test_evaluate_n2_swap():
    assert evaluate((1, 0), N2_INSTANCE) == 22


# n=3 instance from fixture (seed=50)
# assignment (0,1,2): manually compute sum_{i!=j} w(i,j)*d(f(i),f(j))
# flow: ((0,1,29),(40,0,47),(32,48,0)), distance: ((0,18,48),(49,0,37),(9,49,0))
# pairs: (0,1): 1*18, (0,2): 29*48, (1,0): 40*49, (1,2): 47*37, (2,0): 32*9, (2,1): 48*49
# = 18 + 1392 + 1960 + 1739 + 288 + 2352 = 7749
def test_evaluate_n3_identity():
    from src.instance import generate_instance
    inst = generate_instance(3, 50)
    assert evaluate((0, 1, 2), inst) == 7749


def test_partial_cost_empty():
    assert partial_cost((), N2_INSTANCE) == 0


def test_partial_cost_single():
    assert partial_cost((0,), N2_INSTANCE) == 0


def test_partial_cost_two_equals_full():
    """For complete assignment, partial_cost must equal evaluate."""
    assert partial_cost((0, 1), N2_INSTANCE) == evaluate((0, 1), N2_INSTANCE)
    assert partial_cost((1, 0), N2_INSTANCE) == evaluate((1, 0), N2_INSTANCE)


def test_partial_cost_is_lower_bound():
    """partial_cost on prefix must be <= full cost (LB property)."""
    from src.instance import generate_instance
    inst = generate_instance(5, 42)
    from itertools import permutations
    for perm in permutations(range(5)):
        for k in range(6):
            lb = partial_cost(perm[:k], inst)
            full = evaluate(perm, inst)
            assert lb <= full, f"LB {lb} > full {full} for {perm[:k]}"
