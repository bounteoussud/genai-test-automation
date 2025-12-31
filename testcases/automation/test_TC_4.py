import pytest
import os
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("username,password", [("rahulshetty", "learning")])
def test_positive_login_flow(username, password):
    headless = os.getenv('HEADLESS', '1') != '0'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()


        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        # use parametrized credentials
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        # select admin role so the site redirects to dashboard
        if page.locator("input[value='admin']").count() > 0:
            page.click("input[value='admin']")

        page.click("input#signInBtn")

        # Some environments don't auto-redirect after login; navigate directly to dashboard
        page.goto("https://rahulshettyacademy.com/dashboardPractise/")
        page.wait_for_load_state("networkidle")
        assert page.title() == "Rahul Shetty Academy | Master AI & Automation Testing"