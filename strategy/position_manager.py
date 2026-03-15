import math


# =====================================================
# Position Sizing Based on Risk Score + Active Budget
# =====================================================

def calculate_position_value(
    active_budget,
    risk_score,
    entry_price,
    stop_price,
    min_position_value=500
):
    """
    active_budget: nur Trading-Budget (z.B. 2000 €)
    risk_score: 0-100
    entry_price: Einstieg
    stop_price: Stop-Loss
    """

    if active_budget <= 0:
        return 0

    # =================================================
    # Kapital-Allokation basierend auf Risk Score
    # =================================================

    if risk_score >= 85:
        budget_factor = 0.50
    elif risk_score >= 75:
        budget_factor = 0.35
    elif risk_score >= 60:
        budget_factor = 0.25
    else:
        return 0  # Kein Trade unter 60

    allocated_budget = active_budget * budget_factor

    # =================================================
    # Stop-Distanz berücksichtigen
    # =================================================

    stop_distance = abs(entry_price - stop_price)

    if stop_distance == 0:
        return 0

    # Risikoorientierte Positionsberechnung
    risk_per_trade = allocated_budget * 0.02
    position_size = risk_per_trade / stop_distance

    position_value = position_size * entry_price

    # =================================================
    # Mindestgröße erzwingen
    # =================================================

    if position_value < min_position_value:
        position_value = min_position_value

    # =================================================
    # Nicht über zugewiesenes Budget hinaus
    # =================================================

    position_value = min(position_value, allocated_budget)

    return round(position_value, 2)