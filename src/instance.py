from dataclasses import dataclass
from .RandomNumberGenerator import RandomNumberGenerator


@dataclass(frozen=True)
class QAPInstance:
    n: int
    flow: tuple[tuple[int, ...], ...]
    distance: tuple[tuple[int, ...], ...]
    seed: int


def generate_instance(n: int, seed: int) -> QAPInstance:
    rng = RandomNumberGenerator(seed)

    flow = tuple(
        tuple(0 if i == j else rng.nextInt(1, 50) for j in range(n))
        for i in range(n)
    )
    distance = tuple(
        tuple(0 if i == j else rng.nextInt(1, 50) for j in range(n))
        for i in range(n)
    )

    return QAPInstance(n=n, flow=flow, distance=distance, seed=seed)
