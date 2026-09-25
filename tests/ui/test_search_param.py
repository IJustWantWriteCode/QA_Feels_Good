import re

import allure
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("query", ["qa", "aqa", "python"])
@pytest.mark.ui
def test_wikipedia_search_parametrized(page: Page, query: str) -> None:
    with allure.step("Переход на Главную страницу Wikipedia"):
        page.goto("https://en.wikipedia.org/")

    with allure.step("Ищем поисковую строку и вводим запрос"):
        search_input = page.get_by_role("searchbox", name="Search Wikipedia")
        search_input.fill(query)
        search_input.press("Enter")

    with allure.step("Проверка отображения основного заголовка статьи"):
        main_heading = page.get_by_role("heading", level=1)
        expect(main_heading).to_be_visible(timeout=10000)
        expect(main_heading).to_contain_text(re.compile(query, re.IGNORECASE))
