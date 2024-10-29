import pandas as pd
from typing import Dict, Tuple

def calculate_percentage(intake: float, reference: float) -> float:
    """
    Calculate the percentage of intake relative to reference value
    
    Args:
        intake: Current nutrient intake value
        reference: Reference value for the nutrient
    
    Returns:
        float: Percentage of intake relative to reference
    """
    return (intake / reference) * 100

def get_status(percentage: float) -> Tuple[str, str]:
    """
    Determine the status and color code based on the percentage of intake
    
    Args:
        percentage: Percentage of intake relative to reference value
    
    Returns:
        Tuple[str, str]: Status label and corresponding color code
        Status levels:
        - Excess (>200%): purple
        - High (150-200%): orange
        - Adequate (90-150%): green
        - Borderline (70-90%): yellow
        - Deficient (<70%): red
    """
    if percentage > 200:  # More than double the recommended value
        return "Excess", "purple"
    elif percentage > 150:  # 50% more than recommended
        return "High", "orange"
    elif percentage >= 90:
        return "Adequate", "green"
    elif percentage >= 70:
        return "Borderline", "yellow"
    else:
        return "Deficient", "red"

def calculate_results(intakes, reference_values):
    """
    Calculate analysis results for all nutrients
    
    Args:
        intakes: Dictionary of nutrient intakes
        reference_values: Dictionary of reference values for each nutrient
    
    Returns:
        pandas.DataFrame: Results containing nutrient status, percentage, and color coding
    """
    results = []
    for nutrient, intake in intakes.items():
        if nutrient in reference_values:
            percentage = calculate_percentage(intake, reference_values[nutrient])
            status, color = get_status(percentage)
            results.append({
                'Nutrient': nutrient,
                'Intake': intake,
                'Reference': reference_values[nutrient],
                'Percentage': percentage,
                'Status': status,
                'Color': color
            })
    return pd.DataFrame(results)

def get_food_recommendations(nutrient: str, current_intake: float, reference: float, nutrient_sources: Dict) -> Dict:
    """
    Generate food recommendations based on nutrient analysis
    
    Args:
        nutrient: Name of the nutrient
        current_intake: Current intake value
        reference: Reference value for the nutrient
        nutrient_sources: Dictionary containing food sources and their nutrient content
    
    Returns:
        Dict: Recommendations for food modifications
        Each recommendation contains:
        - Amount (in grams)
        - Unit of measurement
        - Nutrient content per 100g
        - Action ("increase" or "reduce")
    """
    difference = reference - current_intake
    # Only make recommendations if difference is significant (>10% of reference)
    if abs(difference) <= reference * 0.1:
        return {}
    
    recommendations = {}
    if nutrient in nutrient_sources:
        if difference > 0:  # Deficit - need to increase intake
            for food, (content, unit) in nutrient_sources[nutrient].items():
                amount_needed = (difference / content) * 100  # Convert to grams
                recommendations[food] = (round(amount_needed, 1), unit, content, "increase")
        else:  # Excess - need to reduce intake
            for food, (content, unit) in nutrient_sources[nutrient].items():
                amount_to_reduce = (abs(difference) / content) * 100  # Convert to grams
                recommendations[food] = (round(amount_to_reduce, 1), unit, content, "reduce")
    return recommendations
