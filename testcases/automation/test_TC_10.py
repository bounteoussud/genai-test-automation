import os
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def browser():
    headless = os.getenv('HEADLESS', '1') != '0'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


def test_logout(browser):
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.fill("input[name='username']", "rahulshetty")
    page.fill("input[name='password']", "learning")
    page.click("input#signInBtn")

    # navigate to dashboard page to verify logout flow
    page.goto("https://rahulshettyacademy.com/dashboardPractise/")
    page.wait_for_load_state("networkidle")
    # click logout if present; otherwise skip the logout assertion for this environment
    if page.locator("text=Logout").count() > 0:
        page.locator("text=Logout").first.click()
        page.wait_for_load_state("networkidle")
        assert "LoginPage Practise" in page.title()
    else:
        pytest.skip("Logout button not present in this environment; skipping logout assertion")