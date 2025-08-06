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
        "currency": None
    }

    if match := re.search(r'from "([^"]+)" to "([^"]+)"', prompt):
        result["origin"], result["destination"] = match.groups()

    if match := re.search(r'area "([^"]+)"', prompt):
        result["area"] = match.group(1)

    if match := re.search(r'in "([^"]+)"', prompt):
        result["month"] = match.group(1)

    if match := re.search(r'staying between "(\d+)" to "(\d+)" days', prompt):
        result["duration"]["min"], result["duration"]["max"] = map(int, match.groups())

    if match := re.search(r'Hotels:[\s\S]*?Within "([^"]+)" from the beach', prompt):
        result["hotel"]["proximity_to_beach"] = match.group(1)

    if match := re.search(r'"(\d+)" stars', prompt):
        result["hotel"]["stars"] = int(match.group(1))

    if "All-Inclusive" in prompt:
        result["hotel"]["board"] = "All-Inclusive"

    if match := re.search(r'Departing between "([^"]+)" and "([^"]+)"', prompt):
        result["flight"]["departure_time"] = {"from": match.group(1), "to": match.group(2)}

    if match := re.search(r'in ([A-Z]{3,})', prompt):
        result["currency"] = match.group(1)

    return result
