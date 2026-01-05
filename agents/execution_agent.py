# agents/execution_agent.py

import subprocess
import os
import re
from utils.logger import get_logger

logger = get_logger("ExecutionAgent")

AUTOMATION_DIR = "testcases/automation"
FAILED_TESTS_FILE = "failed_tests.txt"


def execute_automation_tests():
    logger.info("Starting automation test execution")

    if not os.path.exists(AUTOMATION_DIR):
        logger.error("Automation directory not found")
        return

    # ------------------------------------
    # STEP 1: COLLECT TESTS
    # ------------------------------------
    collect_cmd = ["pytest", AUTOMATION_DIR, "--collect-only", "-q"]

    collect_result = subprocess.run(
        collect_cmd,
        capture_output=True,
        text=True
    )

    collected_tests = [
        line.strip()
        for line in collect_result.stdout.splitlines()
        if line.strip().startswith(AUTOMATION_DIR.replace("\\", "/"))
    ]

    collected_count = len(collected_tests)

    logger.info("========== TEST COLLECTION ==========")
    logger.info(f"Total Tests Collected : {collected_count}")

    if collected_count == 0:
        logger.error("No tests collected. Aborting execution.")
        return

    # ------------------------------------
    # STEP 2: EXECUTE TESTS
    # ------------------------------------
    run_cmd = [
        "pytest",
        AUTOMATION_DIR,
        "-v",
        "--tb=short",
        "--disable-warnings"
    ]

    run_result = subprocess.run(
        run_cmd,
        capture_output=True,
        text=True
    )

    combined_output = (run_result.stdout or "") + "\n" + (run_result.stderr or "")

    logger.info("========== PYTEST OUTPUT ==========")
    logger.info(run_result.stdout)

    if run_result.stderr:
        logger.error(run_result.stderr)

    # ------------------------------------
    # STEP 3: PARSE RESULTS
    # ------------------------------------
    passed = failed = skipped = errors = 0
    failed_tests = []

    # Extract FAILED test nodeids
    for line in combined_output.splitlines():
        if line.startswith("FAILED"):
            failed_tests.append(line.split(" ")[1])

    summary_line = None
    for line in combined_output.splitlines():
        if re.search(r"\d+ passed|\d+ failed|\d+ errors?|\d+ skipped", line):
            summary_line = line

    if summary_line:
        m = re.search(r"(\d+)\s+passed", summary_line)
        if m:
            passed = int(m.group(1))

        m = re.search(r"(\d+)\s+failed", summary_line)
        if m:
            failed = int(m.group(1))

        m = re.search(r"(\d+)\s+errors?", summary_line)
        if m:
            errors = int(m.group(1))

        m = re.search(r"(\d+)\s+skipped", summary_line)
        if m:
            skipped = int(m.group(1))

    # ------------------------------------
    # STEP 4: FAILED TEST DETAILS
    # ------------------------------------
    if failed_tests:
        logger.error("========== FAILED TEST DETAILS ==========")
        for test in failed_tests:
            logger.error(test)

        # Save failed tests for re-run
        with open(FAILED_TESTS_FILE, "w") as f:
            for test in failed_tests:
                f.write(test + "\n")

        logger.info(f"Failed tests saved to {FAILED_TESTS_FILE}")

    # ------------------------------------
    # STEP 5: FINAL SUMMARY
    # ------------------------------------
    logger.info("========== EXECUTION SUMMARY ==========")
    logger.info(f"Total Tests        : {collected_count}")
    logger.info(f"PASSED             : {passed}")
    logger.info(f"FAILED             : {failed}")
    logger.info(f"ERRORS             : {errors}")
    logger.info(f"SKIPPED            : {skipped}")

    if failed > 0 or errors > 0:
        logger.error("Some tests FAILED")
    else:
        logger.info("All tests PASSED")

    logger.info("Automation test execution completed")


def rerun_failed_tests():
    """
    Run only failed tests from last execution
    """
    if not os.path.exists(FAILED_TESTS_FILE):
        logger.error("No failed tests file found. Nothing to re-run.")
        return

    with open(FAILED_TESTS_FILE) as f:
        failed_tests = [line.strip() for line in f if line.strip()]

    if not failed_tests:
        logger.info("No failed tests to re-run.")
        return

    logger.info("Re-running FAILED tests only")

    cmd = ["pytest"] + failed_tests + ["-v", "--tb=short"]

    subprocess.run(cmd)
