def calculate_mabl_hgb(
    weight_kg: float,
    sex: str,
    age_group: str,
    initial_hgb: float,
    lowest_acceptable_hgb: float = 8
) -> float:
    """
    Calculate Maximum Allowable Blood Loss (MABL) using hemoglobin.

    Parameters:
    - weight_kg: Patient weight in kilograms
    - sex: 'male' or 'female'
    - age_group: 'adult', 'child', or 'neonate'
    - initial_hgb: Starting hemoglobin (g/dL)
    - lowest_acceptable_hgb: Minimum acceptable hemoglobin (default = 8 g/dL)

    Returns:
    - MABL in milliliters (mL)
    """

    sex = sex.lower()
    age_group = age_group.lower()

    if sex not in {"male", "female"}:
        raise ValueError("sex must be 'male' or 'female'")

    if age_group not in {"adult", "child", "neonate"}:
        raise ValueError("age_group must be 'adult', 'child', or 'neonate'")

    # Estimated Blood Volume (mL/kg)
    ebv_table = {
        "adult": {"male": 75, "female": 65},
        "child": {"male": 70, "female": 70},
        "neonate": {"male": 90, "female": 90}
    }

    ebv_ml = ebv_table[age_group][sex] * weight_kg

    mabl = ebv_ml * (initial_hgb - lowest_acceptable_hgb) / initial_hgb
    return round(mabl, 1)

