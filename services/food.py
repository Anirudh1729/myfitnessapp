"""Food tracking service with calorie estimation."""

from datetime import date, timedelta
from typing import Optional, List
from database import Database, FoodEntry
from data.exercises import estimate_food_calories, COMMON_DISHES
from utils import calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros


class FoodService:
    """Handle food tracking and calorie estimation."""

    def __init__(self, db: Database):
        self.db = db

    def log_food(self, user_id: int, dish_name: str, meal_type: str,
                 is_homemade: bool = True, custom_calories: int = None,
                 notes: str = "") -> FoodEntry:
        """
        Log a food entry with automatic calorie estimation.

        Args:
            user_id: User ID
            dish_name: Name of the dish
            meal_type: Type of meal ('breakfast', 'lunch', 'dinner', 'snack')
            is_homemade: Whether the dish was homemade (vs ordered/restaurant)
            custom_calories: Override automatic calorie estimation
            notes: Additional notes

        Returns:
            The created FoodEntry
        """
        # Estimate nutrition if not provided
        if custom_calories is not None:
            nutrition = {
                "calories": custom_calories,
                "protein": 0,
                "carbs": 0,
                "fat": 0
            }
        else:
            nutrition = estimate_food_calories(dish_name, is_homemade)

        entry = FoodEntry(
            user_id=user_id,
            date=date.today(),
            meal_type=meal_type,
            dish_name=dish_name,
            is_homemade=is_homemade,
            estimated_calories=nutrition["calories"],
            protein_g=nutrition["protein"],
            carbs_g=nutrition["carbs"],
            fat_g=nutrition["fat"],
            notes=notes
        )

        entry.id = self.db.add_food_entry(entry)
        return entry

    def get_food_log_confirmation(self, entry: FoodEntry, is_homemade: bool) -> str:
        """Get confirmation message after logging food."""
        source = "Homemade" if is_homemade else "Restaurant/Ordered"
        return f"""
--------------------------------------------------------------------------------
  FOOD LOGGED
--------------------------------------------------------------------------------
  Dish: {entry.dish_name}
  Meal: {entry.meal_type.capitalize()}
  Source: {source}
  Estimated Calories: {entry.estimated_calories}
  Macros: P: {entry.protein_g}g | C: {entry.carbs_g}g | F: {entry.fat_g}g
--------------------------------------------------------------------------------
"""

    def get_daily_summary(self, user_id: int, target_date: date = None) -> str:
        """Get daily food intake summary."""
        if target_date is None:
            target_date = date.today()

        entries = self.db.get_food_entries(user_id, target_date)
        user = self.db.get_user(user_id)

        if not user:
            return "\nUser not found.\n"

        # Calculate targets
        bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
        tdee = calculate_tdee(bmr, user.activity_level)
        target_cals = calculate_target_calories(tdee, user.goal)
        target_macros = calculate_macros(target_cals, user.weight_kg, user.goal)

        # Sum up consumed
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0

        meals = {"breakfast": [], "lunch": [], "dinner": [], "snack": []}

        for entry in entries:
            total_calories += entry.estimated_calories
            total_protein += entry.protein_g
            total_carbs += entry.carbs_g
            total_fat += entry.fat_g

            meal_type = entry.meal_type.lower() if entry.meal_type else "snack"
            if meal_type in meals:
                meals[meal_type].append(entry)

        # Calculate remaining
        remaining_cals = target_cals - total_calories
        remaining_protein = target_macros['protein'] - total_protein
        remaining_carbs = target_macros['carbs'] - total_carbs
        remaining_fat = target_macros['fat'] - total_fat

        date_str = target_date.strftime("%A, %B %d, %Y")

        output = f"""
================================================================================
                    DAILY FOOD LOG - {date_str}
================================================================================

"""
        # Show meals
        for meal_name, meal_entries in meals.items():
            if meal_entries:
                output += f"  {meal_name.upper()}:\n"
                for entry in meal_entries:
                    source = "(H)" if entry.is_homemade else "(R)"
                    output += f"    - {entry.dish_name} {source}: {entry.estimated_calories} cal\n"
                output += "\n"

        if not entries:
            output += "  No food logged yet today.\n\n"

        output += f"""--------------------------------------------------------------------------------
                         DAILY TOTALS
--------------------------------------------------------------------------------

                    Consumed    Target      Remaining
  Calories:         {total_calories:>6}      {target_cals:>6}      {remaining_cals:>+6}
  Protein (g):      {total_protein:>6.0f}      {target_macros['protein']:>6}      {remaining_protein:>+6.0f}
  Carbs (g):        {total_carbs:>6.0f}      {target_macros['carbs']:>6}      {remaining_carbs:>+6.0f}
  Fat (g):          {total_fat:>6.0f}      {target_macros['fat']:>6}      {remaining_fat:>+6.0f}

--------------------------------------------------------------------------------
"""
        # Progress bar for calories
        progress = min(100, int((total_calories / target_cals) * 100)) if target_cals > 0 else 0
        bar_width = 40
        filled = int(bar_width * progress / 100)
        bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"

        output += f"  Calorie Progress: {bar} {progress}%\n"

        if remaining_cals > 0:
            output += f"\n  You can still eat ~{remaining_cals} more calories today.\n"
        elif remaining_cals < -200:
            output += f"\n  You're {abs(remaining_cals)} calories over your target.\n"
        else:
            output += f"\n  You've hit your calorie target!\n"

        output += "=" * 80
        return output

    def get_meal_suggestions(self, user_id: int, remaining_calories: int = None) -> str:
        """Get meal suggestions based on remaining calories."""
        user = self.db.get_user(user_id)
        if not user:
            return "\nUser not found.\n"

        if remaining_calories is None:
            # Calculate remaining
            bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
            tdee = calculate_tdee(bmr, user.activity_level)
            target_cals = calculate_target_calories(tdee, user.goal)
            consumed = self.db.get_daily_calories(user_id, date.today())
            remaining_calories = target_cals - consumed

        if remaining_calories <= 0:
            return "\nYou've reached your calorie target for today. Consider light options if you're hungry.\n"

        output = f"""
================================================================================
                    MEAL SUGGESTIONS (~{remaining_calories} calories remaining)
================================================================================

PROTEIN-RICH OPTIONS:
"""
        protein_foods = ["grilled chicken", "salmon", "eggs", "steak", "protein shake"]
        for food in protein_foods:
            if food in COMMON_DISHES:
                cals = COMMON_DISHES[food]["homemade"]
                if cals <= remaining_calories:
                    output += f"  - {food.title()}: ~{cals} cal (Homemade)\n"

        output += "\nBALANCED MEALS:\n"
        balanced = ["chicken breast", "salmon", "steak", "grilled chicken"]
        for food in balanced:
            if food in COMMON_DISHES:
                cals = COMMON_DISHES[food]["homemade"]
                if cals <= remaining_calories:
                    protein = COMMON_DISHES[food]["protein"]
                    output += f"  - {food.title()}: ~{cals} cal, {protein}g protein\n"

        output += "\nLIGHT OPTIONS:\n"
        light = ["garden salad", "yogurt", "fruit", "eggs"]
        for food in light:
            if food in COMMON_DISHES:
                cals = COMMON_DISHES[food]["homemade"]
                output += f"  - {food.title()}: ~{cals} cal\n"

        output += "\n" + "=" * 80
        return output

    def search_food(self, query: str) -> str:
        """Search for foods in the database."""
        query_lower = query.lower()
        matches = []

        for food, data in COMMON_DISHES.items():
            if query_lower in food:
                matches.append((food, data))

        if not matches:
            return f"\nNo foods found matching '{query}'. You can still log it with custom calories.\n"

        output = f"\nFoods matching '{query}':\n"
        output += "-" * 60 + "\n"
        output += f"{'Food':<25} {'Homemade':<12} {'Restaurant':<12}\n"
        output += "-" * 60 + "\n"

        for food, data in matches[:15]:  # Limit results
            output += f"{food.title():<25} {data['homemade']:<12} {data['restaurant']:<12}\n"

        output += "-" * 60 + "\n"
        return output

    def get_weekly_nutrition_summary(self, user_id: int) -> str:
        """Get nutrition summary for the past week."""
        end_date = date.today()
        start_date = end_date - timedelta(days=6)

        user = self.db.get_user(user_id)
        if not user:
            return "\nUser not found.\n"

        # Calculate target
        bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
        tdee = calculate_tdee(bmr, user.activity_level)
        target_cals = calculate_target_calories(tdee, user.goal)

        output = """
================================================================================
                    WEEKLY NUTRITION SUMMARY
================================================================================

"""
        total_week_calories = 0
        days_logged = 0

        for i in range(7):
            current_date = start_date + timedelta(days=i)
            entries = self.db.get_food_entries(user_id, current_date)
            day_calories = sum(e.estimated_calories for e in entries)

            if entries:
                days_logged += 1
                total_week_calories += day_calories

            day_name = current_date.strftime("%a %m/%d")
            if day_calories > 0:
                diff = day_calories - target_cals
                diff_str = f"({diff:+d})"
                bar_pct = min(100, int((day_calories / target_cals) * 100))
                bar = "#" * (bar_pct // 5) + "-" * (20 - bar_pct // 5)
                output += f"  {day_name}: [{bar}] {day_calories:>5} cal {diff_str}\n"
            else:
                output += f"  {day_name}: [--------------------] No data\n"

        output += "\n" + "-" * 60 + "\n"
        if days_logged > 0:
            avg_calories = total_week_calories // days_logged
            output += f"  Average Daily Calories: {avg_calories} (Target: {target_cals})\n"
            output += f"  Days Logged: {days_logged}/7\n"
        else:
            output += "  No food logged this week.\n"

        output += "=" * 80
        return output
