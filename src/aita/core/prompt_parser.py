"""
Prompt Parser: Extracts structured filters from natural language prompts.
"""

import re
from typing import Dict


def parse_prompt(prompt: str) -> Dict:
    result = {
        "origin": None,
        "destination": None,
        "area": None,
        "month": None,
        "duration": {"min": None, "max": None},
        "hotel": {},
        "flight": {},
    }

    # 1. Match origin and destination
    if match := re.search(
        r"\bfrom\s+([A-Za-z\s]+?)\s+to\s+([A-Za-z\s]+?)(?:\s|$|in\b|\.)",
        prompt,
        re.IGNORECASE,
    ):
        result["origin"], result["destination"] = match.groups()
        result["origin"] = result["origin"].strip()
        result["destination"] = result["destination"].strip()

    # 2. Match area (FIXED: use greedy match to capture full name)
    if match := re.search(r'area "?([A-Za-z\s]+)"?', prompt, re.IGNORECASE):
        result["area"] = match.group(1).strip()

    # 3. Match month
    if match := re.search(r'\bin "?([A-Za-z]+)"?', prompt, re.IGNORECASE):
        result["month"] = match.group(1).strip()

    # 4. Match duration
    if match := re.search(
        r'stay(?:ing)? between "?(\d+)"? to "?(\d+)"? days', prompt, re.IGNORECASE
    ):
        result["duration"]["min"], result["duration"]["max"] = map(int, match.groups())

    # 5. Match hotel proximity
    if match := re.search(
        r'hotels?\s+within\s+"?([\d\s\w]+)"?\s+from the beach',
        prompt,
        re.IGNORECASE,
    ):
        result["hotel"]["proximity_to_beach"] = match.group(1).strip()

    # 6. Match hotel stars
    if match := re.search(r'"?(\d+)"?\s*stars?', prompt, re.IGNORECASE):
        result["hotel"]["stars"] = int(match.group(1))

    # 7. Match board type
    if re.search(r"\bAll[- ]Inclusive\b", prompt, re.IGNORECASE):
        result["hotel"]["board"] = "All-Inclusive"

    # 8. Match flight departure time
    if match := re.search(
        r'Departing between "?([\d:apm\s]+)"? and "?([\d:apm\s]+)"?',
        prompt,
        re.IGNORECASE,
    ):
        result["flight"]["departure_time"] = {
            "from": match.group(1).strip(),
            "to": match.group(2).strip(),
        }

    return result
