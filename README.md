# Outlook Email Automation — Block Level 3

Automated test for the full email flow in Outlook Web (outlook.live.com):
**Login → Compose → Add recipient from contacts → Attach file → Send → Verify delivery → Logout**

Built with **Playwright + Pytest-BDD (Python)**.

---

## Requirements

- Python 3.10+
- pip

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your Outlook account details:

```
EMAIL=your_email@outlook.com
PASSWORD=your_password
ACCOUNT_NAME=Your Display Name
```

> **Note:** The account must have a contact named `"Test"` saved in Outlook contacts pointing to a valid email address. The test sends the email to that contact and verifies it arrives in the inbox.

> **Known issue — credentials in `.env`:** This project uses a dedicated test account created solely for this assessment. Credentials are stored in `.env` (gitignored) as a pragmatic shortcut for a throwaway account. In production, credentials would never live in a file on disk — they would be injected at runtime via secure secret management (e.g. GitHub Actions secrets, HashiCorp Vault). This trade-off is intentional and acceptable only because the account has no real data and exists exclusively for automated testing.

### 3. Test attachment

`test_data/test_attachment.txt` is already included and will be attached during the test.

---

## Running the tests

### Headed (visible browser — default)

```bash
py -m pytest -v
```

### Headless

```bash
HEADLESS=true py -m pytest -v
```

---

## Project structure

```
├── features/
│   └── send_email_with_attachment.feature   # Gherkin scenario (Block 3)
├── pages/
│   ├── login_page.py                        # Page Object: login flow
│   ├── inbox_page.py                        # Page Object: inbox, compose trigger, logout
│   └── compose_page.py                      # Page Object: compose dialog
├── steps/
│   └── test_send_email.py                   # Gherkin step definitions
├── test_data/
│   └── test_attachment.txt                  # File attached during the test
├── conftest.py                              # Playwright fixtures + .env loading
├── pytest.ini                               # Pytest + BDD configuration
├── requirements.txt                         # Python dependencies
└── .env.example                             # Credentials template
```

---

## Gherkin scenario

```gherkin
Scenario: Send an email with attachment to a saved contact and logout
  Given the user is on the Outlook login page
  When the user logs in with valid credentials
  Then the inbox should be displayed

  When the user composes a new email
  And the user adds recipient "Test" from contacts
  And the user enters the subject "Test Automation Task"
  And the user enters the body "This email was sent by an automated test."
  And the user attaches the file "test_attachment.txt"
  And the user sends the email
  Then the email should be sent successfully
  And the inbox should receive an email with subject "Test Automation Task"

  When the user logs out
  Then the login page should be displayed
```
