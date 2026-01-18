"""Exercise database with form tips and muscle group information."""

from typing import Dict, List, Optional

# Exercise database with detailed form tips
EXERCISES: Dict[str, dict] = {
    # CHEST EXERCISES
    "bench press": {
        "name": "Bench Press",
        "type": "compound",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "front_delts"],
        "equipment": ["barbell", "bench"],
        "difficulty": "intermediate",
        "form_tips": [
            "Retract your shoulder blades and squeeze them together throughout the lift",
            "Keep your feet flat on the floor with legs at 90 degrees",
            "Grip the bar slightly wider than shoulder-width",
            "Lower the bar to your mid-chest/nipple line",
            "Keep your wrists straight, not bent back",
            "Drive through your heels and maintain an arch in your lower back",
            "Don't bounce the bar off your chest - control the descent",
            "Lock out at the top without flaring your elbows excessively"
        ],
        "common_mistakes": [
            "Flaring elbows out at 90 degrees (aim for 45-75 degrees)",
            "Lifting hips off the bench",
            "Not using leg drive",
            "Bouncing the bar off chest"
        ]
    },
    "incline bench press": {
        "name": "Incline Bench Press",
        "type": "compound",
        "primary_muscles": ["upper_chest"],
        "secondary_muscles": ["triceps", "front_delts"],
        "equipment": ["barbell", "incline_bench"],
        "difficulty": "intermediate",
        "form_tips": [
            "Set the bench to 30-45 degree incline",
            "Keep shoulder blades retracted and pinched together",
            "Lower the bar to your upper chest/clavicle area",
            "Keep your core tight and feet planted",
            "Maintain a slight arch in your lower back",
            "Press up and slightly back toward your face"
        ],
        "common_mistakes": [
            "Setting incline too high (turns into shoulder press)",
            "Flaring elbows out excessively",
            "Not controlling the negative"
        ]
    },
    "dumbbell bench press": {
        "name": "Dumbbell Bench Press",
        "type": "compound",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "front_delts"],
        "equipment": ["dumbbells", "bench"],
        "difficulty": "beginner",
        "form_tips": [
            "Start with dumbbells at chest level, palms facing forward",
            "Keep shoulder blades squeezed together",
            "Press up while bringing dumbbells slightly together at the top",
            "Lower with control, allowing a good stretch at the bottom",
            "Keep wrists neutral and stacked over elbows",
            "Don't let dumbbells drift too far toward your head or belly"
        ],
        "common_mistakes": [
            "Going too heavy and losing control",
            "Not getting full range of motion",
            "Letting dumbbells drift apart at the top"
        ]
    },
    "chest fly": {
        "name": "Chest Fly",
        "type": "isolation",
        "primary_muscles": ["chest"],
        "secondary_muscles": [],
        "equipment": ["dumbbells", "bench"],
        "difficulty": "beginner",
        "form_tips": [
            "Keep a slight bend in your elbows throughout (imagine hugging a tree)",
            "Lower the weights in a wide arc until you feel a stretch",
            "Squeeze your chest to bring the weights back up",
            "Don't go too heavy - this is an isolation movement",
            "Focus on the mind-muscle connection with your chest",
            "Keep your back flat on the bench"
        ],
        "common_mistakes": [
            "Bending elbows too much (turns into a press)",
            "Going too heavy and losing the stretch",
            "Not controlling the negative portion"
        ]
    },
    "push-up": {
        "name": "Push-Up",
        "type": "compound",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "front_delts", "core"],
        "equipment": ["bodyweight"],
        "difficulty": "beginner",
        "form_tips": [
            "Keep your body in a straight line from head to heels",
            "Place hands slightly wider than shoulder-width",
            "Keep elbows at 45 degrees, not flared out",
            "Lower until chest nearly touches the ground",
            "Keep your core tight - don't let hips sag or pike up",
            "Look slightly ahead, not straight down",
            "Fully extend arms at the top"
        ],
        "common_mistakes": [
            "Letting hips sag or pike up",
            "Not going through full range of motion",
            "Flaring elbows out at 90 degrees"
        ]
    },
    "dips": {
        "name": "Dips",
        "type": "compound",
        "primary_muscles": ["chest", "triceps"],
        "secondary_muscles": ["front_delts"],
        "equipment": ["dip_bars"],
        "difficulty": "intermediate",
        "form_tips": [
            "For chest focus: lean forward about 30 degrees",
            "For triceps focus: stay more upright",
            "Lower until upper arms are parallel to the ground",
            "Keep elbows close to your body",
            "Don't let shoulders shrug up toward ears",
            "Control the descent - don't drop down",
            "Press through your palms to return to the top"
        ],
        "common_mistakes": [
            "Going too deep and stressing shoulders",
            "Swinging or using momentum",
            "Not leaning forward enough for chest activation"
        ]
    },

    # BACK EXERCISES
    "deadlift": {
        "name": "Deadlift",
        "type": "compound",
        "primary_muscles": ["back", "hamstrings", "glutes"],
        "secondary_muscles": ["core", "forearms", "traps"],
        "equipment": ["barbell"],
        "difficulty": "advanced",
        "form_tips": [
            "Stand with feet hip-width apart, bar over mid-foot",
            "Grip the bar just outside your knees",
            "Keep your back flat - neutral spine throughout",
            "Push through your heels, not your toes",
            "Keep the bar close to your body the entire lift",
            "Drive your hips forward as the bar passes your knees",
            "Squeeze your glutes at the top - don't hyperextend",
            "Lower by hinging at hips first, then bend knees",
            "Take a deep breath and brace your core before each rep"
        ],
        "common_mistakes": [
            "Rounding the lower back",
            "Letting the bar drift away from your body",
            "Jerking the weight off the floor",
            "Hyperextending at the top",
            "Looking up (keep neck neutral)"
        ]
    },
    "barbell row": {
        "name": "Barbell Row",
        "type": "compound",
        "primary_muscles": ["lats", "upper_back"],
        "secondary_muscles": ["biceps", "rear_delts", "core"],
        "equipment": ["barbell"],
        "difficulty": "intermediate",
        "form_tips": [
            "Hinge at hips to about 45-degree torso angle",
            "Keep your back flat and core braced",
            "Pull the bar to your lower chest/upper abdomen",
            "Squeeze your shoulder blades together at the top",
            "Lower with control - don't just drop the weight",
            "Keep elbows close to your body",
            "Don't use momentum - no jerking or bouncing"
        ],
        "common_mistakes": [
            "Using too much body English/momentum",
            "Rounding the lower back",
            "Not squeezing at the top",
            "Standing too upright"
        ]
    },
    "pull-up": {
        "name": "Pull-Up",
        "type": "compound",
        "primary_muscles": ["lats"],
        "secondary_muscles": ["biceps", "rear_delts", "forearms"],
        "equipment": ["pull-up_bar"],
        "difficulty": "intermediate",
        "form_tips": [
            "Grip the bar slightly wider than shoulder-width",
            "Start from a dead hang with arms fully extended",
            "Pull your chest toward the bar, not just your chin",
            "Squeeze your shoulder blades down and back",
            "Keep your core tight - no excessive swinging",
            "Lower with control to full extension",
            "Think about driving your elbows down to your hips"
        ],
        "common_mistakes": [
            "Using kipping/momentum",
            "Not going through full range of motion",
            "Only pulling chin to bar instead of chest",
            "Shrugging shoulders up"
        ]
    },
    "lat pulldown": {
        "name": "Lat Pulldown",
        "type": "compound",
        "primary_muscles": ["lats"],
        "secondary_muscles": ["biceps", "rear_delts"],
        "equipment": ["cable_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Grip slightly wider than shoulder-width",
            "Lean back slightly (about 15-20 degrees)",
            "Pull the bar to your upper chest",
            "Squeeze your shoulder blades together at the bottom",
            "Control the weight back up - don't let it yank you",
            "Keep your chest up throughout the movement",
            "Think about pulling with your elbows, not your hands"
        ],
        "common_mistakes": [
            "Leaning back too far",
            "Pulling behind the neck (injury risk)",
            "Using momentum to swing the weight",
            "Not getting full range of motion"
        ]
    },
    "seated cable row": {
        "name": "Seated Cable Row",
        "type": "compound",
        "primary_muscles": ["lats", "upper_back"],
        "secondary_muscles": ["biceps", "rear_delts"],
        "equipment": ["cable_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Sit with a slight bend in your knees",
            "Keep your torso upright - don't lean forward excessively",
            "Pull the handle to your lower chest/upper abdomen",
            "Squeeze your shoulder blades together at peak contraction",
            "Control the negative - don't let the weight pull you forward",
            "Keep your elbows close to your body"
        ],
        "common_mistakes": [
            "Excessive forward lean and rocking",
            "Not squeezing at the contraction point",
            "Using too much bicep instead of back"
        ]
    },
    "dumbbell row": {
        "name": "Dumbbell Row",
        "type": "compound",
        "primary_muscles": ["lats", "upper_back"],
        "secondary_muscles": ["biceps", "rear_delts"],
        "equipment": ["dumbbell", "bench"],
        "difficulty": "beginner",
        "form_tips": [
            "Place one knee and hand on a bench for support",
            "Keep your back flat and parallel to the ground",
            "Pull the dumbbell to your hip, not your armpit",
            "Keep your elbow close to your body",
            "Squeeze your lat at the top of the movement",
            "Lower with control, getting a full stretch at the bottom",
            "Don't rotate your torso - keep it square"
        ],
        "common_mistakes": [
            "Rotating the torso to cheat the weight up",
            "Pulling to the armpit instead of hip",
            "Rounding the lower back"
        ]
    },

    # SHOULDER EXERCISES
    "overhead press": {
        "name": "Overhead Press",
        "type": "compound",
        "primary_muscles": ["front_delts"],
        "secondary_muscles": ["triceps", "side_delts", "upper_chest"],
        "equipment": ["barbell"],
        "difficulty": "intermediate",
        "form_tips": [
            "Stand with feet shoulder-width apart",
            "Grip the bar just outside shoulder-width",
            "Start with the bar at your upper chest/front delts",
            "Brace your core and squeeze your glutes",
            "Press straight up, moving your head back slightly",
            "Lock out overhead with bar over mid-foot",
            "Don't lean back excessively - stay tight",
            "Lower under control to the starting position"
        ],
        "common_mistakes": [
            "Excessive back arch/lean",
            "Not bracing the core",
            "Pressing in front of the body instead of overhead",
            "Flaring elbows out too much"
        ]
    },
    "lateral raise": {
        "name": "Lateral Raise",
        "type": "isolation",
        "primary_muscles": ["side_delts"],
        "secondary_muscles": [],
        "equipment": ["dumbbells"],
        "difficulty": "beginner",
        "form_tips": [
            "Stand with slight bend in knees and hips",
            "Keep a slight bend in your elbows",
            "Raise arms out to the sides until parallel with floor",
            "Lead with your elbows, not your hands",
            "Think about pouring water from a pitcher at the top",
            "Control the descent - don't just drop the weights",
            "Keep your traps relaxed - don't shrug"
        ],
        "common_mistakes": [
            "Using too much weight and swinging",
            "Raising arms too high (above shoulder level)",
            "Shrugging the traps",
            "Leading with the hands instead of elbows"
        ]
    },
    "face pull": {
        "name": "Face Pull",
        "type": "isolation",
        "primary_muscles": ["rear_delts"],
        "secondary_muscles": ["traps", "rhomboids"],
        "equipment": ["cable_machine", "rope"],
        "difficulty": "beginner",
        "form_tips": [
            "Set the cable at upper chest to face height",
            "Use a rope attachment with neutral grip",
            "Pull toward your face, separating the rope",
            "Externally rotate at the end - hands finish by ears",
            "Squeeze your shoulder blades together",
            "Keep your elbows high throughout",
            "Control the weight on the way back"
        ],
        "common_mistakes": [
            "Pulling too low (toward chest)",
            "Not externally rotating at the end",
            "Using too much weight and leaning back"
        ]
    },
    "rear delt fly": {
        "name": "Rear Delt Fly",
        "type": "isolation",
        "primary_muscles": ["rear_delts"],
        "secondary_muscles": ["traps", "rhomboids"],
        "equipment": ["dumbbells"],
        "difficulty": "beginner",
        "form_tips": [
            "Bend over at the hips to about 45 degrees",
            "Keep a slight bend in your elbows",
            "Raise arms out to the sides, leading with elbows",
            "Squeeze your shoulder blades at the top",
            "Don't swing or use momentum",
            "Control the descent"
        ],
        "common_mistakes": [
            "Using too much weight",
            "Not bending over enough",
            "Using traps instead of rear delts"
        ]
    },

    # LEG EXERCISES
    "squat": {
        "name": "Squat (Back Squat)",
        "type": "compound",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["hamstrings", "core", "lower_back"],
        "equipment": ["barbell", "squat_rack"],
        "difficulty": "intermediate",
        "form_tips": [
            "Position bar on upper traps (high bar) or rear delts (low bar)",
            "Stand with feet shoulder-width apart, toes slightly out",
            "Brace your core - take a deep breath before descending",
            "Push your hips back and bend knees simultaneously",
            "Keep your chest up and back flat throughout",
            "Descend until hip crease is below knee (parallel or lower)",
            "Keep knees tracking over toes - don't let them cave in",
            "Drive through your whole foot, not just heels or toes",
            "Stand up by driving hips forward"
        ],
        "common_mistakes": [
            "Knees caving inward",
            "Rounding the lower back (butt wink)",
            "Not hitting depth",
            "Leaning too far forward",
            "Rising on toes"
        ]
    },
    "front squat": {
        "name": "Front Squat",
        "type": "compound",
        "primary_muscles": ["quadriceps"],
        "secondary_muscles": ["glutes", "core"],
        "equipment": ["barbell", "squat_rack"],
        "difficulty": "advanced",
        "form_tips": [
            "Rest bar on front delts with elbows high",
            "Use clean grip or crossed-arm grip",
            "Keep elbows up throughout - they should point forward",
            "Maintain a more upright torso than back squat",
            "Descend between your legs, not sitting back",
            "Keep your core extremely tight",
            "Drive up while keeping chest and elbows high"
        ],
        "common_mistakes": [
            "Letting elbows drop",
            "Leaning forward excessively",
            "Wrist pain from grip (work on mobility)"
        ]
    },
    "leg press": {
        "name": "Leg Press",
        "type": "compound",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["hamstrings"],
        "equipment": ["leg_press_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Position feet shoulder-width apart on the platform",
            "Keep your lower back pressed against the pad",
            "Lower the weight until knees are at 90 degrees",
            "Don't let knees cave inward",
            "Don't lock out knees completely at the top",
            "Push through your whole foot",
            "Keep your head against the pad"
        ],
        "common_mistakes": [
            "Going too deep and lifting hips off the pad",
            "Locking out knees at the top",
            "Bouncing at the bottom",
            "Placing feet too high or too low"
        ]
    },
    "romanian deadlift": {
        "name": "Romanian Deadlift (RDL)",
        "type": "compound",
        "primary_muscles": ["hamstrings", "glutes"],
        "secondary_muscles": ["lower_back", "core"],
        "equipment": ["barbell"],
        "difficulty": "intermediate",
        "form_tips": [
            "Start standing with the bar at hip level",
            "Keep a slight bend in your knees (don't lock them)",
            "Push your hips back while lowering the bar",
            "Keep the bar close to your legs throughout",
            "Lower until you feel a deep hamstring stretch",
            "Keep your back flat - neutral spine",
            "Drive hips forward to return to standing",
            "Squeeze glutes at the top"
        ],
        "common_mistakes": [
            "Bending knees too much (turns into a regular deadlift)",
            "Rounding the lower back",
            "Not feeling the hamstring stretch",
            "Letting the bar drift away from legs"
        ]
    },
    "leg curl": {
        "name": "Leg Curl",
        "type": "isolation",
        "primary_muscles": ["hamstrings"],
        "secondary_muscles": [],
        "equipment": ["leg_curl_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Adjust the machine so the pad sits just above your heels",
            "Keep your hips pressed down throughout",
            "Curl the weight up by squeezing your hamstrings",
            "Get a full contraction at the top",
            "Lower with control - don't let it drop",
            "Don't use momentum or lift your hips"
        ],
        "common_mistakes": [
            "Lifting hips off the pad",
            "Using momentum to swing the weight",
            "Not getting full range of motion"
        ]
    },
    "leg extension": {
        "name": "Leg Extension",
        "type": "isolation",
        "primary_muscles": ["quadriceps"],
        "secondary_muscles": [],
        "equipment": ["leg_extension_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Adjust the pad so it sits on your lower shin",
            "Keep your back against the pad",
            "Extend your legs fully and squeeze at the top",
            "Lower with control - don't drop the weight",
            "Keep your toes pointed up or slightly out",
            "Don't swing or use momentum"
        ],
        "common_mistakes": [
            "Using too much weight and swinging",
            "Not getting full extension",
            "Letting the weight drop on the negative"
        ]
    },
    "lunges": {
        "name": "Lunges",
        "type": "compound",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["hamstrings", "core"],
        "equipment": ["bodyweight", "dumbbells"],
        "difficulty": "beginner",
        "form_tips": [
            "Take a big step forward",
            "Lower until back knee nearly touches the ground",
            "Keep your front knee over your ankle, not past your toes",
            "Keep your torso upright throughout",
            "Push through your front heel to return",
            "Keep your core tight for balance",
            "Alternate legs or do all reps on one side"
        ],
        "common_mistakes": [
            "Front knee going past toes",
            "Leaning forward excessively",
            "Taking too short a step",
            "Knee caving inward"
        ]
    },
    "calf raise": {
        "name": "Calf Raise",
        "type": "isolation",
        "primary_muscles": ["calves"],
        "secondary_muscles": [],
        "equipment": ["bodyweight", "calf_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Stand with balls of feet on the edge of a step",
            "Lower your heels below the step for a full stretch",
            "Rise up onto your toes as high as possible",
            "Squeeze your calves at the top",
            "Lower with control - don't bounce",
            "Keep your knees straight but not locked"
        ],
        "common_mistakes": [
            "Not getting full range of motion",
            "Bouncing at the bottom",
            "Bending knees too much"
        ]
    },

    # ARM EXERCISES
    "barbell curl": {
        "name": "Barbell Curl",
        "type": "isolation",
        "primary_muscles": ["biceps"],
        "secondary_muscles": ["forearms"],
        "equipment": ["barbell"],
        "difficulty": "beginner",
        "form_tips": [
            "Stand with feet shoulder-width apart",
            "Grip the bar at shoulder width with underhand grip",
            "Keep your elbows pinned to your sides",
            "Curl the weight up by flexing your biceps",
            "Squeeze at the top of the movement",
            "Lower with control - don't swing",
            "Keep your body still - no swaying"
        ],
        "common_mistakes": [
            "Swinging the body to cheat the weight up",
            "Letting elbows drift forward",
            "Not controlling the negative",
            "Using too much weight"
        ]
    },
    "dumbbell curl": {
        "name": "Dumbbell Curl",
        "type": "isolation",
        "primary_muscles": ["biceps"],
        "secondary_muscles": ["forearms"],
        "equipment": ["dumbbells"],
        "difficulty": "beginner",
        "form_tips": [
            "Stand with dumbbells at your sides, palms facing forward",
            "Keep your elbows close to your body",
            "Curl one or both dumbbells up toward your shoulders",
            "Rotate your wrist slightly outward at the top for peak contraction",
            "Squeeze the bicep at the top",
            "Lower with control"
        ],
        "common_mistakes": [
            "Swinging to generate momentum",
            "Moving elbows forward during the curl",
            "Not getting full range of motion"
        ]
    },
    "hammer curl": {
        "name": "Hammer Curl",
        "type": "isolation",
        "primary_muscles": ["biceps", "brachialis"],
        "secondary_muscles": ["forearms"],
        "equipment": ["dumbbells"],
        "difficulty": "beginner",
        "form_tips": [
            "Hold dumbbells with a neutral grip (palms facing each other)",
            "Keep elbows pinned to your sides",
            "Curl the weight up while maintaining neutral grip",
            "Squeeze at the top",
            "Lower with control",
            "Keep your body still - no swaying"
        ],
        "common_mistakes": [
            "Rotating wrists during the movement",
            "Using momentum",
            "Letting elbows drift forward"
        ]
    },
    "tricep pushdown": {
        "name": "Tricep Pushdown",
        "type": "isolation",
        "primary_muscles": ["triceps"],
        "secondary_muscles": [],
        "equipment": ["cable_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Stand facing the cable machine",
            "Keep your elbows pinned to your sides",
            "Push the weight down until arms are fully extended",
            "Squeeze your triceps at the bottom",
            "Control the weight back up - don't let it fly up",
            "Keep your body still - don't lean into it"
        ],
        "common_mistakes": [
            "Letting elbows drift away from body",
            "Leaning over the weight",
            "Using momentum",
            "Not fully extending at the bottom"
        ]
    },
    "skull crusher": {
        "name": "Skull Crusher (Lying Tricep Extension)",
        "type": "isolation",
        "primary_muscles": ["triceps"],
        "secondary_muscles": [],
        "equipment": ["ez_bar", "bench"],
        "difficulty": "intermediate",
        "form_tips": [
            "Lie on a bench with arms extended holding the weight",
            "Keep upper arms stationary and perpendicular to floor",
            "Lower the weight toward your forehead by bending elbows",
            "Don't flare your elbows out",
            "Extend arms back up by squeezing triceps",
            "Keep the movement controlled throughout"
        ],
        "common_mistakes": [
            "Moving the upper arms",
            "Flaring elbows out",
            "Going too heavy and losing control"
        ]
    },
    "overhead tricep extension": {
        "name": "Overhead Tricep Extension",
        "type": "isolation",
        "primary_muscles": ["triceps"],
        "secondary_muscles": [],
        "equipment": ["dumbbell"],
        "difficulty": "beginner",
        "form_tips": [
            "Hold a dumbbell overhead with both hands",
            "Keep your upper arms close to your ears",
            "Lower the weight behind your head by bending elbows",
            "Keep your elbows pointed forward, not flared",
            "Extend arms back up by squeezing triceps",
            "Keep your core tight and don't arch your back"
        ],
        "common_mistakes": [
            "Flaring elbows out to the sides",
            "Arching the lower back",
            "Moving the upper arms"
        ]
    },

    # CORE EXERCISES
    "plank": {
        "name": "Plank",
        "type": "isolation",
        "primary_muscles": ["core"],
        "secondary_muscles": ["shoulders", "glutes"],
        "equipment": ["bodyweight"],
        "difficulty": "beginner",
        "form_tips": [
            "Support yourself on forearms and toes",
            "Keep your body in a straight line from head to heels",
            "Engage your core - pull belly button toward spine",
            "Don't let your hips sag or pike up",
            "Keep your neck neutral - look at the floor",
            "Squeeze your glutes",
            "Breathe steadily throughout"
        ],
        "common_mistakes": [
            "Hips sagging down",
            "Hips piking up too high",
            "Holding breath",
            "Looking up and straining neck"
        ]
    },
    "crunch": {
        "name": "Crunch",
        "type": "isolation",
        "primary_muscles": ["abs"],
        "secondary_muscles": [],
        "equipment": ["bodyweight"],
        "difficulty": "beginner",
        "form_tips": [
            "Lie on your back with knees bent and feet flat",
            "Place hands behind your head or across your chest",
            "Curl your shoulders off the ground by contracting abs",
            "Don't pull on your neck",
            "Focus on the squeeze at the top",
            "Lower with control",
            "Keep your lower back pressed into the floor"
        ],
        "common_mistakes": [
            "Pulling on the neck",
            "Using momentum",
            "Coming up too high (it's a crunch, not a sit-up)"
        ]
    },
    "hanging leg raise": {
        "name": "Hanging Leg Raise",
        "type": "isolation",
        "primary_muscles": ["abs", "hip_flexors"],
        "secondary_muscles": ["forearms"],
        "equipment": ["pull-up_bar"],
        "difficulty": "intermediate",
        "form_tips": [
            "Hang from a bar with arms fully extended",
            "Keep your legs straight or slightly bent",
            "Raise your legs by contracting your abs",
            "Lift until legs are parallel to floor or higher",
            "Control the descent - don't swing",
            "Keep your body from swinging",
            "For added difficulty, raise legs all the way to the bar"
        ],
        "common_mistakes": [
            "Swinging to generate momentum",
            "Bending knees too much",
            "Not controlling the negative"
        ]
    },
    "russian twist": {
        "name": "Russian Twist",
        "type": "isolation",
        "primary_muscles": ["obliques", "abs"],
        "secondary_muscles": [],
        "equipment": ["bodyweight", "weight_plate"],
        "difficulty": "beginner",
        "form_tips": [
            "Sit with knees bent and feet off the floor",
            "Lean back slightly to engage your core",
            "Rotate your torso from side to side",
            "Keep your core tight throughout",
            "Touch the floor beside you on each rotation",
            "Move in a controlled manner",
            "Add weight for more difficulty"
        ],
        "common_mistakes": [
            "Moving too fast",
            "Not rotating fully",
            "Letting feet touch the ground"
        ]
    },
    "dead bug": {
        "name": "Dead Bug",
        "type": "isolation",
        "primary_muscles": ["core"],
        "secondary_muscles": [],
        "equipment": ["bodyweight"],
        "difficulty": "beginner",
        "form_tips": [
            "Lie on your back with arms extended toward ceiling",
            "Lift legs with knees bent at 90 degrees",
            "Press your lower back into the floor",
            "Slowly lower opposite arm and leg toward the floor",
            "Return to start and repeat on other side",
            "Keep your lower back pressed down throughout",
            "Move slowly and with control"
        ],
        "common_mistakes": [
            "Lower back coming off the floor",
            "Moving too quickly",
            "Not extending fully"
        ]
    },

    # CARDIO EXERCISES
    "running": {
        "name": "Running",
        "type": "cardio",
        "primary_muscles": ["legs", "cardiovascular"],
        "secondary_muscles": ["core"],
        "equipment": ["treadmill", "outdoors"],
        "difficulty": "beginner",
        "form_tips": [
            "Land on your midfoot, not your heel",
            "Keep your cadence high (aim for 170-180 steps/min)",
            "Run tall with slight forward lean from ankles",
            "Keep arms relaxed and swinging naturally",
            "Don't overstride - feet should land under your hips",
            "Breathe rhythmically",
            "Start slow and build up gradually"
        ],
        "common_mistakes": [
            "Overstriding (landing heel-first far in front)",
            "Tensing up shoulders and arms",
            "Looking down instead of ahead"
        ]
    },
    "cycling": {
        "name": "Cycling",
        "type": "cardio",
        "primary_muscles": ["quadriceps", "cardiovascular"],
        "secondary_muscles": ["hamstrings", "glutes", "calves"],
        "equipment": ["stationary_bike", "bicycle"],
        "difficulty": "beginner",
        "form_tips": [
            "Adjust seat height so leg is almost extended at bottom",
            "Keep your core engaged",
            "Pull up on pedals as well as pushing down",
            "Keep knees tracking straight, not bowing out",
            "Relax your grip on the handlebars",
            "Maintain a steady cadence (80-100 RPM)"
        ],
        "common_mistakes": [
            "Seat too low or too high",
            "Bouncing in the saddle",
            "Gripping handlebars too tightly"
        ]
    },
    "rowing": {
        "name": "Rowing",
        "type": "cardio",
        "primary_muscles": ["back", "legs", "cardiovascular"],
        "secondary_muscles": ["arms", "core"],
        "equipment": ["rowing_machine"],
        "difficulty": "intermediate",
        "form_tips": [
            "Drive with your legs first",
            "Then lean back slightly and pull with arms",
            "Handle should come to lower chest",
            "Reverse the motion: arms, lean, then legs",
            "Keep your back straight throughout",
            "Don't rush the recovery - it should be slower than the drive",
            "Aim for a 1:2 ratio of drive to recovery"
        ],
        "common_mistakes": [
            "Pulling with arms before legs are extended",
            "Rushing the recovery",
            "Leaning back too far"
        ]
    },
    "jump rope": {
        "name": "Jump Rope",
        "type": "cardio",
        "primary_muscles": ["calves", "cardiovascular"],
        "secondary_muscles": ["shoulders", "core"],
        "equipment": ["jump_rope"],
        "difficulty": "beginner",
        "form_tips": [
            "Turn the rope with your wrists, not your whole arm",
            "Jump just high enough to clear the rope",
            "Land softly on the balls of your feet",
            "Keep your core engaged",
            "Start slow and build up speed",
            "Keep elbows close to your sides"
        ],
        "common_mistakes": [
            "Jumping too high",
            "Using whole arms to turn rope",
            "Landing flat-footed"
        ]
    },
    "stair climbing": {
        "name": "Stair Climbing",
        "type": "cardio",
        "primary_muscles": ["quadriceps", "glutes", "cardiovascular"],
        "secondary_muscles": ["calves", "hamstrings"],
        "equipment": ["stairs", "stair_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Keep your torso upright",
            "Push through your whole foot",
            "Don't lean heavily on the handrails",
            "Take each step deliberately",
            "Keep a steady pace",
            "Engage your core for balance"
        ],
        "common_mistakes": [
            "Leaning on handrails too much",
            "Taking steps too quickly",
            "Hunching over"
        ]
    },
    "elliptical": {
        "name": "Elliptical",
        "type": "cardio",
        "primary_muscles": ["legs", "cardiovascular"],
        "secondary_muscles": ["arms", "core"],
        "equipment": ["elliptical_machine"],
        "difficulty": "beginner",
        "form_tips": [
            "Stand tall with good posture",
            "Push and pull with both arms and legs",
            "Keep your weight in your heels",
            "Don't lean on the handles",
            "Vary resistance and incline for challenge",
            "Maintain a smooth, fluid motion"
        ],
        "common_mistakes": [
            "Leaning on handles",
            "Only using legs, not arms",
            "Standing on toes instead of heels"
        ]
    }
}

# Common dish calorie database for estimation
COMMON_DISHES = {
    # American/Western
    "burger": {"homemade": 500, "restaurant": 700, "protein": 25, "carbs": 40, "fat": 30},
    "cheeseburger": {"homemade": 550, "restaurant": 800, "protein": 28, "carbs": 42, "fat": 35},
    "pizza slice": {"homemade": 250, "restaurant": 350, "protein": 12, "carbs": 30, "fat": 12},
    "pizza": {"homemade": 2000, "restaurant": 2500, "protein": 80, "carbs": 240, "fat": 90},
    "grilled chicken": {"homemade": 300, "restaurant": 400, "protein": 40, "carbs": 5, "fat": 12},
    "chicken breast": {"homemade": 280, "restaurant": 350, "protein": 45, "carbs": 0, "fat": 8},
    "steak": {"homemade": 400, "restaurant": 550, "protein": 45, "carbs": 0, "fat": 25},
    "salmon": {"homemade": 350, "restaurant": 450, "protein": 40, "carbs": 0, "fat": 20},
    "pasta": {"homemade": 450, "restaurant": 650, "protein": 15, "carbs": 70, "fat": 15},
    "spaghetti": {"homemade": 500, "restaurant": 700, "protein": 18, "carbs": 75, "fat": 18},
    "mac and cheese": {"homemade": 400, "restaurant": 600, "protein": 15, "carbs": 45, "fat": 20},
    "caesar salad": {"homemade": 300, "restaurant": 450, "protein": 15, "carbs": 15, "fat": 25},
    "garden salad": {"homemade": 100, "restaurant": 150, "protein": 3, "carbs": 12, "fat": 6},
    "french fries": {"homemade": 300, "restaurant": 450, "protein": 4, "carbs": 50, "fat": 15},
    "sandwich": {"homemade": 400, "restaurant": 550, "protein": 20, "carbs": 45, "fat": 18},
    "sub sandwich": {"homemade": 500, "restaurant": 700, "protein": 25, "carbs": 60, "fat": 22},
    "hot dog": {"homemade": 300, "restaurant": 400, "protein": 12, "carbs": 25, "fat": 18},
    "tacos": {"homemade": 400, "restaurant": 550, "protein": 20, "carbs": 35, "fat": 22},
    "burrito": {"homemade": 550, "restaurant": 800, "protein": 25, "carbs": 70, "fat": 25},
    "nachos": {"homemade": 500, "restaurant": 800, "protein": 15, "carbs": 55, "fat": 30},
    "wings": {"homemade": 400, "restaurant": 600, "protein": 30, "carbs": 5, "fat": 30},
    "fried chicken": {"homemade": 450, "restaurant": 600, "protein": 35, "carbs": 15, "fat": 30},

    # Asian
    "fried rice": {"homemade": 400, "restaurant": 550, "protein": 12, "carbs": 60, "fat": 15},
    "lo mein": {"homemade": 450, "restaurant": 600, "protein": 15, "carbs": 65, "fat": 18},
    "kung pao chicken": {"homemade": 400, "restaurant": 550, "protein": 30, "carbs": 25, "fat": 22},
    "orange chicken": {"homemade": 450, "restaurant": 600, "protein": 25, "carbs": 50, "fat": 22},
    "general tso chicken": {"homemade": 450, "restaurant": 600, "protein": 25, "carbs": 55, "fat": 25},
    "sweet and sour chicken": {"homemade": 400, "restaurant": 550, "protein": 22, "carbs": 50, "fat": 18},
    "beef and broccoli": {"homemade": 350, "restaurant": 450, "protein": 28, "carbs": 20, "fat": 18},
    "sushi roll": {"homemade": 300, "restaurant": 400, "protein": 12, "carbs": 45, "fat": 8},
    "sashimi": {"homemade": 150, "restaurant": 200, "protein": 25, "carbs": 0, "fat": 5},
    "ramen": {"homemade": 500, "restaurant": 700, "protein": 25, "carbs": 70, "fat": 22},
    "pho": {"homemade": 400, "restaurant": 500, "protein": 25, "carbs": 50, "fat": 12},
    "pad thai": {"homemade": 500, "restaurant": 700, "protein": 20, "carbs": 70, "fat": 22},
    "curry": {"homemade": 450, "restaurant": 600, "protein": 25, "carbs": 35, "fat": 28},
    "tikka masala": {"homemade": 500, "restaurant": 700, "protein": 30, "carbs": 30, "fat": 32},
    "biryani": {"homemade": 550, "restaurant": 750, "protein": 28, "carbs": 70, "fat": 22},
    "naan": {"homemade": 200, "restaurant": 300, "protein": 6, "carbs": 40, "fat": 6},
    "samosa": {"homemade": 200, "restaurant": 300, "protein": 5, "carbs": 25, "fat": 12},
    "dumplings": {"homemade": 300, "restaurant": 400, "protein": 12, "carbs": 35, "fat": 12},
    "spring rolls": {"homemade": 200, "restaurant": 300, "protein": 6, "carbs": 25, "fat": 10},

    # Mediterranean
    "hummus": {"homemade": 150, "restaurant": 200, "protein": 6, "carbs": 15, "fat": 10},
    "falafel": {"homemade": 300, "restaurant": 400, "protein": 12, "carbs": 35, "fat": 15},
    "shawarma": {"homemade": 450, "restaurant": 600, "protein": 30, "carbs": 40, "fat": 22},
    "kebab": {"homemade": 350, "restaurant": 450, "protein": 35, "carbs": 10, "fat": 20},
    "gyro": {"homemade": 500, "restaurant": 700, "protein": 25, "carbs": 45, "fat": 28},
    "greek salad": {"homemade": 250, "restaurant": 350, "protein": 8, "carbs": 12, "fat": 22},

    # Breakfast
    "eggs": {"homemade": 200, "restaurant": 250, "protein": 14, "carbs": 2, "fat": 15},
    "scrambled eggs": {"homemade": 220, "restaurant": 300, "protein": 14, "carbs": 3, "fat": 18},
    "omelette": {"homemade": 300, "restaurant": 450, "protein": 20, "carbs": 5, "fat": 22},
    "pancakes": {"homemade": 350, "restaurant": 500, "protein": 8, "carbs": 55, "fat": 12},
    "waffles": {"homemade": 400, "restaurant": 550, "protein": 8, "carbs": 60, "fat": 15},
    "french toast": {"homemade": 350, "restaurant": 500, "protein": 10, "carbs": 45, "fat": 15},
    "bacon": {"homemade": 200, "restaurant": 250, "protein": 15, "carbs": 0, "fat": 16},
    "sausage": {"homemade": 250, "restaurant": 300, "protein": 12, "carbs": 2, "fat": 22},
    "oatmeal": {"homemade": 200, "restaurant": 300, "protein": 6, "carbs": 35, "fat": 4},
    "cereal": {"homemade": 250, "restaurant": 300, "protein": 6, "carbs": 45, "fat": 3},
    "bagel": {"homemade": 300, "restaurant": 400, "protein": 10, "carbs": 55, "fat": 3},
    "toast": {"homemade": 150, "restaurant": 200, "protein": 4, "carbs": 25, "fat": 4},
    "croissant": {"homemade": 250, "restaurant": 350, "protein": 5, "carbs": 30, "fat": 14},
    "muffin": {"homemade": 300, "restaurant": 450, "protein": 5, "carbs": 50, "fat": 12},
    "smoothie": {"homemade": 250, "restaurant": 400, "protein": 8, "carbs": 45, "fat": 5},

    # Soups
    "chicken soup": {"homemade": 200, "restaurant": 300, "protein": 15, "carbs": 20, "fat": 8},
    "tomato soup": {"homemade": 150, "restaurant": 250, "protein": 4, "carbs": 25, "fat": 5},
    "vegetable soup": {"homemade": 100, "restaurant": 150, "protein": 4, "carbs": 18, "fat": 2},
    "clam chowder": {"homemade": 300, "restaurant": 450, "protein": 12, "carbs": 25, "fat": 20},

    # Snacks/Sides
    "rice": {"homemade": 200, "restaurant": 250, "protein": 4, "carbs": 45, "fat": 0},
    "mashed potatoes": {"homemade": 200, "restaurant": 300, "protein": 4, "carbs": 30, "fat": 8},
    "baked potato": {"homemade": 200, "restaurant": 350, "protein": 5, "carbs": 45, "fat": 8},
    "chips": {"homemade": 150, "restaurant": 200, "protein": 2, "carbs": 15, "fat": 10},
    "popcorn": {"homemade": 100, "restaurant": 200, "protein": 3, "carbs": 20, "fat": 5},
    "nuts": {"homemade": 200, "restaurant": 200, "protein": 6, "carbs": 8, "fat": 18},
    "fruit": {"homemade": 80, "restaurant": 100, "protein": 1, "carbs": 20, "fat": 0},
    "yogurt": {"homemade": 150, "restaurant": 200, "protein": 10, "carbs": 20, "fat": 4},
    "protein bar": {"homemade": 200, "restaurant": 250, "protein": 20, "carbs": 25, "fat": 8},
    "protein shake": {"homemade": 200, "restaurant": 300, "protein": 30, "carbs": 15, "fat": 5},

    # Desserts
    "ice cream": {"homemade": 250, "restaurant": 350, "protein": 4, "carbs": 30, "fat": 14},
    "cake": {"homemade": 350, "restaurant": 500, "protein": 4, "carbs": 55, "fat": 15},
    "brownie": {"homemade": 250, "restaurant": 350, "protein": 3, "carbs": 35, "fat": 12},
    "cookie": {"homemade": 150, "restaurant": 200, "protein": 2, "carbs": 22, "fat": 7},
    "donut": {"homemade": 250, "restaurant": 350, "protein": 3, "carbs": 35, "fat": 14},
    "cheesecake": {"homemade": 350, "restaurant": 500, "protein": 6, "carbs": 35, "fat": 25},

    # Drinks
    "coffee": {"homemade": 5, "restaurant": 5, "protein": 0, "carbs": 0, "fat": 0},
    "latte": {"homemade": 150, "restaurant": 200, "protein": 8, "carbs": 15, "fat": 6},
    "cappuccino": {"homemade": 100, "restaurant": 150, "protein": 6, "carbs": 10, "fat": 5},
    "soda": {"homemade": 150, "restaurant": 200, "protein": 0, "carbs": 40, "fat": 0},
    "juice": {"homemade": 120, "restaurant": 150, "protein": 1, "carbs": 30, "fat": 0},
    "beer": {"homemade": 150, "restaurant": 200, "protein": 1, "carbs": 13, "fat": 0},
    "wine": {"homemade": 120, "restaurant": 150, "protein": 0, "carbs": 4, "fat": 0},
}


def get_exercise(name: str) -> Optional[dict]:
    """Get an exercise by name (case-insensitive)."""
    name_lower = name.lower()
    if name_lower in EXERCISES:
        return EXERCISES[name_lower]
    # Try partial match
    for key, exercise in EXERCISES.items():
        if name_lower in key or key in name_lower:
            return exercise
    return None


def search_exercises(query: str) -> List[dict]:
    """Search for exercises matching a query."""
    query_lower = query.lower()
    results = []
    for key, exercise in EXERCISES.items():
        if query_lower in key or query_lower in exercise["name"].lower():
            results.append(exercise)
        elif any(query_lower in muscle for muscle in exercise["primary_muscles"]):
            results.append(exercise)
    return results


def get_exercises_by_muscle(muscle: str) -> List[dict]:
    """Get all exercises that target a specific muscle group."""
    muscle_lower = muscle.lower()
    results = []
    for exercise in EXERCISES.values():
        if muscle_lower in exercise["primary_muscles"] or muscle_lower in exercise["secondary_muscles"]:
            results.append(exercise)
    return results


def get_form_tips(exercise_name: str) -> List[str]:
    """Get form tips for a specific exercise."""
    exercise = get_exercise(exercise_name)
    if exercise:
        return exercise.get("form_tips", [])
    return []


def estimate_food_calories(dish_name: str, is_homemade: bool = True) -> dict:
    """Estimate calories and macros for a dish."""
    dish_lower = dish_name.lower()

    # Direct match
    if dish_lower in COMMON_DISHES:
        dish = COMMON_DISHES[dish_lower]
        calories = dish["homemade"] if is_homemade else dish["restaurant"]
        return {
            "calories": calories,
            "protein": dish["protein"],
            "carbs": dish["carbs"],
            "fat": dish["fat"]
        }

    # Partial match
    for key, dish in COMMON_DISHES.items():
        if key in dish_lower or dish_lower in key:
            calories = dish["homemade"] if is_homemade else dish["restaurant"]
            return {
                "calories": calories,
                "protein": dish["protein"],
                "carbs": dish["carbs"],
                "fat": dish["fat"]
            }

    # Default estimate based on type hints in the name
    if any(word in dish_lower for word in ["salad", "vegetable", "veg"]):
        return {"calories": 200 if is_homemade else 300, "protein": 5, "carbs": 20, "fat": 10}
    elif any(word in dish_lower for word in ["fried", "crispy", "deep"]):
        return {"calories": 500 if is_homemade else 700, "protein": 20, "carbs": 40, "fat": 30}
    elif any(word in dish_lower for word in ["grilled", "baked", "steamed"]):
        return {"calories": 300 if is_homemade else 400, "protein": 30, "carbs": 15, "fat": 12}
    elif any(word in dish_lower for word in ["soup", "broth"]):
        return {"calories": 150 if is_homemade else 250, "protein": 10, "carbs": 15, "fat": 5}
    elif any(word in dish_lower for word in ["dessert", "sweet", "cake", "ice"]):
        return {"calories": 350 if is_homemade else 500, "protein": 4, "carbs": 50, "fat": 15}

    # Generic default
    return {"calories": 400 if is_homemade else 600, "protein": 20, "carbs": 40, "fat": 18}
