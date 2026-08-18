import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


@pytest.mark.ui
def test_features_items_subset(page: Page) -> None:
    home = HomePage(page)
    home.goto(home.URL)
    home.expect_features_contain({"Blue Top", "Men Tshirt", "Stylish Dress"})
