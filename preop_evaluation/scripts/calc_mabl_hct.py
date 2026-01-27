def calculate_mabl_hct(
    weight_kg: float,
    sex: str,
    age_group: str,
    initial_hct: float,
    lowest_acceptable_hct: float = 24
) -> float:
    """
    Calculate Maximum Allowable Blood Loss (MABL).

    Parameters:
    - weight_kg: Patient weight in kilograms
    - sex: 'male' or 'female'
    - age_group: 'adult', 'child', or 'neonate'
    - initial_hct: Starting hematocrit (e.g., 0.42 or 42)
    - lowest_acceptable_hct: Minimum acceptable hematocrit (default = 24%)

    Returns:
    - MABL in milliliters (mL)
    """

    # Normalize hematocrit if given as percentage
    if initial_hct > 1:
        initial_hct /= 100
    if lowest_acceptable_hct > 1:
        lowest_acceptable_hct /= 100

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

    mabl = ebv_ml * (initial_hct - lowest_acceptable_hct) / initial_hct
    return round(mabl, 1)

