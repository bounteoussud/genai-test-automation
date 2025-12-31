from playwright.sync_api import sync_playwright


def test_login_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        page.fill("input[name='username']", "rahulshetty")
        page.fill("input[name='password']", "learning")
        page.click("input#signInBtn")

        # navigate to dashboard page and verify title contains site name
        page.goto("https://rahulshettyacademy.com/dashboardPractise/")
        page.wait_for_load_state("networkidle")
        assert "Rahul Shetty Academy" in page.title()