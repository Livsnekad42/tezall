import random


def create_randoms(length: int = 4) -> str:
    return ''.join(map(str, random.sample(range(10), length)))


def create_code() -> str:
    return create_randoms(random.randrange(4, 6))
