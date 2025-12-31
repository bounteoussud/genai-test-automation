import os
import pytest
from playwright.sync_api import sync_playwright


def test_pre_login_empty_password():
    headless = os.getenv('HEADLESS', '1') != '0'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        page.fill("input[name='username']", "ramesh")
        page.fill("input[name='password']", "")  # Leave password field empty
        page.click("input#signInBtn")

        # The page displays a modal when credentials are incomplete; assert modal text or any error-like element
        # Try modal first
        if page.locator('.modal-body').count() > 0:
            modal_text = page.locator('.modal-body').inner_text()
            assert 'limited to only fewer functionalities' in modal_text
        else:
            # fallback to any alert element text
            alerts = page.locator(".alert, .alert-danger")
            if alerts.count() > 0:
                assert 'Password' in alerts.nth(0).inner_text()
            else:
                pytest.fail('No modal or alert shown after submitting empty password')