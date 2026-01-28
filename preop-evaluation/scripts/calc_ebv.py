def calculate_ebv(weight_kg: float, sex: str, age_group: str) -> float:
    """
    Calculate Estimated Blood Volume (EBV).

    Parameters:
    - weight_kg: Patient weight in kilograms
    - sex: 'male' or 'female'
    - age_group: 'adult', 'child', or 'neonate'

    Returns:
    - EBV in milliliters (mL)
    """

    sex = sex.lower()
    age_group = age_group.lower()

    if sex not in {"male", "female"}:
        raise ValueError("sex must be 'male' or 'female'")

    if age_group not in {"adult", "child", "neonate"}:
        raise ValueError("age_group must be 'adult', 'child', or 'neonate'")

    # EBV values in mL/kg
    ebv_table = {
        "adult": {"male": 75, "female": 65},
        "child": {"male": 70, "female": 70},
        "neonate": {"male": 90, "female": 90}
    }

    return ebv_table[age_group][sex] * weight_kg

