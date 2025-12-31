import os
import ast
import pandas as pd
from llm.ollama_client import ask_ollama
from utils.logger import get_logger

logger = get_logger("AutomationAgent")

EXCEL_PATH = "testcases/manual/testcases.xlsx"
AUTOMATION_DIR = "testcases/automation"


def sanitize_python_code(code: str) -> str:
    lines = code.splitlines()
    cleaned = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("Here", "Sure", "Note", "Let me", "```")):
            continue
        cleaned.append(line)

    return "\n".join(cleaned).strip()


def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def generate_automation_scripts():
    logger.info("Starting automation script generation")

    if not os.path.exists(EXCEL_PATH):
        logger.error("Manual test case Excel not found")
        return

    df = pd.read_excel(EXCEL_PATH, header=2)
    df.columns = df.columns.str.strip()

    required_columns = {"TC_ID", "Scenario", "Steps", "Expected Result"}
    if not required_columns.issubset(df.columns):
        logger.error("Invalid Excel format")
        return

    df = df.dropna(subset=["TC_ID"])
    os.makedirs(AUTOMATION_DIR, exist_ok=True)

    for _, row in df.iterrows():
        tc_id = int(row["TC_ID"])
        file_path = os.path.join(AUTOMATION_DIR, f"test_TC_{tc_id}.py")

        # 🔒 DO NOT RECREATE IF EXISTS
        if os.path.exists(file_path):
            logger.info(f"Script already exists for TC_{tc_id}, skipping")
            continue

        prompt = f"""
Generate ONLY valid Python code.

STRICT RULES:
- Use playwright.sync_api ONLY
- DO NOT use async_playwright
- DO NOT use pytest.mark.asyncio
- Output executable pytest test
- No explanations

Use URL:
https://rahulshettyacademy.com/loginpagePractise/

Scenario: {row['Scenario']}
Steps: {row['Steps']}
Expected: {row['Expected Result']}
"""

        raw = ask_ollama(prompt, model="llama3")
        code = sanitize_python_code(raw)

        if not code or not is_valid_python(code):
            logger.error(f"Invalid code for TC_{tc_id}")
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        logger.info(f"Created automation script: {file_path}")
