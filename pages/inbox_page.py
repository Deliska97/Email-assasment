from playwright.sync_api import Page


class InboxPage:
    def __init__(self, page: Page):
        self._page = page

    # ── Elements ──────────────────────────────────────────────

    def _compose_button(self):
        # "Nová pošta" in SK locale, "New mail" in EN locale
        return self._page.locator(
            "button[aria-label='Nová pošta'], button[aria-label='New mail']"
        )

    def _account_button(self):
        return self._page.locator("button[aria-label='Adam Test']")

    def _sign_out_button(self):
        return self._page.locator(
            "[aria-label='Odhlásiť sa z tohto konta'], [aria-label='Sign out']"
        )

    # ── Actions ───────────────────────────────────────────────

    def open_compose(self):
        self._compose_button().wait_for(state="visible", timeout=15000)
        self._compose_button().click()
        # wait for compose send button — signals compose dialog is fully rendered
        self._page.locator(
            "button[aria-label='Odoslať'], button[aria-label='Send']"
        ).first.wait_for(state="visible", timeout=10000)

    def logout(self):
        self._account_button().wait_for(state="visible", timeout=10000)
        self._account_button().click()
        self._sign_out_button().wait_for(state="visible", timeout=5000)
        self._sign_out_button().click()

    # ── Assertions ────────────────────────────────────────────

    def should_be_displayed(self):
        self._compose_button().wait_for(state="visible", timeout=20000)
        self._page.wait_for_url("**/mail/**", timeout=20000)
