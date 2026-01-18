"""Goals service for weekly targets and tracking."""

from datetime import date, timedelta
from typing import Optional
from database import Database, WeeklyGoal
from utils import (
    calculate_bmr, calculate_tdee, calculate_target_calories,
    calculate_macros, calculate_target_weight
)
from utils.calories import calculate_ideal_weight_range, get_body_fat_estimate


class GoalsService:
    """Handle weekly goals and progress tracking."""

    def __init__(self, db: Database):
        self.db = db

    def create_weekly_goal(self, user_id: int) -> WeeklyGoal:
        """Create a new weekly goal based on user profile."""
        user = self.db.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        # Calculate targets
        bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
        tdee = calculate_tdee(bmr, user.activity_level)
        target_cals = calculate_target_calories(tdee, user.goal)

        # Get current weight
        current_weight = self.db.get_latest_weight(user_id) or user.weight_kg

        # Calculate target weight for end of week
        target_weight = calculate_target_weight(current_weight, user.goal, weeks=1)

        # Determine target workouts based on experience
        workout_targets = {
            "beginner": 3,
            "intermediate": 4,
            "advanced": 5
        }
        target_workouts = workout_targets.get(user.experience_level, 4)

        # Get Monday of current week
        today = date.today()
        monday = today - timedelta(days=today.weekday())

        goal = WeeklyGoal(
            user_id=user_id,
            week_start=monday,
            target_weight_kg=target_weight,
            target_calories_daily=target_cals,
            target_workouts=target_workouts,
            completed_workouts=0
        )

        goal.id = self.db.create_weekly_goal(goal)
        return goal

    def get_weekly_goal(self, user_id: int) -> Optional[WeeklyGoal]:
        """Get the current weekly goal."""
        return self.db.get_current_weekly_goal(user_id)

    def update_workout_count(self, user_id: int):
        """Update the completed workout count for current goal."""
        goal = self.get_weekly_goal(user_id)
        if goal:
            workouts_this_week = self.db.get_workouts_this_week(user_id)
            goal.completed_workouts = workouts_this_week
            self.db.update_weekly_goal(goal)

    def log_weight(self, user_id: int, weight_kg: float, notes: str = "") -> str:
        """Log weight and return feedback."""
        user = self.db.get_user(user_id)
        if not user:
            return "\nUser not found.\n"

        # Get previous weight
        previous_weight = self.db.get_latest_weight(user_id)

        # Log new weight
        self.db.add_weight_log(user_id, weight_kg, notes=notes)

        # Update user's current weight
        user.weight_kg = weight_kg
        self.db.update_user(user)

        output = f"""
--------------------------------------------------------------------------------
  WEIGHT LOGGED: {weight_kg} kg
--------------------------------------------------------------------------------
"""
        if previous_weight:
            change = weight_kg - previous_weight
            if abs(change) < 0.1:
                output += f"  No significant change from last weigh-in ({previous_weight} kg)\n"
            elif change > 0:
                output += f"  Up {change:.1f} kg from last weigh-in ({previous_weight} kg)\n"
            else:
                output += f"  Down {abs(change):.1f} kg from last weigh-in ({previous_weight} kg)\n"

            # Provide context based on goal
            if user.goal == "lean" and change < 0:
                output += "  You're on track with your cutting goal!\n"
            elif user.goal == "lean" and change > 0.5:
                output += "  Weight went up - review your calorie intake.\n"
            elif user.goal == "bulk" and change > 0:
                output += "  You're on track with your bulking goal!\n"
            elif user.goal == "bulk" and change < -0.5:
                output += "  Weight went down - you may need to eat more.\n"
            elif user.goal == "jacked_model":
                if abs(change) < 0.3:
                    output += "  Good slow progress for a lean physique!\n"

        output += "--------------------------------------------------------------------------------\n"
        return output

    def get_weekly_summary(self, user_id: int) -> str:
        """Get comprehensive weekly summary."""
        user = self.db.get_user(user_id)
        if not user:
            return "\nUser not found.\n"

        goal = self.get_weekly_goal(user_id)
        if not goal:
            # Create a new goal if none exists
            goal = self.create_weekly_goal(user_id)

        # Get weight history
        weight_history = self.db.get_weight_history(user_id, limit=7)
        current_weight = weight_history[0].weight_kg if weight_history else user.weight_kg

        # Calculate progress
        workouts_done = self.db.get_workouts_this_week(user_id)

        # Get calorie data for the week
        today = date.today()
        monday = today - timedelta(days=today.weekday())

        total_calories = 0
        days_with_food = 0
        for i in range(7):
            day = monday + timedelta(days=i)
            if day > today:
                break
            day_cals = self.db.get_daily_calories(user_id, day)
            if day_cals > 0:
                total_calories += day_cals
                days_with_food += 1

        avg_calories = total_calories // days_with_food if days_with_food > 0 else 0

        # Calculate ideal weight range
        ideal_min, ideal_max = calculate_ideal_weight_range(user.height_cm, user.gender)

        output = f"""
================================================================================
                         WEEKLY SUMMARY
================================================================================

  Current Week: {monday.strftime('%b %d')} - {(monday + timedelta(days=6)).strftime('%b %d, %Y')}

WEIGHT PROGRESS:
--------------------------------------------------------------------------------
  Current Weight:  {current_weight:.1f} kg
  Target Weight:   {goal.target_weight_kg:.1f} kg
  Ideal Range:     {ideal_min:.1f} - {ideal_max:.1f} kg
"""
        # Weight trend
        if len(weight_history) >= 2:
            weight_change = weight_history[0].weight_kg - weight_history[-1].weight_kg
            if abs(weight_change) < 0.1:
                output += "  Trend:           Stable\n"
            elif weight_change > 0:
                output += f"  Trend:           Up {weight_change:.1f} kg\n"
            else:
                output += f"  Trend:           Down {abs(weight_change):.1f} kg\n"

        output += f"""
WORKOUT PROGRESS:
--------------------------------------------------------------------------------
  Completed:       {workouts_done} / {goal.target_workouts} workouts
"""
        # Progress bar for workouts
        workout_pct = min(100, int((workouts_done / goal.target_workouts) * 100)) if goal.target_workouts > 0 else 0
        bar_width = 20
        filled = int(bar_width * workout_pct / 100)
        bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
        output += f"  Progress:        {bar} {workout_pct}%\n"

        output += f"""
NUTRITION PROGRESS:
--------------------------------------------------------------------------------
  Target Daily:    {goal.target_calories_daily} calories
  Average Daily:   {avg_calories} calories
  Days Logged:     {days_with_food} / {min(7, (today - monday).days + 1)}
"""
        if avg_calories > 0:
            cal_diff = avg_calories - goal.target_calories_daily
            if abs(cal_diff) < 100:
                output += "  Status:          On target!\n"
            elif cal_diff > 0:
                output += f"  Status:          {cal_diff} over target\n"
            else:
                output += f"  Status:          {abs(cal_diff)} under target\n"

        output += """
================================================================================
"""

        # Recommendations
        output += "\nRECOMMENDATIONS:\n"

        if workouts_done < goal.target_workouts:
            remaining = goal.target_workouts - workouts_done
            days_left = 7 - (today - monday).days
            if remaining <= days_left:
                output += f"  - You have {remaining} more workout(s) to hit your weekly target\n"
            else:
                output += f"  - You're behind on workouts. Try to fit in {remaining} sessions\n"

        if avg_calories > 0:
            if user.goal == "lean" and avg_calories > goal.target_calories_daily + 200:
                output += "  - Cut calories are too high. Focus on protein and reduce carbs/fats\n"
            elif user.goal == "bulk" and avg_calories < goal.target_calories_daily - 200:
                output += "  - You need to eat more! Add calorie-dense foods\n"

        if len(weight_history) < 3:
            output += "  - Log your weight more frequently for better tracking\n"

        output += "\n" + "=" * 80
        return output

    def get_calorie_recommendation(self, user_id: int) -> str:
        """Get detailed calorie and macro recommendations."""
        user = self.db.get_user(user_id)
        if not user:
            return "\nUser not found.\n"

        bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
        tdee = calculate_tdee(bmr, user.activity_level)
        target_cals = calculate_target_calories(tdee, user.goal)
        macros = calculate_macros(target_cals, user.weight_kg, user.goal)
        bf_estimate, bf_category = get_body_fat_estimate(
            user.weight_kg, user.height_cm, user.age, user.gender
        )

        goal_descriptions = {
            'jacked_model': 'Build lean muscle while staying cut (slight deficit)',
            'lean': 'Lose body fat while preserving muscle (moderate deficit)',
            'bulk': 'Build maximum muscle (calorie surplus)',
            'maintain': 'Maintain current weight (eat at TDEE)'
        }

        output = f"""
================================================================================
                    CALORIE & MACRO RECOMMENDATIONS
================================================================================

YOUR STATS:
  Weight: {user.weight_kg} kg
  Height: {user.height_cm} cm
  Age: {user.age}
  Activity: {user.activity_level.replace('_', ' ').title()}
  Est. Body Fat: {bf_estimate}% ({bf_category})

CALCULATIONS:
  Basal Metabolic Rate (BMR):     {int(bmr)} cal/day
    (Calories your body burns at complete rest)

  Total Daily Energy Expenditure: {int(tdee)} cal/day
    (BMR adjusted for your activity level)

YOUR GOAL: {user.goal.replace('_', ' ').title()}
  {goal_descriptions.get(user.goal, '')}

================================================================================
                         DAILY TARGETS
================================================================================

  +------------------------+
  |  CALORIES: {target_cals:>5}      |
  +------------------------+
  |  Protein:  {macros['protein']:>4}g       |
  |  Carbs:    {macros['carbs']:>4}g       |
  |  Fat:      {macros['fat']:>4}g       |
  +------------------------+

MACRO BREAKDOWN:
  - Protein ({macros['protein']}g): {macros['protein'] * 4} calories ({int(macros['protein'] * 4 / target_cals * 100)}%)
  - Carbs ({macros['carbs']}g): {macros['carbs'] * 4} calories ({int(macros['carbs'] * 4 / target_cals * 100)}%)
  - Fat ({macros['fat']}g): {macros['fat'] * 9} calories ({int(macros['fat'] * 9 / target_cals * 100)}%)

================================================================================
                         MEAL TIMING GUIDE
================================================================================

For your goal ({user.goal.replace('_', ' ')}), consider this meal structure:

"""
        if user.goal in ['jacked_model', 'lean']:
            output += f"""  BREAKFAST (25% of calories): ~{int(target_cals * 0.25)} cal
    - Focus on protein to start the day
    - Example: Eggs + oatmeal + fruit

  LUNCH (30% of calories): ~{int(target_cals * 0.30)} cal
    - Balanced meal with protein, carbs, vegetables
    - Example: Chicken breast + rice + vegetables

  DINNER (30% of calories): ~{int(target_cals * 0.30)} cal
    - Protein-focused, moderate carbs
    - Example: Salmon + sweet potato + salad

  SNACKS (15% of calories): ~{int(target_cals * 0.15)} cal
    - Protein-rich snacks preferred
    - Example: Greek yogurt, protein shake, nuts
"""
        else:  # bulk or maintain
            output += f"""  BREAKFAST (20% of calories): ~{int(target_cals * 0.20)} cal
    - Start strong with protein and carbs
    - Example: Eggs + toast + fruit + protein shake

  LUNCH (25% of calories): ~{int(target_cals * 0.25)} cal
    - Big balanced meal
    - Example: Steak + pasta + vegetables

  PRE-WORKOUT (~10%): ~{int(target_cals * 0.10)} cal
    - Carbs for energy
    - Example: Banana + rice cakes

  POST-WORKOUT (20%): ~{int(target_cals * 0.20)} cal
    - Protein + fast carbs
    - Example: Protein shake + fruit

  DINNER (25% of calories): ~{int(target_cals * 0.25)} cal
    - Complete meal with all macros
    - Example: Chicken + rice + vegetables + olive oil
"""

        output += """
TIPS:
  - Hit your protein target every day (most important macro)
  - Drink at least 3 liters of water daily
  - Eat protein with every meal
  - Time carbs around your workouts
  - Don't fear healthy fats

================================================================================
"""
        return output

    def get_long_term_projection(self, user_id: int, weeks: int = 12) -> str:
        """Get long-term weight projection."""
        user = self.db.get_user(user_id)
        if not user:
            return "\nUser not found.\n"

        current_weight = self.db.get_latest_weight(user_id) or user.weight_kg
        ideal_min, ideal_max = calculate_ideal_weight_range(user.height_cm, user.gender)

        output = f"""
================================================================================
                    {weeks}-WEEK PROJECTION
================================================================================

  Current Weight: {current_weight:.1f} kg
  Goal: {user.goal.replace('_', ' ').title()}
  Ideal Range: {ideal_min:.1f} - {ideal_max:.1f} kg

PROJECTED PROGRESS:
"""
        weight = current_weight
        for week in range(1, weeks + 1):
            weight = calculate_target_weight(weight, user.goal, weeks=1)
            marker = ""
            if ideal_min <= weight <= ideal_max:
                marker = " <-- In ideal range"
            output += f"  Week {week:>2}: {weight:.1f} kg{marker}\n"

        final_weight = calculate_target_weight(current_weight, user.goal, weeks=weeks)
        total_change = final_weight - current_weight

        output += f"""
--------------------------------------------------------------------------------
  Projected Final Weight: {final_weight:.1f} kg
  Total Change: {total_change:+.1f} kg

NOTE: These projections assume consistent adherence to your nutrition and
training plan. Actual results will vary based on many factors.

================================================================================
"""
        return output
