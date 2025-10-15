# Application URLs per environment
ENVIRONMENTS = {
    "qa": "https://yuvanbank-qa-r1-test.netlify.app",
    "stage": "https://yuvanbank-stage-r1-test.netlify.app",
    "prod": "https://yuvanbank-prod.netlify.app/"
}

# Default environment
DEFAULT_ENV = "qa"

# Timeout settings
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
POLL_FREQUENCY = 0.5

# Browser settings
BROWSER = "chrome"   # chrome / firefox / edge
HEADLESS = False

# Test data defaults (can be overridden from Excel)
DEFAULT_PASSWORD = "Password123!"
DEFAULT_EMAIL_DOMAIN = "testmail.com"

# User credentials (if needed for login tests)
USERS = {
    "admin": {"email": "admin@testmail.com", "password": "Admin@123"},
    "user": {"email": "user@testmail.com", "password": "User@123"},
}
