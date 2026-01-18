"""Workout tracking service."""

from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple, Dict
from database import Database, Workout, WorkoutExercise
from data import get_exercise, get_form_tips, search_exercises, EXERCISES
from utils.calories import calculate_workout_calories


# Movement pattern keywords for exercise inference
MOVEMENT_PATTERNS = {
    "push": {
        "keywords": ["press", "push", "dip", "fly", "flye", "extension", "kickback", "pushdown"],
        "primary_muscles": ["chest", "triceps", "front_delts"],
        "type": "compound"
    },
    "pull": {
        "keywords": ["row", "pull", "curl", "pulldown", "chin", "shrug", "face pull"],
        "primary_muscles": ["back", "biceps", "rear_delts"],
        "type": "compound"
    },
    "squat": {
        "keywords": ["squat", "leg press", "lunge", "split squat", "hack"],
        "primary_muscles": ["quadriceps", "glutes"],
        "type": "compound"
    },
    "hinge": {
        "keywords": ["deadlift", "rdl", "romanian", "hip hinge", "good morning", "hip thrust"],
        "primary_muscles": ["hamstrings", "glutes", "lower_back"],
        "type": "compound"
    },
    "lateral": {
        "keywords": ["lateral", "raise", "side", "abduction"],
        "primary_muscles": ["side_delts"],
        "type": "isolation"
    },
    "isolation_arm": {
        "keywords": ["curl", "extension", "tricep", "bicep", "hammer", "preacher"],
        "primary_muscles": ["biceps", "triceps"],
        "type": "isolation"
    },
    "core": {
        "keywords": ["crunch", "plank", "ab", "sit-up", "leg raise", "twist", "rollout"],
        "primary_muscles": ["abs", "core", "obliques"],
        "type": "isolation"
    },
    "calf": {
        "keywords": ["calf", "raise", "toe"],
        "primary_muscles": ["calves"],
        "type": "isolation"
    },
    "cardio": {
        "keywords": ["run", "jog", "bike", "cycle", "row", "swim", "elliptical", "treadmill", "stair"],
        "primary_muscles": ["cardiovascular"],
        "type": "cardio"
    }
}

# Generic form tips by movement pattern
GENERIC_FORM_TIPS = {
    "push": [
        "Keep your shoulder blades retracted and stable",
        "Control the negative (lowering) portion of the movement",
        "Don't lock out joints explosively - maintain tension",
        "Keep your core braced throughout the movement",
        "Breathe out on the pushing/concentric phase",
        "Maintain proper elbow positioning to protect shoulders"
    ],
    "pull": [
        "Initiate the movement by squeezing your back/target muscle",
        "Keep your chest up and shoulders back",
        "Pull with your elbows, not your hands",
        "Squeeze at the peak contraction",
        "Control the negative - don't let the weight drop",
        "Avoid using momentum to move the weight"
    ],
    "squat": [
        "Keep your chest up and back straight",
        "Push your knees out in line with your toes",
        "Maintain weight through your mid-foot to heel",
        "Descend to at least parallel depth",
        "Brace your core before each rep",
        "Drive up through your heels"
    ],
    "hinge": [
        "Keep a neutral spine throughout the movement",
        "Push your hips back to initiate the movement",
        "Keep the weight close to your body",
        "Feel the stretch in your hamstrings",
        "Squeeze your glutes at the top",
        "Don't round your lower back"
    ],
    "lateral": [
        "Lead with your elbows, not your hands",
        "Keep a slight bend in your elbows",
        "Raise to shoulder height, not above",
        "Control the descent - don't drop the weight",
        "Keep your traps relaxed - don't shrug",
        "Use lighter weight with strict form"
    ],
    "isolation_arm": [
        "Keep your upper arm stationary throughout",
        "Focus on the mind-muscle connection",
        "Don't swing or use body momentum",
        "Squeeze the target muscle at peak contraction",
        "Control both the positive and negative",
        "Use a full range of motion"
    ],
    "core": [
        "Focus on contracting your abs, not just moving",
        "Keep your lower back pressed down when lying",
        "Breathe steadily - don't hold your breath",
        "Move in a controlled manner",
        "Engage your core before starting each rep",
        "Quality over quantity - focus on form"
    ],
    "calf": [
        "Get a full stretch at the bottom of the movement",
        "Rise up as high as possible on your toes",
        "Squeeze the calves at the top",
        "Control the descent - no bouncing",
        "Keep knees straight for gastrocnemius, bent for soleus",
        "Use a slow, controlled tempo"
    ],
    "cardio": [
        "Maintain proper posture throughout",
        "Start with a warm-up at lower intensity",
        "Stay hydrated during your session",
        "Focus on breathing rhythm",
        "Cool down gradually at the end",
        "Listen to your body and adjust intensity as needed"
    ],
    "general": [
        "Start with a weight you can control with good form",
        "Focus on the mind-muscle connection",
        "Use a full range of motion",
        "Control both the lifting and lowering phases",
        "Breathe properly - exhale on exertion",
        "If unsure, use lighter weight until form is mastered"
    ]
}


class WorkoutService:
    """Handle workout tracking and exercise management."""

    def __init__(self, db: Database):
        self.db = db

    def _infer_exercise_properties(self, exercise_name: str, description: str = "") -> Dict:
        """
        Infer exercise properties from name and optional description.

        Returns dict with type, primary_muscles, secondary_muscles, form_tips, common_mistakes
        """
        name_lower = exercise_name.lower()
        desc_lower = description.lower() if description else ""
        combined = f"{name_lower} {desc_lower}"

        # Find the best matching movement pattern
        best_match = None
        best_score = 0

        for pattern_name, pattern_info in MOVEMENT_PATTERNS.items():
            score = 0
            for keyword in pattern_info["keywords"]:
                if keyword in combined:
                    score += len(keyword)  # Longer matches score higher

            if score > best_score:
                best_score = score
                best_match = pattern_name

        # Default to general compound if no match
        if not best_match:
            best_match = "general"
            pattern_info = {
                "primary_muscles": ["general"],
                "type": "compound"
            }
        else:
            pattern_info = MOVEMENT_PATTERNS[best_match]

        # Get form tips for this pattern
        form_tips = GENERIC_FORM_TIPS.get(best_match, GENERIC_FORM_TIPS["general"]).copy()

        # Add description-based customization
        if description:
            form_tips.insert(0, f"Note: {description}")

        # Generate common mistakes based on pattern
        common_mistakes = self._generate_common_mistakes(best_match, exercise_name)

        # Determine secondary muscles
        secondary = []
        if "chest" in pattern_info["primary_muscles"]:
            secondary = ["triceps", "front_delts"]
        elif "back" in pattern_info["primary_muscles"]:
            secondary = ["biceps", "rear_delts"]
        elif "quadriceps" in pattern_info["primary_muscles"]:
            secondary = ["glutes", "hamstrings"]
        elif "hamstrings" in pattern_info["primary_muscles"]:
            secondary = ["glutes", "lower_back"]

        return {
            "type": pattern_info["type"],
            "primary_muscles": pattern_info["primary_muscles"],
            "secondary_muscles": secondary,
            "form_tips": form_tips,
            "common_mistakes": common_mistakes,
            "difficulty": "intermediate",
            "movement_pattern": best_match
        }

    def _generate_common_mistakes(self, pattern: str, exercise_name: str) -> List[str]:
        """Generate common mistakes based on movement pattern."""
        mistakes = {
            "push": [
                "Using momentum instead of controlled movement",
                "Flaring elbows out too wide",
                "Not getting full range of motion",
                "Arching back excessively"
            ],
            "pull": [
                "Using too much bicep, not enough back",
                "Jerking the weight instead of smooth movement",
                "Shrugging shoulders during the movement",
                "Not squeezing at peak contraction"
            ],
            "squat": [
                "Knees caving inward",
                "Rising on toes / heels coming up",
                "Rounding the lower back",
                "Not hitting proper depth"
            ],
            "hinge": [
                "Rounding the lower back",
                "Not pushing hips back far enough",
                "Bending knees too much (should be slight bend)",
                "Weight drifting away from body"
            ],
            "lateral": [
                "Using too much weight and swinging",
                "Shrugging traps instead of isolating delts",
                "Raising arms too high",
                "Not controlling the negative"
            ],
            "isolation_arm": [
                "Swinging the body for momentum",
                "Moving the upper arm/elbow",
                "Partial range of motion",
                "Going too heavy and losing form"
            ],
            "core": [
                "Using hip flexors instead of abs",
                "Pulling on the neck",
                "Holding breath",
                "Moving too fast"
            ],
            "calf": [
                "Bouncing at the bottom",
                "Not getting full stretch",
                "Bending knees during standing raises",
                "Using momentum"
            ],
            "cardio": [
                "Starting too fast without warm-up",
                "Poor posture/form",
                "Not staying hydrated",
                "Ignoring pain signals"
            ]
        }
        return mistakes.get(pattern, [
            "Using too much weight before mastering form",
            "Not controlling the movement",
            "Partial range of motion",
            "Using momentum"
        ])

    def add_custom_exercise(self, exercise_name: str, description: str = "") -> Tuple[bool, str, Optional[Dict]]:
        """
        Add a custom exercise to the database with inferred form tips.

        Returns:
            Tuple of (success, message, exercise_info)
        """
        # First check if it already exists in built-in database
        existing = get_exercise(exercise_name)
        if existing:
            return False, f"'{existing['name']}' already exists in the exercise database.", existing

        # Check if it exists in custom exercises
        custom = self.db.get_custom_exercise(exercise_name)
        if custom:
            return False, f"'{custom['name']}' already exists as a custom exercise.", custom

        # Infer properties
        inferred = self._infer_exercise_properties(exercise_name, description)

        # Format the name properly (title case)
        formatted_name = exercise_name.title()

        # Add to database
        result = self.db.add_custom_exercise(
            name=formatted_name,
            exercise_type=inferred["type"],
            primary_muscles=inferred["primary_muscles"],
            secondary_muscles=inferred["secondary_muscles"],
            equipment=["varies"],
            difficulty=inferred["difficulty"],
            form_tips=inferred["form_tips"],
            common_mistakes=inferred["common_mistakes"],
            description=description
        )

        if result == -1:
            return False, "Failed to add exercise (may already exist).", None

        # Create exercise info dict
        exercise_info = {
            "name": formatted_name,
            "type": inferred["type"],
            "primary_muscles": inferred["primary_muscles"],
            "secondary_muscles": inferred["secondary_muscles"],
            "equipment": ["varies"],
            "difficulty": inferred["difficulty"],
            "form_tips": inferred["form_tips"],
            "common_mistakes": inferred["common_mistakes"]
        }

        return True, f"Successfully added '{formatted_name}' to your exercise database!", exercise_info

    def get_exercise_info(self, exercise_name: str) -> Optional[Dict]:
        """
        Get exercise info from built-in database or custom exercises.
        """
        # First check built-in
        exercise = get_exercise(exercise_name)
        if exercise:
            return exercise

        # Then check custom
        custom = self.db.get_custom_exercise(exercise_name)
        if custom:
            return custom

        return None

    def get_exercise_with_recommendations(self, user_id: int, exercise_name: str) -> str:
        """
        Get exercise form tips AND progressive overload recommendations in one view.
        Used during workout logging.
        """
        exercise = self.get_exercise_info(exercise_name)

        if not exercise:
            # Offer to add as custom exercise
            return f"""
================================================================================
  EXERCISE NOT FOUND: {exercise_name}
================================================================================

This exercise isn't in our database yet.

To add it, use the 'add' command:
  add {exercise_name}

Or with a description:
  add {exercise_name} | targets the upper back with a wide grip

Once added, you'll see form tips and can track progressive overload!
================================================================================
"""

        # Build comprehensive display
        output = f"""
================================================================================
                    {exercise['name'].upper()}
================================================================================

TYPE: {exercise['type'].replace('_', ' ').title()}
PRIMARY MUSCLES: {', '.join(m.replace('_', ' ').title() for m in exercise.get('primary_muscles', []))}
SECONDARY: {', '.join(m.replace('_', ' ').title() for m in exercise.get('secondary_muscles', [])) or 'None'}

"""
        # Form tips
        tips = exercise.get("form_tips", [])
        if tips:
            output += "PROPER FORM:\n"
            for i, tip in enumerate(tips, 1):
                output += f"  {i}. {tip}\n"
            output += "\n"

        # Common mistakes
        mistakes = exercise.get("common_mistakes", [])
        if mistakes:
            output += "AVOID THESE MISTAKES:\n"
            for mistake in mistakes:
                output += f"  - {mistake}\n"
            output += "\n"

        # Progressive overload recommendation
        output += "-" * 60 + "\n"
        output += "RECOMMENDED WEIGHT/REPS FOR TODAY:\n"
        output += "-" * 60 + "\n"

        # Get history
        history = self.db.get_exercise_history_detailed(user_id, exercise['name'], limit=3)
        last_performance = self.db.get_last_exercise_weight(user_id, exercise['name'])

        if not last_performance:
            output += """
  FIRST TIME DOING THIS EXERCISE!

  Recommended Starting Approach:
  - Start with a light weight you can easily control
  - Focus on form for your first 2-3 sets
  - Find a weight where you can do 8-12 reps with good form
  - Log this session as your baseline for next time

"""
        else:
            last_weight, last_reps = last_performance

            # Calculate recommendations
            weight_increase = 2.5 if last_weight < 50 else 5

            output += f"""
  YOUR LAST SESSION: {last_weight} kg x {last_reps} reps

  TODAY'S PROGRESSIVE OVERLOAD OPTIONS:
  +-----------------------------------------------------------------+
  | OPTION 1 (Add Reps):    {last_weight:>6.1f} kg x {last_reps + 1:>2} reps              |
  |   -> Same weight, 1 more rep per set                            |
  |                                                                 |
  | OPTION 2 (Add Weight):  {last_weight + weight_increase:>6.1f} kg x {last_reps:>2} reps              |
  |   -> Increase weight by {weight_increase}kg, same reps                      |
  |                                                                 |
  | OPTION 3 (Add Sets):    {last_weight:>6.1f} kg x {last_reps:>2} reps + 1 set       |
  |   -> Same weight/reps, add an extra set                         |
  +-----------------------------------------------------------------+

"""
            # Show recent history
            if history:
                output += "  RECENT HISTORY:\n"
                for h in history[:3]:
                    output += f"    {h['date']}: {h['sets']} sets x {h['reps']} reps @ {h['weight_kg']} kg\n"
                output += "\n"

        output += "=" * 80
        return output

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
