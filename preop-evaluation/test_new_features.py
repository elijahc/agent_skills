#!/usr/bin/env python3
from scripts.parse_patient import parse_patient
from scripts.comorbidity_assessment import calculate_comorbidity_score, get_risk_recommendation

# Test 1: Basic patient with height/weight
patient1 = parse_patient(
    "Cholecystectomy",
    "65 year old female, 70 kg, 162 cm tall, history of well-controlled diabetes"
)
print("Test 1 - Basic patient:")
print(f"  Age: {patient1.get('age')}")
print(f"  Weight: {patient1.get('weight_kg')} kg")
print(f"  Height: {patient1.get('height_cm')} cm ({patient1.get('height_in')} in)")
print(f"  Systemic disease: {patient1.get('systemic_disease')}")

# Test 2: Comorbidity score
assessment = calculate_comorbidity_score(patient1)
print(f"\nComorbidity Assessment:")
print(f"  Score: {assessment['score']}")
print(f"  Risk: {assessment['risk_category']}")
print(f"  Comorbidities: {assessment['comorbidities']}")

# Test 3: Risk recommendation
recommendation = get_risk_recommendation(assessment['risk_category'])
print(f"\nRecommendation: {recommendation[:80]}...")

# Test 4: High-risk patient with lbs and feet/inches
patient2 = parse_patient(
    "Open AAA repair",
    "78 year old male, 190 lbs, 5'10\", septic shock, on vasopressors, ESRD"
)
print(f"\n\nTest 2 - High-risk patient:")
print(f"  Age: {patient2.get('age')}")
print(f"  Weight: {patient2.get('weight_kg')} kg (from lbs)")
print(f"  Height: {patient2.get('height_cm')} cm (from feet/inches)")
print(f"  Systemic disease: {patient2.get('systemic_disease')}")

assessment2 = calculate_comorbidity_score(patient2)
print(f"\nComorbidity Assessment:")
print(f"  Score: {assessment2['score']}")
print(f"  Risk: {assessment2['risk_category']}")
print(f"  Considerations: {assessment2['considerations']}")
