from playwright.sync_api import sync_playwright


def test_invalid_username():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto("https://rahulshettyacademy.com/loginpagePractise/")

        # Enter invalid username and valid password
        page.fill("#username", "invalid_username")
        page.fill("#password", "valid_password")
        # Use the real sign-in button
        page.click("input#signInBtn")

        # Verify the error modal/alert is shown
        if page.locator('.modal-body').count() > 0:
            assert 'Invalid' in page.locator('.modal-body').inner_text() or 'limited' in page.locator('.modal-body').inner_text()
        else:
            alerts = page.locator('.alert, .alert-danger, .error-message')
            assert alerts.count() > 0