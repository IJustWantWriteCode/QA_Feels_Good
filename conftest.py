import pytest
import random


@pytest.fixture()
def random_int_for_test():
    a, b = random.randint(1, 9), random.randint(1, 9)
    return a, b
