import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.inbox_page import InboxPage
from pages.compose_page import ComposePage

load_dotenv()


@pytest.fixture(scope="function")
def page():
    headless = os.environ.get("HEADLESS", "false").lower() == "true"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
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
