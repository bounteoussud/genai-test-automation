import os
from agents.requirement_agent import generate_manual_tests
from agents.automation_agent import generate_automation_scripts
from agents.execution_agent import execute_automation_tests
from utils.requirement_hash import get_requirement_hash
from utils.excel_validator import is_excel_valid
from utils.logger import get_logger

logger = get_logger("Main")

user_requirement = """
Login functionality for Facebook website.
Validate pre-login, login, and post-login scenarios.
"""

excel_path = "testcases/manual/testcases.xlsx"
req_hash = get_requirement_hash(user_requirement)

if not os.path.exists(excel_path):
    logger.info("Manual test cases not found. Generating...")
    generate_manual_tests(user_requirement, req_hash)

elif not is_excel_valid(req_hash):
    logger.info("Requirement changed. Regenerating manual tests...")
    generate_manual_tests(user_requirement, req_hash)

else:
    logger.info("Manual test cases are up-to-date.")

# Generate automation only if missing
generate_automation_scripts()

# Execute automation & show consolidated result
execute_automation_tests()
