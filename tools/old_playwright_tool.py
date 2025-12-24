"""Playwright automation tool for UI testing."""

from crewai.tools import BaseTool
from playwright.sync_api import sync_playwright


class PlaywrightTool(BaseTool):
    name: str = "playwright_ui_automation"
    description: str = "Runs Playwright UI automation for a given application URL"

    def _run(self, app_url: str) -> str:
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Test Case 1: Open homepage
            page.goto(app_url)
            results.append("Opened homepage successfully")

            # Test Case 2: Validate page title
            title = page.title()
            results.append(f"Page title: {title}")

            # Capture screenshot
            page.screenshot(path="amazon_home.png")
            results.append("Screenshot captured")

            browser.close()

        # CrewAI tools must return string
        return "\n".join(results)
