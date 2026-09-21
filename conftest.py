import random
from collections.abc import Generator

import allure
import pytest
import requests
from allure_commons.types import AttachmentType
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page and not page.is_closed():
            allure.attach(
                page.screenshot(full_page=True),
                name="failure_screenshot",
                attachment_type=AttachmentType.PNG,
            )

            allure.attach(
                page.content(),
                name="failure_page_source",
                attachment_type=AttachmentType.HTML,
            )
