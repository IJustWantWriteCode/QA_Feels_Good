import os
import pytest
from dotenv import load_dotenv
from pages.login_page import LoginPage
from playwright.sync_api import expect

load_dotenv()

@pytest.mark.ui
def test_successful_login(page):
    login_page = LoginPage(page)
    page.goto("https://www.saucedemo.com/")

    username = os.getenv("SAUCE_USER", "standard_user")
    password = os.getenv("SAUCE_PASS", "secret_sauce")

    login_page.login(username, password)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.pause()

@pytest.mark.ui
def test_locked_out_user(page):
    login_page = LoginPage(page)
    page.goto("https://www.saucedemo.com/")

    login_page.login("locked_out_user", "secret_sauce")
    error = login_page.get_error_message()
    assert "Epic sadface" in error

    page.pause()