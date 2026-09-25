import random
from typing import Any, Generator

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
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(autouse=True)
def block_ads_and_analytics(page: Page) -> None:
    page.route(
        "**/*{google,doubleclick,adservice,adsystem,googlesyndication,analytics}*/**",
        lambda route: route.abort(),
    )


@pytest.fixture(scope="session")
def api_session() -> Generator[Session, None, None]:
    session = requests.Session()
    yield session
    session.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[Any]
) -> Generator[None, Any, None]:
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        funcargs = getattr(item, "funcargs", {})
        page = funcargs.get("page")

        if page and not page.is_closed():
            try:
                screenshot = page.screenshot(timeout=5000, full_page=True)
                allure.attach(
                    screenshot,
                    name="failure_screenshot",
                    attachment_type=AttachmentType.PNG,
                )
            except Exception as e:
                print(f"\n[Warning] Не удалось сделать скриншот для Allure: {e}")
            try:
                content = page.content()
                allure.attach(
                    content,
                    name="failure_page_source",
                    attachment_type=AttachmentType.HTML,
                )
            except Exception as e:
                print(f"\n[Warning] Не удалось получить DOM-дерево для Allure: {e}")
