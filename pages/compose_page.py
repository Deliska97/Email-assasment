import os
from pathlib import Path
from playwright.sync_api import Page, expect


TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"


class ComposePage:
    def __init__(self, page: Page):
        self._page = page

    # ── Elements ──────────────────────────────────────────────

    def _to_field(self):
        # Outlook Web uses a contenteditable div for the To pill input
        return self._page.locator("div[aria-label='Komu'], div[aria-label='To']").first

    def _subject_input(self):
        return self._page.locator(
            "input[aria-label='Predmet'], input[aria-label='Subject'], "
            "input[placeholder='Pridať predmet'], input[placeholder='Add a subject']"
        )

    def _body_field(self):
        return self._page.locator(
            "div[role='textbox'][aria-label*='Telo'], "
            "div[role='textbox'][aria-label*='Message body'], "
            "div[role='textbox']"
        ).first

    def _attach_button(self):
        return self._page.locator(
            "button[aria-label*='Priložiť'], button[aria-label*='Attach']"
        ).first

    def _send_button(self):
        return self._page.locator(
            "button[aria-label='Odoslať'], button[aria-label='Send']"
        ).first

    def _discard_button(self):
        return self._page.locator("#discardCompose")

    # ── Actions ───────────────────────────────────────────────

    def add_recipient_from_contacts(self, name: str):
        self._to_field().wait_for(state="visible", timeout=10000)
        self._to_field().click()
        self._page.keyboard.type(name, delay=100)

        # contact suggestions are <button role="option">; inbox threads are <div role="option">
        # filtering to button avoids false matches from inbox search results
        suggestion = self._page.locator("button[role='option']").filter(
            has_text=name.lower()
        ).first
        suggestion.wait_for(state="visible", timeout=8000)
        suggestion.click()

    def enter_subject(self, subject: str):
        self._subject_input().wait_for(state="visible", timeout=5000)
        self._subject_input().fill(subject)

    def enter_body(self, body: str):
        self._body_field().wait_for(state="visible", timeout=5000)
        self._body_field().click()
        self._page.keyboard.type(body)

    def attach_file(self, filename: str):
        file_path = TEST_DATA_DIR / filename
        self._attach_button().wait_for(state="visible", timeout=5000)
        self._attach_button().click()

        # Outlook opens a sub-menu: "Prehľadávať tento počítač" (SK) / "Browse This Computer" (EN)
        browse_computer = self._page.locator(
            "button[role='menuitem'][aria-label*='Prehľad'], "
            "button[role='menuitem'][aria-label*='Browse'], "
            "button[role='menuitem'][aria-label*='computer'], "
            "button[role='menuitem'][aria-label*='device']"
        )

        browse_computer.wait_for(state="visible", timeout=5000)
        with self._page.expect_file_chooser() as fc_info:
            browse_computer.click()
        fc_info.value.set_files(str(file_path))

        # wait for attachment chip to appear (file uploaded to server)
        attachment = self._page.locator(f"[aria-label*='{filename}'], [title*='{filename}']").first
        attachment.wait_for(state="visible", timeout=20000)

    def send(self):
        # Ctrl+Enter sends from the active compose dialog regardless of other
        # send buttons present in the reading pane
        self._send_button().wait_for(state="visible", timeout=5000)
        self._body_field().click()
        self._page.keyboard.press("Control+Enter")

    # ── Assertions ────────────────────────────────────────────

    def should_be_sent_successfully(self):
        # after sending, the compose body (textbox) disappears as the dialog closes
        body = self._page.locator(
            "div[role='textbox'][aria-label*='Telo'], "
            "div[role='textbox'][aria-label*='Message body']"
        )
        expect(body).not_to_be_visible(timeout=20000)
