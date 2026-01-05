import os
import re
from openpyxl import Workbook


def write_manual_tests(llm_output: str, requirement_hash: str):
    os.makedirs("testcases/manual", exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "TestCases"

    # Header
    ws.append(["REQUIREMENT_HASH", requirement_hash])
    ws.append([])
    ws.append(["TC_ID", "Scenario", "Steps", "Expected Result"])

    valid_count = 0

    for raw_line in llm_output.splitlines():
        line = raw_line.strip()

        if "|" not in line:
            continue

        # Extract TC_ID
        tc_match = re.match(r"^\s*(\d+)\s*\|", line)
        if not tc_match:
            continue

        tc_id = int(tc_match.group(1))

        # Remove TC_ID from line
        line = re.sub(r"^\s*\d+\s*\|\s*", "", line)

        parts = [p.strip() for p in line.split("|") if p.strip()]

        if len(parts) < 3:
            continue

        scenario = parts[0]
        steps = " | ".join(parts[1:-1])   # ALL middle parts
        expected = parts[-1]

        ws.append([tc_id, scenario, steps, expected])
        valid_count += 1

    if valid_count == 0:
        raise Exception("No valid test cases parsed from LLM output")

    wb.save("testcases/manual/testcases.xlsx")
