import os

from playwright.sync_api import Page

from pages import timeouts


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
        name = os.environ["ACCOUNT_NAME"]
        return self._page.locator(f"button[aria-label='{name}']")

    def _sign_out_button(self):
        return self._page.locator(
            "[aria-label='Odhlásiť sa z tohto konta'], "
            "[aria-label='Odhlásiť sa'], "
            "[aria-label='Sign out of this account'], "
            "[aria-label='Sign out'], "
            "a:has-text('Odhlásiť sa'), "
            "a:has-text('Sign out')"
        ).first

    # ── Actions ───────────────────────────────────────────────

    def open_compose(self):
        self._compose_button().wait_for(state="visible", timeout=timeouts.NAVIGATION)
        self._compose_button().click()
        # wait for compose send button — signals compose dialog is fully rendered
        self._page.locator(
            "button[aria-label='Odoslať'], button[aria-label='Send']"
        ).first.wait_for(state="visible", timeout=timeouts.UI_RESPONSE)

    def logout(self):
        self._account_button().wait_for(state="visible", timeout=timeouts.UI_RESPONSE)
        self._account_button().click()
        self._sign_out_button().wait_for(state="visible", timeout=timeouts.UI_RESPONSE)
        self._sign_out_button().click()

    # ── Assertions ────────────────────────────────────────────

    def should_be_displayed(self):
        self._compose_button().wait_for(state="visible", timeout=timeouts.PAGE_LOAD)
        self._page.wait_for_url("**/mail/**", timeout=timeouts.PAGE_LOAD)

    def should_receive_email_with_subject(self, subject: str):
        # Inbox email list items are div[role='option'] whose aria-label contains the subject.
        # Outlook delivers self-sent emails within seconds — allow up to 60s for propagation.
        email_item = self._page.locator(f"div[role='option'][aria-label*='{subject}']").first
        email_item.wait_for(state="visible", timeout=timeouts.EMAIL_DELIVERY)
