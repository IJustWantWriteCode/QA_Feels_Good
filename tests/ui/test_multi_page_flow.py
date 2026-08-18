import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


@pytest.mark.ui
def test_add_product_to_cart(page: Page) -> None:
    home = HomePage(page)
    home.goto(home.URL)

    product = home.go_to_products()
    detail = product.open_first_product()
    cart = detail.add_to_cart().go_to_cart_from_modal_window()

    assert cart.is_product_in_cart("Blue Top") is True
