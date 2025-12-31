import os
from playwright.sync_api import sync_playwright


def test_invalid_login():
    headless = os.getenv('HEADLESS', '1') != '0'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        page.fill("input[name='username']", "invalid_username")
        page.fill("input[name='password']", "invalid_password")
        page.click("input#signInBtn")

        # Check for modal first, then alerts
        if page.locator('.modal-body').count() > 0:
            txt = page.locator('.modal-body').inner_text()
            assert 'Invalid' in txt or 'limited to only fewer' in txt
        else:
            alerts = page.locator('.alert, .alert-danger')
            if alerts.count() > 0:
                assert 'Invalid' in alerts.nth(0).inner_text()
            else:
                raise AssertionError('No error modal or alert found after invalid login')