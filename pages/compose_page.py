from pathlib import Path

from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Page, expect

from pages import timeouts

TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"


class ComposePage:
    def __init__(self, page: Page):
        self._page = page

    # ── Elements ──────────────────────────────────────────────

    def _to_field(self):
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

    # ── Actions ───────────────────────────────────────────────

    def add_recipient_from_contacts(self, name: str):
        self._to_field().wait_for(state="visible", timeout=timeouts.UI_RESPONSE)
        self._to_field().click()
        self._page.keyboard.type(name, delay=100)

        # Outlook renders contact suggestions as <button role="option"> and inbox
        # search results as <div role="option">. Restricting to button avoids
        # false matches when the inbox already contains emails whose subject or
        # body contains the typed name. .first is safe here because the account
        # has a single contact matching the provided name.
        suggestion = self._page.locator("button[role='option']").filter(has_text=name).first
        suggestion.wait_for(state="visible", timeout=timeouts.UI_RESPONSE)
        suggestion.click()

    def enter_subject(self, subject: str):
        self._subject_input().wait_for(state="visible", timeout=timeouts.ELEMENT_VISIBLE)
        self._subject_input().fill(subject)

    def enter_body(self, body: str):
        self._body_field().wait_for(state="visible", timeout=timeouts.ELEMENT_VISIBLE)
        self._body_field().click()
        self._page.keyboard.type(body)

    def attach_file(self, filename: str):
        file_path = TEST_DATA_DIR / filename
        self._attach_button().wait_for(state="visible", timeout=timeouts.ELEMENT_VISIBLE)
        self._attach_button().click()

        # Outlook opens a sub-menu: "Prehľadávať tento počítač" (SK) / "Browse This Computer" (EN)
        browse_computer = self._page.locator(
            "button[role='menuitem'][aria-label*='Prehľad'], "
            "button[role='menuitem'][aria-label*='Browse'], "
            "button[role='menuitem'][aria-label*='computer'], "
            "button[role='menuitem'][aria-label*='device']"
        )
        browse_computer.wait_for(state="visible", timeout=timeouts.UI_RESPONSE)

        # Intercept the upload POST response directly — this is the only reliable
        # signal that the file is on the server. networkidle never fires on Outlook
        # (background polling keeps connections open), and a page-level progressbar
        # selector picks up unrelated Outlook indicators.
        with self._page.expect_response(
            lambda r: r.request.method == "POST" and "attachment" in r.url.lower(),
            timeout=timeouts.NETWORK,
        ):
            with self._page.expect_file_chooser() as fc_info:
                browse_computer.click()
            fc_info.value.set_files(str(file_path))

        # UI-level sanity check: chip must be visible before we proceed
        attachment = self._page.locator(f"[aria-label*='{filename}'], [title*='{filename}']").first
        attachment.wait_for(state="visible", timeout=timeouts.UI_RESPONSE)

    def send(self):
        # Ctrl+Enter sends from the active compose dialog regardless of other
        # send buttons present in the reading pane
        self._send_button().wait_for(state="visible", timeout=timeouts.ELEMENT_VISIBLE)
        self._body_field().click()
        self._page.keyboard.press("Control+Enter")

        # safety net: dismiss "attachments still loading" dialog if it slips through
        upload_ok = self._page.locator("button:has-text('OK')").first
        try:
            upload_ok.wait_for(state="visible", timeout=timeouts.OPTIONAL_DIALOG)
            upload_ok.click()
            upload_ok.wait_for(state="hidden", timeout=timeouts.NETWORK)
            self._body_field().click()
            self._page.keyboard.press("Control+Enter")
        except PlaywrightTimeoutError:
            pass  # dialog did not appear — send went through cleanly

    # ── Assertions ────────────────────────────────────────────

    def should_be_sent_successfully(self):
        # Outlook Web does not expose a dedicated "sent" confirmation element.
        # The most reliable available signal is that the compose dialog closes,
        # which causes the message body textbox to leave the DOM. End-to-end
        # delivery is separately verified by should_receive_email_with_subject().
        body = self._page.locator(
            "div[role='textbox'][aria-label*='Telo'], "
            "div[role='textbox'][aria-label*='Message body']"
        )
        expect(body).not_to_be_visible(timeout=timeouts.PAGE_LOAD)
