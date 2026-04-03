import pytest
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.inbox_page import InboxPage
from pages.compose_page import ComposePage


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        p = context.new_page()
        yield p
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def login_page(page):
    return LoginPage(page)


@pytest.fixture(scope="function")
def inbox_page(page):
    return InboxPage(page)


@pytest.fixture(scope="function")
def compose_page(page):
    return ComposePage(page)
