from playwright.sync_api import sync_playwright


def test_username_length():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        page.fill("input[name='username']", "ab")  # Enter a username with less than 3 characters
        page.fill("input[name='password']", "abc123")
        page.click("input#signInBtn")

        # Check for modal or alert
        if page.locator('.modal-body').count() > 0:
            txt = page.locator('.modal-body').inner_text()
            assert 'at least 3' in txt or 'limited to only fewer' in txt
        else:
            alerts = page.locator('.alert, .alert-danger, .error-message')
            assert alerts.count() > 0
            assert '3' in alerts.nth(0).inner_text()