from playwright.sync_api import Page

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
        self._email_input().wait_for(state="visible", timeout=15000)

    def login(self, email: str, password: str):
        self._email_input().fill(email)
        self._page.keyboard.press("Enter")

        self._password_input().wait_for(state="visible", timeout=15000)
        self._password_input().fill(password)
        self._page.keyboard.press("Enter")

        # dismiss "Stay signed in?" if it appears
        try:
            self._stay_signed_in_close().wait_for(state="visible", timeout=6000)
            self._stay_signed_in_close().click()
        except Exception:
            pass

        self._page.wait_for_function(
            "!window.location.href.includes('login.live.com')",
            timeout=30000,
        )

    # ── Assertions ────────────────────────────────────────────

    def should_be_displayed(self):
        # after logout Outlook redirects to microsoft.com or login.live.com
        # — either way the inbox compose button must be gone
        self._page.wait_for_function(
            "!window.location.href.includes('outlook.live.com/mail')",
            timeout=15000,
        )
