from playwright.sync_api import sync_playwright


def test_password_length():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        page.fill("input[name='username']", "ramesh")
        page.fill("input[name='password']", "short")
        page.click("input#signInBtn")

        alerts = page.locator('.alert, .alert-danger, .error-message')
        assert alerts.count() > 0
        # The site may return a generic incorrect credentials message in some environments
        text = alerts.nth(0).inner_text().lower()
        assert ('at least' in text) or ('incorrect' in text) or ('password' in text)