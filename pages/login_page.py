from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Page

from pages import timeouts

LOGIN_URL = (
    "https://login.live.com/login.srf"
    "?wa=wsignin1.0&rpsnv=16"
    "&wreply=https%3A%2F%2Foutlook.live.com%2Fmail%2F0%2F"
    "&id=292841"
)


class LoginPage:
    def __init__(self, page: Page):
        self._page = page

    # ── Elements ──────────────────────────────────────────────

    def _email_input(self):
        return self._page.locator("#usernameEntry")

    def _password_input(self):
        return self._page.locator("#passwordEntry")

    def _stay_signed_in_close(self):
        return self._page.locator("#close-button")

    # ── Actions ───────────────────────────────────────────────

    def navigate(self):
        self._page.goto(LOGIN_URL)
        self._email_input().wait_for(state="visible", timeout=timeouts.NAVIGATION)

    def login(self, email: str, password: str):
        self._email_input().fill(email)
        self._page.keyboard.press("Enter")

        self._password_input().wait_for(state="visible", timeout=timeouts.NAVIGATION)
        self._password_input().fill(password)
        self._page.keyboard.press("Enter")

        # dismiss "Stay signed in?" if it appears
        try:
            self._stay_signed_in_close().wait_for(state="visible", timeout=timeouts.OPTIONAL_DIALOG)
            self._stay_signed_in_close().click()
        except PlaywrightTimeoutError:
            pass  # dialog did not appear — safe to continue

        self._page.wait_for_url("**/mail/**", timeout=timeouts.NETWORK)

    # ── Assertions ────────────────────────────────────────────

    def should_be_displayed(self):
        # After logout Outlook redirects to ConsumerSignout.html, not back to the
        # login form directly. Confirming we left the mail app is the correct signal.
        self._page.wait_for_url(
            lambda url: "ConsumerSignout" in url or "login.live.com" in url or "login.microsoftonline.com" in url,
            timeout=timeouts.NAVIGATION,
        )
