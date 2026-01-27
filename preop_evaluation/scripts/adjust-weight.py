def calculate_ibw(sex: str, height_in: float) -> float:
    """
    Calculate Ideal Body Weight (IBW) using the Devine formula.

    Parameters:
    - sex: 'male' or 'female'
    - height_in: height in inches

    Returns:
    - IBW in kg
    """

    sex = sex.lower()

    if sex not in ("male", "female"):
        raise ValueError("Sex must be 'male' or 'female'")

    # Base IBW at 60 inches
    if sex == "male":
        ibw = 50.0
    else:
        ibw = 45.5

    if height_in >= 60:
        ibw += 2.3 * (height_in - 60)
    else:
        # Common modification for height < 60 inches
        # Using midpoint: subtract 3.5 lb per inch (~1.6 kg)
        ibw -= 1.6 * (60 - height_in)

    return round(ibw, 2)


def calculate_abw(actual_body_weight_kg: float, ibw_kg: float) -> float:
    """
    Calculate Adjusted Body Weight (ABW).

    ABW = IBW + 0.4 * (Actual Body Weight - IBW)

    Only applicable when actual body weight > IBW.

    Returns:
    - ABW in kg
    """

    if actual_body_weight_kg <= ibw_kg:
        return round(actual_body_weight_kg, 2)

    abw = ibw_kg + 0.4 * (actual_body_weight_kg - ibw_kg)
    return round(abw, 2)

