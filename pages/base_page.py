from playwright.sync_api import Page
from typing import Self


class BasePage:
    """Базовый класс для всех Page Objects. Содержит общие методы."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> Self:
        """Переход на указанный URL с ожиданием загрузки."""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def wait_for_page_load(self) -> Self:
        """Явное ожидание полной загрузки страницы (networkidle)."""
        self.page.wait_for_load_state("networkidle")
        return self
