from crewai.tools import BaseTool
from playwright.sync_api import sync_playwright

class PlaywrightTool(BaseTool):
    name: str = "playwright_ui_automation"
    description: str = "Runs Playwright UI tests on the given application URL"

    def _run(self, app_url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(app_url)
            title = page.title()

            screenshot_path = "outputs/amazon_home.png"
            page.screenshot(path=screenshot_path)

            browser.close()

        return f"""
        UI Automation Completed:
        - URL opened: {app_url}
        - Page title: {title}
        - Screenshot saved at: {screenshot_path}
        """
