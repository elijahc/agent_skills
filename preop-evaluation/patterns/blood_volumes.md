# Blood volume calculation patterns

## Calculating MABL

Calculating MABL is useful for the provider to estimate the patient's transfusion risk. Long procedures or procedures with high bleeding risk and low MABL (<500 mL) suggests higher transfusion risk.

### Using hemoglobin

```python
# If hemoglobin concentration is supplied, use calc_mabl_hgb.py
mabl = calculate_mabl_hgb(
    weight_kg=70,
    sex="male",
    age_group="adult",
    initial_hgb=13.5
)

print(f"MABL (Hgb-based): {mabl} mL")

```

### Using hematocrit

```python
# If hematocrit is known, use calc_mabl_hct.py
mabl = calculate_mabl_hct(
    weight_kg=80,
    sex="female",
    age_group="adult",
    initial_hct=40
)

print(f"MABL: {mabl} mL")

```

## Calculating estimated blood volume (EBV)

```python
# EBV can calculated as a separate quantity if requested, don't report an EBV unless asked
ebv = calculate_ebv(70, "male", "adult")

```

## When to calculate blood volumes

**Only calculate MABL and EBV for major surgeries** with significant bleeding risk, such as:
- Vascular surgery (AAA repair, carotid endarterectomy)
- Cardiac surgery
- Major orthopedic surgery (total joint replacement, femur fracture)
- Trauma surgery
- Major GI resections
- Hepatic resections

**Do not report EBV unless explicitly requested.** MABL is more clinically relevant for anesthesia planning.

**Default thresholds:**
- MABL < 500 mL: Low transfusion risk
- MABL 500-1500 mL: Moderate transfusion risk - ensure adequate IV access
- MABL > 1500 mL: High transfusion risk - consider cell salvage, massive transfusion protocol

## Integration with patient data

Use output from `parse_patient()` to get weight and demographics:

```python
from scripts.parse_patient import parse_patient
from scripts.calc_mabl_hgb import calculate_mabl_hgb

patient = parse_patient(
    "Open AAA repair",
    "62 year old male, 85 kg, hemoglobin 13.5 g/dL"
)

mabl = calculate_mabl_hgb(
    weight_kg=patient['weight_kg'],
    sex='male',
    age_group='adult',
    initial_hgb=13.5
)

print(f"Maximum Allowable Blood Loss: {mabl} mL")
```
