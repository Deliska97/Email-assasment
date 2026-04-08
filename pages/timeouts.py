"""Centralised timeout constants (all values in milliseconds).

Intent-based names communicate *why* an operation might take time,
making each wait self-documenting at the call site.
"""

ELEMENT_VISIBLE = 5_000    # element is already part of the rendered DOM
UI_RESPONSE     = 10_000   # element appears as a result of a user interaction
NAVIGATION      = 15_000   # page-level navigation / URL transition
PAGE_LOAD       = 20_000   # full page load with dynamic content
NETWORK         = 30_000   # network operations (login redirect, file upload)
EMAIL_DELIVERY  = 60_000   # email propagation latency before inbox delivery
OPTIONAL_DIALOG = 5_000    # dialogs that may not appear; timeout == "not shown"
