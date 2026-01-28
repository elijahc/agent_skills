from typing import Dict, Union


def calculate_comorbidity_score(patient: Dict) -> Dict[str, Union[int, str, list]]:
    """
    Calculate a simplified perioperative comorbidity score based on patient data.
    
    Uses systemic_disease severity level and patient age to estimate perioperative risk.
    Returns a score (0-10+), risk category, and recommended interventions.
    
    Parameters:
    - patient: Patient dictionary (typically output from parse_patient())
              Expected keys: age, systemic_disease, weight_kg
    
    Returns:
    - Dictionary with:
        - 'score': Comorbidity score (0-15)
        - 'risk_category': 'low' | 'moderate' | 'high' | 'very_high'
        - 'comorbidities': List of identified conditions
        - 'considerations': List of perioperative considerations
    """
    
    score = 0
    comorbidities = []
    considerations = []
    
    age = patient.get('age')
    systemic_disease = patient.get('systemic_disease', 'none').lower()
    weight_kg = patient.get('weight_kg')
    brain_dead = patient.get('brain_dead', False)
    moribund = patient.get('moribund', False)
    
    # -------------------------
    # Systemic disease severity scoring
    # -------------------------
    if brain_dead:
        score += 10
        comorbidities.append("Brain dead - organ procurement case")
    elif moribund:
        score += 9
        comorbidities.append("Moribund - actively dying")
    elif systemic_disease == "constant_threat":
        score += 6
        comorbidities.append("Life-threatening systemic disease (septic shock, ECMO, respiratory failure, etc.)")
        considerations.append("Consider ICU admission post-op")
        considerations.append("Optimize hemodynamics pre-op")
    elif systemic_disease == "severe":
        score += 4
        comorbidities.append("Severe systemic disease (cirrhosis, heart failure, ESRD, etc.)")
        considerations.append("Careful fluid management")
        considerations.append("Consider regional anesthesia if appropriate")
    elif systemic_disease == "mild":
        score += 1
        comorbidities.append("Mild systemic disease (controlled HTN, DM, asthma, etc.)")
        considerations.append("Continue home medications")
    
    # -------------------------
    # Age-based risk
    # -------------------------
    if age is not None:
        if age >= 80:
            score += 2
            comorbidities.append("Age ≥80 years")
            considerations.append("Increased risk of delirium and cognitive decline")
        elif age >= 70:
            score += 1
            comorbidities.append("Age 70-79")
    
    # -------------------------
    # BMI-based risk
    # -------------------------
    if weight_kg is not None:
        height_cm = patient.get('height_cm')
        if height_cm is not None:
            bmi = weight_kg / ((height_cm / 100) ** 2)
            if bmi >= 35:
                score += 2
                comorbidities.append(f"Obesity (BMI {bmi:.1f})")
                considerations.append("Increased aspiration risk - modified rapid sequence")
                considerations.append("Difficult airway assessment essential")
            elif bmi >= 30:
                score += 1
                comorbidities.append(f"Overweight (BMI {bmi:.1f})")
    
    # -------------------------
    # Emergency status
    # -------------------------
    if patient.get('emergency', False):
        score += 1
        comorbidities.append("Emergency procedure")
        considerations.append("Limited preop optimization time")
        considerations.append("NPO status may not be met")
    
    # -------------------------
    # Determine risk category
    # -------------------------
    if score >= 12:
        risk_category = "very_high"
    elif score >= 8:
        risk_category = "high"
    elif score >= 3:
        risk_category = "moderate"
    else:
        risk_category = "low"
    
    return {
        'score': score,
        'risk_category': risk_category,
        'comorbidities': comorbidities,
        'considerations': considerations
    }


def get_risk_recommendation(risk_category: str) -> str:
    """
    Get clinical recommendation based on risk category.
    
    Parameters:
    - risk_category: 'low', 'moderate', 'high', or 'very_high'
    
    Returns:
    - String recommendation for agent to present to user
    """
    
    recommendations = {
        'low': (
            "Low perioperative risk. Standard preop assessment and anesthetic plan appropriate. "
            "Routine monitoring and recovery expected."
        ),
        'moderate': (
            "Moderate perioperative risk. Ensure thorough preop evaluation, "
            "optimize comorbidities if possible, and plan for potential complications."
        ),
        'high': (
            "High perioperative risk. Strongly recommend multidisciplinary consultation, "
            "thorough optimization of comorbidities, and discussion of risks/benefits with patient. "
            "Consider ICU-level monitoring if available."
        ),
        'very_high': (
            "Very high perioperative risk. This patient requires careful interdisciplinary planning. "
            "Discuss case with surgical team, anesthesia leadership, and if possible, intensivist. "
            "Detailed risk/benefit discussion with patient and family essential."
        )
    }
    
    return recommendations.get(risk_category, "Unable to determine risk recommendation")
