import pytest
from src.instance import generate_instance


def test_n3_seed50_dimensions():
    inst = generate_instance(3, 50)
    assert inst.n == 3
    assert len(inst.flow) == 3
    assert all(len(row) == 3 for row in inst.flow)
    assert len(inst.distance) == 3
    assert all(len(row) == 3 for row in inst.distance)


def test_n3_seed50_flow_values():
    """Fixture: manually recorded output for n=3, seed=50."""
    inst = generate_instance(3, 50)
    assert inst.flow == ((0, 1, 29), (40, 0, 47), (32, 48, 0))


def test_n3_seed50_distance_values():
    """Fixture: manually recorded output for n=3, seed=50."""
    inst = generate_instance(3, 50)
    assert inst.distance == ((0, 18, 48), (49, 0, 37), (9, 49, 0))


def test_diagonal_is_zero():
    for n in (3, 5, 7):
        inst = generate_instance(n, seed=1)
        for i in range(n):
            assert inst.flow[i][i] == 0
            assert inst.distance[i][i] == 0


def test_off_diagonal_positive():
    inst = generate_instance(5, seed=99)
    for i in range(5):
        for j in range(5):
            if i != j:
                assert inst.flow[i][j] >= 1
                assert inst.distance[i][j] >= 1


def test_reproducibility():
    a = generate_instance(6, 42)
    b = generate_instance(6, 42)
    assert a.flow == b.flow
    assert a.distance == b.distance


def test_different_seeds_differ():
    a = generate_instance(6, 42)
    b = generate_instance(6, 43)
    assert a.flow != b.flow
