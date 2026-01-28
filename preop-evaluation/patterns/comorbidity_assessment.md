# Comorbidity Assessment Patterns

## Overview

The `calculate_comorbidity_score()` function evaluates perioperative risk based on patient demographics, comorbidity burden, and clinical status. It returns a score, risk category, identified comorbidities, and clinical considerations for agent presentation.

## Usage Pattern

```python
from scripts.parse_patient import parse_patient
from scripts.comorbidity_assessment import calculate_comorbidity_score, get_risk_recommendation

# First parse the patient
patient = parse_patient(
    "Total hip replacement",
    "78 year old male, 72 kg, 168 cm, severe osteoarthritis, history of COPD on home oxygen"
)

# Calculate comorbidity score
assessment = calculate_comorbidity_score(patient)

# Get clinical recommendation
recommendation = get_risk_recommendation(assessment['risk_category'])
```

## Scoring System

**Score Calculation:**
- Systemic disease severity: 0-10 points (brain dead=10, moribund=9, constant threat=6, severe=4, mild=1, none=0)
- Age >= 80: +2 points
- Age 70-79: +1 point
- Obesity (BMI >= 35): +2 points
- Overweight (BMI 30-34): +1 point
- Emergency procedure: +1 point

**Risk Categories:**
- **Low Risk** (0-2 points): Routine preop assessment, standard anesthetic plan
- **Moderate Risk** (3-7 points): Thorough evaluation, optimize comorbidities if time permits
- **High Risk** (8-11 points): Multidisciplinary consultation, extensive optimization, detailed risk discussion
- **Very High Risk** (12+ points): Leadership consultation, ICU-level care planning, comprehensive risk/benefit discussion

## Example assessments

### Low-risk patient

```python
patient = parse_patient(
    "Cholecystectomy",
    "42 year old female, 65 kg, 162 cm, no significant medical history"
)

assessment = calculate_comorbidity_score(patient)
# Returns:
# {
#   'score': 0,
#   'risk_category': 'low',
#   'comorbidities': [],
#   'considerations': []
# }

recommendation = get_risk_recommendation('low')
# "Low perioperative risk. Standard preop assessment and anesthetic plan appropriate..."
```

### Moderate-risk patient

```python
patient = parse_patient(
    "Total knee replacement",
    "68 year old male, 85 kg, 175 cm, well-controlled hypertension and type 2 diabetes"
)

assessment = calculate_comorbidity_score(patient)
# Returns:
# {
#   'score': 3,
#   'risk_category': 'moderate',
#   'comorbidities': [
#     'Age 70-79',
#     'Mild systemic disease (controlled HTN, DM, asthma, etc.)'
#   ],
#   'considerations': [
#     'Continue home medications',
#   ]
# }
```

### High-risk patient

```python
patient = parse_patient(
    "Open AAA repair",
    "76 year old male, 72 kg, 170 cm, ESRD on dialysis, severe COPD, ejection fraction 35%, septic shock"
)

assessment = calculate_comorbidity_score(patient)
# Returns:
# {
#   'score': 9,
#   'risk_category': 'high',
#   'comorbidities': [
#     'Age 70-79',
#     'Life-threatening systemic disease (septic shock, ECMO, respiratory failure, etc.)'
#   ],
#   'considerations': [
#     'Consider ICU admission post-op',
#     'Optimize hemodynamics pre-op'
#   ]
# }
```

### Very High-Risk patient (organ donation)

```python
patient = parse_patient(
    "Heart procurement",
    "Declared brain dead, 34 year old male, 78 kg, 185 cm"
)

assessment = calculate_comorbidity_score(patient)
# Returns:
# {
#   'score': 10,
#   'risk_category': 'very_high',
#   'comorbidities': [
#     'Brain dead - organ procurement case'
#   ],
#   'considerations': []
# }
```

## When to use comorbidity assessment

**Use after `parse_patient()`** to stratify perioperative risk. This is essential for:
- Determining level of preop optimization needed
- Guiding interdisciplinary consultation decisions
- Counseling patients on perioperative risk
- Planning ICU vs floor recovery
- Identifying high-risk procedures that warrant careful planning

## Integration with other calculations

Once patient demographics are extracted and comorbidity risk is assessed, use other tools:
- **ASA status** (from `determine_asa.py`): Formal anesthesia risk classification
- **Weight adjustments** (from `adjust_weight.py`): Calculate IBW/ABW for drug dosing
- **Blood volume** (from blood volume scripts): Calculate MABL for major surgeries
