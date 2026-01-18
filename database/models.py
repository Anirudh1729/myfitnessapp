"""Database models for the fitness app."""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List


@dataclass
class User:
    """User profile and measurements."""
    id: Optional[int] = None
    name: str = ""
    age: int = 0
    gender: str = ""  # 'male' or 'female'
    height_cm: float = 0.0
    weight_kg: float = 0.0
    goal: str = "jacked_model"  # 'jacked_model', 'lean', 'bulk', 'maintain'
    activity_level: str = "moderate"  # 'sedentary', 'light', 'moderate', 'active', 'very_active'
    experience_level: str = "beginner"  # 'beginner', 'intermediate', 'advanced'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Workout:
    """A workout session."""
    id: Optional[int] = None
    user_id: int = 0
    workout_type: str = ""  # 'weight_lifting', 'cardio', 'mixed'
    date: Optional[date] = None
    duration_minutes: int = 0
    notes: str = ""
    created_at: Optional[datetime] = None


@dataclass
class WorkoutExercise:
    """An exercise performed during a workout."""
    id: Optional[int] = None
    workout_id: int = 0
    exercise_name: str = ""
    exercise_type: str = ""  # 'compound', 'isolation', 'cardio'
    sets: int = 0
    reps: int = 0
    weight_kg: float = 0.0
    duration_minutes: int = 0  # For cardio
    distance_km: float = 0.0  # For cardio
    calories_burned: int = 0
    notes: str = ""


@dataclass
class FoodEntry:
    """A food entry for tracking nutrition."""
    id: Optional[int] = None
    user_id: int = 0
    date: Optional[date] = None
    meal_type: str = ""  # 'breakfast', 'lunch', 'dinner', 'snack'
    dish_name: str = ""
    is_homemade: bool = True
    estimated_calories: int = 0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0
    notes: str = ""
    created_at: Optional[datetime] = None


@dataclass
class WeeklyGoal:
    """Weekly goals and progress tracking."""
    id: Optional[int] = None
    user_id: int = 0
    week_start: Optional[date] = None
    target_weight_kg: float = 0.0
    actual_weight_kg: Optional[float] = None
    target_calories_daily: int = 0
    target_workouts: int = 0
    completed_workouts: int = 0
    notes: str = ""


@dataclass
class WeightLog:
    """Daily weight measurements."""
    id: Optional[int] = None
    user_id: int = 0
    date: Optional[date] = None
    weight_kg: float = 0.0
    notes: str = ""


@dataclass
class ExerciseProgress:
    """Track progressive overload for exercises."""
    id: Optional[int] = None
    user_id: int = 0
    exercise_name: str = ""
    date: Optional[date] = None
    max_weight_kg: float = 0.0
    max_reps: int = 0
    estimated_1rm: float = 0.0  # Estimated one-rep max
