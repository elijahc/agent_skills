---
name: preop-evaluation
description: A skill to help anesthesiologists risk stratify a patient according to their comorbidities and compute important perioperative variables
---

# Anesthetic preop evaluation

## Quick start

Begin by asking the user what they know about the patient. Minimum useful information: age, weight, and gender. Ideally also collect:
- Height (for BMI and drug dosing calculations)
- Hemoglobin or hematocrit (relevant for major surgery)
- Comorbidities and systemic disease burden
- Emergency vs elective status

## Workflow

1. **Parse patient info**: Use `parse_patient()` to extract demographics and clinical status from procedure name and free text. See [patterns/patient_parsing.md](patterns/patient_parsing.md).

2. **Assess comorbidity risk**: Use `calculate_comorbidity_score()` to stratify perioperative risk and identify clinical considerations. See [patterns/comorbidity_assessment.md](patterns/comorbidity_assessment.md).

3. **Determine ASA status**: Use `determine_asa()` for formal anesthesia risk classification based on systemic disease severity.

4. **Calculate weight adjustments**: Use `calculate_ibw()` and `calculate_abw()` if dosing needs adjustment for obesity.

5. **Calculate blood volume metrics**: For major surgeries with bleeding risk, use `calculate_mabl_hgb()` or `calculate_mabl_hct()` to estimate transfusion risk. See [patterns/blood_volumes.md](patterns/blood_volumes.md).

## Key Features

- **Patient parsing**: Automatically extracts age, weight, height, and comorbidity information from unstructured text
- **Comorbidity scoring**: Quantifies perioperative risk with clinical recommendations
- **ASA classification**: Standardized anesthesia risk assessment
- **Blood volume calculations**: MABL and EBV for transfusion risk estimation
- **Weight-based dosing**: IBW and ABW calculations for drug dosing accuracy