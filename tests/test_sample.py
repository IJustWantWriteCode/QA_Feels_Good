import pytest
from datetime import datetime


@pytest.fixture(scope="module")
def start_tests():
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    db_state = {"status_type": "connected", "data": [1, 2, 3]}
    print(
        f"\n[{timestamp}]Начат прогон тестов из файла test_sample.py. "
        f"Состояние: {db_state}"
    )
    yield
    db_state["status_type"] = "disconnected"
    db_state["data"].clear()
    timestamp_end = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(
        f"\n[{timestamp_end}]Прогон тестов из файла test_sample.py окончен. "
        f"Состояние: {db_state}"
    )


@pytest.fixture(autouse=True)
def run_around_tests():
    print("Тест начат")
    yield
    print("\nТест окончен")


def test_sample_1(start_tests, random_int_for_test):
    a, b = random_int_for_test
    assert a + b == b + a


def test_sample_2(random_int_for_test):
    a, b = random_int_for_test
    assert not a - b == b - a
