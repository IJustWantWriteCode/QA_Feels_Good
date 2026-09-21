import allure
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("query", ["qa", "aqa", "python"])
@pytest.mark.ui
def test_duckduckgo_search_parametrized(page: Page, query: str) -> None:
    with allure.step("Переход на страницу поискового сервиса 'duckduckgo'"):
        page.goto("https://duckduckgo.com/")

    with allure.step("Ищем поисковую строку, заполняем данными и нажимаем 'Поиск'"):
        search_input = page.get_by_role("combobox", name="Поиск в DuckDuckGo")
        search_input.fill(query)
        search_input.press("Enter")
    with allure.step("Проверка отображения результатов на странице"):
        results = page.get_by_test_id("result")
        expect(results.first).to_be_visible(timeout=10000)

    assert results.count() >= 5
