from playwright.sync_api import expect
from .base_page import BasePage


class CartPage(BasePage):
    """Страница корзины /view_cart"""

    def is_product_in_cart(self, product_name: str) -> bool:
        """Проверяет, что товар с указанным названием присутствует в корзине."""
        # Ищем строку таблицы корзины, содержащую название товара
        product_row = self.page.locator("table#cart_info_table").filter(
            has_text=product_name
        )
        expect(product_row).to_be_visible(timeout=5000)
        return True
