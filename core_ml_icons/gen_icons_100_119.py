#!/usr/bin/env python3
from pathlib import Path
import csv, json

base = Path("/Users/idjugostran/Projects/icons-ai/core_ml_icons")
icons_dir = base / "icons"

def write_csv(fp, rows):
    with open(fp, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(["text", "label"])
        for r in rows:
            w.writerow(r)

def process_icon(icon, st_en, pst_en, reg_en, conv_en, typo_en, bnd_en, valid_en, test_en):
    icon_dir = icons_dir / icon
    icon_dir.mkdir(parents=True, exist_ok=True)

    train_en = [(t, icon) for t in st_en + pst_en + reg_en + conv_en + typo_en + bnd_en]

    write_csv(icon_dir / "train_en.csv", train_en)
    write_csv(icon_dir / "valid_en.csv", [(t, icon) for t in valid_en])
    write_csv(icon_dir / "test_en.csv",  [(t, icon) for t in test_en])

    icon_log = {
        "icon": icon,
        "rows": {"train_en": len(train_en), "valid_en": 3, "test_en": 3},
        "categories": {
            "search_terms":           {"en": st_en},
            "phrase_per_search_term": {"en": pst_en},
            "regular":                {"en": reg_en},
            "conversational":         {"en": conv_en},
            "typo":                   {"en": typo_en},
            "boundary":               {"en": bnd_en},
            "valid":                  {"en": valid_en},
            "test":                   {"en": test_en},
        }
    }
    with open(icon_dir / "icon_log.json", "w", encoding="utf-8") as f:
        json.dump(icon_log, f, ensure_ascii=False, indent=2)

    n_st, n_pst = len(st_en), len(pst_en)
    print(f"  {icon}: {len(train_en)} train rows  ({n_st} st + {n_pst} pst + 24)")

# ============================================================
# 100. chimney
# ============================================================
process_icon(
    "chimney",
    st_en = ["brick", "exhaust", "fireplace", "house", "roof", "vent"],
    pst_en = [
        "Clean the brick chimney", "Repair cracked bricks on the chimney",
        "Clear the exhaust pipe", "Fix the exhaust blockage",
        "Light the fireplace tonight", "Clean the fireplace ash",
        "Inspect the chimney on the house", "Paint the house chimney",
        "Check the chimney on the roof", "Seal the roof chimney flashing",
        "Clear the chimney vent", "Inspect the vent cap",
    ],
    reg_en = [
        "Hire a chimney sweep",
        "Schedule chimney inspection before winter",
        "Clean out the accumulated soot",
        "Get the chimney professionally checked",
        "Fix the broken chimney cap",
        "Clear a bird nest from the chimney",
        "Install a chimney liner",
        "Reseal the chimney flashing",
        "Check chimney for cracks",
        "Have the flue cleaned",
    ],
    conv_en = [
        "Clean that chimney",
        "Chimney needs sweeping",
        "Get the fireplace going",
        "Chimney's blocked again",
    ],
    typo_en = [
        "chimey sweep appointment",
        "fireplce cleaning",
        "cimney inspection",
        "exhuast vent blocked",
    ],
    bnd_en = [
        "Fix the roof tiles after the storm",
        "Paint the exterior house walls",
        "Repair the attic insulation",
        "Replace cracked roof shingles",
        "Install a wood burning stove indoors",
        "Fix the leaking skylight",
    ],
    valid_en = [
        "Schedule annual chimney cleaning",
        "Check if the chimney is blocked",
        "Book a chimney sweep appointment",
    ],
    test_en = [
        "Get the chimney swept before winter",
        "Repair the chimney flue",
        "Chimney maintenance needed",
    ],
)

# ============================================================
# 101. chopsticks
# ============================================================
process_icon(
    "chopsticks",
    st_en = ["bamboo", "chopsticks", "utensils"],
    pst_en = [
        "Buy bamboo chopsticks", "Get reusable bamboo utensils",
        "Learn to use chopsticks", "Eat with chopsticks tonight",
        "Pack utensils for lunch", "Get proper utensils for sushi",
    ],
    reg_en = [
        "Order sushi for dinner",
        "Cook ramen at home",
        "Go to a Japanese restaurant",
        "Pack Asian food for lunch",
        "Try eating with chopsticks",
        "Buy a chopstick set",
        "Make stir-fry tonight",
        "Have dim sum this weekend",
        "Cook Pad Thai for dinner",
        "Visit a Chinese restaurant",
    ],
    conv_en = [
        "Sushi night!",
        "Grab some chopsticks",
        "Asian food run",
        "Ramen craving",
    ],
    typo_en = [
        "chopsticsk for sushi",
        "bamboo utensilss",
        "order ramen noodels",
        "eat with choptsicks",
    ],
    bnd_en = [
        "Set the table with forks and knives",
        "Grab a spoon for the soup",
        "Order pizza for delivery",
        "Use a fork for pasta",
        "Get a spatula for cooking",
        "Pick up some plastic cutlery",
    ],
    valid_en = [
        "Have sushi with chopsticks",
        "Cook Asian noodles for dinner",
        "Get bamboo reusable utensils",
    ],
    test_en = [
        "Order Thai food for the family",
        "Eat ramen with chopsticks",
        "Japanese dinner tonight",
    ],
)

# ============================================================
# 102. clapperboard
# ============================================================
process_icon(
    "clapperboard",
    st_en = ["camera", "clapper", "clapper board", "director", "film", "movie", "record"],
    pst_en = [
        "Set up the camera for filming", "Buy a camera for the video shoot",
        "Use the clapper on set", "Get the clapper ready for the take",
        "Bring the clapper board to the shoot", "Mark the scene with the clapper board",
        "Work as a film director", "Direct the next scene",
        "Buy film rolls for the camera", "Develop the film rolls",
        "Attend the movie audition", "Watch the premiere of the movie",
        "Record the short film today", "Record the promotional video",
    ],
    reg_en = [
        "Film the birthday party video",
        "Schedule a professional video shoot",
        "Edit the short film project",
        "Plan the scenes for the movie",
        "Hire a videographer for the event",
        "Practice acting for the audition",
        "Write a screenplay",
        "Attend a film production class",
        "Set up lighting for the shoot",
        "Review the behind-the-scenes footage",
    ],
    conv_en = [
        "Action!",
        "Movie shoot today",
        "Film something cool",
        "Shooting a scene now",
    ],
    typo_en = [
        "film the moive",
        "clapperborad on set",
        "hire a diractor",
        "recrod the video",
    ],
    bnd_en = [
        "Watch a movie on Netflix",
        "Buy movie tickets online",
        "Set up a podcast recording",
        "Take photos at the event",
        "Stream the live concert",
        "Download a TV show episode",
    ],
    valid_en = [
        "Prepare the set for filming",
        "Organize a video shoot",
        "Bring the clapperboard to production",
    ],
    test_en = [
        "Direct the school play video",
        "Film the documentary scene",
        "Start shooting the short film",
    ],
)

# ============================================================
# 103. clipboard-list
# ============================================================
process_icon(
    "clipboard-list",
    st_en = ["cheatsheet", "checklist", "completed", "done", "finished", "itinerary", "schedule", "summary", "survey", "tick", "todo", "wishlist"],
    pst_en = [
        "Make a cheatsheet for the exam", "Use a cheatsheet at the meeting",
        "Create a checklist for the trip", "Follow the project checklist",
        "Mark tasks as completed", "Review completed items on the list",
        "Mark the task as done", "Check what's done already",
        "See what's finished", "Wrap up the finished tasks",
        "Plan the travel itinerary", "Review the trip itinerary",
        "Build a daily schedule", "Update the work schedule",
        "Write a project summary", "Read the meeting summary",
        "Send out a customer survey", "Fill out the feedback survey",
        "Put a tick on the task", "Tick off each item on the list",
        "Add an item to the todo list", "Review today's todo list",
        "Add gifts to my wishlist", "Check my wishlist",
    ],
    reg_en = [
        "Make a grocery list",
        "Create a daily to-do list",
        "Plan tasks for tomorrow",
        "Review my weekly checklist",
        "Organize the project tasks",
        "Check off completed items",
        "Plan the meeting agenda",
        "Write down everything I need to do",
        "Set priorities for the week",
        "Track daily habits",
    ],
    conv_en = [
        "Quick task list",
        "Write that stuff down",
        "Check off the list",
        "What's left to do?",
    ],
    typo_en = [
        "create a chcklist",
        "to-od list for tomorrow",
        "review the scheduel",
        "add to my whishlist",
    ],
    bnd_en = [
        "Set a meeting reminder in the calendar",
        "Write notes in my journal",
        "Send a calendar invite",
        "Draft a project proposal",
        "Archive old documents",
        "Update the project Gantt chart",
    ],
    valid_en = [
        "Go through my checklist",
        "Plan tomorrow's tasks",
        "Review the to-do list",
    ],
    test_en = [
        "Complete the task list",
        "Organize daily activities",
        "Create a project checklist",
    ],
)

# ============================================================
# 104. clock
# ============================================================
process_icon(
    "clock",
    st_en = ["clock", "date", "hour", "late", "minute", "pending", "schedule", "time", "timer", "timestamp", "watch"],
    pst_en = [
        "Check the clock on the wall", "Hang a new clock in the kitchen",
        "Check today's date", "Set the date on the calendar",
        "Work for one more hour", "Take an hour-long break",
        "Running late to the meeting", "Don't be late for class",
        "Give me five more minutes", "Set a five-minute reminder",
        "Review pending tasks", "Check pending approvals",
        "Check my schedule for today", "Update the work schedule",
        "What time is it?", "Manage time better this week",
        "Set a timer for 20 minutes", "Start the cooking timer",
        "Add a timestamp to the file", "Check the timestamp on the email",
        "Buy a new watch", "Check my watch",
    ],
    reg_en = [
        "Set a reminder for 3pm",
        "Check what time the meeting starts",
        "Be on time for the appointment",
        "Set a timer for cooking",
        "Track how long the task takes",
        "Schedule the event at the right time",
        "Know when the store closes",
        "Check the opening hours",
        "Time myself on this task",
        "Plan around the time zone difference",
    ],
    conv_en = [
        "What time is it?",
        "Don't be late!",
        "Running late again",
        "Need more time",
    ],
    typo_en = [
        "set the clokc on the wall",
        "check my watche",
        "scheudle for tomorrow",
        "timer for 20 minuets",
    ],
    bnd_en = [
        "Set an alarm to wake up at 7am",
        "Add event to the calendar",
        "Set a countdown for the race",
        "Book an appointment",
        "Snooze the morning alarm",
        "Set a recurring daily alarm",
    ],
    valid_en = [
        "Check the time for the meeting",
        "Set a timer while cooking",
        "Track time on the project",
    ],
    test_en = [
        "Know when to leave for work",
        "Set a work timer",
        "Check what time it is now",
    ],
)

# ============================================================
# 105. clothes-hanger
# ============================================================
process_icon(
    "clothes-hanger",
    st_en = ["clothing", "dry cleaner", "hang", "wire"],
    pst_en = [
        "Organize clothing in the wardrobe", "Sort clothing by season",
        "Drop off at the dry cleaner", "Pick up from the dry cleaner",
        "Hang the jacket up", "Hang freshly washed clothes",
        "Use wire hangers from the cleaner", "Replace wire hangers with wood ones",
    ],
    reg_en = [
        "Organize the wardrobe",
        "Hang up the laundry",
        "Sort clothes by color",
        "Pick up dry cleaning",
        "Buy new hangers for the closet",
        "Declutter the closet",
        "Hang the dress for tomorrow",
        "Pack clothes for the trip",
        "Put away clean laundry",
        "Rotate seasonal clothes",
    ],
    conv_en = [
        "Hang that up",
        "Closet's a mess",
        "Drop off the dry cleaning",
        "Wardrobe sort",
    ],
    typo_en = [
        "hang the laundrey",
        "dry clener pickup",
        "orgnaize the wardrobe",
        "colthes need hanging",
    ],
    bnd_en = [
        "Fold laundry and put it away",
        "Iron the shirts before work",
        "Do a load of laundry",
        "Buy a new outfit",
        "Pack a suitcase for travel",
        "Donate clothes to charity",
    ],
    valid_en = [
        "Organize clothes on hangers",
        "Pick up dry cleaning today",
        "Hang up wardrobe items",
    ],
    test_en = [
        "Sort through the closet",
        "Hang the clean clothes",
        "Drop clothes at dry cleaner",
    ],
)

# ============================================================
# 106. cloud-meatball
# ============================================================
process_icon(
    "cloud-meatball",
    st_en = ["FLDSMDFR", "food", "spaghetti", "storm"],
    pst_en = [
        "Watch Cloudy with a Chance of Meatballs", "Build the FLDSMDFR machine",
        "Order food delivery during the storm", "Cook comfort food on a rainy day",
        "Make spaghetti and meatballs", "Cook spaghetti for dinner",
        "Prepare for the coming storm", "Stay inside during the storm",
    ],
    reg_en = [
        "Cook pasta for dinner",
        "Make meatballs from scratch",
        "Prepare spaghetti bolognese",
        "Order Italian food delivery",
        "Cook comfort food on a rainy night",
        "Make a big pot of pasta",
        "Italian food night at home",
        "Make homemade marinara sauce",
        "Pasta and meatball recipe",
        "Cook dinner while it rains outside",
    ],
    conv_en = [
        "Spaghetti night!",
        "Meatball time",
        "Pasta dinner",
        "Comfort food weather",
    ],
    typo_en = [
        "make spagetti and meatbals",
        "pasta dinnre tonight",
        "meatbal recipe",
        "cook spagetti bolognese",
    ],
    bnd_en = [
        "Check the thunderstorm forecast",
        "Prepare for the heavy rainfall",
        "Order pizza delivery",
        "Make a grilled cheese sandwich",
        "Cook soup on a cold day",
        "Buy groceries before the storm hits",
    ],
    valid_en = [
        "Make spaghetti and meatballs",
        "Cook Italian food for dinner",
        "Pasta night at home",
    ],
    test_en = [
        "Prepare the meatball recipe",
        "Cook pasta from scratch",
        "Italian dinner tonight",
    ],
)

# ============================================================
# 107. cloud-music
# ============================================================
process_icon(
    "cloud-music",
    st_en = ["download", "music", "spotify", "streaming"],
    pst_en = [
        "Download the album for offline listening", "Download music before the flight",
        "Listen to music on the go", "Discover new music today",
        "Subscribe to Spotify premium", "Make a Spotify playlist",
        "Stream music while working", "Find a music streaming service",
    ],
    reg_en = [
        "Make a playlist for the gym",
        "Listen to music while cooking",
        "Discover new artists this week",
        "Download songs for offline listening",
        "Subscribe to a music streaming service",
        "Create a road trip playlist",
        "Sync music library to phone",
        "Find background music for work",
        "Share a playlist with friends",
        "Explore a new music genre",
    ],
    conv_en = [
        "Need some tunes",
        "Download that song",
        "Music vibes",
        "Playlist time",
    ],
    typo_en = [
        "dowload the song",
        "stremaing music app",
        "subsricbe to spotify",
        "lsiten to music online",
    ],
    bnd_en = [
        "Watch a music video on YouTube",
        "Buy a concert ticket",
        "Listen to a podcast episode",
        "Play music from a CD",
        "Tune in to the radio station",
        "Watch a live music stream",
    ],
    valid_en = [
        "Stream music while working",
        "Download a playlist for offline use",
        "Listen to new music releases",
    ],
    test_en = [
        "Make a gym workout playlist",
        "Subscribe to music streaming",
        "Find new songs online",
    ],
)

# ============================================================
# 108. cloud-sun
# ============================================================
process_icon(
    "cloud-sun",
    st_en = ["clear", "cloud", "day", "daytime", "fall", "outdoors", "overcast", "partly cloudy", "sun", "sun behind cloud"],
    pst_en = [
        "Enjoy clear weather today", "Clear skies for the picnic",
        "Clouds rolling in this afternoon", "Watch the clouds pass by",
        "Have a great day outside", "Plan activities for the day",
        "Enjoy the daytime sunshine", "Go out during daytime hours",
        "Take kids out on a fall day", "Enjoy the cool fall weather",
        "Take the kids to play outdoors", "Plan an outdoor activity",
        "Overcast but still warm outside", "Dress for overcast weather",
        "Partly cloudy morning ahead", "Partly cloudy but pleasant",
        "Enjoy the sun between clouds", "Sun is out today",
        "Sun peeking behind the clouds", "Enjoy sun behind cloud weather",
    ],
    reg_en = [
        "Check the weather before going out",
        "Plan a picnic for a partly cloudy day",
        "Take a walk in mild weather",
        "Wear sunscreen even on a cloudy day",
        "Pack a light jacket for the day",
        "Check if it will rain today",
        "Go for a run in mild weather",
        "Enjoy the mild sunny day",
        "Do outdoor chores today",
        "Plan a bike ride for later",
    ],
    conv_en = [
        "Nice-ish day out",
        "Little bit cloudy",
        "Sunny with some clouds",
        "Not bad weather today",
    ],
    typo_en = [
        "partly clouyd day",
        "check the wheter outside",
        "cloudy but suny",
        "go outdors today",
    ],
    bnd_en = [
        "Heavy rain expected all day",
        "Full sunshine and no clouds",
        "Thunderstorm warning issued",
        "Wear a raincoat today",
        "Bring an umbrella for the day",
        "Snow expected this afternoon",
    ],
    valid_en = [
        "Partly cloudy day ahead",
        "Check weather for outdoor plans",
        "Nice day with some clouds",
    ],
    test_en = [
        "Take a walk on a partly cloudy day",
        "Mild weather for outdoor activities",
        "Enjoy cloud-and-sun weather",
    ],
)

# ============================================================
# 109. clouds-sun
# ============================================================
process_icon(
    "clouds-sun",
    st_en = ["cloudy", "day", "moonlight", "overcast", "sky", "summer"],
    pst_en = [
        "It's going to be cloudy today", "Dress for a cloudy day",
        "Enjoy the day despite the clouds", "Plan the day around the weather",
        "Walk under the moonlight tonight", "Enjoy the moonlight after dinner",
        "Overcast sky this morning", "Overcast but warm today",
        "Look at the beautiful sky", "Photograph the dramatic sky",
        "Summer clouds rolling in", "Enjoy a warm cloudy summer day",
    ],
    reg_en = [
        "Plan outdoor activities despite clouds",
        "Pack sunscreen for a cloudy summer day",
        "Take a walk under the cloudy sky",
        "Check if it will clear up later",
        "Plan a BBQ despite the overcast sky",
        "Go to the beach on a cloudy day",
        "Keep an umbrella handy today",
        "Enjoy mild summer weather",
        "Play outside while it's not raining",
        "Take photos of the dramatic clouds",
    ],
    conv_en = [
        "Bit cloudy today",
        "Summer clouds",
        "Overcast again",
        "Gloomy sky",
    ],
    typo_en = [
        "cloudey summer day",
        "overacst sky today",
        "suumer clouds outside",
        "cloudy sumemr weather",
    ],
    bnd_en = [
        "Sunny and completely clear all day",
        "Heavy rain forecast for today",
        "Thunderstorm tonight",
        "Partly cloudy with some sun breaks",
        "Cold and foggy morning",
        "Snow day today",
    ],
    valid_en = [
        "Cloudy summer day ahead",
        "Overcast sky for the picnic",
        "Check the sky before heading out",
    ],
    test_en = [
        "Plan around the cloudy weather",
        "Summer day with cloud cover",
        "Overcast but warm outside",
    ],
)

# ============================================================
# 110. code
# ============================================================
process_icon(
    "code",
    st_en = ["brackets", "code", "development", "html", "mysql", "sql"],
    pst_en = [
        "Open and close brackets properly", "Use correct brackets in the code",
        "Write clean code today", "Review the code before deploying",
        "Start a new development project", "Work on app development",
        "Write HTML for the webpage", "Learn HTML basics",
        "Optimize the MySQL database", "Write a MySQL query",
        "Optimize the SQL query", "Write a SQL script for the database",
    ],
    reg_en = [
        "Fix the bug in the app",
        "Write code for the new feature",
        "Review the pull request",
        "Set up the development environment",
        "Refactor old code",
        "Learn a new programming language",
        "Debug the failing tests",
        "Write unit tests",
        "Update the code documentation",
        "Deploy the new version",
    ],
    conv_en = [
        "Time to code",
        "Fix that bug",
        "Dev work today",
        "Write some code",
    ],
    typo_en = [
        "wriet the html code",
        "fixe the bug in code",
        "develoment project setup",
        "SQL databse query",
    ],
    bnd_en = [
        "Design the app user interface",
        "Create a database schema diagram",
        "Write the project documentation",
        "Set up cloud infrastructure",
        "Configure the server settings",
        "Manage the codebase on GitHub",
    ],
    valid_en = [
        "Write code for the new feature",
        "Fix the bug in the codebase",
        "Review the HTML structure",
    ],
    test_en = [
        "Start a new coding project",
        "Debug the application",
        "Optimize the SQL queries",
    ],
)

# ============================================================
# 111. coffee-pot
# ============================================================
process_icon(
    "coffee-pot",
    st_en = ["beverage", "breakfast", "brew", "cafe", "carafe", "drink", "morning"],
    pst_en = [
        "Make a hot beverage", "Get a beverage before the meeting",
        "Prepare a light breakfast", "Have breakfast before work",
        "Brew a fresh pot of coffee", "Brew morning espresso",
        "Visit the local cafe", "Work from the cafe today",
        "Fill the carafe with coffee", "Buy a new carafe for the office",
        "Get a hot drink to warm up", "Make a warm drink before bed",
        "Start the morning routine", "Coffee first thing in the morning",
    ],
    reg_en = [
        "Make coffee before work",
        "Buy coffee beans at the store",
        "Brew a fresh pot in the office",
        "Go to the coffee shop to work",
        "Try a new coffee blend",
        "Clean the coffee maker",
        "Fill up on coffee for the morning",
        "Get a to-go coffee",
        "Make enough coffee for everyone",
        "Set the coffee maker timer for morning",
    ],
    conv_en = [
        "Need coffee now",
        "Morning coffee run",
        "Brew a pot",
        "Coffee time!",
    ],
    typo_en = [
        "brew some cofee",
        "mornin coffee routine",
        "make a pot of coffe",
        "visti the cafe today",
    ],
    bnd_en = [
        "Make a cup of tea instead",
        "Prepare a smoothie for breakfast",
        "Get an energy drink",
        "Buy a coffee capsule machine",
        "Visit a tea shop",
        "Brew herbal tea before bed",
    ],
    valid_en = [
        "Make coffee for the morning",
        "Brew a fresh pot at the office",
        "Get coffee before the meeting",
    ],
    test_en = [
        "Go to the cafe to work",
        "Fill the coffee pot",
        "Start the morning with coffee",
    ],
)

# ============================================================
# 112. coins
# ============================================================
process_icon(
    "coins",
    st_en = ["currency", "dime", "financial", "gold", "money", "penny", "premium"],
    pst_en = [
        "Exchange currency at the airport", "Check the currency exchange rate",
        "Find a dime on the sidewalk", "Save every dime",
        "Review financial reports", "Plan the financial budget",
        "Buy gold coins as an investment", "Check gold prices today",
        "Save money for vacation", "Track daily money spending",
        "Find a lucky penny", "Count the pennies in the jar",
        "Upgrade to premium membership", "Get premium access to the app",
    ],
    reg_en = [
        "Save loose change in a jar",
        "Count coins from the piggy bank",
        "Pay for parking with coins",
        "Sort coins by denomination",
        "Deposit coins at the bank",
        "Give kids their weekly allowance",
        "Check the change from the store",
        "Roll coins to deposit at the bank",
        "Save up coins for something special",
        "Collect foreign coins from travels",
    ],
    conv_en = [
        "Counting my coins",
        "Save every penny",
        "Check my change",
        "Piggy bank time",
    ],
    typo_en = [
        "save som money",
        "exchagne currency for trip",
        "count the conis",
        "finanical planning session",
    ],
    bnd_en = [
        "Use a credit card for payment",
        "Transfer money via the bank app",
        "Check account balance",
        "Invest in the stock market",
        "Pay with cash at the register",
        "Get a discount coupon",
    ],
    valid_en = [
        "Save loose change",
        "Count coins in the jar",
        "Exchange currency for travel",
    ],
    test_en = [
        "Deposit coins at the bank",
        "Save money each week",
        "Check the change from shopping",
    ],
)

# ============================================================
# 113. command
# ============================================================
process_icon(
    "command",
    st_en = ["Place of Interest Sign", "apple key", "loop"],
    pst_en = [
        "Use the Place of Interest Sign in document", "Look up the Place of Interest Sign",
        "Press the apple key to open Spotlight", "Use the apple key shortcut",
        "Create a loop in the automation", "Use a loop to repeat the task",
    ],
    reg_en = [
        "Learn Mac keyboard shortcuts",
        "Set up automation shortcuts",
        "Use Command+Space to search",
        "Find the right key combination",
        "Create a custom keyboard shortcut",
        "Speed up workflow with shortcuts",
        "Memorize common Mac shortcuts",
        "Configure keyboard shortcuts in settings",
        "Use shortcuts to save time at work",
        "Look up Mac keyboard commands",
    ],
    conv_en = [
        "Learn shortcuts",
        "Quick key combo",
        "Command key tricks",
        "Mac shortcut tip",
    ],
    typo_en = [
        "keyborad shortcut on mac",
        "comand key shortcut",
        "use the aple key",
        "mac shortcutt",
    ],
    bnd_en = [
        "Set up a keyboard macro",
        "Configure hotkeys in the app",
        "Use Tab key to switch windows",
        "Press Ctrl+Z to undo",
        "Set up voice commands",
        "Create an automation workflow",
    ],
    valid_en = [
        "Use Command key shortcut",
        "Set up a keyboard shortcut",
        "Learn Mac shortcuts",
    ],
    test_en = [
        "Find useful keyboard shortcuts",
        "Speed up work with shortcuts",
        "Configure custom key bindings",
    ],
)

# ============================================================
# 114. compact-disc
# ============================================================
process_icon(
    "compact-disc",
    st_en = ["album", "blu-ray", "cd", "disc", "disk", "dvd", "media", "movie", "music", "optical", "record", "vinyl"],
    pst_en = [
        "Buy the new album on CD", "Rip the album from CD to digital",
        "Watch a Blu-ray movie", "Buy a Blu-ray disc",
        "Burn files to a CD", "Buy blank CDs",
        "Clean the disc surface", "Store discs properly",
        "Save files to disk", "Back up data to disk",
        "Rent a DVD from the store", "Watch a DVD tonight",
        "Organize the media collection", "Convert media to digital format",
        "Watch a movie on DVD", "Find the movie on disc",
        "Listen to music on optical disc", "Store music on optical disc",
        "Record the performance to disc", "Record to a blank disc",
        "Buy a vintage vinyl record", "Play vinyl on the turntable",
        "Rip the CD to MP3", "Sort the CD collection",
    ],
    reg_en = [
        "Rip the CD collection to digital",
        "Find the DVD in the collection",
        "Clean a scratched disc",
        "Organize the media library",
        "Convert old CDs to MP3",
        "Watch a Blu-ray movie tonight",
        "Buy a movie on physical disc",
        "Archive data to optical disc",
        "Find that old vinyl record",
        "Play music from a CD player",
    ],
    conv_en = [
        "Pop in a DVD",
        "Playing a CD",
        "Old school disc",
        "Vinyl night",
    ],
    typo_en = [
        "watche the dvd movie",
        "brun a cd disc",
        "viynl record collection",
        "rip the cds to digitla",
    ],
    bnd_en = [
        "Stream music on Spotify",
        "Download the movie online",
        "Listen to music on a cassette tape",
        "Play music on the radio",
        "Use a USB drive for data",
        "Cloud backup the files",
    ],
    valid_en = [
        "Rip the CD collection",
        "Watch a movie on DVD",
        "Play vinyl records tonight",
    ],
    test_en = [
        "Organize the disc collection",
        "Convert CDs to digital format",
        "Find the old album on CD",
    ],
)

# ============================================================
# 115. compass
# ============================================================
process_icon(
    "compass",
    st_en = ["compass", "directions", "directory", "location", "magnetic", "menu", "navigation", "orienteering", "safari", "travel"],
    pst_en = [
        "Use a compass to navigate the trail", "Find direction with a compass",
        "Get directions to the venue", "Ask for directions in the city",
        "Search the directory for the address", "Browse the business directory",
        "Share my current location", "Find my location on the map",
        "Check the magnetic north", "Use a magnetic compass for hiking",
        "Open the app menu", "Find the right option in the menu",
        "Use the navigation app", "Navigation for the road trip",
        "Try orienteering in the park", "Join an orienteering event",
        "Open Safari on my Mac", "Browse the web in Safari",
        "Plan the travel route", "Navigate during travel abroad",
    ],
    reg_en = [
        "Find the way to the new restaurant",
        "Navigate through the hiking trail",
        "Get directions for the commute",
        "Use the compass app on the phone",
        "Plan a route for the road trip",
        "Find north on the trail map",
        "Navigate in a new city",
        "Download an offline map for hiking",
        "Orient yourself on the trail",
        "Follow the compass heading",
    ],
    conv_en = [
        "Which way is north?",
        "Need directions",
        "Find the way",
        "Navigation help",
    ],
    typo_en = [
        "use a compas to navigate",
        "get directoins to the place",
        "navgation for the hike",
        "find my locaion",
    ],
    bnd_en = [
        "Use a drafting compass to draw a circle",
        "Draw a perfect circle with a drafting tool",
        "Use GPS tracker on phone",
        "Check the map for altitude",
        "Read a topographic map",
        "Use a ruler to measure distances on the map",
    ],
    valid_en = [
        "Navigate with a compass",
        "Get directions to the destination",
        "Find the trail with the compass",
    ],
    test_en = [
        "Orient yourself on the hiking trail",
        "Navigate in an unfamiliar city",
        "Use compass for outdoor navigation",
    ],
)

# ============================================================
# 116. compass-drafting
# ============================================================
process_icon(
    "compass-drafting",
    st_en = ["design", "map", "mechanical drawing", "plot", "plotting"],
    pst_en = [
        "Design the floor plan", "Use a compass for geometric design",
        "Draw circles on the map", "Plot points on the map",
        "Create a mechanical drawing", "Make a precise mechanical drawing",
        "Plot the data on a graph", "Plot the route on a chart",
        "Start plotting the house layout", "Plot the architectural design",
    ],
    reg_en = [
        "Draw the blueprint with a drafting compass",
        "Design the room layout on paper",
        "Create an architectural sketch",
        "Draw geometric shapes for the project",
        "Measure and draw accurate circles",
        "Plan the garden layout on paper",
        "Draft the engineering diagram",
        "Make precise technical drawings",
        "Draw the map of the property",
        "Create a detailed floor plan",
    ],
    conv_en = [
        "Sketch it out",
        "Draw the plan",
        "Draft the design",
        "Measure and draw",
    ],
    typo_en = [
        "drw the bluepirnt",
        "desiign the floor plan",
        "mechanicel drawing",
        "use drafting compas",
    ],
    bnd_en = [
        "Navigate with a trail compass",
        "Use a protractor to measure angles",
        "Draw a straight line with a ruler",
        "Use a level to check alignment",
        "Take compass bearings on a hike",
        "Read the map for directions",
    ],
    valid_en = [
        "Draft the building blueprint",
        "Draw the floor plan with precision",
        "Create geometric shapes for design",
    ],
    test_en = [
        "Make an architectural drawing",
        "Plot the engineering diagram",
        "Design the room layout on paper",
    ],
)

# ============================================================
# 117. computer
# ============================================================
process_icon(
    "computer",
    st_en = ["computer", "desktop", "display", "monitor", "tower"],
    pst_en = [
        "Buy a new computer", "Fix the computer at home",
        "Set up the desktop computer", "Clean the desktop workspace",
        "Adjust the display brightness", "Replace the broken display",
        "Buy a better monitor", "Clean the monitor screen",
        "Upgrade the computer tower", "Repair the tower PC",
    ],
    reg_en = [
        "Set up the home office computer",
        "Buy a new desktop PC",
        "Upgrade the RAM on the computer",
        "Clean the dust from the computer",
        "Back up the computer files",
        "Install a new program on the PC",
        "Repair the computer",
        "Update the computer software",
        "Connect the monitor to the PC",
        "Replace the old computer",
    ],
    conv_en = [
        "New computer day",
        "Fix my PC",
        "Desktop setup",
        "Computer upgrade",
    ],
    typo_en = [
        "set up the dekstop",
        "by a new compter",
        "fix the monitr screen",
        "upgrade the computre",
    ],
    bnd_en = [
        "Buy a new laptop",
        "Set up a tablet for work",
        "Connect a keyboard to the laptop",
        "Install software on the phone",
        "Use a gaming console instead",
        "Set up a server rack",
    ],
    valid_en = [
        "Set up the desktop computer",
        "Buy a new PC for work",
        "Repair the home computer",
    ],
    test_en = [
        "Upgrade the computer hardware",
        "Set up the office desktop",
        "Install software on the computer",
    ],
)

# ============================================================
# 118. computer-mouse
# ============================================================
process_icon(
    "computer-mouse",
    st_en = ["click", "computer", "computer mouse", "cursor", "input", "peripheral"],
    pst_en = [
        "Click the button on screen", "Double click to open the file",
        "Set up the computer workspace", "Fix the computer setup",
        "Buy a wireless computer mouse", "Replace the computer mouse",
        "Move the cursor to the right position", "Cursor is not responding",
        "Set up input devices", "Configure the input settings",
        "Buy a new peripheral device", "Connect the peripheral to the laptop",
    ],
    reg_en = [
        "Buy a wireless mouse for the laptop",
        "Set up the computer mouse",
        "Replace the worn mouse pad",
        "Configure mouse sensitivity",
        "Connect the mouse via Bluetooth",
        "Clean the mouse sensor",
        "Get an ergonomic mouse",
        "Update mouse drivers",
        "Fix the mouse not responding",
        "Buy a gaming mouse",
    ],
    conv_en = [
        "Mouse not working",
        "Get a new mouse",
        "Set up the mouse",
        "Need a better mouse",
    ],
    typo_en = [
        "by a wirelss mouse",
        "computter mouse not working",
        "set up the compuer mouse",
        "cursro not responding",
    ],
    bnd_en = [
        "Buy a mechanical keyboard",
        "Set up the laptop trackpad",
        "Use touch screen instead",
        "Connect a drawing tablet",
        "Buy a stylus pen",
        "Configure the trackball device",
    ],
    valid_en = [
        "Buy a wireless computer mouse",
        "Set up the mouse for the computer",
        "Fix the mouse cursor issue",
    ],
    test_en = [
        "Replace the computer mouse",
        "Configure mouse settings",
        "Get an ergonomic mouse for work",
    ],
)

# ============================================================
# 119. container-storage
# ============================================================
process_icon(
    "container-storage",
    st_en = ["archive", "box", "crate", "intermodal", "inventory", "shipping", "warehouse"],
    pst_en = [
        "Archive old files and documents", "Move old records to archive",
        "Pack items in a box", "Label and seal the box",
        "Ship items in a wooden crate", "Build a crate for shipping",
        "Ship goods via intermodal container", "Track the intermodal shipment",
        "Do a full inventory count", "Update the inventory list",
        "Arrange shipping for the order", "Track the shipping container",
        "Organize the warehouse shelves", "Manage warehouse inventory",
    ],
    reg_en = [
        "Organize storage in the garage",
        "Pack boxes for the move",
        "Label all storage boxes",
        "Ship a package to a customer",
        "Track the delivery",
        "Organize the storage room",
        "Do an inventory check",
        "Send items to the warehouse",
        "Unpack boxes after moving",
        "Rent a storage unit",
    ],
    conv_en = [
        "Pack it up",
        "Box everything",
        "Ship it out",
        "Storage run",
    ],
    typo_en = [
        "pak the boxes",
        "shiping the container",
        "inventroy check",
        "orgnaize the warehouse",
    ],
    bnd_en = [
        "Buy a storage shelf unit",
        "Organize the pantry shelves",
        "Send a letter by mail",
        "Use cloud storage for backup",
        "Manage files on the hard drive",
        "Sort documents in the filing cabinet",
    ],
    valid_en = [
        "Pack boxes for storage",
        "Ship goods to the warehouse",
        "Do an inventory check",
    ],
    test_en = [
        "Organize items in storage",
        "Label the shipping boxes",
        "Track the container shipment",
    ],
)

print("\nAll 20 icons processed successfully!")
