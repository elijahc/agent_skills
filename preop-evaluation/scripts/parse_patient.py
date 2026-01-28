import re
from typing import Dict, Union

def parse_patient(procedure_name: str, free_text: str) -> Dict[str, Union[bool, str, int]]:
    """
    Parse patient information from free text and return a normalized patient dictionary.

    Assumptions:
    - Patient is NOT brain dead unless explicitly stated.
    - Organ donation procedures require explicit confirmation of brain death.
    """

    text = f"{procedure_name} {free_text}".lower()
    text = re.sub(r"\s+", " ", text)

    patient: Dict[str, Union[bool, str, int, float]] = {
        "brain_dead": False,
        "moribund": False,
        "systemic_disease": "none",
    }

    # -------------------------
    # Weight extraction (kg or lbs)
    # -------------------------
    weight_patterns = [
        r"(\d{1,3}(?:\.\d{1,2})?)\s*kg\b",
        r"weighs?\s+(\d{1,3}(?:\.\d{1,2})?)\s*kg\b",
        r"weight\s+(\d{1,3}(?:\.\d{1,2})?)\s*kg\b",
        r"(\d{1,3}(?:\.\d{1,2})?)\s*lbs?\b",
        r"(\d{1,3}(?:\.\d{1,2})?)\s*#\b",
    ]

    for pattern in weight_patterns:
        match = re.search(pattern, text)
        if match:
            weight_value = float(match.group(1))
            # Check if it's in pounds (convert to kg)
            if "lb" in pattern or "#" in pattern:
                weight_value = weight_value / 2.20462
            # Validate reasonable weight range
            if 2 < weight_value < 300:
                patient["weight_kg"] = round(weight_value, 2)
            break

    # -------------------------
    # Height extraction (cm or feet/inches)
    # -------------------------
    height_patterns = [
        r"(\d{1,3})\s*cm\b",
        r"height\s+(\d{1,3})\s*cm\b",
        r"(\d)\s*'?\s*(\d{1,2})\s*\"?",  # 5'10", 5'10, 5 10
        r"(\d)\s+ft\s+(\d{1,2})\s+in\b",
    ]

    for pattern in height_patterns:
        match = re.search(pattern, text)
        if match:
            if len(match.groups()) == 2:
                # Feet and inches format
                feet = int(match.group(1))
                inches = int(match.group(2))
                height_cm = (feet * 12 + inches) * 2.54
            else:
                # Centimeters format
                height_cm = float(match.group(1))
            # Validate reasonable height range (80-250 cm)
            if 80 < height_cm < 250:
                patient["height_cm"] = round(height_cm, 2)
                # Also store height in inches for Devine formula compatibility
                patient["height_in"] = round(height_cm / 2.54, 2)
            break

    # -------------------------
    # Age extraction
    # -------------------------
    age_patterns = [
        r"\b(\d{1,3})\s*yo\b",
        r"\b(\d{1,3})\s*y\/o\b",
        r"\b(\d{1,3})\s*year[- ]old\b",
        r"\bage\s*(\d{1,3})\b",
    ]

    for pattern in age_patterns:
        match = re.search(pattern, text)
        if match:
            age = int(match.group(1))
            if 0 < age < 120:
                patient["age"] = age
            break

    # -------------------------
    # Organ donation detection
    # -------------------------
    organ_donation_terms = [
        "organ donation",
        "organ donor",
        "procurement",
        "organ procurement",
        "donor hepatectomy",
        "donor nephrectomy",
        "heart procurement",
        "lung procurement",
    ]

    is_donation_case = any(term in text for term in organ_donation_terms)

    # -------------------------
    # Brain death confirmation
    # -------------------------
    brain_dead_terms = [
        "brain dead",
        "brain-dead",
        "declared brain dead",
        "brain death confirmed",
    ]

    if is_donation_case and any(term in text for term in brain_dead_terms):
        patient["brain_dead"] = True
        patient["moribund"] = True
        patient["systemic_disease"] = "constant_threat"
        return patient

    # -------------------------
    # Moribund / end-of-life
    # -------------------------
    moribund_terms = [
        "moribund",
        "actively dying",
        "imminent death",
        "expected to die",
        "comfort measures only",
        "end of life",
    ]

    if any(term in text for term in moribund_terms):
        patient["moribund"] = True
        patient["systemic_disease"] = "constant_threat"

    # -------------------------
    # Systemic disease severity
    # -------------------------
    constant_threat_terms = [
        "septic shock",
        "multi-organ failure",
        "respiratory failure",
        "on multiple pressors",
        "ecmo",
        "hemodynamically unstable",
        "critical illness",
    ]

    severe_terms = [
        "severe",
        "decompensated",
        "poorly controlled",
        "end-stage",
        "esrd",
        "cirrhosis",
        "heart failure",
        "copd exacerbation",
        "oxygen dependent",
    ]

    mild_terms = [
        "mild",
        "well controlled",
        "controlled with medication",
        "history of",
        "hypertension",
        "diabetes",
        "asthma",
        "obesity",
    ]

    if any(term in text for term in constant_threat_terms):
        patient["systemic_disease"] = "constant_threat"
    elif any(term in text for term in severe_terms):
        patient["systemic_disease"] = "severe"
    elif any(term in text for term in mild_terms):
        patient["systemic_disease"] = "mild"

    return patient

