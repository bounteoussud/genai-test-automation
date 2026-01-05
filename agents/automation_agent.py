# agents/automation_agent.py
import os
import re
import ast
import pandas as pd
from llm.ollama_client import ask_ollama
from utils.logger import get_logger

logger = get_logger("AutomationAgent")

EXCEL_PATH = "testcases/manual/testcases.xlsx"
AUTOMATION_DIR = "testcases/automation"
CONFTEST_PATH = os.path.join(AUTOMATION_DIR, "conftest.py")


# ---------------------------------------------------
# CREATE CONFTST.PY (CRITICAL FIX)
# ---------------------------------------------------
def create_conftest_if_missing():
    os.makedirs(AUTOMATION_DIR, exist_ok=True)

    if os.path.exists(CONFTEST_PATH):
        return

    conftest_code = """import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # SEE browser actions
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()
"""

    with open(CONFTEST_PATH, "w", encoding="utf-8") as f:
        f.write(conftest_code)

    logger.info("conftest.py generated successfully")


# ---------------------------------------------------
# UTILITIES
# ---------------------------------------------------
def extract_python_code(response: str) -> str:
    if not response:
        return ""

    match = re.search(r"```(?:python)?(.*?)```", response, re.DOTALL)
    if match:
        return match.group(1).strip()

    return response.strip()


def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        logger.error(f"Syntax error in generated code: {e}")
        return False


# ---------------------------------------------------
# MAIN SCRIPT GENERATOR
# ---------------------------------------------------
def generate_automation_scripts():
    logger.info("Starting automation script generation")

    if not os.path.exists(EXCEL_PATH):
        logger.error("Manual test case Excel not found")
        return

    create_conftest_if_missing()

    df = pd.read_excel(EXCEL_PATH, header=2)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["TC_ID"])

    for _, row in df.iterrows():
        tc_id = int(row["TC_ID"])
        file_path = os.path.join(AUTOMATION_DIR, f"test_TC_{tc_id}.py")

        if os.path.exists(file_path):
            logger.info(f"Script already exists for TC_{tc_id}, skipping")
            continue

        prompt = f"""
You are a Senior QA Automation Engineer.

Convert the MANUAL TEST CASE into an EXECUTABLE pytest + Playwright test.

STRICT RULES (NO EXCEPTIONS):
- Output ONLY valid Python code
- NO markdown, NO explanations, NO comments
- Use Playwright SYNC API only
- Use pytest
- Use existing `page` fixture (DO NOT create fixture)
- One test function only
- Test name must be: test_TC_{tc_id}
- Use real URL: https://www.opencart.com/index.php
- Convert EACH step EXACTLY as written
- DO NOT invent steps
- DO NOT change step meaning
- If selector is unclear, use text-based selector
- Use only: page.goto, page.click, page.fill
- End with at least ONE assert
- DO NOT use example.com
- DO NOT define fixtures
- DO NOT use sync_playwright

MANDATORY STRUCTURE:

import pytest

def test_TC_{tc_id}(page):
    page.goto("https://www.opencart.com/index.php")
    ...

Manual Test Case:
Scenario: {row["Scenario"]}
Steps: {row["Steps"]}
Expected Result: {row["Expected Result"]}
"""

        script = None
        MAX_RETRIES = 3

        for attempt in range(1, MAX_RETRIES + 1):
            logger.info(f"Generating TC_{tc_id} (Attempt {attempt})")

            raw = ask_ollama(prompt, model="llama3")
            script = extract_python_code(raw)

            if script and is_valid_python(script):
                break

            logger.warning(f"Invalid code attempt {attempt} for TC_{tc_id}")

        if not script or not is_valid_python(script):
            logger.error(f"Failed to generate valid script for TC_{tc_id}")
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(script)

        logger.info(f"Automation script created for TC_{tc_id}")

    logger.info("Automation script generation completed")
