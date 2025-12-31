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


def test_pre_login(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.fill("input[name='username']", "")
    page.click("input#signInBtn")
    # The page shows a modal when username is empty; assert that modal text appears
    modal_text = page.locator('.modal-body').inner_text()
    assert 'limited to only fewer functionalities' in modal_text