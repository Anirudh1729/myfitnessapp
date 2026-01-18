"""Onboarding service for new users."""

from typing import Optional
from database import Database, User
from utils import calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros
from utils.calories import get_body_fat_estimate, calculate_ideal_weight_range


class OnboardingService:
    """Handle user onboarding and profile setup."""

    def __init__(self, db: Database):
        self.db = db

    def get_welcome_message(self) -> str:
        """Get welcome message for new users."""
        return """
================================================================================
                    WELCOME TO MY FITNESS APP
================================================================================

Your personal fitness companion for:
  - Tracking workouts (weight lifting & cardio)
  - Logging food with calorie estimates
  - Planning workouts with progressive overload
  - Setting and achieving weekly goals

Let's set up your profile to personalize your experience!
================================================================================
"""

    def validate_name(self, name: str) -> tuple[bool, str]:
        """Validate user name input."""
        if not name or len(name.strip()) < 2:
            return False, "Please enter a name with at least 2 characters."
        if len(name) > 50:
            return False, "Name is too long. Please use 50 characters or less."
        return True, ""

    def validate_age(self, age_str: str) -> tuple[bool, str, int]:
        """Validate age input."""
        try:
            age = int(age_str)
            if age < 13:
                return False, "You must be at least 13 years old to use this app.", 0
            if age > 120:
                return False, "Please enter a valid age.", 0
            return True, "", age
        except ValueError:
            return False, "Please enter a valid number for age.", 0

    def validate_gender(self, gender: str) -> tuple[bool, str, str]:
        """Validate gender input."""
        gender_lower = gender.lower().strip()
        if gender_lower in ['m', 'male']:
            return True, "", "male"
        elif gender_lower in ['f', 'female']:
            return True, "", "female"
        else:
            return False, "Please enter 'M' for male or 'F' for female.", ""

    def validate_height(self, height_str: str) -> tuple[bool, str, float]:
        """Validate height input (in cm)."""
        try:
            height = float(height_str)
            if height < 100:
                return False, "Height seems too low. Please enter height in centimeters.", 0
            if height > 250:
                return False, "Height seems too high. Please enter height in centimeters.", 0
            return True, "", height
        except ValueError:
            return False, "Please enter a valid number for height.", 0

    def validate_weight(self, weight_str: str) -> tuple[bool, str, float]:
        """Validate weight input (in kg)."""
        try:
            weight = float(weight_str)
            if weight < 30:
                return False, "Weight seems too low. Please enter weight in kilograms.", 0
            if weight > 300:
                return False, "Weight seems too high. Please enter weight in kilograms.", 0
            return True, "", weight
        except ValueError:
            return False, "Please enter a valid number for weight.", 0

    def validate_goal(self, goal: str) -> tuple[bool, str, str]:
        """Validate fitness goal input."""
        goal_map = {
            '1': 'jacked_model',
            '2': 'lean',
            '3': 'bulk',
            '4': 'maintain',
            'jacked': 'jacked_model',
            'model': 'jacked_model',
            'actor': 'jacked_model',
            'lean': 'lean',
            'cut': 'lean',
            'bulk': 'bulk',
            'gain': 'bulk',
            'maintain': 'maintain',
            'maintenance': 'maintain'
        }
        goal_lower = goal.lower().strip()
        if goal_lower in goal_map:
            return True, "", goal_map[goal_lower]
        return False, "Please select a valid goal (1-4).", ""

    def validate_activity_level(self, level: str) -> tuple[bool, str, str]:
        """Validate activity level input."""
        level_map = {
            '1': 'sedentary',
            '2': 'light',
            '3': 'moderate',
            '4': 'active',
            '5': 'very_active',
            'sedentary': 'sedentary',
            'light': 'light',
            'moderate': 'moderate',
            'active': 'active',
            'very_active': 'very_active'
        }
        level_lower = level.lower().strip()
        if level_lower in level_map:
            return True, "", level_map[level_lower]
        return False, "Please select a valid activity level (1-5).", ""

    def validate_experience(self, exp: str) -> tuple[bool, str, str]:
        """Validate experience level input."""
        exp_map = {
            '1': 'beginner',
            '2': 'intermediate',
            '3': 'advanced',
            'beginner': 'beginner',
            'intermediate': 'intermediate',
            'advanced': 'advanced',
            'newbie': 'beginner',
            'new': 'beginner'
        }
        exp_lower = exp.lower().strip()
        if exp_lower in exp_map:
            return True, "", exp_map[exp_lower]
        return False, "Please select a valid experience level (1-3).", ""

    def create_user(self, name: str, age: int, gender: str, height_cm: float,
                    weight_kg: float, goal: str, activity_level: str,
                    experience_level: str) -> User:
        """Create a new user in the database."""
        user = User(
            name=name,
            age=age,
            gender=gender,
            height_cm=height_cm,
            weight_kg=weight_kg,
            goal=goal,
            activity_level=activity_level,
            experience_level=experience_level
        )
        user.id = self.db.create_user(user)

        # Log initial weight
        self.db.add_weight_log(user.id, weight_kg)

        return user

    def get_user_summary(self, user: User) -> str:
        """Generate a summary of user profile and recommendations."""
        bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
        tdee = calculate_tdee(bmr, user.activity_level)
        target_cals = calculate_target_calories(tdee, user.goal)
        macros = calculate_macros(target_cals, user.weight_kg, user.goal)
        body_fat, bf_category = get_body_fat_estimate(
            user.weight_kg, user.height_cm, user.age, user.gender
        )
        ideal_min, ideal_max = calculate_ideal_weight_range(user.height_cm, user.gender)

        goal_descriptions = {
            'jacked_model': 'Build a lean, muscular "model/actor" physique',
            'lean': 'Get lean and cut body fat',
            'bulk': 'Build muscle mass',
            'maintain': 'Maintain current physique'
        }

        return f"""
================================================================================
                         PROFILE SUMMARY
================================================================================

  Name: {user.name}
  Age: {user.age} years
  Gender: {user.gender.capitalize()}
  Height: {user.height_cm} cm
  Current Weight: {user.weight_kg} kg

  Goal: {goal_descriptions.get(user.goal, user.goal)}
  Activity Level: {user.activity_level.replace('_', ' ').title()}
  Experience: {user.experience_level.capitalize()}

--------------------------------------------------------------------------------
                      YOUR RECOMMENDATIONS
--------------------------------------------------------------------------------

  Estimated Body Fat: {body_fat}% ({bf_category})
  Ideal Weight Range: {ideal_min} - {ideal_max} kg

  Basal Metabolic Rate (BMR): {int(bmr)} calories/day
  Total Daily Energy Expenditure (TDEE): {int(tdee)} calories/day

  TARGET DAILY INTAKE:
  +------------------+
  | Calories: {target_cals:>5} |
  | Protein:  {macros['protein']:>4}g |
  | Carbs:    {macros['carbs']:>4}g |
  | Fat:      {macros['fat']:>4}g |
  +------------------+

================================================================================
  Your profile has been created! You're ready to start tracking your fitness.
================================================================================
"""

    def check_existing_user(self) -> Optional[User]:
        """Check if a user already exists in the database."""
        return self.db.get_user()

    def get_goal_options(self) -> str:
        """Get formatted goal options for display."""
        return """
Fitness Goals:
  [1] Jacked Model/Actor Body (DEFAULT)
      Build lean muscle while staying cut. The ideal aesthetic physique.

  [2] Get Lean (Cut)
      Focus on losing body fat while preserving muscle.

  [3] Bulk Up
      Focus on building maximum muscle mass.

  [4] Maintain
      Keep your current physique and fitness level.
"""

    def get_activity_options(self) -> str:
        """Get formatted activity level options for display."""
        return """
Activity Level (outside of workouts):
  [1] Sedentary      - Desk job, little to no exercise
  [2] Light          - Light exercise 1-3 days/week
  [3] Moderate       - Moderate exercise 3-5 days/week
  [4] Active         - Hard exercise 6-7 days/week
  [5] Very Active    - Very hard exercise, physical job
"""

    def get_experience_options(self) -> str:
        """Get formatted experience level options for display."""
        return """
Lifting Experience:
  [1] Beginner       - New to weight training (< 1 year)
  [2] Intermediate   - Consistent training for 1-3 years
  [3] Advanced       - Serious training for 3+ years
"""
