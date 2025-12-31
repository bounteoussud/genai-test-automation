from playwright.sync_api import sync_playwright


def test_invalid_credentials():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        page.fill("#username", "invalid_username")
        page.fill("#password", "invalid_password")
        page.click("input#signInBtn")

        # If a modal appears first, dismiss it then check for the invalid credentials alert
        if page.locator('.modal-body').count() > 0:
            # dismiss modal
            page.evaluate("() => { const b = document.querySelector('#okayBtn'); if (b) b.click(); }")
            page.wait_for_timeout(500)

        alerts = page.locator('.alert, .alert-danger, .error-message')
        assert alerts.count() > 0
        txt = alerts.nth(0).inner_text().lower()
        assert ('invalid' in txt) or ('incorrect' in txt) or ('username' in txt and 'password' in txt)