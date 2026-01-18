"""Calorie and macro calculations for fitness goals."""

from typing import Dict, Tuple


# Activity level multipliers for TDEE calculation
ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,       # Little to no exercise
    "light": 1.375,         # Light exercise 1-3 days/week
    "moderate": 1.55,       # Moderate exercise 3-5 days/week
    "active": 1.725,        # Hard exercise 6-7 days/week
    "very_active": 1.9      # Very hard exercise, physical job
}

# Goal-based calorie adjustments
GOAL_ADJUSTMENTS = {
    "jacked_model": {"calories": -300, "protein_mult": 1.0},   # Lean bulk / recomp
    "lean": {"calories": -500, "protein_mult": 1.1},           # Cut
    "bulk": {"calories": 300, "protein_mult": 0.9},            # Bulk
    "maintain": {"calories": 0, "protein_mult": 1.0}           # Maintenance
}


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.

    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'

    Returns:
        BMR in calories per day
    """
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    return round(bmr, 0)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculate Total Daily Energy Expenditure.

    Args:
        bmr: Basal Metabolic Rate
        activity_level: Activity level ('sedentary', 'light', 'moderate', 'active', 'very_active')

    Returns:
        TDEE in calories per day
    """
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
    return round(bmr * multiplier, 0)


def calculate_target_calories(tdee: float, goal: str) -> int:
    """
    Calculate target daily calories based on goal.

    Args:
        tdee: Total Daily Energy Expenditure
        goal: Fitness goal ('jacked_model', 'lean', 'bulk', 'maintain')

    Returns:
        Target calories per day
    """
    adjustment = GOAL_ADJUSTMENTS.get(goal, GOAL_ADJUSTMENTS["maintain"])
    return int(tdee + adjustment["calories"])


def calculate_macros(target_calories: int, weight_kg: float, goal: str) -> Dict[str, int]:
    """
    Calculate target macronutrients based on calories and goal.

    Args:
        target_calories: Daily calorie target
        weight_kg: Body weight in kg
        goal: Fitness goal

    Returns:
        Dictionary with protein, carbs, and fat in grams
    """
    adjustment = GOAL_ADJUSTMENTS.get(goal, GOAL_ADJUSTMENTS["maintain"])

    # Protein: 2.2g per kg of body weight (adjusted by goal)
    protein_g = int(weight_kg * 2.2 * adjustment["protein_mult"])
    protein_calories = protein_g * 4

    # Fat: 25% of calories
    fat_calories = target_calories * 0.25
    fat_g = int(fat_calories / 9)

    # Carbs: Remaining calories
    carb_calories = target_calories - protein_calories - fat_calories
    carbs_g = int(carb_calories / 4)

    return {
        "protein": max(protein_g, 100),  # Minimum 100g protein
        "carbs": max(carbs_g, 100),      # Minimum 100g carbs
        "fat": max(fat_g, 40)            # Minimum 40g fat
    }


def estimate_weekly_weight_change(calorie_deficit: int) -> float:
    """
    Estimate weekly weight change based on calorie deficit/surplus.

    Args:
        calorie_deficit: Daily calorie deficit (negative) or surplus (positive)

    Returns:
        Estimated weekly weight change in kg
    """
    # 7700 calories = 1 kg of body weight
    weekly_calorie_change = calorie_deficit * 7
    return round(weekly_calorie_change / 7700, 2)


def calculate_target_weight(current_weight: float, goal: str, weeks: int = 1) -> float:
    """
    Calculate target weight for the end of a specified period.

    Args:
        current_weight: Current weight in kg
        goal: Fitness goal
        weeks: Number of weeks

    Returns:
        Target weight in kg
    """
    if goal == "jacked_model":
        # Slow recomp: lose ~0.25kg per week
        weekly_change = -0.25
    elif goal == "lean":
        # Cut: lose ~0.5kg per week
        weekly_change = -0.5
    elif goal == "bulk":
        # Bulk: gain ~0.25kg per week
        weekly_change = 0.25
    else:  # maintain
        weekly_change = 0

    return round(current_weight + (weekly_change * weeks), 1)


def get_body_fat_estimate(weight_kg: float, height_cm: float, age: int, gender: str) -> Tuple[float, str]:
    """
    Rough body fat estimate using BMI-based formula.
    Note: This is a rough estimate. For accurate measurement, use calipers or DEXA.

    Returns:
        Tuple of (estimated body fat percentage, category)
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if gender.lower() == "male":
        # Adult male formula
        body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
    else:
        # Adult female formula
        body_fat = (1.20 * bmi) + (0.23 * age) - 5.4

    body_fat = max(5, min(50, body_fat))  # Clamp to reasonable range

    # Categorize
    if gender.lower() == "male":
        if body_fat < 10:
            category = "Essential/Competition"
        elif body_fat < 14:
            category = "Athletic"
        elif body_fat < 18:
            category = "Fitness"
        elif body_fat < 25:
            category = "Average"
        else:
            category = "Above Average"
    else:
        if body_fat < 18:
            category = "Essential/Competition"
        elif body_fat < 22:
            category = "Athletic"
        elif body_fat < 25:
            category = "Fitness"
        elif body_fat < 32:
            category = "Average"
        else:
            category = "Above Average"

    return round(body_fat, 1), category


def calculate_ideal_weight_range(height_cm: float, gender: str) -> Tuple[float, float]:
    """
    Calculate ideal weight range based on height.
    Uses healthy BMI range (18.5-24.9).

    Returns:
        Tuple of (min_weight, max_weight) in kg
    """
    height_m = height_cm / 100

    # For a "jacked model" physique, we use slightly higher BMI range
    min_bmi = 22  # Lean and muscular
    max_bmi = 27  # Muscular upper range

    min_weight = min_bmi * (height_m ** 2)
    max_weight = max_bmi * (height_m ** 2)

    return round(min_weight, 1), round(max_weight, 1)


def calculate_workout_calories(workout_type: str, duration_minutes: int, weight_kg: float) -> int:
    """
    Estimate calories burned during a workout.

    Args:
        workout_type: Type of workout ('weight_lifting', 'cardio', 'mixed')
        duration_minutes: Duration in minutes
        weight_kg: Body weight in kg

    Returns:
        Estimated calories burned
    """
    # MET values (Metabolic Equivalent of Task)
    met_values = {
        "weight_lifting": 5.0,  # Moderate intensity weight training
        "cardio": 7.0,          # Moderate cardio (jogging)
        "mixed": 6.0,           # Circuit training
        "hiit": 8.0,            # High intensity interval training
        "yoga": 3.0,
        "walking": 3.5,
        "running": 9.8,
        "cycling": 7.5,
        "swimming": 8.0
    }

    met = met_values.get(workout_type.lower(), 5.0)

    # Calories = MET * weight (kg) * duration (hours)
    hours = duration_minutes / 60
    calories = met * weight_kg * hours

    return int(calories)
