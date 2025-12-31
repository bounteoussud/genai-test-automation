# agents/requirement_agent.py

from llm.ollama_client import ask_ollama
from utils.excel_writer import write_manual_tests
from utils.logger import get_logger

logger = get_logger("RequirementAgent")


def generate_manual_tests(user_story: str, requirement_hash: str):
    logger.info("Generating manual test cases")

    prompt = f"""
You are a Senior QA Analyst.

Application URL:
https://rahulshettyacademy.com/loginpagePractise/

Your task:
Generate comprehensive MANUAL TEST CASES.

Scope:
1. Pre-login scenarios
2. Post-login scenarios

Cover:
- UI validation
- Field validations
- Positive login flow
- Negative login scenarios
- Error messages
- Navigation after login
- Logout behavior

STRICT OUTPUT FORMAT:
Each test case MUST be in ONE LINE using pipe (|).

Format:
TC_ID | Scenario | Steps | Expected Result

Rules:
- TC_ID must be numeric only (1, 2, 3...)
- Steps must be numbered: 1. 2. 3.
- NO headings
- NO markdown
- NO blank lines
"""

    response = ask_ollama(prompt, model="llama3")
    logger.info(f"Raw LLM Output:\n{response}")

    if not response or not response.strip():
        raise Exception("LLM returned empty response for manual test cases")

    # ✅ Use the passed requirement_hash directly
    write_manual_tests(response, requirement_hash)

    logger.info("Manual test cases generated and saved to Excel")
