import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("query", ["qa", "aqa", "python"])
@pytest.mark.ui
def test_duckduckgo_search_parametrized(page: Page, query: str) -> None:
    page.goto("https://duckduckgo.com/")

    search_input = page.get_by_role("combobox", name="Поиск в DuckDuckGo")
    search_input.fill(query)
    search_input.press("Enter")

    results = page.get_by_test_id("result")
    expect(results.first).to_be_visible(timeout=10000)

    assert results.count() >= 5
