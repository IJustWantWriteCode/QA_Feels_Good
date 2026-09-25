import allure
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage


@pytest.mark.ui
def test_add_product_to_cart(page: Page) -> None:
    home = HomePage(page)
    with allure.step("Открытие домашней страницы"):
        home.goto(home.URL)
    with allure.step("Переход в каталог"):
        product = home.go_to_products()
    with allure.step("Переход на карточку первого товара"):
        detail = product.open_first_product()
    with allure.step("Добавление товара в корзину и переход в нее из модального окна"):
        cart = detail.add_to_cart().go_to_cart_from_modal_window()

    assert cart.is_product_in_cart("Blue Top") is True
