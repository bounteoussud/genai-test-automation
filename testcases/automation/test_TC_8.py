from playwright.sync_api import sync_playwright


def test_invalid_password():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        page.fill("input[name='username']", "rahul")
        page.fill("input[name='password']", "invalid_password")
        page.click("input#signInBtn")

        # Look for any alert/modal indicating invalid credentials
        if page.locator('.modal-body').count() > 0:
            # If a modal appeared, click Okay then check alerts
            page.evaluate("() => { const b = document.querySelector('#okayBtn'); if (b) b.click(); }")
            page.wait_for_timeout(500)
        alerts = page.locator('.alert, .alert-danger, .error-message')
        assert alerts.count() > 0
        txt = alerts.nth(0).inner_text().lower()
        assert ('invalid' in txt) or ('incorrect' in txt) or ('username' in txt or 'password' in txt)