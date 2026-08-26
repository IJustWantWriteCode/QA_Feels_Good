from playwright.sync_api import Page, expect
from .base_page import BasePage
from .products_page import ProductsPage


class HomePage(BasePage):
    """Главная страница automationexercise.com"""

    URL = "https://automationexercise.com/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Локаторы хранятся внутри класса
        self.products_link = page.get_by_role("link", name="Products")
        self._features_item_names = (
            page.get_by_text("Features Items").locator("..").locator(".productinfo p")
        )

    def go_to_products(self) -> ProductsPage:
        """Клик по ссылке Products и переход на страницу Products."""
        self.products_link.click()
        # Ждём загрузки новой страницы
        self.page.wait_for_load_state("domcontentloaded")
        return ProductsPage(self.page)

    def get_features_item_names(self) -> list[str]:
        """Собирает названия видимых товаров в секции Features Items."""
        expect(self._features_item_names.first).to_be_visible()
        return [
            el.inner_text().strip()
            for el in self._features_item_names.all()
            if el.is_visible()
        ]

    def expect_features_contain(self, names: set[str]) -> None:
        """Проверяет, что ключевые товары присутствуют в секции (subset)."""
        actual = set(self.get_features_item_names())
        assert names.issubset(
            actual
        ), f"Не все ожидаемые товары найдены. Найдено: {actual}"
