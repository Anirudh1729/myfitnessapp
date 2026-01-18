"""Workout planning service with rest days and progressive overload."""

from datetime import date, timedelta
from typing import Dict, List, Optional
from database import Database


# Workout split templates
WORKOUT_SPLITS = {
    "push_pull_legs": {
        "name": "Push/Pull/Legs (PPL)",
        "description": "Classic 6-day split focusing on movement patterns",
        "days_per_week": 6,
        "schedule": {
            "Day 1": {
                "name": "Push",
                "muscles": ["Chest", "Shoulders", "Triceps"],
                "exercises": [
                    ("Bench Press", "compound", "3-4 sets x 6-8 reps"),
                    ("Overhead Press", "compound", "3 sets x 8-10 reps"),
                    ("Incline Dumbbell Press", "compound", "3 sets x 8-12 reps"),
                    ("Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Tricep Pushdown", "isolation", "3 sets x 10-12 reps"),
                    ("Overhead Tricep Extension", "isolation", "2 sets x 12-15 reps")
                ]
            },
            "Day 2": {
                "name": "Pull",
                "muscles": ["Back", "Biceps", "Rear Delts"],
                "exercises": [
                    ("Deadlift", "compound", "3-4 sets x 5-6 reps"),
                    ("Pull-Up", "compound", "3 sets x 6-10 reps"),
                    ("Barbell Row", "compound", "3 sets x 8-10 reps"),
                    ("Face Pull", "isolation", "3 sets x 15-20 reps"),
                    ("Barbell Curl", "isolation", "3 sets x 8-12 reps"),
                    ("Hammer Curl", "isolation", "2 sets x 10-12 reps")
                ]
            },
            "Day 3": {
                "name": "Legs",
                "muscles": ["Quadriceps", "Hamstrings", "Glutes", "Calves"],
                "exercises": [
                    ("Squat", "compound", "4 sets x 6-8 reps"),
                    ("Romanian Deadlift", "compound", "3 sets x 8-10 reps"),
                    ("Leg Press", "compound", "3 sets x 10-12 reps"),
                    ("Leg Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Leg Extension", "isolation", "3 sets x 12-15 reps"),
                    ("Calf Raise", "isolation", "4 sets x 12-15 reps")
                ]
            },
            "Day 4": {
                "name": "Push",
                "muscles": ["Chest", "Shoulders", "Triceps"],
                "exercises": [
                    ("Incline Bench Press", "compound", "3-4 sets x 6-8 reps"),
                    ("Dumbbell Bench Press", "compound", "3 sets x 8-12 reps"),
                    ("Dumbbell Shoulder Press", "compound", "3 sets x 8-10 reps"),
                    ("Cable Fly", "isolation", "3 sets x 12-15 reps"),
                    ("Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Skull Crusher", "isolation", "3 sets x 10-12 reps")
                ]
            },
            "Day 5": {
                "name": "Pull",
                "muscles": ["Back", "Biceps", "Rear Delts"],
                "exercises": [
                    ("Barbell Row", "compound", "4 sets x 6-8 reps"),
                    ("Lat Pulldown", "compound", "3 sets x 8-12 reps"),
                    ("Seated Cable Row", "compound", "3 sets x 10-12 reps"),
                    ("Rear Delt Fly", "isolation", "3 sets x 12-15 reps"),
                    ("Dumbbell Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Preacher Curl", "isolation", "2 sets x 12-15 reps")
                ]
            },
            "Day 6": {
                "name": "Legs",
                "muscles": ["Quadriceps", "Hamstrings", "Glutes", "Calves"],
                "exercises": [
                    ("Front Squat", "compound", "3 sets x 6-8 reps"),
                    ("Romanian Deadlift", "compound", "3 sets x 8-10 reps"),
                    ("Lunges", "compound", "3 sets x 10-12 each leg"),
                    ("Leg Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Leg Extension", "isolation", "3 sets x 12-15 reps"),
                    ("Seated Calf Raise", "isolation", "4 sets x 15-20 reps")
                ]
            },
            "Day 7": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            }
        }
    },
    "upper_lower": {
        "name": "Upper/Lower Split",
        "description": "4-day split alternating upper and lower body",
        "days_per_week": 4,
        "schedule": {
            "Day 1": {
                "name": "Upper A (Strength)",
                "muscles": ["Chest", "Back", "Shoulders", "Arms"],
                "exercises": [
                    ("Bench Press", "compound", "4 sets x 5-6 reps"),
                    ("Barbell Row", "compound", "4 sets x 5-6 reps"),
                    ("Overhead Press", "compound", "3 sets x 6-8 reps"),
                    ("Pull-Up", "compound", "3 sets x 6-10 reps"),
                    ("Barbell Curl", "isolation", "3 sets x 8-10 reps"),
                    ("Skull Crusher", "isolation", "3 sets x 8-10 reps")
                ]
            },
            "Day 2": {
                "name": "Lower A (Strength)",
                "muscles": ["Quadriceps", "Hamstrings", "Glutes"],
                "exercises": [
                    ("Squat", "compound", "4 sets x 5-6 reps"),
                    ("Romanian Deadlift", "compound", "4 sets x 6-8 reps"),
                    ("Leg Press", "compound", "3 sets x 8-10 reps"),
                    ("Leg Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Calf Raise", "isolation", "4 sets x 10-12 reps")
                ]
            },
            "Day 3": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            },
            "Day 4": {
                "name": "Upper B (Hypertrophy)",
                "muscles": ["Chest", "Back", "Shoulders", "Arms"],
                "exercises": [
                    ("Incline Dumbbell Press", "compound", "4 sets x 8-12 reps"),
                    ("Lat Pulldown", "compound", "4 sets x 8-12 reps"),
                    ("Dumbbell Shoulder Press", "compound", "3 sets x 10-12 reps"),
                    ("Cable Row", "compound", "3 sets x 10-12 reps"),
                    ("Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Face Pull", "isolation", "3 sets x 15-20 reps"),
                    ("Dumbbell Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Tricep Pushdown", "isolation", "3 sets x 10-12 reps")
                ]
            },
            "Day 5": {
                "name": "Lower B (Hypertrophy)",
                "muscles": ["Quadriceps", "Hamstrings", "Glutes"],
                "exercises": [
                    ("Leg Press", "compound", "4 sets x 10-12 reps"),
                    ("Romanian Deadlift", "compound", "3 sets x 10-12 reps"),
                    ("Lunges", "compound", "3 sets x 10-12 each leg"),
                    ("Leg Extension", "isolation", "3 sets x 12-15 reps"),
                    ("Leg Curl", "isolation", "3 sets x 12-15 reps"),
                    ("Calf Raise", "isolation", "4 sets x 15-20 reps")
                ]
            },
            "Day 6": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            },
            "Day 7": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            }
        }
    },
    "full_body": {
        "name": "Full Body",
        "description": "3-day full body routine, great for beginners",
        "days_per_week": 3,
        "schedule": {
            "Day 1": {
                "name": "Full Body A",
                "muscles": ["All Major Muscle Groups"],
                "exercises": [
                    ("Squat", "compound", "3 sets x 6-8 reps"),
                    ("Bench Press", "compound", "3 sets x 6-8 reps"),
                    ("Barbell Row", "compound", "3 sets x 6-8 reps"),
                    ("Overhead Press", "compound", "3 sets x 8-10 reps"),
                    ("Romanian Deadlift", "compound", "3 sets x 8-10 reps"),
                    ("Plank", "isolation", "3 sets x 30-60 sec")
                ]
            },
            "Day 2": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            },
            "Day 3": {
                "name": "Full Body B",
                "muscles": ["All Major Muscle Groups"],
                "exercises": [
                    ("Deadlift", "compound", "3 sets x 5 reps"),
                    ("Incline Dumbbell Press", "compound", "3 sets x 8-10 reps"),
                    ("Pull-Up", "compound", "3 sets x AMRAP"),
                    ("Dumbbell Shoulder Press", "compound", "3 sets x 8-10 reps"),
                    ("Leg Press", "compound", "3 sets x 10-12 reps"),
                    ("Face Pull", "isolation", "3 sets x 15-20 reps")
                ]
            },
            "Day 4": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            },
            "Day 5": {
                "name": "Full Body C",
                "muscles": ["All Major Muscle Groups"],
                "exercises": [
                    ("Front Squat", "compound", "3 sets x 8-10 reps"),
                    ("Dumbbell Bench Press", "compound", "3 sets x 8-10 reps"),
                    ("Seated Cable Row", "compound", "3 sets x 10-12 reps"),
                    ("Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Lunges", "compound", "3 sets x 10-12 each"),
                    ("Barbell Curl", "isolation", "2 sets x 10-12 reps"),
                    ("Tricep Pushdown", "isolation", "2 sets x 10-12 reps")
                ]
            },
            "Day 6": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            },
            "Day 7": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            }
        }
    },
    "bro_split": {
        "name": "Bro Split",
        "description": "5-day split with one muscle group per day",
        "days_per_week": 5,
        "schedule": {
            "Day 1": {
                "name": "Chest",
                "muscles": ["Chest"],
                "exercises": [
                    ("Bench Press", "compound", "4 sets x 6-8 reps"),
                    ("Incline Dumbbell Press", "compound", "3 sets x 8-10 reps"),
                    ("Dips", "compound", "3 sets x 8-12 reps"),
                    ("Cable Fly", "isolation", "3 sets x 12-15 reps"),
                    ("Push-Up", "compound", "2 sets x AMRAP")
                ]
            },
            "Day 2": {
                "name": "Back",
                "muscles": ["Back"],
                "exercises": [
                    ("Deadlift", "compound", "4 sets x 5 reps"),
                    ("Pull-Up", "compound", "4 sets x 6-10 reps"),
                    ("Barbell Row", "compound", "3 sets x 8-10 reps"),
                    ("Lat Pulldown", "compound", "3 sets x 10-12 reps"),
                    ("Seated Cable Row", "compound", "3 sets x 10-12 reps")
                ]
            },
            "Day 3": {
                "name": "Shoulders",
                "muscles": ["Shoulders"],
                "exercises": [
                    ("Overhead Press", "compound", "4 sets x 6-8 reps"),
                    ("Dumbbell Shoulder Press", "compound", "3 sets x 8-10 reps"),
                    ("Lateral Raise", "isolation", "4 sets x 12-15 reps"),
                    ("Face Pull", "isolation", "3 sets x 15-20 reps"),
                    ("Rear Delt Fly", "isolation", "3 sets x 12-15 reps")
                ]
            },
            "Day 4": {
                "name": "Legs",
                "muscles": ["Legs"],
                "exercises": [
                    ("Squat", "compound", "4 sets x 6-8 reps"),
                    ("Romanian Deadlift", "compound", "3 sets x 8-10 reps"),
                    ("Leg Press", "compound", "3 sets x 10-12 reps"),
                    ("Leg Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Leg Extension", "isolation", "3 sets x 12-15 reps"),
                    ("Calf Raise", "isolation", "4 sets x 12-15 reps")
                ]
            },
            "Day 5": {
                "name": "Arms",
                "muscles": ["Biceps", "Triceps"],
                "exercises": [
                    ("Barbell Curl", "isolation", "4 sets x 8-10 reps"),
                    ("Skull Crusher", "isolation", "4 sets x 8-10 reps"),
                    ("Hammer Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Tricep Pushdown", "isolation", "3 sets x 10-12 reps"),
                    ("Dumbbell Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Overhead Tricep Extension", "isolation", "3 sets x 10-12 reps")
                ]
            },
            "Day 6": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            },
            "Day 7": {
                "name": "Rest",
                "muscles": [],
                "exercises": []
            }
        }
    },
    "ppls_shoulder_focus": {
        "name": "Push/Pull/Legs/Shoulders (PPLS)",
        "description": "6-day split with dedicated shoulder day. 25 sets/workout, 16 sets/muscle/week. Extra shoulder emphasis.",
        "days_per_week": 6,
        "volume_info": {
            "sets_per_workout": 25,
            "weekly_volume": {
                "chest": 16,
                "back": 16,
                "side_delts": 22,
                "front_delts": 16,
                "rear_delts": 18,
                "biceps": 16,
                "triceps": 16,
                "quads": 10,
                "hamstrings": 8,
                "calves": 4
            }
        },
        "schedule": {
            "Day 1": {
                "name": "Push A (Chest Focus)",
                "muscles": ["Chest", "Triceps", "Side Delts", "Front Delts"],
                "total_sets": 25,
                "exercises": [
                    ("Bench Press", "compound", "4 sets x 6-8 reps"),
                    ("Incline Dumbbell Press", "compound", "3 sets x 8-10 reps"),
                    ("Cable Fly", "isolation", "3 sets x 12-15 reps"),
                    ("Skull Crusher", "compound", "3 sets x 8-10 reps"),
                    ("Tricep Pushdown", "isolation", "3 sets x 10-12 reps"),
                    ("Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Cable Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Front Raise", "isolation", "3 sets x 12-15 reps")
                ]
            },
            "Day 2": {
                "name": "Pull A",
                "muscles": ["Back", "Lats", "Biceps", "Rear Delts", "Traps"],
                "total_sets": 25,
                "exercises": [
                    ("Deadlift", "compound", "4 sets x 5 reps"),
                    ("Barbell Row", "compound", "3 sets x 8-10 reps"),
                    ("Lat Pulldown", "compound", "3 sets x 10-12 reps"),
                    ("Barbell Curl", "isolation", "3 sets x 8-10 reps"),
                    ("Hammer Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Face Pull", "isolation", "3 sets x 15-20 reps"),
                    ("Rear Delt Fly", "isolation", "3 sets x 12-15 reps"),
                    ("Shrugs", "isolation", "3 sets x 10-12 reps")
                ]
            },
            "Day 3": {
                "name": "Legs",
                "muscles": ["Quads", "Hamstrings", "Glutes", "Calves"],
                "total_sets": 25,
                "exercises": [
                    ("Squat", "compound", "4 sets x 6-8 reps"),
                    ("Leg Press", "compound", "3 sets x 10-12 reps"),
                    ("Leg Extension", "isolation", "3 sets x 12-15 reps"),
                    ("Romanian Deadlift", "compound", "4 sets x 8-10 reps"),
                    ("Leg Curl", "isolation", "4 sets x 10-12 reps"),
                    ("Standing Calf Raise", "isolation", "2 sets x 12-15 reps"),
                    ("Seated Calf Raise", "isolation", "2 sets x 15-20 reps"),
                    ("Hip Thrust", "compound", "3 sets x 10-12 reps")
                ]
            },
            "Day 4": {
                "name": "Shoulders (Emphasis Day)",
                "muscles": ["Side Delts", "Front Delts", "Rear Delts", "Traps"],
                "total_sets": 25,
                "exercises": [
                    ("Overhead Press", "compound", "4 sets x 6-8 reps"),
                    ("Arnold Press", "compound", "2 sets x 10-12 reps"),
                    ("Lateral Raise", "isolation", "4 sets x 12-15 reps"),
                    ("Cable Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Machine Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Face Pull", "isolation", "3 sets x 15-20 reps"),
                    ("Rear Delt Fly", "isolation", "3 sets x 12-15 reps"),
                    ("Shrugs", "isolation", "3 sets x 10-12 reps")
                ]
            },
            "Day 5": {
                "name": "Push B (Tricep Focus)",
                "muscles": ["Chest", "Triceps", "Side Delts", "Front Delts"],
                "total_sets": 25,
                "exercises": [
                    ("Incline Bench Press", "compound", "3 sets x 6-8 reps"),
                    ("Dumbbell Bench Press", "compound", "3 sets x 8-10 reps"),
                    ("Close Grip Bench Press", "compound", "4 sets x 8-10 reps"),
                    ("Skull Crusher", "isolation", "3 sets x 10-12 reps"),
                    ("Overhead Tricep Extension", "isolation", "3 sets x 10-12 reps"),
                    ("Lateral Raise", "isolation", "3 sets x 12-15 reps"),
                    ("Upright Row", "compound", "3 sets x 10-12 reps"),
                    ("Front Raise", "isolation", "3 sets x 12-15 reps")
                ]
            },
            "Day 6": {
                "name": "Pull B",
                "muscles": ["Back", "Lats", "Biceps", "Rear Delts", "Traps"],
                "total_sets": 25,
                "exercises": [
                    ("Pull-Up", "compound", "3 sets x 6-10 reps"),
                    ("Seated Cable Row", "compound", "3 sets x 10-12 reps"),
                    ("Dumbbell Curl", "isolation", "4 sets x 8-10 reps"),
                    ("Preacher Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Incline Dumbbell Curl", "isolation", "3 sets x 10-12 reps"),
                    ("Face Pull", "isolation", "3 sets x 15-20 reps"),
                    ("Reverse Pec Deck", "isolation", "3 sets x 12-15 reps"),
                    ("Shrugs", "isolation", "3 sets x 10-12 reps")
                ]
            },
            "Day 7": {
                "name": "Rest",
                "muscles": [],
                "total_sets": 0,
                "exercises": []
            }
        }
    }
}


class PlannerService:
    """Handle workout planning and scheduling."""

    def __init__(self, db: Database):
        self.db = db

    def get_recommended_split(self, experience_level: str, days_available: int = None) -> str:
        """Get recommended workout split based on experience."""
        if experience_level == "beginner":
            return "full_body"
        elif experience_level == "intermediate":
            return "upper_lower"
        else:  # advanced
            return "push_pull_legs"

    def get_available_splits(self) -> str:
        """Get formatted list of available workout splits."""
        output = """
================================================================================
                         WORKOUT SPLIT OPTIONS
================================================================================

"""
        for i, (key, split) in enumerate(WORKOUT_SPLITS.items(), 1):
            output += f"  [{i}] {split['name']}\n"
            output += f"      {split['description']}\n"
            output += f"      Training Days: {split['days_per_week']}/week\n\n"

        output += "=" * 80
        return output

    def get_workout_plan(self, split_name: str) -> str:
        """Get detailed workout plan for a split."""
        if split_name not in WORKOUT_SPLITS:
            # Try to find by number
            splits_list = list(WORKOUT_SPLITS.keys())
            try:
                index = int(split_name) - 1
                if 0 <= index < len(splits_list):
                    split_name = splits_list[index]
                else:
                    return f"\nInvalid split selection. Please choose 1-{len(splits_list)}.\n"
            except ValueError:
                return f"\nSplit '{split_name}' not found.\n"

        split = WORKOUT_SPLITS[split_name]

        output = f"""
================================================================================
                    {split['name'].upper()} WORKOUT PLAN
================================================================================

{split['description']}
Training Days: {split['days_per_week']}/week

"""
        # Show volume info if available
        if 'volume_info' in split:
            vol = split['volume_info']
            output += f"Sets per Workout: {vol['sets_per_workout']}\n\n"
            output += "WEEKLY VOLUME BY MUSCLE GROUP:\n"
            output += "-" * 40 + "\n"
            for muscle, sets in vol['weekly_volume'].items():
                muscle_name = muscle.replace('_', ' ').title()
                output += f"  {muscle_name:<15} {sets} sets\n"
            output += "-" * 40 + "\n"

        for day_key, day_data in split['schedule'].items():
            total_sets = day_data.get('total_sets', '')
            sets_str = f" ({total_sets} sets)" if total_sets else ""
            output += f"\n{day_key}: {day_data['name']}{sets_str}\n"
            output += "-" * 40 + "\n"

            if day_data['muscles']:
                output += f"  Target: {', '.join(day_data['muscles'])}\n\n"

            if day_data['exercises']:
                for exercise, ex_type, rep_scheme in day_data['exercises']:
                    type_indicator = "[C]" if ex_type == "compound" else "[I]"
                    output += f"  {type_indicator} {exercise}: {rep_scheme}\n"
            else:
                output += "  Rest and Recovery\n"
                output += "  - Light stretching or mobility work\n"
                output += "  - Active recovery (walk, light swimming)\n"
                output += "  - Focus on sleep and nutrition\n"

        output += "\n" + "=" * 80
        output += "\n[C] = Compound exercise  [I] = Isolation exercise\n"
        return output

    def get_todays_workout(self, user_id: int, split_name: str = None) -> str:
        """Get the workout scheduled for today."""
        user = self.db.get_user(user_id)
        if not user:
            return "\nUser not found.\n"

        # Use user's experience level to determine default split
        if split_name is None:
            split_name = self.get_recommended_split(user.experience_level)

        split = WORKOUT_SPLITS.get(split_name)
        if not split:
            return f"\nSplit '{split_name}' not found.\n"

        # Determine which day of the program we're on
        # Simple approach: use day of week modulo schedule length
        today = date.today()
        day_of_week = today.weekday()  # 0 = Monday

        # Map to schedule
        schedule_keys = list(split['schedule'].keys())
        day_index = day_of_week % len(schedule_keys)
        day_key = schedule_keys[day_index]
        day_data = split['schedule'][day_key]

        day_name = today.strftime("%A, %B %d")

        output = f"""
================================================================================
                    TODAY'S WORKOUT - {day_name}
================================================================================

Program: {split['name']}
Today: {day_data['name']}
"""
        if day_data['muscles']:
            output += f"Target Muscles: {', '.join(day_data['muscles'])}\n"

        output += "\n" + "-" * 60 + "\n"

        if day_data['exercises']:
            output += "\nEXERCISES:\n\n"
            for i, (exercise, ex_type, rep_scheme) in enumerate(day_data['exercises'], 1):
                output += f"  {i}. {exercise}\n"
                output += f"     {rep_scheme}\n"

                # Check for progressive overload opportunity
                last_perf = self.db.get_last_exercise_weight(user_id, exercise)
                if last_perf:
                    last_weight, last_reps = last_perf
                    output += f"     Last: {last_weight}kg x {last_reps} reps\n"
                output += "\n"
        else:
            output += """
  REST DAY

  Recovery Tips:
  - Get 7-9 hours of quality sleep
  - Stay hydrated (aim for 3+ liters of water)
  - Light stretching or foam rolling
  - Active recovery: walk, swim, or yoga
  - Focus on hitting your protein target

"""

        output += "-" * 60 + "\n"

        # Add workout tips based on experience
        if day_data['exercises']:
            if user.experience_level == "beginner":
                output += """
TIPS FOR TODAY:
- Focus on form over weight - quality reps matter most
- Rest 2-3 minutes between compound exercises
- Rest 1-2 minutes between isolation exercises
- If unsure about form, use lighter weight
"""
            elif user.experience_level == "intermediate":
                output += """
TIPS FOR TODAY:
- Aim to beat your previous performance (progressive overload)
- Rest 2-3 minutes for heavy compounds, 60-90 sec for isolations
- Focus on mind-muscle connection
- Track your weights and reps
"""
            else:
                output += """
TIPS FOR TODAY:
- Push for progressive overload where possible
- Consider intensity techniques on final sets
- Listen to your body - adjust volume if needed
- Prioritize compound movements early in workout
"""

        output += "\n" + "=" * 80
        return output

    def get_weekly_schedule(self, split_name: str = None, experience_level: str = "intermediate") -> str:
        """Get the weekly workout schedule."""
        if split_name is None:
            split_name = self.get_recommended_split(experience_level)

        split = WORKOUT_SPLITS.get(split_name)
        if not split:
            return f"\nSplit '{split_name}' not found.\n"

        today = date.today()
        monday = today - timedelta(days=today.weekday())

        output = f"""
================================================================================
                    WEEKLY SCHEDULE - {split['name']}
================================================================================

"""
        schedule_keys = list(split['schedule'].keys())

        for i in range(7):
            current_date = monday + timedelta(days=i)
            day_name = current_date.strftime("%A")
            date_str = current_date.strftime("%m/%d")

            # Get workout for this day
            day_index = i % len(schedule_keys)
            day_data = split['schedule'][schedule_keys[day_index]]

            is_today = current_date == today
            marker = " <-- TODAY" if is_today else ""

            if day_data['exercises']:
                output += f"  {day_name:<10} ({date_str}): {day_data['name']}{marker}\n"
                muscles = ', '.join(day_data['muscles']) if day_data['muscles'] else ""
                if muscles:
                    output += f"               {muscles}\n"
            else:
                output += f"  {day_name:<10} ({date_str}): REST{marker}\n"

        output += """
--------------------------------------------------------------------------------

PROGRESSIVE OVERLOAD GUIDELINES:
  - Add 2.5kg to upper body exercises every 1-2 weeks
  - Add 5kg to lower body exercises every 1-2 weeks
  - If you can't complete all reps, stay at current weight
  - Deload (reduce weight by 10%) every 4-6 weeks

"""
        output += "=" * 80
        return output

    def get_rest_day_advice(self) -> str:
        """Get advice for rest days."""
        return """
================================================================================
                         REST DAY GUIDE
================================================================================

REST IS WHEN YOU GROW!

Your muscles repair and grow during rest, not during training. Rest days are
essential for:
  - Muscle protein synthesis (building muscle)
  - Nervous system recovery
  - Injury prevention
  - Maintaining workout intensity

ACTIVE RECOVERY OPTIONS:
  - Light walking (20-30 minutes)
  - Swimming
  - Yoga or stretching
  - Foam rolling
  - Light cycling

WHAT TO FOCUS ON:

  1. SLEEP (Most Important!)
     - Aim for 7-9 hours
     - Keep consistent sleep schedule
     - Avoid screens 1 hour before bed

  2. NUTRITION
     - Still hit your protein target (don't reduce on rest days)
     - Stay hydrated
     - Eat quality whole foods

  3. MOBILITY
     - Stretch tight muscle groups
     - Work on problem areas
     - Foam roll for 10-15 minutes

  4. MENTAL RECOVERY
     - Reduce stress where possible
     - Practice relaxation techniques
     - Don't overthink training

SIGNS YOU NEED MORE REST:
  - Persistent fatigue
  - Decreased performance
  - Mood changes
  - Poor sleep quality
  - Frequent injuries or illness

================================================================================
"""

    def get_progressive_overload_guide(self) -> str:
        """Get guide on progressive overload."""
        return """
================================================================================
                    PROGRESSIVE OVERLOAD GUIDE
================================================================================

Progressive overload is THE key to building muscle and strength. It means
gradually increasing the demands on your muscles over time.

METHODS OF PROGRESSIVE OVERLOAD:

  1. INCREASE WEIGHT (Primary Method)
     - Add 2.5kg for upper body exercises
     - Add 5kg for lower body exercises
     - Only increase when you can complete all sets with good form

  2. INCREASE REPS
     - Stay at same weight
     - Add 1-2 reps per set
     - When you hit top of rep range, increase weight

  3. INCREASE SETS
     - Add an extra set to exercises
     - Keep weight and reps the same
     - Good for intermediate/advanced lifters

  4. INCREASE FREQUENCY
     - Train muscle groups more often
     - Ensure adequate recovery
     - Works best with lower volume per session

  5. DECREASE REST TIME
     - Same weight, reps, sets
     - Less rest between sets
     - Increases workout density

WEEKLY PROGRESSION EXAMPLE:

  Week 1: Bench Press 60kg x 3 sets x 8 reps
  Week 2: Bench Press 60kg x 3 sets x 9 reps
  Week 3: Bench Press 60kg x 3 sets x 10 reps
  Week 4: Bench Press 62.5kg x 3 sets x 8 reps (Increased weight!)
  Week 5: Bench Press 62.5kg x 3 sets x 9 reps
  ...and so on

WHEN TO DELOAD:

  - Every 4-6 weeks, reduce volume/weight by 40-50%
  - If progress stalls for 2+ weeks
  - If feeling overly fatigued or sore
  - After particularly intense training blocks

TRACKING IS KEY:
  Log every workout! You can't improve what you don't measure.

================================================================================
"""
