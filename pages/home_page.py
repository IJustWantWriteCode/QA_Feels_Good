from playwright.sync_api import Page
from .base_page import BasePage
from .products_page import ProductsPage


class HomePage(BasePage):
    """Главная страница automationexercise.com"""

    URL = "https://automationexercise.com/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Локаторы хранятся внутри класса
        self.products_link = page.get_by_role("link", name="Products")

    def go_to_products(self) -> ProductsPage:
        """Клик по ссылке Products и переход на страницу Products."""
        self.products_link.click()
        # Ждём загрузки новой страницы
        self.page.wait_for_load_state("domcontentloaded")
        return ProductsPage(self.page)
