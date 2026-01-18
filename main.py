#!/usr/bin/env python3
"""My Fitness App - A CLI fitness tracking application."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from database import Database
from services import OnboardingService, WorkoutService, FoodService, PlannerService, GoalsService


class FitnessApp:
    """Main fitness application CLI."""

    def __init__(self):
        self.db = Database()
        self.onboarding = OnboardingService(self.db)
        self.workout = WorkoutService(self.db)
        self.food = FoodService(self.db)
        self.planner = PlannerService(self.db)
        self.goals = GoalsService(self.db)
        self.user = None
        self.current_workout = None

    def run(self):
        """Run the main application loop."""
        self.clear_screen()

        # Check for existing user or run onboarding
        self.user = self.onboarding.check_existing_user()
        if not self.user:
            self.run_onboarding()
        else:
            print(f"\nWelcome back, {self.user.name}!")

        # Ensure weekly goal exists
        goal = self.goals.get_weekly_goal(self.user.id)
        if not goal:
            self.goals.create_weekly_goal(self.user.id)

        # Main menu loop
        self.main_menu()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self):
        """Pause and wait for user input."""
        input("\nPress Enter to continue...")

    def get_input(self, prompt: str, default: str = None) -> str:
        """Get user input with optional default value."""
        if default:
            result = input(f"{prompt} [{default}]: ").strip()
            return result if result else default
        return input(f"{prompt}: ").strip()

    def run_onboarding(self):
        """Run the onboarding process for new users."""
        print(self.onboarding.get_welcome_message())
        self.pause()

        # Get name
        while True:
            name = self.get_input("What's your name?")
            valid, error = self.onboarding.validate_name(name)
            if valid:
                break
            print(f"  Error: {error}")

        # Get age
        while True:
            age_str = self.get_input("How old are you?")
            valid, error, age = self.onboarding.validate_age(age_str)
            if valid:
                break
            print(f"  Error: {error}")

        # Get gender
        while True:
            gender_str = self.get_input("Gender (M/F)")
            valid, error, gender = self.onboarding.validate_gender(gender_str)
            if valid:
                break
            print(f"  Error: {error}")

        # Get height
        while True:
            height_str = self.get_input("Height in centimeters (e.g., 175)")
            valid, error, height = self.onboarding.validate_height(height_str)
            if valid:
                break
            print(f"  Error: {error}")

        # Get weight
        while True:
            weight_str = self.get_input("Current weight in kilograms (e.g., 75)")
            valid, error, weight = self.onboarding.validate_weight(weight_str)
            if valid:
                break
            print(f"  Error: {error}")

        # Get goal
        print(self.onboarding.get_goal_options())
        while True:
            goal_str = self.get_input("Select your goal (1-4)", "1")
            valid, error, goal = self.onboarding.validate_goal(goal_str)
            if valid:
                break
            print(f"  Error: {error}")

        # Get activity level
        print(self.onboarding.get_activity_options())
        while True:
            activity_str = self.get_input("Select your activity level (1-5)", "3")
            valid, error, activity = self.onboarding.validate_activity_level(activity_str)
            if valid:
                break
            print(f"  Error: {error}")

        # Get experience level
        print(self.onboarding.get_experience_options())
        while True:
            exp_str = self.get_input("Select your experience level (1-3)", "1")
            valid, error, experience = self.onboarding.validate_experience(exp_str)
            if valid:
                break
            print(f"  Error: {error}")

        # Create user
        self.user = self.onboarding.create_user(
            name=name,
            age=age,
            gender=gender,
            height_cm=height,
            weight_kg=weight,
            goal=goal,
            activity_level=activity,
            experience_level=experience
        )

        # Show summary
        self.clear_screen()
        print(self.onboarding.get_user_summary(self.user))
        self.pause()

    def main_menu(self):
        """Display and handle main menu."""
        while True:
            self.clear_screen()
            print(f"""
================================================================================
                    MY FITNESS APP - Main Menu
================================================================================

  Welcome, {self.user.name}!
  Today: {date.today().strftime('%A, %B %d, %Y')}

  [1] Start Workout
  [2] Log Food
  [3] Log Weight
  [4] View Today's Plan
  [5] View Weekly Summary
  [6] Workout Plans & Guides
  [7] Calorie & Nutrition Info
  [8] Exercise Database
  [9] Settings & Profile
  [0] Exit

================================================================================
""")
            choice = self.get_input("Select an option")

            if choice == "1":
                self.workout_menu()
            elif choice == "2":
                self.food_menu()
            elif choice == "3":
                self.log_weight_menu()
            elif choice == "4":
                self.view_todays_plan()
            elif choice == "5":
                self.view_weekly_summary()
            elif choice == "6":
                self.plans_guides_menu()
            elif choice == "7":
                self.nutrition_menu()
            elif choice == "8":
                self.exercise_database_menu()
            elif choice == "9":
                self.settings_menu()
            elif choice == "0":
                print("\nGoodbye! Keep pushing towards your goals!")
                self.db.close()
                sys.exit(0)

    def workout_menu(self):
        """Handle workout tracking."""
        self.clear_screen()
        print("""
================================================================================
                         START WORKOUT
================================================================================

  [1] Weight Lifting
  [2] Cardio
  [3] Mixed (Weights + Cardio)
  [4] View Recent Workouts
  [0] Back to Main Menu

================================================================================
""")
        choice = self.get_input("Select workout type")

        if choice == "0":
            return
        elif choice == "4":
            print(self.workout.get_recent_workouts(self.user.id))
            self.pause()
            return

        workout_types = {"1": "weight_lifting", "2": "cardio", "3": "mixed"}
        workout_type = workout_types.get(choice, "weight_lifting")

        # Start workout
        self.current_workout = self.workout.start_workout(self.user.id, workout_type)
        print(f"\n  Workout started! Type: {workout_type.replace('_', ' ').title()}")

        # Exercise logging loop
        while True:
            print("""
  Commands:
    - Type exercise name to log it
    - 'done' to finish workout
    - 'form <exercise>' for form tips
    - 'search <query>' to find exercises
    - 'summary' to see workout so far
""")
            cmd = self.get_input("Exercise or command").strip().lower()

            if cmd == "done":
                break
            elif cmd == "summary":
                print(self.workout.get_workout_summary(self.current_workout.id))
            elif cmd.startswith("form "):
                exercise_name = cmd[5:]
                print(self.workout.get_form_tips_display(exercise_name))
            elif cmd.startswith("search "):
                query = cmd[7:]
                print(self.workout.get_exercise_search_results(query))
            elif cmd:
                self.log_exercise(cmd, workout_type)

        # Show workout summary
        print(self.workout.get_workout_summary(self.current_workout.id))

        # Update goals
        self.goals.update_workout_count(self.user.id)

        self.current_workout = None
        self.pause()

    def log_exercise(self, exercise_name: str, workout_type: str):
        """Log a single exercise."""
        # Show form tips and progressive overload suggestion
        print(self.workout.get_form_tips_display(exercise_name))
        print(self.workout.get_progressive_overload_suggestion(self.user.id, exercise_name))

        if workout_type == "cardio":
            duration = self.get_input("Duration (minutes)", "30")
            distance = self.get_input("Distance in km (optional, press Enter to skip)", "0")

            exercise, _ = self.workout.add_exercise(
                workout_id=self.current_workout.id,
                user_id=self.user.id,
                exercise_name=exercise_name,
                duration_minutes=int(duration) if duration else 0,
                distance_km=float(distance) if distance else 0
            )
            print(f"\n  Logged: {exercise.exercise_name} - {duration} min")
        else:
            sets = self.get_input("Sets", "3")
            reps = self.get_input("Reps", "10")
            weight = self.get_input("Weight (kg)", "0")

            exercise, exercise_info = self.workout.add_exercise(
                workout_id=self.current_workout.id,
                user_id=self.user.id,
                exercise_name=exercise_name,
                sets=int(sets) if sets else 0,
                reps=int(reps) if reps else 0,
                weight_kg=float(weight) if weight else 0
            )

            print(f"\n  Logged: {exercise.exercise_name} - {sets}x{reps} @ {weight}kg")

    def food_menu(self):
        """Handle food logging."""
        while True:
            self.clear_screen()
            print("""
================================================================================
                         LOG FOOD
================================================================================

  [1] Log a Meal/Dish
  [2] View Today's Food Log
  [3] Search Food Database
  [4] Get Meal Suggestions
  [5] View Weekly Nutrition
  [0] Back to Main Menu

================================================================================
""")
            choice = self.get_input("Select an option")

            if choice == "0":
                return
            elif choice == "1":
                self.log_food_item()
            elif choice == "2":
                print(self.food.get_daily_summary(self.user.id))
                self.pause()
            elif choice == "3":
                query = self.get_input("Search for food")
                print(self.food.search_food(query))
                self.pause()
            elif choice == "4":
                print(self.food.get_meal_suggestions(self.user.id))
                self.pause()
            elif choice == "5":
                print(self.food.get_weekly_nutrition_summary(self.user.id))
                self.pause()

    def log_food_item(self):
        """Log a single food item."""
        dish = self.get_input("What did you eat?")
        if not dish:
            return

        meal = self.get_input("Meal type (breakfast/lunch/dinner/snack)", "snack")
        homemade = self.get_input("Homemade or ordered? (h/o)", "h")
        is_homemade = homemade.lower().startswith("h")

        custom_cal = self.get_input("Custom calories? (Enter to auto-estimate)", "")
        custom_calories = int(custom_cal) if custom_cal else None

        entry = self.food.log_food(
            user_id=self.user.id,
            dish_name=dish,
            meal_type=meal,
            is_homemade=is_homemade,
            custom_calories=custom_calories
        )

        print(self.food.get_food_log_confirmation(entry, is_homemade))
        self.pause()

    def log_weight_menu(self):
        """Handle weight logging."""
        self.clear_screen()
        print("""
================================================================================
                         LOG WEIGHT
================================================================================
""")
        weight_str = self.get_input("Enter your weight (kg)")
        try:
            weight = float(weight_str)
            if 30 <= weight <= 300:
                feedback = self.goals.log_weight(self.user.id, weight)
                print(feedback)
            else:
                print("  Invalid weight. Please enter a value between 30 and 300 kg.")
        except ValueError:
            print("  Invalid input. Please enter a number.")

        self.pause()

    def view_todays_plan(self):
        """View today's workout plan."""
        self.clear_screen()
        split = self.planner.get_recommended_split(self.user.experience_level)
        print(self.planner.get_todays_workout(self.user.id, split))
        self.pause()

    def view_weekly_summary(self):
        """View weekly summary."""
        self.clear_screen()
        print(self.goals.get_weekly_summary(self.user.id))
        self.pause()

    def plans_guides_menu(self):
        """View workout plans and guides."""
        while True:
            self.clear_screen()
            print("""
================================================================================
                    WORKOUT PLANS & GUIDES
================================================================================

  [1] View Available Workout Splits
  [2] View Full Workout Plan
  [3] View Weekly Schedule
  [4] Progressive Overload Guide
  [5] Rest Day Guide
  [0] Back to Main Menu

================================================================================
""")
            choice = self.get_input("Select an option")

            if choice == "0":
                return
            elif choice == "1":
                print(self.planner.get_available_splits())
                self.pause()
            elif choice == "2":
                print(self.planner.get_available_splits())
                split_choice = self.get_input("Select a split (1-4)")
                print(self.planner.get_workout_plan(split_choice))
                self.pause()
            elif choice == "3":
                split = self.planner.get_recommended_split(self.user.experience_level)
                print(self.planner.get_weekly_schedule(split, self.user.experience_level))
                self.pause()
            elif choice == "4":
                print(self.planner.get_progressive_overload_guide())
                self.pause()
            elif choice == "5":
                print(self.planner.get_rest_day_advice())
                self.pause()

    def nutrition_menu(self):
        """View nutrition information."""
        while True:
            self.clear_screen()
            print("""
================================================================================
                    CALORIE & NUTRITION INFO
================================================================================

  [1] View Your Calorie Recommendations
  [2] View Today's Nutrition Summary
  [3] View Long-term Projection
  [0] Back to Main Menu

================================================================================
""")
            choice = self.get_input("Select an option")

            if choice == "0":
                return
            elif choice == "1":
                print(self.goals.get_calorie_recommendation(self.user.id))
                self.pause()
            elif choice == "2":
                print(self.food.get_daily_summary(self.user.id))
                self.pause()
            elif choice == "3":
                weeks = self.get_input("Projection weeks", "12")
                print(self.goals.get_long_term_projection(self.user.id, int(weeks)))
                self.pause()

    def exercise_database_menu(self):
        """Browse exercise database."""
        while True:
            self.clear_screen()
            print("""
================================================================================
                    EXERCISE DATABASE
================================================================================

  [1] View All Exercises
  [2] Search Exercises
  [3] View Form Tips for Exercise
  [4] View Exercise History
  [0] Back to Main Menu

================================================================================
""")
            choice = self.get_input("Select an option")

            if choice == "0":
                return
            elif choice == "1":
                print(self.workout.get_all_exercises())
                self.pause()
            elif choice == "2":
                query = self.get_input("Search for exercise")
                print(self.workout.get_exercise_search_results(query))
                self.pause()
            elif choice == "3":
                exercise = self.get_input("Exercise name")
                print(self.workout.get_form_tips_display(exercise))
                self.pause()
            elif choice == "4":
                exercise = self.get_input("Exercise name")
                print(self.workout.get_exercise_history(self.user.id, exercise))
                self.pause()

    def settings_menu(self):
        """Handle settings and profile."""
        while True:
            self.clear_screen()
            print(f"""
================================================================================
                    SETTINGS & PROFILE
================================================================================

  Current Profile:
    Name: {self.user.name}
    Age: {self.user.age}
    Gender: {self.user.gender.capitalize()}
    Height: {self.user.height_cm} cm
    Weight: {self.user.weight_kg} kg
    Goal: {self.user.goal.replace('_', ' ').title()}
    Activity Level: {self.user.activity_level.replace('_', ' ').title()}
    Experience: {self.user.experience_level.capitalize()}

  [1] Update Weight
  [2] Update Goal
  [3] Update Activity Level
  [4] Update Experience Level
  [5] View Weight History
  [0] Back to Main Menu

================================================================================
""")
            choice = self.get_input("Select an option")

            if choice == "0":
                return
            elif choice == "1":
                weight_str = self.get_input("New weight (kg)")
                try:
                    weight = float(weight_str)
                    self.user.weight_kg = weight
                    self.db.update_user(self.user)
                    self.db.add_weight_log(self.user.id, weight)
                    print("  Weight updated!")
                except ValueError:
                    print("  Invalid weight.")
                self.pause()
            elif choice == "2":
                print(self.onboarding.get_goal_options())
                goal_str = self.get_input("Select new goal (1-4)")
                valid, _, goal = self.onboarding.validate_goal(goal_str)
                if valid:
                    self.user.goal = goal
                    self.db.update_user(self.user)
                    print("  Goal updated!")
                self.pause()
            elif choice == "3":
                print(self.onboarding.get_activity_options())
                activity_str = self.get_input("Select activity level (1-5)")
                valid, _, activity = self.onboarding.validate_activity_level(activity_str)
                if valid:
                    self.user.activity_level = activity
                    self.db.update_user(self.user)
                    print("  Activity level updated!")
                self.pause()
            elif choice == "4":
                print(self.onboarding.get_experience_options())
                exp_str = self.get_input("Select experience level (1-3)")
                valid, _, experience = self.onboarding.validate_experience(exp_str)
                if valid:
                    self.user.experience_level = experience
                    self.db.update_user(self.user)
                    print("  Experience level updated!")
                self.pause()
            elif choice == "5":
                history = self.db.get_weight_history(self.user.id, limit=30)
                print("\n  Weight History (last 30 entries):")
                print("  " + "-" * 30)
                for log in history:
                    log_date = log.date if isinstance(log.date, str) else str(log.date)
                    print(f"    {log_date}: {log.weight_kg} kg")
                print("  " + "-" * 30)
                self.pause()


def main():
    """Main entry point."""
    app = FitnessApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nExiting... Keep working towards your goals!")
        app.db.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
