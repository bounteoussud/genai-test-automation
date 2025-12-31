# agents/execution_agent.py

import subprocess
import os
import json
from utils.logger import get_logger

logger = get_logger("ExecutionAgent")

AUTOMATION_DIR = "testcases/automation"
REPORT_FILE = "test_report.json"


def execute_automation_tests():
    logger.info("Starting automation test execution")

    if not os.path.exists(AUTOMATION_DIR):
        logger.error("Automation directory not found")
        return

    test_files = [
        os.path.join(AUTOMATION_DIR, f)
        for f in os.listdir(AUTOMATION_DIR)
        if f.startswith("test_") and f.endswith(".py")
    ]

    if not test_files:
        logger.warning("No automation tests found")
        return

    command = [
        "pytest",
        "-v",
        "--json-report",
        f"--json-report-file={REPORT_FILE}",
    ] + test_files

    result = subprocess.run(command, capture_output=True, text=True)

    logger.info("========== PYTEST OUTPUT ==========")
    logger.info(result.stdout)

    if result.stderr:
        logger.error(result.stderr)

    if not os.path.exists(REPORT_FILE):
        logger.error("Pytest report not generated")
        return

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        report = json.load(f)

    summary = report.get("summary", {})

    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    errors = summary.get("error", 0)

    logger.info("========== EXECUTION SUMMARY ==========")
    logger.info(f"Total Tests : {total}")
    logger.info(f"PASSED      : {passed}")
    logger.info(f"FAILED      : {failed}")
    logger.info(f"SKIPPED     : {skipped}")
    logger.info(f"ERRORS      : {errors}")

    if failed > 0 or errors > 0:
        logger.error("Some tests FAILED or ERRORED")
    else:
        logger.info("All tests PASSED")
