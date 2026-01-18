"""Workout tracking service."""

from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple
from database import Database, Workout, WorkoutExercise
from data import get_exercise, get_form_tips, search_exercises, EXERCISES
from utils.calories import calculate_workout_calories


class WorkoutService:
    """Handle workout tracking and exercise management."""

    def __init__(self, db: Database):
        self.db = db

    def start_workout(self, user_id: int, workout_type: str) -> Workout:
        """Start a new workout session."""
        workout = Workout(
            user_id=user_id,
            workout_type=workout_type,
            date=date.today(),
            duration_minutes=0
        )
        workout.id = self.db.create_workout(workout)
        return workout

    def add_exercise(self, workout_id: int, user_id: int, exercise_name: str,
                     sets: int = 0, reps: int = 0, weight_kg: float = 0,
                     duration_minutes: int = 0, distance_km: float = 0,
                     notes: str = "") -> Tuple[WorkoutExercise, Optional[dict]]:
        """
        Add an exercise to a workout.

        Returns:
            Tuple of (WorkoutExercise, exercise_info dict or None)
        """
        # Look up exercise in database
        exercise_info = get_exercise(exercise_name)

        exercise_type = "unknown"
        if exercise_info:
            exercise_type = exercise_info.get("type", "unknown")
            # Use the canonical name from our database
            exercise_name = exercise_info["name"]

        # Calculate calories burned (rough estimate)
        calories = 0
        if exercise_type == "cardio":
            # Get user weight for calorie calculation
            user = self.db.get_user(user_id)
            if user and duration_minutes > 0:
                calories = calculate_workout_calories("cardio", duration_minutes, user.weight_kg)
        elif sets > 0 and reps > 0:
            # Rough estimate for weight training: ~0.05 cal per rep per kg lifted
            calories = int(sets * reps * weight_kg * 0.05)

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_name=exercise_name,
            exercise_type=exercise_type,
            sets=sets,
            reps=reps,
            weight_kg=weight_kg,
            duration_minutes=duration_minutes,
            distance_km=distance_km,
            calories_burned=calories,
            notes=notes
        )

        workout_exercise.id = self.db.add_exercise_to_workout(workout_exercise)

        # Update exercise progress for progressive overload tracking
        if weight_kg > 0 and reps > 0:
            self.db.update_exercise_progress(user_id, exercise_name, weight_kg, reps)

        return workout_exercise, exercise_info

    def get_form_tips_display(self, exercise_name: str) -> str:
        """Get formatted form tips for display."""
        exercise = get_exercise(exercise_name)
        if not exercise:
            return f"\nNo form tips found for '{exercise_name}'.\n"

        tips = exercise.get("form_tips", [])
        mistakes = exercise.get("common_mistakes", [])

        output = f"""
================================================================================
                    FORM TIPS: {exercise['name'].upper()}
================================================================================

Type: {exercise['type'].replace('_', ' ').title()}
Primary Muscles: {', '.join(m.replace('_', ' ').title() for m in exercise['primary_muscles'])}
Secondary Muscles: {', '.join(m.replace('_', ' ').title() for m in exercise.get('secondary_muscles', [])) or 'None'}
Difficulty: {exercise.get('difficulty', 'N/A').title()}

PROPER FORM:
"""
        for i, tip in enumerate(tips, 1):
            output += f"  {i}. {tip}\n"

        if mistakes:
            output += "\nCOMMON MISTAKES TO AVOID:\n"
            for mistake in mistakes:
                output += f"  - {mistake}\n"

        output += "=" * 80
        return output

    def get_progressive_overload_suggestion(self, user_id: int, exercise_name: str) -> str:
        """Get progressive overload suggestion based on history."""
        exercise = get_exercise(exercise_name)
        canonical_name = exercise['name'] if exercise else exercise_name

        last_performance = self.db.get_last_exercise_weight(user_id, canonical_name)

        if not last_performance:
            return f"\nThis is your first time logging {canonical_name}. Start with a comfortable weight!\n"

        last_weight, last_reps = last_performance

        # Progressive overload suggestions
        suggestion = f"""
--------------------------------------------------------------------------------
                    PROGRESSIVE OVERLOAD SUGGESTION
--------------------------------------------------------------------------------

Last Performance: {last_weight} kg x {last_reps} reps

Progression Options (pick ONE):
"""
        # Option 1: Add reps
        if last_reps < 12:
            suggestion += f"  1. Same weight, more reps: {last_weight} kg x {last_reps + 1}-{last_reps + 2} reps\n"

        # Option 2: Add weight
        weight_increase = 2.5 if last_weight < 50 else 5
        suggestion += f"  2. More weight, same reps: {last_weight + weight_increase} kg x {last_reps} reps\n"

        # Option 3: Add sets
        suggestion += f"  3. Add an extra set at current weight/reps\n"

        suggestion += """
TIP: Only increase when you can complete all sets with good form!
--------------------------------------------------------------------------------
"""
        return suggestion

    def search_exercise(self, query: str) -> List[dict]:
        """Search for exercises matching a query."""
        return search_exercises(query)

    def get_exercise_search_results(self, query: str) -> str:
        """Get formatted search results."""
        results = self.search_exercise(query)
        if not results:
            return f"\nNo exercises found matching '{query}'.\n"

        output = f"\nExercises matching '{query}':\n"
        output += "-" * 40 + "\n"
        for ex in results[:10]:  # Limit to 10 results
            output += f"  - {ex['name']} ({ex['type']})\n"
        output += "-" * 40 + "\n"
        return output

    def get_all_exercises(self) -> str:
        """Get a list of all available exercises."""
        output = """
================================================================================
                         EXERCISE DATABASE
================================================================================

CHEST:
"""
        # Group by primary muscle
        muscle_groups = {}
        for ex in EXERCISES.values():
            for muscle in ex['primary_muscles']:
                if muscle not in muscle_groups:
                    muscle_groups[muscle] = []
                muscle_groups[muscle].append(ex)

        for muscle, exercises in sorted(muscle_groups.items()):
            output += f"\n{muscle.upper().replace('_', ' ')}:\n"
            for ex in exercises:
                output += f"  - {ex['name']}\n"

        output += "\n" + "=" * 80
        return output

    def get_workout_summary(self, workout_id: int) -> str:
        """Get a summary of a workout."""
        exercises = self.db.get_workout_exercises(workout_id)

        if not exercises:
            return "\nNo exercises logged in this workout yet.\n"

        total_volume = 0
        total_calories = 0

        output = """
--------------------------------------------------------------------------------
                         WORKOUT SUMMARY
--------------------------------------------------------------------------------

"""
        for ex in exercises:
            if ex.exercise_type == "cardio":
                output += f"  {ex.exercise_name}:\n"
                if ex.duration_minutes:
                    output += f"    Duration: {ex.duration_minutes} min\n"
                if ex.distance_km:
                    output += f"    Distance: {ex.distance_km} km\n"
            else:
                volume = ex.sets * ex.reps * ex.weight_kg
                total_volume += volume
                output += f"  {ex.exercise_name}:\n"
                output += f"    {ex.sets} sets x {ex.reps} reps @ {ex.weight_kg} kg\n"
                output += f"    Volume: {volume:.0f} kg\n"

            if ex.calories_burned:
                output += f"    Calories: ~{ex.calories_burned}\n"
                total_calories += ex.calories_burned

            output += "\n"

        output += "-" * 40 + "\n"
        if total_volume > 0:
            output += f"  Total Volume: {total_volume:.0f} kg\n"
        output += f"  Est. Calories Burned: ~{total_calories}\n"
        output += "-" * 40 + "\n"

        return output

    def get_recent_workouts(self, user_id: int, days: int = 7) -> str:
        """Get recent workout history."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        workouts = self.db.get_workouts(user_id, start_date, end_date)

        if not workouts:
            return f"\nNo workouts in the last {days} days.\n"

        output = f"""
================================================================================
                    WORKOUT HISTORY (Last {days} Days)
================================================================================

"""
        for workout in workouts:
            workout_date = workout.date if isinstance(workout.date, str) else str(workout.date)
            output += f"  {workout_date} - {workout.workout_type.replace('_', ' ').title()}\n"

            exercises = self.db.get_workout_exercises(workout.id)
            for ex in exercises:
                if ex.exercise_type == "cardio":
                    output += f"    - {ex.exercise_name}: {ex.duration_minutes} min"
                    if ex.distance_km:
                        output += f", {ex.distance_km} km"
                    output += "\n"
                else:
                    output += f"    - {ex.exercise_name}: {ex.sets}x{ex.reps} @ {ex.weight_kg}kg\n"
            output += "\n"

        output += "=" * 80
        return output

    def get_exercise_history(self, user_id: int, exercise_name: str) -> str:
        """Get history for a specific exercise."""
        exercise = get_exercise(exercise_name)
        canonical_name = exercise['name'] if exercise else exercise_name

        progress = self.db.get_exercise_progress(user_id, canonical_name, limit=10)

        if not progress:
            return f"\nNo history found for {canonical_name}.\n"

        output = f"""
================================================================================
                    {canonical_name.upper()} - PROGRESS HISTORY
================================================================================

"""
        for p in progress:
            progress_date = p.date if isinstance(p.date, str) else str(p.date)
            output += f"  {progress_date}: {p.max_weight_kg} kg x {p.max_reps} reps"
            output += f" (Est. 1RM: {p.estimated_1rm:.1f} kg)\n"

        output += "\n" + "=" * 80
        return output
