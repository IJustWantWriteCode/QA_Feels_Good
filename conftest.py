import random
from collections.abc import Generator

import pytest
import requests
from playwright.sync_api import Page, sync_playwright
from requests import Session


@pytest.fixture()
def random_int_for_test() -> tuple[int, int]:
    a, b = random.randint(1, 9), random.randint(1, 9)
    return a, b


@pytest.fixture(scope="function")
def page() -> Generator[Page, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def api_session() -> Generator[Session, None, None]:
    session = requests.Session()
    yield session
    session.close()
