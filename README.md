# Outlook Email Automation — Block Level 3

Automated test for the full email flow in Outlook Web (outlook.live.com):
**Login → Compose → Add recipient from contacts → Attach file → Send → Logout**

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

Edit `.env` and fill in your Outlook credentials:

```
EMAIL=your_email@outlook.com
PASSWORD=your_password
```

> **Note:** The account must have at least one saved contact pointing to a valid email address. The test uses the contact named `"Test"`.

### 3. Prepare test attachment

The file `test_data/test_attachment.txt` is already included. It is attached to the email during the test.

---

## Running the tests

### Headed (visible browser — recommended for demos)

```bash
py -m pytest steps/test_send_email.py -v
```

### Headless

Edit `steps/conftest.py` and change `headless=False` to `headless=True`, then run:

```bash
py -m pytest steps/test_send_email.py -v
```

---

## Project structure

```
├── features/
│   └── send_email_with_attachment.feature   # Gherkin scenario (Block 3)
├── pages/
│   ├── login_page.py                        # Login flow page object
│   ├── inbox_page.py                        # Inbox actions (compose, logout)
│   └── compose_page.py                      # Compose dialog (To, Subject, Body, Attach, Send)
├── steps/
│   ├── conftest.py                          # Playwright browser/page fixtures
│   └── test_send_email.py                   # Gherkin step definitions
├── test_data/
│   └── test_attachment.txt                  # File attached during the test
├── conftest.py                              # Root conftest — loads .env
├── pytest.ini                               # Pytest + BDD configuration
└── requirements.txt                         # Python dependencies
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

  When the user logs out
  Then the login page should be displayed
```
