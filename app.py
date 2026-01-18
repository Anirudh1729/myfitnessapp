"""
My Fitness App - Web Version
A mobile-friendly Flask web application for fitness tracking.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
from datetime import date, timedelta
from database.db import Database
from database.models import User, Workout, FoodEntry
from services.workout import WorkoutService
from services.food import FoodService
from services.planner import PlannerService, WORKOUT_SPLITS
from services.goals import GoalsService
from data.exercises import EXERCISE_DATABASE, estimate_food_calories
from utils.calories import calculate_bmr, calculate_tdee, calculate_target_calories

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize database and services
db = Database()
workout_service = WorkoutService(db)
food_service = FoodService(db)
planner = PlannerService(db)
goals_service = GoalsService(db)


def get_user():
    """Get current user or None if not onboarded."""
    return db.get_user()


def get_user_id():
    """Get current user ID, defaulting to 1."""
    user = get_user()
    return user.id if user else 1


def user_to_dict(user):
    """Convert User object to dictionary for templates."""
    if not user:
        return None
    return {
        'id': user.id,
        'name': user.name,
        'age': user.age,
        'gender': user.gender,
        'height': user.height_cm,
        'weight': user.weight_kg,
        'goal': user.goal,
        'activity_level': user.activity_level,
        'experience_level': user.experience_level,
        'workout_split': getattr(user, 'workout_split', 'ppls_shoulder_focus'),
        'target_weight': getattr(user, 'target_weight', user.weight_kg)
    }


def get_todays_workout_data(user):
    """Get today's workout as structured data for templates."""
    if not user:
        return None

    # Get the user's split (default to ppls_shoulder_focus)
    split_name = getattr(user, 'workout_split', 'ppls_shoulder_focus')
    split = WORKOUT_SPLITS.get(split_name)

    if not split:
        return None

    # Determine which day of the program we're on
    today = date.today()
    day_of_week = today.weekday()  # 0 = Monday

    # Map to schedule
    schedule_keys = list(split['schedule'].keys())
    day_index = day_of_week % len(schedule_keys)
    day_key = schedule_keys[day_index]
    day_data = split['schedule'][day_key]

    # Build structured data
    exercises = []
    for exercise, ex_type, rep_scheme in day_data.get('exercises', []):
        # Parse rep scheme (e.g., "3 sets x 8-10 reps")
        parts = rep_scheme.split(' x ')
        sets = int(parts[0].split()[0]) if parts else 3
        reps = parts[1].split()[0] if len(parts) > 1 else '8-10'

        exercises.append({
            'name': exercise,
            'type': ex_type,
            'sets': sets,
            'reps': reps
        })

    return {
        'name': day_data['name'],
        'description': f"Target: {', '.join(day_data.get('muscles', []))}",
        'exercises': exercises,
        'total_sets': day_data.get('total_sets', sum(e['sets'] for e in exercises)),
        'is_rest': len(exercises) == 0
    }


def get_current_split_data(user):
    """Get current split as structured data."""
    if not user:
        return None

    split_name = getattr(user, 'workout_split', 'ppls_shoulder_focus')
    split = WORKOUT_SPLITS.get(split_name)

    if not split:
        return None

    return {
        'id': split_name,
        'name': split['name'],
        'description': split['description'],
        'days_per_week': split['days_per_week'],
        'volume_info': split.get('volume_info')
    }


def get_weekly_schedule_data(user):
    """Get weekly schedule as structured data."""
    if not user:
        return {}

    split_name = getattr(user, 'workout_split', 'ppls_shoulder_focus')
    split = WORKOUT_SPLITS.get(split_name)

    if not split:
        return {}

    today = date.today()
    monday = today - timedelta(days=today.weekday())

    schedule_keys = list(split['schedule'].keys())
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    weekly = {}
    for i in range(7):
        day_name = day_names[i]
        day_index = i % len(schedule_keys)
        day_data = split['schedule'][schedule_keys[day_index]]

        exercises = []
        for exercise, ex_type, rep_scheme in day_data.get('exercises', []):
            parts = rep_scheme.split(' x ')
            sets = int(parts[0].split()[0]) if parts else 3
            reps = parts[1].split()[0] if len(parts) > 1 else '8-10'
            exercises.append({
                'name': exercise,
                'type': ex_type,
                'sets': sets,
                'reps': reps
            })

        weekly[day_name] = {
            'name': day_data['name'],
            'muscles': day_data.get('muscles', []),
            'exercises': exercises,
            'is_rest': len(exercises) == 0
        }

    return weekly


# ----- Main Routes -----

@app.route('/')
def index():
    """Home page - redirect to onboarding or dashboard."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """Main dashboard with quick actions."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    user_id = user.id
    user_dict = user_to_dict(user)

    # Get today's workouts
    today = date.today()
    workouts = db.get_workouts(user_id, today, today)
    today_workouts = []
    for w in workouts:
        exercises = db.get_workout_exercises(w.id)
        today_workouts.append({
            'type': w.workout_type,
            'exercises_count': len(exercises)
        })

    # Get today's food
    food_entries = db.get_food_entries(user_id, today)
    today_food = []
    for f in food_entries:
        today_food.append({
            'name': f.dish_name,
            'calories': f.estimated_calories,
            'protein': f.protein_g,
            'carbs': f.carbs_g,
            'fat': f.fat_g,
            'meal_type': f.meal_type,
            'is_homemade': f.is_homemade
        })

    today_calories = sum(f['calories'] for f in today_food)

    # Calculate calorie goal
    bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
    tdee = calculate_tdee(bmr, user.activity_level)
    calorie_goal = calculate_target_calories(tdee, user.goal)

    return render_template('dashboard.html',
                         user=user_dict,
                         today_workouts=today_workouts,
                         today_food=today_food,
                         today_calories=today_calories,
                         calorie_goal=calorie_goal)


# ----- Onboarding Routes -----

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    """User onboarding flow."""
    if request.method == 'POST':
        data = request.form

        user = User(
            name=data.get('name', 'User'),
            age=int(data.get('age', 25)),
            gender=data.get('gender', 'male'),
            height_cm=float(data.get('height', 170)),
            weight_kg=float(data.get('weight', 70)),
            goal=data.get('goal', 'jacked_model'),
            activity_level=data.get('activity_level', 'moderate'),
            experience_level=data.get('experience_level', 'intermediate')
        )

        db.create_user(user)
        return redirect(url_for('dashboard'))

    return render_template('onboarding.html')


# ----- Workout Routes -----

@app.route('/workout')
def workout_menu():
    """Workout tracking menu."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    user_dict = user_to_dict(user)
    user_id = user.id

    # Get today's plan
    todays_workout = get_todays_workout_data(user)

    # Get recent workouts
    end_date = date.today()
    start_date = end_date - timedelta(days=14)
    workouts = db.get_workouts(user_id, start_date, end_date)

    recent_workouts = []
    for w in workouts[:5]:
        exercises = db.get_workout_exercises(w.id)
        recent_workouts.append({
            'date': str(w.date),
            'type': w.workout_type,
            'exercises_count': len(exercises)
        })

    return render_template('workout_menu.html',
                         user=user_dict,
                         todays_workout=todays_workout,
                         recent_workouts=recent_workouts)


@app.route('/workout/start', methods=['GET', 'POST'])
def start_workout():
    """Start a new workout session."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    if request.method == 'POST':
        workout_type = request.form.get('workout_type', 'strength')
        workout = workout_service.start_workout(user.id, workout_type)
        session['current_workout_id'] = workout.id
        return redirect(url_for('active_workout'))

    todays_workout = get_todays_workout_data(user)
    return render_template('start_workout.html', todays_workout=todays_workout)


@app.route('/workout/active')
def active_workout():
    """Active workout session - log exercises."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    workout_id = session.get('current_workout_id')
    if not workout_id:
        return redirect(url_for('start_workout'))

    # Get exercises logged so far
    exercises = db.get_workout_exercises(workout_id)
    exercises_logged = []
    for e in exercises:
        exercises_logged.append({
            'name': e.exercise_name,
            'weight': e.weight_kg,
            'reps': e.reps,
            'sets': e.sets
        })

    todays_workout = get_todays_workout_data(user)

    return render_template('active_workout.html',
                         workout_id=workout_id,
                         exercises_logged=exercises_logged,
                         todays_workout=todays_workout)


@app.route('/workout/log-exercise', methods=['POST'])
def log_exercise():
    """Log an exercise to the current workout."""
    user = get_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    workout_id = session.get('current_workout_id')
    if not workout_id:
        return jsonify({'error': 'No active workout'}), 400

    data = request.json
    exercise_name = data.get('exercise')
    weight = float(data.get('weight', 0))
    reps = int(data.get('reps', 0))
    sets = int(data.get('sets', 1))
    notes = data.get('notes', '')

    workout_service.add_exercise(
        workout_id, user.id, exercise_name,
        sets=sets, reps=reps, weight_kg=weight, notes=notes
    )

    return jsonify({'success': True})


@app.route('/workout/finish', methods=['POST'])
def finish_workout():
    """Finish the current workout."""
    session.pop('current_workout_id', None)
    return redirect(url_for('workout_menu'))


@app.route('/exercise/info/<exercise_name>')
def exercise_info(exercise_name):
    """Get exercise info with form tips and recommendations."""
    user = get_user()
    user_id = user.id if user else 1

    # Get exercise info
    exercise = workout_service.get_exercise_info(exercise_name)

    if not exercise:
        return jsonify({
            'name': exercise_name,
            'type': 'unknown',
            'primary_muscles': [],
            'form_tips': ['No form tips available'],
            'common_mistakes': [],
            'last_performance': None
        })

    # Get last performance
    last_perf = db.get_last_exercise_weight(user_id, exercise.get('name', exercise_name))

    return jsonify({
        'name': exercise.get('name', exercise_name),
        'type': exercise.get('type', 'compound'),
        'primary_muscles': exercise.get('primary_muscles', []),
        'secondary_muscles': exercise.get('secondary_muscles', []),
        'form_tips': exercise.get('form_tips', [])[:3],
        'common_mistakes': exercise.get('common_mistakes', [])[:2],
        'last_performance': {
            'weight': last_perf[0],
            'reps': last_perf[1]
        } if last_perf else None
    })


@app.route('/exercise/search')
def search_exercises():
    """Search exercises by name."""
    query = request.args.get('q', '').lower()
    results = []

    # Search built-in exercises
    for name, data in EXERCISE_DATABASE.items():
        if query in name.lower():
            results.append({
                'name': name,
                'type': data.get('type', 'compound'),
                'primary_muscles': data.get('primary_muscles', [])
            })

    # Search custom exercises
    custom = db.get_all_custom_exercises()
    for ex in custom:
        if query in ex['name'].lower():
            results.append({
                'name': ex['name'],
                'type': ex.get('exercise_type', 'compound'),
                'primary_muscles': ex.get('primary_muscles', '').split(',') if ex.get('primary_muscles') else []
            })

    return jsonify(results[:20])


@app.route('/exercise/add', methods=['POST'])
def add_exercise():
    """Add a custom exercise."""
    data = request.json
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({'error': 'Exercise name required'}), 400

    success, message, exercise_info = workout_service.add_custom_exercise(name, description)

    return jsonify({
        'success': success,
        'message': message,
        'exercise': exercise_info
    })


# ----- Food Routes -----

@app.route('/food')
def food_menu():
    """Food tracking menu."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    user_dict = user_to_dict(user)
    user_id = user.id

    # Get today's food
    today = date.today()
    food_entries = db.get_food_entries(user_id, today)

    today_food = []
    for f in food_entries:
        today_food.append({
            'name': f.dish_name,
            'calories': f.estimated_calories,
            'protein': f.protein_g,
            'carbs': f.carbs_g,
            'fat': f.fat_g,
            'meal_type': f.meal_type,
            'is_homemade': f.is_homemade
        })

    total_calories = sum(f['calories'] for f in today_food)

    # Calculate calorie goal
    bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
    tdee = calculate_tdee(bmr, user.activity_level)
    calorie_goal = calculate_target_calories(tdee, user.goal)

    return render_template('food_menu.html',
                         user=user_dict,
                         today_food=today_food,
                         total_calories=total_calories,
                         calorie_goal=calorie_goal)


@app.route('/food/log', methods=['POST'])
def log_food():
    """Log a food item."""
    user = get_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json

    entry = FoodEntry(
        user_id=user.id,
        date=date.today(),
        meal_type=data.get('meal_type', 'snack'),
        dish_name=data.get('name'),
        is_homemade=data.get('is_homemade', True),
        estimated_calories=int(data.get('calories', 0)),
        protein_g=float(data.get('protein', 0)),
        carbs_g=float(data.get('carbs', 0)),
        fat_g=float(data.get('fat', 0))
    )

    db.add_food_entry(entry)
    return jsonify({'success': True})


@app.route('/food/estimate', methods=['POST'])
def estimate_calories():
    """Estimate calories for a food item."""
    data = request.json
    dish_name = data.get('dish')
    is_homemade = data.get('is_homemade', True)

    estimate = estimate_food_calories(dish_name, is_homemade)
    return jsonify(estimate)


# ----- Progress Routes -----

@app.route('/progress')
def progress():
    """View progress and stats."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    user_dict = user_to_dict(user)
    user_id = user.id

    # Get weekly workout stats
    today = date.today()
    monday = today - timedelta(days=today.weekday())

    workouts = db.get_workouts(user_id, monday, today)
    total_sets = 0
    for w in workouts:
        exercises = db.get_workout_exercises(w.id)
        total_sets += sum(e.sets for e in exercises)

    weekly_workouts = {
        'total_workouts': len(workouts),
        'total_sets': total_sets
    }

    # Get weekly calories
    total_cals = 0
    days_logged = 0
    for i in range(7):
        day = monday + timedelta(days=i)
        if day > today:
            break
        day_cals = db.get_daily_calories(user_id, day)
        if day_cals > 0:
            total_cals += day_cals
            days_logged += 1

    weekly_calories = {
        'total': total_cals,
        'average': total_cals // days_logged if days_logged > 0 else 0
    }

    # Get weight history
    weight_logs = db.get_weight_history(user_id, limit=10)
    weight_history = []
    for w in weight_logs:
        weight_history.append({
            'date': str(w.date),
            'weight': w.weight_kg
        })

    return render_template('progress.html',
                         user=user_dict,
                         weekly_workouts=weekly_workouts,
                         weekly_calories=weekly_calories,
                         weight_history=weight_history)


@app.route('/progress/log-weight', methods=['POST'])
def log_weight():
    """Log current weight."""
    user = get_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    weight = float(data.get('weight'))

    db.add_weight_log(user.id, weight)

    # Update user's current weight
    user.weight_kg = weight
    db.update_user(user)

    return jsonify({'success': True})


# ----- Plan Routes -----

@app.route('/plan')
def workout_plan():
    """View workout plan."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    user_dict = user_to_dict(user)

    current_split = get_current_split_data(user)
    weekly_schedule = get_weekly_schedule_data(user)

    return render_template('plan.html',
                         user=user_dict,
                         current_split=current_split,
                         weekly_schedule=weekly_schedule)


@app.route('/plan/change-split', methods=['POST'])
def change_split():
    """Change workout split."""
    user = get_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    new_split = data.get('split')

    # Store the split preference (we'd need to add this to user model properly)
    # For now, just return success - the split will be stored in session
    session['workout_split'] = new_split
    return jsonify({'success': True})


# ----- Settings Routes -----

@app.route('/settings')
def settings():
    """User settings."""
    user = get_user()
    if not user:
        return redirect(url_for('onboarding'))

    user_dict = user_to_dict(user)
    return render_template('settings.html', user=user_dict)


@app.route('/settings/update', methods=['POST'])
def update_settings():
    """Update user settings."""
    user = get_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json

    # Update user fields
    if 'name' in data:
        user.name = data['name']
    if 'age' in data:
        user.age = int(data['age'])
    if 'gender' in data:
        user.gender = data['gender']
    if 'weight' in data:
        user.weight_kg = float(data['weight'])
    if 'height' in data:
        user.height_cm = float(data['height'])
    if 'goal' in data:
        user.goal = data['goal']
    if 'activity_level' in data:
        user.activity_level = data['activity_level']
    if 'experience_level' in data:
        user.experience_level = data['experience_level']

    db.update_user(user)
    return jsonify({'success': True})


# ----- API for Exercise Database -----

@app.route('/api/exercises')
def get_all_exercises():
    """Get all exercises (built-in + custom)."""
    exercises = []

    for name, data in EXERCISE_DATABASE.items():
        exercises.append({
            'name': name,
            'type': data.get('type', 'compound'),
            'primary_muscles': data.get('primary_muscles', []),
            'equipment': data.get('equipment', 'barbell'),
            'is_custom': False
        })

    custom = db.get_all_custom_exercises()
    for ex in custom:
        exercises.append({
            'name': ex['name'],
            'type': ex.get('exercise_type', 'compound'),
            'primary_muscles': ex.get('primary_muscles', '').split(',') if ex.get('primary_muscles') else [],
            'equipment': ex.get('equipment', 'other'),
            'is_custom': True
        })

    return jsonify(exercises)


@app.route('/api/splits')
def get_splits():
    """Get available workout splits."""
    splits = []
    for key, split in WORKOUT_SPLITS.items():
        splits.append({
            'id': key,
            'name': split['name'],
            'description': split['description'],
            'days_per_week': split['days_per_week']
        })
    return jsonify(splits)


if __name__ == '__main__':
    # Run on all interfaces so it's accessible from iPhone
    app.run(host='0.0.0.0', port=5000, debug=True)
