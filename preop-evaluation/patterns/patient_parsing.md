# Patient parsing patterns

## Overview

The `parse_patient()` function extracts key patient demographics and clinical status from procedure name and free-text clinical notes. It returns a normalized patient dictionary used by downstream calculations.

## Extracted Fields

- **age**: Patient age in years (extracted from "45yo", "age 45", etc.)
- **weight_kg**: Patient weight in kilograms (extracted from "70 kg", "155 lbs", etc.)
- **height_cm**: Patient height in centimeters (extracted from "5'10\"", "170 cm", etc.)
- **height_in**: Patient height in inches (calculated from height_cm for Devine formula)
- **brain_dead**: Boolean indicating brain death (requires explicit confirmation for organ donation cases)
- **moribund**: Boolean indicating end-of-life status
- **systemic_disease**: Severity level - 'none' | 'mild' | 'severe' | 'constant_threat'

## Example patient parsing behaviors

### Basic adult patient with demographics

```python
parse_patient(
    "Cholecystectomy",
    "65 year old female, 70 kg, 162 cm tall, history of well-controlled diabetes"
)

{
  'age': 65,
  'weight_kg': 70.0,
  'height_cm': 162.0,
  'height_in': 63.78,
  'brain_dead': False,
  'moribund': False,
  'systemic_disease': 'mild',
}
```

### Organ donation without brain death confirmation

```python
parse_patient(
    "Organ procurement - liver",
    "45yo male donor, 85 kg, hemodynamically stable"
)

{
  'age': 45,
  'weight_kg': 85.0,
  'brain_dead': False,
  'moribund': False,
  'systemic_disease': 'none',
}
```

### Organ donation with brain death confirmation

```python
parse_patient(
    "Heart procurement",
    "Declared brain dead, 32yo male, 90 kg, 185 cm"
)

{
  'age': 32,
  'weight_kg': 90.0,
  'height_cm': 185.0,
  'height_in': 72.83,
  'brain_dead': True,
  'moribund': True,
  'systemic_disease': 'constant_threat',
}
```

### High-risk patient

```python
parse_patient(
    "Emergent laparotomy",
    "78 year old male, 62 kg, 165 cm, septic shock, on vasopressors, ESRD on dialysis"
)

{
  'age': 78,
  'weight_kg': 62.0,
  'height_cm': 165.0,
  'height_in': 64.96,
  'brain_dead': False,
  'moribund': False,
  'systemic_disease': 'constant_threat',
  'emergency': True
}
```

## When to use parse_patient()

**Always start here** before any other calculation. Use the procedure description and clinical notes as input to normalize patient information.

