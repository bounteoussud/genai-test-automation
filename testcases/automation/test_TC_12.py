from playwright.sync_api import sync_playwright


def test_pre_login_valid_credentials():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto("https://rahulshettyacademy.com/loginpagePractise/")

        # Enter valid username and password without clicking the login button
        page.fill("#username", "rahulshetty")
        page.fill("#password", "Learning@123")

        # No action should be taken, so we expect the login page title to remain
        assert "LoginPage Practise" in page.title()

        browser.close()