import pytest
from datetime import datetime


@pytest.fixture(scope="module")
def start_tests():
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    db_state = {"status_type": "connected", "data": [1, 2, 3]}
    print(
        f"\n[{timestamp}]Начат прогон тестов из файла test_sample.py. "
        f"Состояние: {db_state['status_type']}. "
        f"Данные: {db_state['data']}"
    )
    yield
    db_state["status_type"] = "disconnected"
    db_state["data"].clear()
    timestamp_end = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(
        f"\n[{timestamp_end}]Прогон тестов из файла test_sample.py окончен. "
        f"Состояние: {db_state['status_type']}. "
        f"Данные: {db_state['data']}"
    )


@pytest.fixture(autouse=True)
def run_around_tests():
    print("Тест начат")
    yield
    print("\nТест окончен\n")


def test_sample_1(start_tests, random_int_for_test, page):
    a, b = random_int_for_test
    assert a + b == b + a


def test_sample_2(random_int_for_test, page):
    a, b = random_int_for_test
    assert not a - b == b - a


@pytest.mark.parametrize(
    "percent_crit, damage",
    [
        (1.25, 55),
        (1.07, 23),
    ],
    ids=["high_level_damage", "low_level_damage"],
)
@pytest.mark.parametrize(
    "bonus_armor, armor",
    [
        (1.25, 44),
        (1.10, 34),
    ],
    ids=["high_level_armor", "low_level_armor"],
)
@pytest.mark.smoke
@pytest.mark.xfail(
    strict=False, reason="Урон может быть недостаточным в некоторых комбинациях"
)
def test_damage_and_armor(percent_crit, damage, bonus_armor, armor, page):

    total_damage = round(percent_crit * damage, 2)
    total_armor = round(bonus_armor * armor, 2)

    if total_damage > total_armor:
        message = f"Успех: Урон ({total_damage}) пробил броню ({total_armor})"
    elif total_damage < total_armor:
        message = (
            f"Провал: Броня ({total_armor}) оказалась больше урона ({total_damage})"
        )
    else:
        message = f"Провал: Урон ({total_damage}) равен броне ({total_armor})"

    print(f"\n[РЕЗУЛЬТАТ]: {message}")
    assert total_damage > total_armor, message
