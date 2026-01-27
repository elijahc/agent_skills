from typing import Dict


def determine_asa(patient: Dict) -> str:
    """
    Determine ASA Physical Status from structured patient input.

    Expected keys:
    - emergency (bool)
    - brain_dead (bool)
    - moribund (bool)
    - systemic_disease (str): none | mild | severe | constant_threat
    - functional_limitation (bool)
    """

    emergency = patient.get("emergency", False)
    brain_dead = patient.get("brain_dead", False)
    moribund = patient.get("moribund", False)
    systemic = patient.get("systemic_disease", "none")
    functional_limitation = patient.get("functional_limitation", False)

    # ASA VI
    if brain_dead:
        asa = "ASA VI"

    # ASA V
    elif moribund:
        asa = "ASA V"

    # ASA IV
    elif systemic == "constant_threat":
        asa = "ASA IV"

    # ASA III
    elif systemic == "severe":
        asa = "ASA III"

    # ASA II
    elif systemic == "mild":
        asa = "ASA II"

    # ASA I
    elif systemic == "none":
        asa = "ASA I"

    else:
        return "Unable to determine ASA status"

    if emergency:
        asa += "E"

    return asa

