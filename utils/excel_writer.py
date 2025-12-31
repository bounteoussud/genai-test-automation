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

    for raw_line in llm_output.splitlines():
        line = raw_line.strip()

        # Skip non-testcase lines
        if "|" not in line:
            continue

        # Remove leading numbering like "1.", "1 |", "1.|"
        line = re.sub(r"^\d+\s*\.?\s*\|", "", line)

        parts = [p.strip() for p in line.split("|") if p.strip()]

        if len(parts) < 3:
            continue

        # TC_ID comes from original numbering
        tc_match = re.match(r"^\s*(\d+)", raw_line)
        if not tc_match:
            continue

        tc_id = int(tc_match.group(1))
        scenario = parts[0]
        steps = parts[1]
        expected = " | ".join(parts[2:])  # allow extra pipes safely

        ws.append([tc_id, scenario, steps, expected])

    wb.save("testcases/manual/testcases.xlsx")
