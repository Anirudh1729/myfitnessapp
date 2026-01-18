# My Fitness App

A comprehensive CLI fitness tracking application to help you achieve your fitness goals.

## Features

### Workout Tracking
- Track weight lifting sessions with sets, reps, and weight
- Track cardio sessions with duration and distance
- Built-in exercise database with 50+ exercises
- Form tips and common mistakes for each exercise
- Progressive overload suggestions based on your history

### Food Tracking
- Log meals and snacks with automatic calorie estimation
- Distinguishes between homemade and restaurant/ordered food
- Database of 100+ common dishes with macros
- Daily and weekly nutrition summaries

### Workout Planning
- Multiple workout splits available:
  - Push/Pull/Legs (6 days)
  - Upper/Lower (4 days)
  - Full Body (3 days)
  - Bro Split (5 days)
- Daily workout recommendations based on your experience level
- Progressive overload guidelines
- Rest day advice

### Goal Setting & Tracking
- Personalized calorie and macro recommendations
- Weekly weight goals based on your objectives
- Long-term weight projections
- Body fat estimation

### Onboarding
- Comprehensive setup process
- Collects measurements and fitness goals
- Default goal: Build a lean, "model/actor" style physique

## Installation

No external dependencies required! The app uses only Python standard library.

```bash
cd myfitnessapp
python main.py
```

## Usage

### First Run
On first run, you'll go through an onboarding process:
1. Enter your name, age, and gender
2. Enter your height and weight
3. Select your fitness goal (default: jacked model/actor body)
4. Select your activity level
5. Select your lifting experience

### Main Menu
- **Start Workout**: Begin a weight lifting, cardio, or mixed session
- **Log Food**: Track your meals with automatic calorie estimation
- **Log Weight**: Record your daily weight
- **View Today's Plan**: See your scheduled workout for today
- **View Weekly Summary**: Check your progress toward weekly goals
- **Workout Plans & Guides**: Browse workout splits and training guides
- **Calorie & Nutrition Info**: View your personalized calorie/macro targets
- **Exercise Database**: Search exercises and view form tips
- **Settings & Profile**: Update your profile information

### During Workouts
- Type an exercise name to log it
- Type `form <exercise>` to see form tips
- Type `search <query>` to find exercises
- Type `summary` to see your workout progress
- Type `done` to finish the workout

## File Structure

```
myfitnessapp/
├── main.py              # Main CLI application
├── database/
│   ├── db.py            # SQLite database operations
│   └── models.py        # Data models
├── data/
│   └── exercises.py     # Exercise database with form tips
├── services/
│   ├── onboarding.py    # User onboarding
│   ├── workout.py       # Workout tracking
│   ├── food.py          # Food tracking
│   ├── planner.py       # Workout planning
│   └── goals.py         # Goals and recommendations
└── utils/
    └── calories.py      # Calorie/macro calculations
```

## Data Storage

All data is stored locally in `~/.myfitnessapp/fitness.db` using SQLite.

## Fitness Goals

- **Jacked Model/Actor** (default): Build lean muscle while staying cut with a slight calorie deficit
- **Lean/Cut**: Focus on fat loss with a moderate calorie deficit
- **Bulk**: Build maximum muscle with a calorie surplus
- **Maintain**: Keep current physique at maintenance calories

## Calculations

- **BMR**: Calculated using Mifflin-St Jeor equation
- **TDEE**: BMR adjusted for activity level
- **Target Calories**: TDEE adjusted for your goal
- **Protein**: 2.2g per kg of body weight (adjusted for goal)
- **Fat**: 25% of total calories
- **Carbs**: Remaining calories after protein and fat
