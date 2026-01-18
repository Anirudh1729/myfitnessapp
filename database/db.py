"""Database connection and operations."""

import sqlite3
import os
from datetime import datetime, date
from typing import Optional, List
from .models import User, Workout, WorkoutExercise, FoodEntry, WeeklyGoal, WeightLog, ExerciseProgress


class Database:
    """SQLite database handler for the fitness app."""

    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to user's home directory
            home = os.path.expanduser("~")
            db_dir = os.path.join(home, ".myfitnessapp")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "fitness.db")

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                height_cm REAL,
                weight_kg REAL,
                goal TEXT DEFAULT 'jacked_model',
                activity_level TEXT DEFAULT 'moderate',
                experience_level TEXT DEFAULT 'beginner',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Workouts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                workout_type TEXT NOT NULL,
                date DATE NOT NULL,
                duration_minutes INTEGER DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Workout exercises table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER NOT NULL,
                exercise_name TEXT NOT NULL,
                exercise_type TEXT,
                sets INTEGER DEFAULT 0,
                reps INTEGER DEFAULT 0,
                weight_kg REAL DEFAULT 0,
                duration_minutes INTEGER DEFAULT 0,
                distance_km REAL DEFAULT 0,
                calories_burned INTEGER DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (workout_id) REFERENCES workouts(id)
            )
        ''')

        # Food entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                meal_type TEXT,
                dish_name TEXT NOT NULL,
                is_homemade INTEGER DEFAULT 1,
                estimated_calories INTEGER DEFAULT 0,
                protein_g REAL DEFAULT 0,
                carbs_g REAL DEFAULT 0,
                fat_g REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Weekly goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                week_start DATE NOT NULL,
                target_weight_kg REAL,
                actual_weight_kg REAL,
                target_calories_daily INTEGER,
                target_workouts INTEGER DEFAULT 4,
                completed_workouts INTEGER DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Weight log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weight_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                weight_kg REAL NOT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Exercise progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercise_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exercise_name TEXT NOT NULL,
                date DATE NOT NULL,
                max_weight_kg REAL,
                max_reps INTEGER,
                estimated_1rm REAL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Custom exercises table (user-added exercises)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                exercise_type TEXT DEFAULT 'compound',
                primary_muscles TEXT,
                secondary_muscles TEXT,
                equipment TEXT,
                difficulty TEXT DEFAULT 'intermediate',
                form_tips TEXT,
                common_mistakes TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()

    # User operations
    def create_user(self, user: User) -> int:
        """Create a new user and return their ID."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, age, gender, height_cm, weight_kg, goal, activity_level, experience_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.name, user.age, user.gender, user.height_cm, user.weight_kg,
              user.goal, user.activity_level, user.experience_level))
        self.conn.commit()
        return cursor.lastrowid

    def get_user(self, user_id: int = None) -> Optional[User]:
        """Get a user by ID, or the first user if no ID provided."""
        cursor = self.conn.cursor()
        if user_id:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        else:
            cursor.execute('SELECT * FROM users ORDER BY id LIMIT 1')
        row = cursor.fetchone()
        if row:
            return User(
                id=row['id'],
                name=row['name'],
                age=row['age'],
                gender=row['gender'],
                height_cm=row['height_cm'],
                weight_kg=row['weight_kg'],
                goal=row['goal'],
                activity_level=row['activity_level'],
                experience_level=row['experience_level'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        return None

    def update_user(self, user: User):
        """Update user information."""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users SET name=?, age=?, gender=?, height_cm=?, weight_kg=?,
            goal=?, activity_level=?, experience_level=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (user.name, user.age, user.gender, user.height_cm, user.weight_kg,
              user.goal, user.activity_level, user.experience_level, user.id))
        self.conn.commit()

    # Workout operations
    def create_workout(self, workout: Workout) -> int:
        """Create a new workout and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO workouts (user_id, workout_type, date, duration_minutes, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (workout.user_id, workout.workout_type, workout.date or date.today(),
              workout.duration_minutes, workout.notes))
        self.conn.commit()
        return cursor.lastrowid

    def add_exercise_to_workout(self, exercise: WorkoutExercise) -> int:
        """Add an exercise to a workout."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO workout_exercises (workout_id, exercise_name, exercise_type, sets, reps,
            weight_kg, duration_minutes, distance_km, calories_burned, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (exercise.workout_id, exercise.exercise_name, exercise.exercise_type,
              exercise.sets, exercise.reps, exercise.weight_kg, exercise.duration_minutes,
              exercise.distance_km, exercise.calories_burned, exercise.notes))
        self.conn.commit()
        return cursor.lastrowid

    def get_workouts(self, user_id: int, start_date: date = None, end_date: date = None) -> List[Workout]:
        """Get workouts for a user within a date range."""
        cursor = self.conn.cursor()
        query = 'SELECT * FROM workouts WHERE user_id = ?'
        params = [user_id]

        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)

        query += ' ORDER BY date DESC'
        cursor.execute(query, params)

        workouts = []
        for row in cursor.fetchall():
            workouts.append(Workout(
                id=row['id'],
                user_id=row['user_id'],
                workout_type=row['workout_type'],
                date=row['date'],
                duration_minutes=row['duration_minutes'],
                notes=row['notes'],
                created_at=row['created_at']
            ))
        return workouts

    def get_workout_exercises(self, workout_id: int) -> List[WorkoutExercise]:
        """Get all exercises for a workout."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM workout_exercises WHERE workout_id = ?', (workout_id,))

        exercises = []
        for row in cursor.fetchall():
            exercises.append(WorkoutExercise(
                id=row['id'],
                workout_id=row['workout_id'],
                exercise_name=row['exercise_name'],
                exercise_type=row['exercise_type'],
                sets=row['sets'],
                reps=row['reps'],
                weight_kg=row['weight_kg'],
                duration_minutes=row['duration_minutes'],
                distance_km=row['distance_km'],
                calories_burned=row['calories_burned'],
                notes=row['notes']
            ))
        return exercises

    # Food operations
    def add_food_entry(self, entry: FoodEntry) -> int:
        """Add a food entry."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO food_entries (user_id, date, meal_type, dish_name, is_homemade,
            estimated_calories, protein_g, carbs_g, fat_g, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entry.user_id, entry.date or date.today(), entry.meal_type, entry.dish_name,
              1 if entry.is_homemade else 0, entry.estimated_calories, entry.protein_g,
              entry.carbs_g, entry.fat_g, entry.notes))
        self.conn.commit()
        return cursor.lastrowid

    def get_food_entries(self, user_id: int, target_date: date = None) -> List[FoodEntry]:
        """Get food entries for a user on a specific date."""
        cursor = self.conn.cursor()
        if target_date:
            cursor.execute('SELECT * FROM food_entries WHERE user_id = ? AND date = ? ORDER BY created_at',
                          (user_id, target_date))
        else:
            cursor.execute('SELECT * FROM food_entries WHERE user_id = ? AND date = ? ORDER BY created_at',
                          (user_id, date.today()))

        entries = []
        for row in cursor.fetchall():
            entries.append(FoodEntry(
                id=row['id'],
                user_id=row['user_id'],
                date=row['date'],
                meal_type=row['meal_type'],
                dish_name=row['dish_name'],
                is_homemade=bool(row['is_homemade']),
                estimated_calories=row['estimated_calories'],
                protein_g=row['protein_g'],
                carbs_g=row['carbs_g'],
                fat_g=row['fat_g'],
                notes=row['notes'],
                created_at=row['created_at']
            ))
        return entries

    def get_daily_calories(self, user_id: int, target_date: date = None) -> int:
        """Get total calories consumed on a specific date."""
        cursor = self.conn.cursor()
        target = target_date or date.today()
        cursor.execute('SELECT SUM(estimated_calories) FROM food_entries WHERE user_id = ? AND date = ?',
                      (user_id, target))
        result = cursor.fetchone()[0]
        return result or 0

    # Weekly goals operations
    def create_weekly_goal(self, goal: WeeklyGoal) -> int:
        """Create a weekly goal."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO weekly_goals (user_id, week_start, target_weight_kg, target_calories_daily,
            target_workouts, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (goal.user_id, goal.week_start, goal.target_weight_kg, goal.target_calories_daily,
              goal.target_workouts, goal.notes))
        self.conn.commit()
        return cursor.lastrowid

    def get_current_weekly_goal(self, user_id: int) -> Optional[WeeklyGoal]:
        """Get the current week's goal."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM weekly_goals WHERE user_id = ?
            ORDER BY week_start DESC LIMIT 1
        ''', (user_id,))
        row = cursor.fetchone()
        if row:
            return WeeklyGoal(
                id=row['id'],
                user_id=row['user_id'],
                week_start=row['week_start'],
                target_weight_kg=row['target_weight_kg'],
                actual_weight_kg=row['actual_weight_kg'],
                target_calories_daily=row['target_calories_daily'],
                target_workouts=row['target_workouts'],
                completed_workouts=row['completed_workouts'],
                notes=row['notes']
            )
        return None

    def update_weekly_goal(self, goal: WeeklyGoal):
        """Update a weekly goal."""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE weekly_goals SET target_weight_kg=?, actual_weight_kg=?,
            target_calories_daily=?, target_workouts=?, completed_workouts=?, notes=?
            WHERE id=?
        ''', (goal.target_weight_kg, goal.actual_weight_kg, goal.target_calories_daily,
              goal.target_workouts, goal.completed_workouts, goal.notes, goal.id))
        self.conn.commit()

    # Weight log operations
    def add_weight_log(self, user_id: int, weight_kg: float, log_date: date = None, notes: str = "") -> int:
        """Add a weight measurement."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO weight_log (user_id, date, weight_kg, notes)
            VALUES (?, ?, ?, ?)
        ''', (user_id, log_date or date.today(), weight_kg, notes))
        self.conn.commit()
        return cursor.lastrowid

    def get_weight_history(self, user_id: int, limit: int = 30) -> List[WeightLog]:
        """Get weight history for a user."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM weight_log WHERE user_id = ?
            ORDER BY date DESC LIMIT ?
        ''', (user_id, limit))

        logs = []
        for row in cursor.fetchall():
            logs.append(WeightLog(
                id=row['id'],
                user_id=row['user_id'],
                date=row['date'],
                weight_kg=row['weight_kg'],
                notes=row['notes']
            ))
        return logs

    def get_latest_weight(self, user_id: int) -> Optional[float]:
        """Get the most recent weight for a user."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT weight_kg FROM weight_log WHERE user_id = ?
            ORDER BY date DESC LIMIT 1
        ''', (user_id,))
        row = cursor.fetchone()
        return row['weight_kg'] if row else None

    # Exercise progress operations
    def update_exercise_progress(self, user_id: int, exercise_name: str, weight_kg: float, reps: int):
        """Update exercise progress for tracking progressive overload."""
        # Calculate estimated 1RM using Brzycki formula
        estimated_1rm = weight_kg * (36 / (37 - reps)) if reps < 37 else weight_kg

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO exercise_progress (user_id, exercise_name, date, max_weight_kg, max_reps, estimated_1rm)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, exercise_name, date.today(), weight_kg, reps, estimated_1rm))
        self.conn.commit()

    def get_exercise_progress(self, user_id: int, exercise_name: str, limit: int = 10) -> List[ExerciseProgress]:
        """Get progress history for a specific exercise."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM exercise_progress WHERE user_id = ? AND exercise_name = ?
            ORDER BY date DESC LIMIT ?
        ''', (user_id, exercise_name, limit))

        progress = []
        for row in cursor.fetchall():
            progress.append(ExerciseProgress(
                id=row['id'],
                user_id=row['user_id'],
                exercise_name=row['exercise_name'],
                date=row['date'],
                max_weight_kg=row['max_weight_kg'],
                max_reps=row['max_reps'],
                estimated_1rm=row['estimated_1rm']
            ))
        return progress

    def get_last_exercise_weight(self, user_id: int, exercise_name: str) -> Optional[tuple]:
        """Get the last weight and reps used for an exercise."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT max_weight_kg, max_reps FROM exercise_progress
            WHERE user_id = ? AND exercise_name = ?
            ORDER BY date DESC LIMIT 1
        ''', (user_id, exercise_name))
        row = cursor.fetchone()
        return (row['max_weight_kg'], row['max_reps']) if row else None

    def get_workouts_this_week(self, user_id: int) -> int:
        """Get the number of workouts completed this week."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM workouts
            WHERE user_id = ? AND date >= date('now', 'weekday 0', '-7 days')
        ''', (user_id,))
        return cursor.fetchone()[0]

    # Custom exercise operations
    def add_custom_exercise(self, name: str, exercise_type: str, primary_muscles: List[str],
                           secondary_muscles: List[str], equipment: List[str], difficulty: str,
                           form_tips: List[str], common_mistakes: List[str], description: str = "") -> int:
        """Add a custom exercise to the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO custom_exercises (name, exercise_type, primary_muscles, secondary_muscles,
                equipment, difficulty, form_tips, common_mistakes, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name,
                exercise_type,
                ','.join(primary_muscles),
                ','.join(secondary_muscles),
                ','.join(equipment),
                difficulty,
                '|||'.join(form_tips),
                '|||'.join(common_mistakes),
                description
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Exercise already exists
            return -1

    def get_custom_exercise(self, name: str) -> Optional[dict]:
        """Get a custom exercise by name."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM custom_exercises WHERE LOWER(name) = LOWER(?)', (name,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'name': row['name'],
                'type': row['exercise_type'],
                'primary_muscles': row['primary_muscles'].split(',') if row['primary_muscles'] else [],
                'secondary_muscles': row['secondary_muscles'].split(',') if row['secondary_muscles'] else [],
                'equipment': row['equipment'].split(',') if row['equipment'] else [],
                'difficulty': row['difficulty'],
                'form_tips': row['form_tips'].split('|||') if row['form_tips'] else [],
                'common_mistakes': row['common_mistakes'].split('|||') if row['common_mistakes'] else [],
                'description': row['description']
            }
        return None

    def get_all_custom_exercises(self) -> List[dict]:
        """Get all custom exercises."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM custom_exercises ORDER BY name')
        exercises = []
        for row in cursor.fetchall():
            exercises.append({
                'id': row['id'],
                'name': row['name'],
                'type': row['exercise_type'],
                'primary_muscles': row['primary_muscles'].split(',') if row['primary_muscles'] else [],
                'secondary_muscles': row['secondary_muscles'].split(',') if row['secondary_muscles'] else [],
                'equipment': row['equipment'].split(',') if row['equipment'] else [],
                'difficulty': row['difficulty'],
                'form_tips': row['form_tips'].split('|||') if row['form_tips'] else [],
                'common_mistakes': row['common_mistakes'].split('|||') if row['common_mistakes'] else [],
                'description': row['description']
            })
        return exercises

    def get_exercise_history_detailed(self, user_id: int, exercise_name: str, limit: int = 5) -> List[dict]:
        """Get detailed exercise history with all sets from recent workouts."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT we.*, w.date FROM workout_exercises we
            JOIN workouts w ON we.workout_id = w.id
            WHERE w.user_id = ? AND LOWER(we.exercise_name) = LOWER(?)
            ORDER BY w.date DESC, we.id DESC
            LIMIT ?
        ''', (user_id, exercise_name, limit))

        history = []
        for row in cursor.fetchall():
            history.append({
                'date': row['date'],
                'sets': row['sets'],
                'reps': row['reps'],
                'weight_kg': row['weight_kg'],
                'notes': row['notes']
            })
        return history
