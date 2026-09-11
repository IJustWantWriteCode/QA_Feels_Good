import pytest
import random
from playwright.sync_api import sync_playwright
import requests


@pytest.fixture()
def random_int_for_test():
    a, b = random.randint(1, 9), random.randint(1, 9)
    return a, b


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    yield session
    session.close()
