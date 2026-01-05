# agents/requirement_agent.py

from llm.ollama_client import ask_ollama
from utils.excel_writer import write_manual_tests
from utils.logger import get_logger

logger = get_logger("RequirementAgent")


def generate_manual_tests(user_story: str, requirement_hash: str):
    logger.info("Generating manual test cases")

    prompt = f"""
We are developing manual test cases based on the following user story:

Application URL:
https://www.opencart.com/index.php

Your task:
Generate comprehensive MANUAL TEST CASES.

Scope:
1. Login scenarios

STRICT OUTPUT FORMAT (VERY IMPORTANT):
Each test case MUST be in EXACTLY ONE LINE.

Format:
TC_ID | Scenario | Steps | Expected Result

CRITICAL RULES:
- Use ONLY 3 pipe symbols (|) per line
- Steps MUST be written in a SINGLE column
- Separate steps using semicolon (;)
- DO NOT use pipe (|) inside Steps or Expected Result
- TC_ID must be numeric only (1,2,3...)
- NO headings
- NO markdown
- NO blank lines
- NO extra text

EXAMPLE (FOLLOW EXACTLY):
1 | Login with valid credentials | Navigate to Application URL ; Click on Login; Enter username and password; Click Login | User logged in successfully

"""

    response = ask_ollama(prompt, model="llama3")

    if not response or not response.strip():
        raise Exception("LLM returned empty response")

    logger.info("Cleaning LLM output before saving to Excel")

    cleaned_lines = []
    for line in response.splitlines():
        line = line.strip()

        # Skip garbage lines
        if not line:
            continue
        if not line[0].isdigit():
            continue

        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            logger.warning(f"Skipping invalid line: {line}")
            continue

        cleaned_lines.append(" | ".join(parts))

    if not cleaned_lines:
        raise Exception("No valid test cases parsed from LLM output")

    cleaned_response = "\n".join(cleaned_lines)

    write_manual_tests(cleaned_response, requirement_hash)

    logger.info("Manual test cases generated and saved to Excel")
