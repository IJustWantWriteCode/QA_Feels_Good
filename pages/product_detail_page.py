from playwright.sync_api import expect
from .base_page import BasePage
from .cart_page import CartPage
from typing import Self


class ProductDetailPage(BasePage):
    """Страница детальной информации о товаре"""

    def add_to_cart(self) -> Self:
        """Нажимает кнопку Add to cart и подтверждает модальное окно."""
        add_button = self.page.get_by_role("button", name="Add to cart")
        add_button.click()

        # Явное ожидание появления модального окна
        expect(self.page.get_by_text("Added!")).to_be_visible(timeout=5000)

        return self

    def go_to_cart_from_modal_window(self) -> CartPage:
        """Переходит в корзину по ссылке View Cart из модального окна."""
        # Кликаем "View Cart" в модальном окне
        view_cart = self.page.get_by_role("link", name="View Cart")
        view_cart.click()
        self.page.wait_for_load_state("domcontentloaded")
        return CartPage(self.page)

    def go_to_cart(self) -> CartPage:
        """Прямой переход в корзину (если нужно)."""
        self.page.goto("https://automationexercise.com/view_cart")
        return CartPage(self.page)
