import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from pages.login_page import LoginPage
from pages.inbox_page import InboxPage
from pages.compose_page import ComposePage

scenarios("send_email_with_attachment.feature")


# ── Given ────────────────────────────────────────────────────

@given("the user is on the Outlook login page")
def navigate_to_login(login_page: LoginPage):
    login_page.navigate()


# ── When ─────────────────────────────────────────────────────

@when("the user logs in with valid credentials")
def login(login_page: LoginPage):
    login_page.login(
        email=os.environ["EMAIL"],
        password=os.environ["PASSWORD"],
    )


@when("the user composes a new email")
def open_compose(inbox_page: InboxPage):
    inbox_page.open_compose()


@when(parsers.parse('the user adds recipient "{name}" from contacts'))
def add_recipient(compose_page: ComposePage, name: str):
    compose_page.add_recipient_from_contacts(name)


@when(parsers.parse('the user enters the subject "{subject}"'))
def enter_subject(compose_page: ComposePage, subject: str):
    compose_page.enter_subject(subject)


@when(parsers.parse('the user enters the body "{body}"'))
def enter_body(compose_page: ComposePage, body: str):
    compose_page.enter_body(body)


@when(parsers.parse('the user attaches the file "{filename}"'))
def attach_file(compose_page: ComposePage, filename: str):
    compose_page.attach_file(filename)


@when("the user sends the email")
def send_email(compose_page: ComposePage):
    compose_page.send()


@when("the user logs out")
def logout(inbox_page: InboxPage):
    inbox_page.logout()


# ── Then ─────────────────────────────────────────────────────

@then("the inbox should be displayed")
def inbox_should_be_displayed(inbox_page: InboxPage):
    inbox_page.should_be_displayed()


@then("the email should be sent successfully")
def email_should_be_sent(compose_page: ComposePage):
    compose_page.should_be_sent_successfully()


@then(parsers.parse('the inbox should receive an email with subject "{subject}"'))
def inbox_should_receive_email(inbox_page: InboxPage, subject: str):
    inbox_page.should_receive_email_with_subject(subject)


@then("the login page should be displayed")
def login_page_should_be_displayed(login_page: LoginPage):
    login_page.should_be_displayed()
