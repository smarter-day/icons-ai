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
    print(f"  {icon}: {len(train_en)} train rows  ({len(st_en)} st + {len(pst_en)} pst + 24)")

# ============================================================
# 150. drone
# ============================================================
process_icon(
    "drone",
    st_en = ["aerial", "surveillance", "uav", "unmanned", "vehicle"],
    pst_en = [
        "Take aerial photos with the drone", "Fly the drone for aerial footage",
        "Set up surveillance with the drone", "Use a drone for surveillance",
        "Register the UAV before flying", "Fly the UAV in the open field",
        "Fly an unmanned aircraft", "Control the unmanned vehicle remotely",
        "Operate the drone vehicle", "Buy a new drone vehicle",
    ],
    reg_en = [
        "Fly the drone over the park",
        "Take aerial photos with the drone",
        "Register the drone with authorities",
        "Buy a camera drone",
        "Learn to fly a drone",
        "Charge the drone battery",
        "Film the wedding with a drone",
        "Use the drone for real estate photos",
        "Fly the drone at the beach",
        "Check drone flight regulations",
    ],
    conv_en = [
        "Drone flight!",
        "Fly the drone",
        "Aerial shot",
        "Drone day",
    ],
    typo_en = [
        "fly the droen",
        "aerail photos with drone",
        "regster the uav",
        "drone baterry charge",
    ],
    bnd_en = [
        "Take a photo with the camera",
        "Fly a kite in the park",
        "Use a helicopter for the tour",
        "Film with a mounted action camera",
        "Use a satellite for surveillance",
        "Pilot a remote-control plane",
    ],
    valid_en = [
        "Fly the drone for aerial footage",
        "Register the drone",
        "Take aerial photos",
    ],
    test_en = [
        "Learn to fly a drone",
        "Buy a camera drone",
        "Film with the drone",
    ],
)

# ============================================================
# 151. dryer
# ============================================================
process_icon(
    "dryer",
    st_en = ["clean", "clothes", "laundromat", "laundry", "washing machine"],
    pst_en = [
        "Keep the house clean", "Clean the appliance filter",
        "Dry the clothes after washing", "Tumble dry clothes on low heat",
        "Go to the laundromat", "Use the laundromat dryer",
        "Do the laundry today", "Sort laundry before washing",
        "Use the washing machine first", "Transfer from washing machine to dryer",
    ],
    reg_en = [
        "Dry clothes after the wash cycle",
        "Clean the dryer lint filter",
        "Put the wet clothes in the dryer",
        "Set the dryer to low heat",
        "Use the dryer for bedsheets",
        "Dry a load of towels",
        "Check if clothes are dry",
        "Reduce drying time with dryer balls",
        "Fix the dryer that won't heat",
        "Do laundry and dry it today",
    ],
    conv_en = [
        "Dryer's running",
        "Laundry day",
        "Clothes in the dryer",
        "Dry that load",
    ],
    typo_en = [
        "put cltohs in the dryer",
        "clena the lint filtter",
        "do the laudnry",
        "use the wahing machine",
    ],
    bnd_en = [
        "Hang clothes on the line to dry",
        "Iron the shirts after drying",
        "Use the washing machine for cleaning",
        "Fold and put away the laundry",
        "Buy laundry detergent",
        "Dry clean the delicate items",
    ],
    valid_en = [
        "Put clothes in the dryer",
        "Clean the dryer lint filter",
        "Do a load of laundry",
    ],
    test_en = [
        "Dry the bedsheets",
        "Use the dryer on low heat",
        "Transfer clothes to the dryer",
    ],
)

# ============================================================
# 152. duck
# ============================================================
process_icon(
    "duck",
    st_en = ["bath", "bird", "duck", "fauna", "quack", "rubber"],
    pst_en = [
        "Give the baby a bath", "Bath time with the rubber duck",
        "Watch a bird swim in the pond", "Spot a bird at the lake",
        "Feed the ducks at the pond", "See a duck swim by",
        "Observe local fauna", "See fauna at the nature reserve",
        "Hear a duck quack", "Listen to ducks quacking",
        "Play with the rubber duck in the bath", "Buy a rubber duck for the kids",
    ],
    reg_en = [
        "Feed ducks at the park pond",
        "Watch ducks swim with the kids",
        "Buy a rubber duck for bath time",
        "Take kids to see ducks",
        "Photograph ducks at the lake",
        "Spot a mother duck with ducklings",
        "Watch ducks in the rain",
        "See ducks at the nature reserve",
        "Bring bread to feed the ducks",
        "Watch ducks dive underwater",
    ],
    conv_en = [
        "Ducks at the pond!",
        "Rubber ducky",
        "Feed the ducks",
        "Quack quack",
    ],
    typo_en = [
        "feed the dukcs",
        "rubber dukc in the bath",
        "watcch ducks swming",
        "see duckks at the pond",
    ],
    bnd_en = [
        "Watch a swan glide on the lake",
        "Feed geese at the park",
        "Spot a heron at the river",
        "Watch penguins at the zoo",
        "See pelicans at the beach",
        "Observe pigeons in the city",
    ],
    valid_en = [
        "Feed ducks at the park",
        "Buy a rubber duck for the bath",
        "Watch ducks swim",
    ],
    test_en = [
        "Take kids to see ducks",
        "Photograph ducks at the pond",
        "Spot ducklings at the lake",
    ],
)

# ============================================================
# 153. dumbbell
# ============================================================
process_icon(
    "dumbbell",
    st_en = ["exercise", "gym", "strength", "weight", "weight-lifting", "workout"],
    pst_en = [
        "Do exercise in the morning", "Follow the exercise plan",
        "Go to the gym today", "Sign up for the gym",
        "Build strength with resistance training", "Improve core strength",
        "Lift weights at the gym", "Buy a set of weights",
        "Practice weight-lifting technique", "Enter a weight-lifting competition",
        "Plan the weekly workout", "Complete the workout routine",
    ],
    reg_en = [
        "Go to the gym",
        "Lift weights in the morning",
        "Do a full body workout",
        "Buy dumbbells for the home gym",
        "Follow a strength training program",
        "Work out with a personal trainer",
        "Complete the leg day workout",
        "Build muscle with weight training",
        "Rest between workout sets",
        "Track gym progress",
    ],
    conv_en = [
        "Gym time!",
        "Lift some weights",
        "Workout today",
        "Hit the gym",
    ],
    typo_en = [
        "go to the gmy",
        "lift wieghts",
        "do a workoout",
        "strenght training",
    ],
    bnd_en = [
        "Go for a morning run",
        "Do yoga for flexibility",
        "Ride the exercise bike",
        "Swim laps at the pool",
        "Play tennis for cardio",
        "Do push-ups at home",
    ],
    valid_en = [
        "Go to the gym",
        "Lift weights in the morning",
        "Follow a strength training program",
    ],
    test_en = [
        "Buy dumbbells for home",
        "Complete the workout routine",
        "Build muscle with weight training",
    ],
)

# ============================================================
# 154. egg
# ============================================================
process_icon(
    "egg",
    st_en = ["breakfast", "chicken", "easter", "egg", "food", "shell", "yolk"],
    pst_en = [
        "Make a breakfast with eggs", "Cook a hearty breakfast",
        "Buy chicken eggs at the store", "Raise backyard chickens for eggs",
        "Decorate easter eggs", "Hide easter eggs in the yard",
        "Boil an egg for breakfast", "Crack an egg into the pan",
        "Cook egg-based food", "Make a food dish with eggs",
        "Crack the eggshell carefully", "Dispose of the eggshell",
        "Separate the yolk from the white", "Use only the egg yolk",
    ],
    reg_en = [
        "Boil eggs for breakfast",
        "Make a hard-boiled egg",
        "Scramble eggs in the morning",
        "Buy a dozen eggs",
        "Make an omelette",
        "Decorate Easter eggs with the kids",
        "Poach eggs for brunch",
        "Add eggs to the grocery list",
        "Use eggs in the cake batter",
        "Check the egg expiry date",
    ],
    conv_en = [
        "Egg for breakfast",
        "Boil some eggs",
        "Easter egg hunt",
        "Egg run",
    ],
    typo_en = [
        "boil an eeg for breakfast",
        "scamble eggs",
        "decorate eastr eggs",
        "buy a dozne eggs",
    ],
    bnd_en = [
        "Fry an egg sunny-side up",
        "Make a fried egg sandwich",
        "Cook scrambled eggs with bacon",
        "Bake a quiche",
        "Make a deviled egg platter",
        "Use egg whites for the meringue",
    ],
    valid_en = [
        "Boil eggs for breakfast",
        "Buy a dozen eggs",
        "Decorate Easter eggs",
    ],
    test_en = [
        "Make an omelette",
        "Poach eggs for brunch",
        "Scramble eggs in the morning",
    ],
)

# ============================================================
# 155. egg-fried
# ============================================================
process_icon(
    "egg-fried",
    st_en = ["breakfast", "chicken", "yolk"],
    pst_en = [
        "Make a fried egg for breakfast", "Cook a full English breakfast",
        "Buy eggs from the chicken farm", "Use fresh chicken eggs",
        "Break the yolk when frying", "Keep the yolk intact when frying",
    ],
    reg_en = [
        "Fry an egg sunny-side up",
        "Make a fried egg sandwich",
        "Cook a fried egg for breakfast",
        "Fry an egg in butter",
        "Make eggs over easy",
        "Fry an egg with bacon",
        "Cook a breakfast fry-up",
        "Fry an egg in the cast iron pan",
        "Make a fried egg on toast",
        "Cook the egg until the white is set",
    ],
    conv_en = [
        "Fry an egg",
        "Sunny side up",
        "Egg on toast",
        "Breakfast fry-up",
    ],
    typo_en = [
        "fry an eeg",
        "sunney side up egg",
        "fried eggg for breakfast",
        "cook egss in buter",
    ],
    bnd_en = [
        "Boil an egg for the salad",
        "Scramble eggs in a pan",
        "Make a hard-boiled egg",
        "Poach an egg for brunch",
        "Make an omelette",
        "Bake eggs in the oven",
    ],
    valid_en = [
        "Fry an egg for breakfast",
        "Make eggs sunny-side up",
        "Cook a fried egg on toast",
    ],
    test_en = [
        "Fry an egg in butter",
        "Make a fried egg sandwich",
        "Cook a breakfast fry-up",
    ],
)

# ============================================================
# 156. elephant
# ============================================================
process_icon(
    "elephant",
    st_en = ["animal", "elephant", "fauna", "mammal", "pachyderm", "trunk"],
    pst_en = [
        "See the animals at the zoo", "Learn about wild animals",
        "Visit the elephant sanctuary", "Watch elephants in the wild",
        "Spot fauna on the safari", "Observe fauna at the nature park",
        "See the large mammals", "Learn about African mammals",
        "Learn about pachyderms", "Read about the pachyderm family",
        "Watch the elephant use its trunk", "Elephant picking up food with its trunk",
    ],
    reg_en = [
        "Visit the elephant sanctuary",
        "Watch elephants at the zoo",
        "Go on a safari",
        "See elephants in the wild",
        "Take kids to see elephants",
        "Learn about elephant behavior",
        "Donate to elephant conservation",
        "Watch a nature documentary about elephants",
        "Ride an elephant on the Thailand trip",
        "Photograph an elephant in Africa",
    ],
    conv_en = [
        "Safari time!",
        "See the elephants",
        "Elephant watching",
        "Zoo visit",
    ],
    typo_en = [
        "visit the elephnat sanctuary",
        "wacth elephants at the zoo",
        "go on a safri",
        "see elephnts in the wild",
    ],
    bnd_en = [
        "See giraffes on the safari",
        "Watch hippos at the waterhole",
        "See rhinos in the wild",
        "Spot a lion on the savanna",
        "Watch gorillas at the zoo",
        "See a mammoth exhibit at the museum",
    ],
    valid_en = [
        "Visit the elephant sanctuary",
        "Watch elephants in the wild",
        "See elephants at the zoo",
    ],
    test_en = [
        "Go on a safari to see elephants",
        "Learn about elephant conservation",
        "Photograph elephants in Africa",
    ],
)

# ============================================================
# 157. elevator
# ============================================================
process_icon(
    "elevator",
    st_en = ["elevator", "hoist", "lift"],
    pst_en = [
        "Take the elevator to the office", "Wait for the elevator",
        "Use the hoist to lift the equipment", "Hoist supplies to the upper floor",
        "Use the lift instead of stairs", "Call the lift on this floor",
    ],
    reg_en = [
        "Take the elevator to the top floor",
        "Hold the elevator for someone",
        "Press the floor button in the elevator",
        "Use the elevator with the stroller",
        "Report the broken elevator",
        "Wait for the elevator at work",
        "Use the service elevator",
        "Take the lift to the parking level",
        "Check if the elevator is accessible",
        "Use the freight elevator for moving",
    ],
    conv_en = [
        "Take the elevator",
        "Lift is broken",
        "Going up",
        "Hold the elevator!",
    ],
    typo_en = [
        "take the elavator",
        "wiat for the lift",
        "use the elevatr",
        "pres the floor buton",
    ],
    bnd_en = [
        "Take the stairs for exercise",
        "Use the escalator to go up",
        "Climb the steps to the office",
        "Use the ramp for accessibility",
        "Go up on the moving walkway",
        "Use the fire exit stairwell",
    ],
    valid_en = [
        "Take the elevator to the office",
        "Hold the elevator for someone",
        "Use the lift instead of stairs",
    ],
    test_en = [
        "Press the floor button in the elevator",
        "Report the broken elevator",
        "Use the elevator with heavy luggage",
    ],
)

# ============================================================
# 158. envelope
# ============================================================
process_icon(
    "envelope",
    st_en = ["e-mail", "email", "envelope", "letter", "mail", "message", "newsletter", "notification", "offer", "support"],
    pst_en = [
        "Send an e-mail to the team", "Check e-mail in the morning",
        "Read new email in the inbox", "Reply to the email",
        "Seal the envelope before mailing", "Address the envelope",
        "Write a letter to a friend", "Send a handwritten letter",
        "Check the mail in the mailbox", "Send mail to the address",
        "Send a message to the group", "Reply to the message",
        "Subscribe to the newsletter", "Unsubscribe from the newsletter",
        "Turn on email notifications", "Check the notification",
        "Review the special offer email", "Reply to the job offer",
        "Contact customer support", "Email support for help",
    ],
    reg_en = [
        "Check email in the morning",
        "Reply to the work email",
        "Send a letter to a friend",
        "Subscribe to the newsletter",
        "Contact support via email",
        "Write a thank-you email",
        "Check unread messages in inbox",
        "Send an email with an attachment",
        "Follow up on the unanswered email",
        "Unsubscribe from junk mail",
    ],
    conv_en = [
        "Check your email",
        "Reply to that message",
        "Got mail!",
        "Send a message",
    ],
    typo_en = [
        "chekc the emial",
        "sned a message",
        "reapply to email",
        "subsrcibe to newsletter",
    ],
    bnd_en = [
        "Send a text message on the phone",
        "Post a letter at the post office",
        "Send a direct message on social media",
        "Leave a voicemail",
        "Send a fax to the office",
        "Chat on messaging app",
    ],
    valid_en = [
        "Check email in the morning",
        "Send a letter to a friend",
        "Subscribe to the newsletter",
    ],
    test_en = [
        "Reply to the work email",
        "Contact support via email",
        "Send an email with an attachment",
    ],
)

# ============================================================
# 159. eraser
# ============================================================
process_icon(
    "eraser",
    st_en = ["art", "delete", "remove", "rubber"],
    pst_en = [
        "Use an eraser in art class", "Draw and erase in the sketchbook",
        "Delete the file from the folder", "Delete old messages",
        "Remove the mistake from the drawing", "Remove the sticker from the surface",
        "Use a rubber eraser on pencil marks", "Buy a new rubber eraser",
    ],
    reg_en = [
        "Erase a pencil mark on paper",
        "Use the eraser tool in Photoshop",
        "Delete old files from the computer",
        "Erase mistakes in the sketchbook",
        "Buy a good eraser for drawing",
        "Remove pencil lines after inking",
        "Use the digital eraser in the app",
        "Clear the whiteboard with an eraser",
        "Erase notes from the chalkboard",
        "Remove unwanted lines from the drawing",
    ],
    conv_en = [
        "Erase that",
        "Delete the mistake",
        "Clean it up",
        "Remove it",
    ],
    typo_en = [
        "erase a pencil mrk",
        "delet the flie",
        "use the erasre tool",
        "remov the mistake",
    ],
    bnd_en = [
        "Cross out a mistake with a pen",
        "Use correction fluid to fix the error",
        "Strike through old text",
        "Undo the last action in the app",
        "Cut out the section from the paper",
        "Cover the text with a sticker",
    ],
    valid_en = [
        "Erase pencil marks on paper",
        "Clear the whiteboard",
        "Use the eraser in the drawing app",
    ],
    test_en = [
        "Delete old files",
        "Remove mistakes from the sketch",
        "Use the digital eraser tool",
    ],
)

# ============================================================
# 160. ethernet
# ============================================================
process_icon(
    "ethernet",
    st_en = ["cable", "cat 5", "cat 6", "connection", "hardware", "internet", "network", "wired"],
    pst_en = [
        "Buy an ethernet cable", "Plug in the ethernet cable",
        "Use a Cat 5 cable for the network", "Replace the old Cat 5 cable",
        "Upgrade to a Cat 6 cable", "Install Cat 6 for faster speed",
        "Check the network connection", "Fix the unstable connection",
        "Set up the network hardware", "Buy new networking hardware",
        "Connect to the internet via cable", "Troubleshoot internet connection",
        "Set up the home network", "Add a device to the network",
        "Use wired connection for stability", "Switch from wifi to wired",
    ],
    reg_en = [
        "Connect the computer via ethernet",
        "Buy a longer ethernet cable",
        "Use wired internet for faster speed",
        "Set up the home network",
        "Plug the router into the wall",
        "Fix the slow internet connection",
        "Set up a wired gaming connection",
        "Replace the old network cable",
        "Connect the smart TV via ethernet",
        "Run an ethernet cable through the wall",
    ],
    conv_en = [
        "Plug in the cable",
        "Wired connection",
        "Ethernet setup",
        "Network cable",
    ],
    typo_en = [
        "plug in the etehrnet cable",
        "use wried connection",
        "buy a cat6 cabel",
        "fix the internt connection",
    ],
    bnd_en = [
        "Connect to WiFi instead",
        "Use a WiFi extender",
        "Set up a Bluetooth connection",
        "Use a USB hub for connectivity",
        "Connect via mobile hotspot",
        "Install fiber optic internet",
    ],
    valid_en = [
        "Connect via ethernet cable",
        "Set up a wired network connection",
        "Use ethernet for stable internet",
    ],
    test_en = [
        "Buy an ethernet cable",
        "Plug the computer into the router",
        "Fix the wired network connection",
    ],
)

# ============================================================
# 161. euro-sign
# ============================================================
process_icon(
    "euro-sign",
    st_en = ["Euro Sign", "currency"],
    pst_en = [
        "Check the Euro exchange rate", "Pay in Euro at the shop",
        "Exchange currency at the airport", "Convert currency before the trip",
    ],
    reg_en = [
        "Exchange money to Euros",
        "Check the EUR exchange rate",
        "Pay with Euros in Europe",
        "Transfer money in Euros",
        "Convert dollars to Euros",
        "Budget the trip in Euros",
        "Find the best Euro exchange rate",
        "Pay the invoice in Euros",
        "Check the Euro to dollar rate",
        "Withdraw Euros from the ATM",
    ],
    conv_en = [
        "Euro trip budget",
        "Convert to euros",
        "Pay in euros",
        "Check euro rate",
    ],
    typo_en = [
        "exchagne to euross",
        "pay in eruo",
        "check eur excahnge rate",
        "covnert to euros",
    ],
    bnd_en = [
        "Convert to US dollars",
        "Pay in British pounds",
        "Check the Japanese yen rate",
        "Exchange for Swiss francs",
        "Pay in Thai baht",
        "Use a credit card abroad",
    ],
    valid_en = [
        "Exchange money to Euros",
        "Pay with Euros in Europe",
        "Check the EUR exchange rate",
    ],
    test_en = [
        "Convert dollars to Euros",
        "Budget the trip in Euros",
        "Withdraw Euros from the ATM",
    ],
)

# ============================================================
# 162. expand
# ============================================================
process_icon(
    "expand",
    st_en = ["enlarge", "expand", "fullscreen", "maximize", "resize", "scale", "size", "viewfinder"],
    pst_en = [
        "Enlarge the text on screen", "Enlarge the image for printing",
        "Expand the view for more detail", "Expand the sidebar panel",
        "Switch to fullscreen mode", "Watch video in fullscreen",
        "Maximize the browser window", "Maximize the app on screen",
        "Resize the window to fit", "Resize the image before uploading",
        "Scale the design to the right size", "Scale up the graphic",
        "Change the font size", "Increase the image size",
        "Use the viewfinder to frame the shot", "Look through the viewfinder",
    ],
    reg_en = [
        "Open the image in full screen",
        "Maximize the app window",
        "Zoom in on the document",
        "Expand the video player",
        "Make the text bigger on screen",
        "Resize the window for better view",
        "Scale the image for the poster",
        "View the presentation in fullscreen",
        "Enlarge the map for navigation",
        "Zoom into the photo detail",
    ],
    conv_en = [
        "Go fullscreen",
        "Make it bigger",
        "Expand the view",
        "Zoom in",
    ],
    typo_en = [
        "swithc to fullsceen",
        "maximze the window",
        "rezise the image",
        "enmarge the text",
    ],
    bnd_en = [
        "Minimize the window",
        "Shrink the image size",
        "Collapse the sidebar",
        "Zoom out on the document",
        "Reduce the font size",
        "Use picture-in-picture mode",
    ],
    valid_en = [
        "Switch to fullscreen mode",
        "Maximize the app window",
        "Enlarge the image",
    ],
    test_en = [
        "Expand the video player",
        "Make the text bigger",
        "Resize the window to full",
    ],
)

# ============================================================
# 163. face-exhaling
# ============================================================
process_icon(
    "face-exhaling",
    st_en = ["breath", "exhale", "exhaustion", "relief", "sigh"],
    pst_en = [
        "Take a deep breath before starting", "Breathe slowly to calm down",
        "Exhale and release the tension", "Exhale deeply after exercise",
        "Recover from exhaustion", "Manage work exhaustion",
        "Feel relief after finishing the task", "Sigh with relief",
        "Let out a long sigh", "Sigh after a stressful day",
    ],
    reg_en = [
        "Take a deep breath to relax",
        "Exhale after a stressful meeting",
        "Feel relieved after the exam",
        "Breathe deeply before the presentation",
        "Take a breather after the sprint",
        "Feel the exhaustion after a long day",
        "Sigh with relief when it's done",
        "Do breathing exercises to calm down",
        "Take a moment to breathe and recover",
        "Relax after finally finishing the work",
    ],
    conv_en = [
        "Finally done",
        "Take a breather",
        "Big sigh of relief",
        "Exhausted but done",
    ],
    typo_en = [
        "take a deap breath",
        "feel relif after finishing",
        "exhaustoin from work",
        "big sigh of releif",
    ],
    bnd_en = [
        "Cry from stress",
        "Laugh out loud",
        "Feel dizzy after spinning",
        "Feel nervous before speaking",
        "Take a nap when exhausted",
        "Meditate to reduce stress",
    ],
    valid_en = [
        "Take a deep breath to relax",
        "Feel relieved after finishing",
        "Exhale after the stressful day",
    ],
    test_en = [
        "Sigh with relief when done",
        "Recover from exhaustion",
        "Breathe deeply to calm down",
    ],
)

# ============================================================
# 164. face-woozy
# ============================================================
process_icon(
    "face-woozy",
    st_en = ["dizzy", "drunk", "exhaustion", "intoxicated", "tipsy"],
    pst_en = [
        "Feel dizzy after spinning around", "Dizzy from the heat",
        "Avoid drinking until drunk", "Feel drunk after one too many",
        "Overcome exhaustion from overworking", "Deal with exhaustion after the trip",
        "Feel intoxicated after drinking", "Stay safe when intoxicated",
        "Feel tipsy after a glass of wine", "Know when you're tipsy",
    ],
    reg_en = [
        "Feel dizzy after standing up too fast",
        "Rest when feeling woozy",
        "Drink water when feeling dizzy",
        "Avoid alcohol to stay sober",
        "Rest after feeling exhausted",
        "Recover from a dizzy spell",
        "Feel lightheaded after exercise",
        "Take a break when feeling unwell",
        "Sit down when feeling woozy",
        "Tell someone if you feel dizzy",
    ],
    conv_en = [
        "Feeling woozy",
        "Too much to drink",
        "Spinning head",
        "Need to sit down",
    ],
    typo_en = [
        "feeling dizzy and woozy",
        "too muhc to drink",
        "feel intocixated",
        "drnik water if dizzy",
    ],
    bnd_en = [
        "Feel nervous before a speech",
        "Feel tired and need a nap",
        "Laugh until you cry",
        "Feel relieved after hard work",
        "Feel frustrated at the situation",
        "Feel sleepy after a big meal",
    ],
    valid_en = [
        "Feel dizzy and need to sit down",
        "Rest when feeling woozy",
        "Drink water when lightheaded",
    ],
    test_en = [
        "Recover from a dizzy spell",
        "Feel unwell after overdrinking",
        "Take a break when feeling woozy",
    ],
)

# ============================================================
# 165. falafel
# ============================================================
process_icon(
    "falafel",
    st_en = ["chickpea", "falafel", "garbanzo", "meatball"],
    pst_en = [
        "Use chickpeas to make falafel", "Buy canned chickpeas",
        "Make falafel from scratch", "Order falafel from the restaurant",
        "Use garbanzo beans in the recipe", "Cook garbanzo bean soup",
        "Roll the meatball-shaped falafel", "Fry falafel like meatballs",
    ],
    reg_en = [
        "Make homemade falafel",
        "Order falafel wrap for lunch",
        "Try falafel at the Middle Eastern restaurant",
        "Bake falafel instead of frying",
        "Buy falafel mix at the store",
        "Serve falafel with tahini",
        "Put falafel in a pita wrap",
        "Make a falafel salad bowl",
        "Prepare falafel for a dinner party",
        "Find the best falafel recipe",
    ],
    conv_en = [
        "Falafel lunch!",
        "Make falafel",
        "Middle Eastern food",
        "Wrap with falafel",
    ],
    typo_en = [
        "make homemade faelafel",
        "order falafl wrap",
        "chickpea falaefal",
        "falafel with tahnia",
    ],
    bnd_en = [
        "Make a pita sandwich with gyro meat",
        "Order a kebab wrap",
        "Make meatballs with beef",
        "Cook hummus from chickpeas",
        "Eat a shawarma wrap",
        "Make a veggie burger patty",
    ],
    valid_en = [
        "Make homemade falafel",
        "Order a falafel wrap",
        "Serve falafel with tahini",
    ],
    test_en = [
        "Try falafel at the restaurant",
        "Bake falafel for dinner",
        "Make a falafel salad bowl",
    ],
)

# ============================================================
# 166. family
# ============================================================
process_icon(
    "family",
    st_en = ["adults", "child", "family", "folk", "kid", "parent", "together"],
    pst_en = [
        "Plan an outing for the adults", "Adults-only dinner reservation",
        "Take the child to school", "Read a bedtime story to the child",
        "Plan a family vacation", "Spend time with the family",
        "Hang out with the folk at home", "Visit the folk this weekend",
        "Plan activities for the kids", "Take the kids to the park",
        "Help the parent with errands", "Call the parent on their birthday",
        "Do something together as a family", "Cook dinner together",
    ],
    reg_en = [
        "Plan a family dinner",
        "Take the kids to the park",
        "Go on a family road trip",
        "Visit the grandparents",
        "Watch a movie together as a family",
        "Cook a meal together",
        "Schedule family time on the weekend",
        "Play a board game with the family",
        "Take family photos",
        "Plan a family vacation",
    ],
    conv_en = [
        "Family night!",
        "Family time",
        "With the family",
        "Family fun day",
    ],
    typo_en = [
        "famly dinner tonight",
        "take the kds to the park",
        "plan a familly vacation",
        "wach movie togehter",
    ],
    bnd_en = [
        "Go out with friends",
        "Plan a solo trip",
        "Hang out with coworkers",
        "Have a couples date night",
        "Organize a class reunion",
        "Meet new neighbors",
    ],
    valid_en = [
        "Plan a family dinner",
        "Go on a family vacation",
        "Spend time together as a family",
    ],
    test_en = [
        "Take the kids to the park",
        "Watch a movie with the family",
        "Cook a meal together",
    ],
)

# ============================================================
# 167. fan
# ============================================================
process_icon(
    "fan",
    st_en = ["ac", "air conditioning", "blade", "blower", "cool", "hot"],
    pst_en = [
        "Turn on the AC to cool down", "Set the AC temperature",
        "Turn on the air conditioning", "Service the air conditioning unit",
        "Clean the fan blade", "Replace a broken blade",
        "Use the blower to cool the room", "Set the blower speed",
        "Cool the room down with the fan", "Cool off in the hot weather",
        "Stay cool when it's hot outside", "Cool down on a hot day",
    ],
    reg_en = [
        "Turn on the ceiling fan",
        "Set the fan to high speed",
        "Buy a portable fan for summer",
        "Cool the bedroom with a fan",
        "Clean the fan blades",
        "Fix the noisy fan",
        "Turn on the AC for the heat wave",
        "Use a desk fan while working",
        "Set up the fan in the living room",
        "Replace the old fan",
    ],
    conv_en = [
        "Turn on the fan",
        "So hot today",
        "Cool the room",
        "AC on",
    ],
    typo_en = [
        "trun on the ceeling fan",
        "set the ac tempratrue",
        "clen the fan blaeds",
        "buy a portble fan",
    ],
    bnd_en = [
        "Turn on the heater in winter",
        "Open the window for fresh air",
        "Use the air purifier",
        "Set up the humidifier",
        "Install a ventilation system",
        "Run the exhaust fan in the bathroom",
    ],
    valid_en = [
        "Turn on the ceiling fan",
        "Cool the room with the fan",
        "Set the AC temperature",
    ],
    test_en = [
        "Buy a portable fan for summer",
        "Clean the fan blades",
        "Fix the noisy fan",
    ],
)

# ============================================================
# 168. faucet
# ============================================================
process_icon(
    "faucet",
    st_en = ["drinking", "drip", "hygiene", "kitchen", "potable water", "sanitation", "sink", "water"],
    pst_en = [
        "Drink clean drinking water", "Filter drinking water",
        "Fix the dripping faucet", "Stop the drip to save water",
        "Practice good hygiene habits", "Wash hands for hygiene",
        "Clean the kitchen faucet", "Replace the kitchen faucet",
        "Make sure the water is potable", "Test if the water is potable",
        "Maintain sanitation in the kitchen", "Improve sanitation at home",
        "Wash dishes in the sink", "Unclog the sink drain",
        "Turn off the water faucet", "Check water pressure",
    ],
    reg_en = [
        "Fix the leaking faucet",
        "Wash hands before eating",
        "Turn off the tap to save water",
        "Replace the old kitchen faucet",
        "Unclog the sink drain",
        "Clean the faucet aerator",
        "Install a water filter on the tap",
        "Check the water pressure",
        "Repair the dripping tap",
        "Call a plumber for the faucet",
    ],
    conv_en = [
        "Fix that drip",
        "Turn off the tap",
        "Leaking faucet",
        "Wash your hands",
    ],
    typo_en = [
        "fix the leakign faucet",
        "wash hads before eating",
        "trun off the taap",
        "replace the kitcen faucet",
    ],
    bnd_en = [
        "Fix the leaking shower head",
        "Repair the toilet flush",
        "Unclog the bathtub drain",
        "Replace the bathroom faucet",
        "Fix the leaking pipe under the sink",
        "Install a new water heater",
    ],
    valid_en = [
        "Fix the leaking faucet",
        "Wash hands before cooking",
        "Turn off the tap to save water",
    ],
    test_en = [
        "Replace the kitchen faucet",
        "Repair the dripping tap",
        "Install a water filter on the faucet",
    ],
)

# ============================================================
# 169. fax
# ============================================================
process_icon(
    "fax",
    st_en = ["business", "communicate", "facsimile", "fax", "fax machine", "send"],
    pst_en = [
        "Send a business document by fax", "Receive a business fax",
        "Communicate via fax at the office", "Use fax to communicate",
        "Send a facsimile of the contract", "Receive a facsimile",
        "Send documents by fax", "Use the fax machine at work",
        "Set up the fax machine", "Fix the fax machine paper jam",
        "Send the signed form by fax", "Send the report by fax",
    ],
    reg_en = [
        "Send a document by fax",
        "Receive a fax from the client",
        "Set up the fax machine at the office",
        "Send the signed contract by fax",
        "Check the fax inbox",
        "Fax the insurance form",
        "Send medical records by fax",
        "Use the all-in-one printer to fax",
        "Send a legal document by fax",
        "Confirm the fax was received",
    ],
    conv_en = [
        "Fax it over",
        "Send by fax",
        "Fax the form",
        "Old school fax",
    ],
    typo_en = [
        "sned the documnet by fax",
        "recieve a fax",
        "fax the sigend contract",
        "set up the fax machien",
    ],
    bnd_en = [
        "Send a document by email",
        "Scan and email the contract",
        "Send a text message",
        "Mail the letter by post",
        "Share the document via cloud",
        "Print and hand-deliver the form",
    ],
    valid_en = [
        "Send a document by fax",
        "Set up the fax machine",
        "Fax the signed contract",
    ],
    test_en = [
        "Send medical records by fax",
        "Check the fax inbox",
        "Confirm the fax was received",
    ],
)

# ============================================================
# 170. ferris-wheel
# ============================================================
process_icon(
    "ferris-wheel",
    st_en = ["amusement park", "fair", "ferris wheel", "ride", "theme park", "wheel"],
    pst_en = [
        "Visit an amusement park", "Buy tickets to the amusement park",
        "Go to the state fair", "Enjoy the fair this weekend",
        "Ride the ferris wheel", "See the city from the ferris wheel",
        "Try the tallest ride at the park", "Line up for the ride",
        "Plan a day at the theme park", "Visit the theme park with kids",
        "Watch the big wheel spin", "Ride at the top of the wheel",
    ],
    reg_en = [
        "Take the kids to the amusement park",
        "Ride the ferris wheel at the fair",
        "Buy tickets for the theme park",
        "Go to the county fair",
        "Wait in line for the ferris wheel",
        "See the view from the top of the ferris wheel",
        "Take photos from the ferris wheel",
        "Visit the theme park on a weekend",
        "Plan a fun day at the fair",
        "Eat carnival food at the fair",
    ],
    conv_en = [
        "Ferris wheel!",
        "Theme park day",
        "Ride the big wheel",
        "Fair time!",
    ],
    typo_en = [
        "ride the ferris whele",
        "visit the amsuement park",
        "go to the couty fair",
        "theme pakr with kids",
    ],
    bnd_en = [
        "Ride a roller coaster at the park",
        "Go on the carousel",
        "Try the bumper cars",
        "Ride the water slide",
        "Go on the Tilt-a-Whirl",
        "Try the drop tower ride",
    ],
    valid_en = [
        "Ride the ferris wheel",
        "Visit the amusement park",
        "See the view from the top",
    ],
    test_en = [
        "Go to the county fair",
        "Take kids to the theme park",
        "Take photos from the ferris wheel",
    ],
)

# ============================================================
# 171. file
# ============================================================
process_icon(
    "file",
    st_en = ["cv", "document", "page", "pdf", "resume"],
    pst_en = [
        "Update the CV before applying", "Send the CV to the recruiter",
        "Save the document", "Open the document in Word",
        "Turn to the next page", "Print the document page",
        "Export the file as PDF", "Send the document as PDF",
        "Update the resume", "Send the resume to the company",
    ],
    reg_en = [
        "Save the document to the folder",
        "Open a new file in Word",
        "Export the report as PDF",
        "Update the resume",
        "Create a new document",
        "Rename the file",
        "Attach the document to the email",
        "Print the document",
        "Share the PDF with the team",
        "Sign the document digitally",
    ],
    conv_en = [
        "Save the file",
        "Open the doc",
        "Send the PDF",
        "New document",
    ],
    typo_en = [
        "save the documnet",
        "open a neew file",
        "exprt as pdf",
        "update the resurme",
    ],
    bnd_en = [
        "Save to a folder structure",
        "Organize files in a directory",
        "Attach a photo to the email",
        "Create a spreadsheet",
        "Write in a text editor",
        "Archive old documents",
    ],
    valid_en = [
        "Save the document",
        "Export the report as PDF",
        "Update and send the resume",
    ],
    test_en = [
        "Create a new document",
        "Attach the file to the email",
        "Print the document",
    ],
)

# ============================================================
# 172. film
# ============================================================
process_icon(
    "film",
    st_en = ["cinema", "film", "film frames", "frames", "movie", "strip", "video"],
    pst_en = [
        "Go to the cinema tonight", "Buy tickets at the cinema",
        "Watch a film at home", "Recommend a good film",
        "Look at the film frames on the strip", "Edit the film frames",
        "Count the frames per second", "Edit frames in the video",
        "Watch the movie at the premiere", "See the movie trailer",
        "Scan the old film strip", "Find a 35mm film strip",
        "Edit the video clip", "Record a video for the project",
    ],
    reg_en = [
        "Watch a movie at the cinema",
        "Stream a film tonight",
        "Edit the video project",
        "Watch the new film release",
        "Buy a movie ticket online",
        "Choose a film to watch",
        "Review the film footage",
        "Watch a classic film",
        "Download a movie for offline watching",
        "Recommend a film to a friend",
    ],
    conv_en = [
        "Movie night!",
        "Watch a film",
        "Cinema run",
        "What film tonight?",
    ],
    typo_en = [
        "go to the ciinema",
        "wathc a flim tonight",
        "buy movei tickets",
        "straeam a film",
    ],
    bnd_en = [
        "Record on a film canister",
        "Watch a documentary series",
        "Listen to a movie soundtrack",
        "Read a movie script",
        "Develop a roll of film",
        "Shoot a video with the camera",
    ],
    valid_en = [
        "Watch a movie at the cinema",
        "Stream a film tonight",
        "Edit the video footage",
    ],
    test_en = [
        "Buy a movie ticket online",
        "Recommend a film to a friend",
        "Choose what film to watch",
    ],
)

# ============================================================
# 173. film-canister
# ============================================================
process_icon(
    "film-canister",
    st_en = ["35mm", "darkroom", "develop", "image", "photo", "photography", "retro", "vintage"],
    pst_en = [
        "Shoot with a 35mm camera", "Buy a 35mm film roll",
        "Develop film in the darkroom", "Set up a darkroom at home",
        "Develop the film roll", "Take the film to be developed",
        "Scan the developed image", "Print the image on photo paper",
        "Take a photo on film", "Buy a disposable film camera",
        "Learn film photography", "Practice film photography",
        "Get a retro look with film", "Embrace the retro photography style",
        "Find vintage film cameras", "Shoot with a vintage camera",
    ],
    reg_en = [
        "Shoot with a film camera",
        "Buy a roll of 35mm film",
        "Develop the film at the photo lab",
        "Collect vintage film cameras",
        "Learn analog photography",
        "Scan old film negatives",
        "Print photos from film",
        "Try shooting on film for the first time",
        "Find a darkroom to develop film",
        "Take photos on a disposable camera",
    ],
    conv_en = [
        "Shoot on film",
        "Analog vibes",
        "Develop the roll",
        "Retro photography",
    ],
    typo_en = [
        "shoot with 35mm flim",
        "devlop the film roll",
        "by a disposbale camera",
        "vintge film photography",
    ],
    bnd_en = [
        "Shoot with a digital camera",
        "Edit photos in Lightroom",
        "Take photos with the phone",
        "Print photos from a digital file",
        "Use a mirrorless camera",
        "Record video with a cinema camera",
    ],
    valid_en = [
        "Shoot with a 35mm film camera",
        "Develop the film at the photo lab",
        "Buy a roll of analog film",
    ],
    test_en = [
        "Learn analog photography",
        "Scan old film negatives",
        "Collect vintage film cameras",
    ],
)

# ============================================================
# 174. fish
# ============================================================
process_icon(
    "fish",
    st_en = ["fauna", "fish", "seafood", "swimming", "zodiac"],
    pst_en = [
        "Observe fish in the pond", "Learn about aquatic fauna",
        "Buy fresh fish at the market", "Cook fish for dinner",
        "Order seafood at the restaurant", "Buy seafood for the BBQ",
        "Watch fish swimming in the tank", "Swimming with fish while snorkeling",
        "Check the Pisces zodiac sign", "Read the Pisces horoscope",
    ],
    reg_en = [
        "Cook fish for dinner",
        "Buy fresh fish at the market",
        "Go fishing at the lake",
        "Feed the fish in the aquarium",
        "Clean the fish tank",
        "Set up a home aquarium",
        "Catch fish on the fishing trip",
        "Make a fish and chips dinner",
        "Find a good seafood restaurant",
        "Grill fish for the BBQ",
    ],
    conv_en = [
        "Fish for dinner",
        "Go fishing",
        "Clean the tank",
        "Seafood night",
    ],
    typo_en = [
        "cook fsh for dinner",
        "buy freesh fish",
        "go fihsing at the lake",
        "feed the fsh in tank",
    ],
    bnd_en = [
        "Cook shrimp for the seafood platter",
        "Order crab legs at the restaurant",
        "Set up a saltwater aquarium",
        "Watch sharks at the aquarium",
        "See dolphins at the ocean park",
        "Buy salmon at the grocery store",
    ],
    valid_en = [
        "Cook fish for dinner",
        "Go fishing at the lake",
        "Feed the fish in the aquarium",
    ],
    test_en = [
        "Buy fresh fish at the market",
        "Grill fish for the BBQ",
        "Clean the fish tank",
    ],
)

# ============================================================
# 175. flag-checkered
# ============================================================
process_icon(
    "flag-checkered",
    st_en = ["checkered", "finish", "racing", "start", "win"],
    pst_en = [
        "Wave the checkered flag at the finish", "Checkered flag for the winner",
        "Cross the finish line first", "Run toward the finish line",
        "Watch the racing event", "Go to the car racing event",
        "Start the race with the flag", "Flag the start of the event",
        "Celebrate the win", "Win the competition",
    ],
    reg_en = [
        "Watch the Formula 1 race",
        "Attend a car racing event",
        "Wave the checkered flag",
        "Cheer as the driver crosses the finish line",
        "Celebrate the race victory",
        "Watch a NASCAR race",
        "Go to the local go-kart race",
        "Complete the marathon run",
        "Finish the challenge",
        "Reach the goal",
    ],
    conv_en = [
        "Race day!",
        "Finish line",
        "Checkered flag",
        "We won!",
    ],
    typo_en = [
        "wach the formula 1 raice",
        "wave the checkerd flag",
        "cross the finsh line",
        "celebarte the race win",
    ],
    bnd_en = [
        "Score a goal in soccer",
        "Win the tennis match",
        "Complete a board game",
        "Finish a marathon",
        "Cross the swimming finish",
        "Complete the obstacle course",
    ],
    valid_en = [
        "Wave the checkered flag at the race",
        "Cross the finish line",
        "Celebrate the racing victory",
    ],
    test_en = [
        "Watch the car race",
        "Reach the finish line",
        "Win the competition",
    ],
)

# ============================================================
# 176. flashlight
# ============================================================
process_icon(
    "flashlight",
    st_en = ["camping", "flashlight", "lamp", "light", "tool", "torch"],
    pst_en = [
        "Pack a flashlight for camping", "Use a flashlight at the campsite",
        "Grab the flashlight for the power outage", "Find things with the flashlight",
        "Replace the lamp batteries", "Buy a bright lamp",
        "Turn on the light in the dark", "Find the light switch",
        "Pack the torch as a tool", "Use the tool for the job",
        "Use the torch to navigate in the dark", "Carry a torch on the night hike",
    ],
    reg_en = [
        "Pack a flashlight for the camping trip",
        "Use the flashlight during a power outage",
        "Check the batteries in the flashlight",
        "Carry a torch on the night hike",
        "Buy a headlamp for camping",
        "Find the way in the dark with a torch",
        "Keep a flashlight in the car",
        "Search the attic with a flashlight",
        "Use the phone flashlight in a pinch",
        "Set up emergency lights",
    ],
    conv_en = [
        "Grab the flashlight",
        "Power's out",
        "Dark in here",
        "Need a torch",
    ],
    typo_en = [
        "pack a flashlgiht for camping",
        "use the troch in the dark",
        "chekc the flashlgiht batteries",
        "by a hedlamp",
    ],
    bnd_en = [
        "Turn on the room light switch",
        "Set up a camping lantern",
        "Use a candle during a power outage",
        "Install outdoor security lights",
        "Use the phone as a light source",
        "Set up a lamp in the living room",
    ],
    valid_en = [
        "Pack a flashlight for camping",
        "Use the torch during the power outage",
        "Keep a flashlight in the car",
    ],
    test_en = [
        "Search the attic with a flashlight",
        "Carry a torch on the night hike",
        "Check the flashlight batteries",
    ],
)

# ============================================================
# 177. flask
# ============================================================
process_icon(
    "flask",
    st_en = ["beaker", "chemicals", "experiment", "knowledge", "labs", "liquid", "science", "vial"],
    pst_en = [
        "Use a beaker in the lab", "Clean the glass beaker",
        "Handle chemicals safely", "Store chemicals in labeled containers",
        "Set up a science experiment", "Run the chemistry experiment",
        "Expand knowledge through science", "Gain knowledge in the lab",
        "Work at the research labs", "Set up the labs for testing",
        "Pour liquid into the flask", "Measure liquid with precision",
        "Learn basic science concepts", "Apply science to real problems",
        "Store the sample in a vial", "Label the vial correctly",
    ],
    reg_en = [
        "Do a science experiment at home",
        "Set up a chemistry lab",
        "Mix chemicals for the experiment",
        "Measure liquids in the beaker",
        "Follow the lab safety rules",
        "Record the results of the experiment",
        "Pour the solution into the flask",
        "Work on a science project",
        "Study chemistry",
        "Visit the science museum",
    ],
    conv_en = [
        "Science experiment",
        "Lab time",
        "Mix the chemicals",
        "Flask and beaker",
    ],
    typo_en = [
        "do a scince experiment",
        "mix the chemiacls",
        "measuer liquids in beakre",
        "folow lab safty rules",
    ],
    bnd_en = [
        "Cook a meal in the kitchen",
        "Mix a cocktail at the bar",
        "Use a test tube for the biology class",
        "Set up the microscope",
        "Measure ingredients for baking",
        "Do a medical lab test",
    ],
    valid_en = [
        "Set up a science experiment",
        "Mix chemicals in the flask",
        "Record the lab results",
    ],
    test_en = [
        "Pour liquid into the beaker",
        "Work on the chemistry project",
        "Follow lab safety procedures",
    ],
)

# ============================================================
# 178. flatbread
# ============================================================
process_icon(
    "flatbread",
    st_en = ["arepa", "flatbread", "lavash", "naan", "pita"],
    pst_en = [
        "Make an arepa for breakfast", "Try Colombian arepa",
        "Bake flatbread at home", "Buy flatbread at the bakery",
        "Make lavash wraps", "Use lavash for the appetizer",
        "Order naan with the curry", "Bake naan in the oven",
        "Buy pita bread at the store", "Make pita from scratch",
    ],
    reg_en = [
        "Make naan to go with the curry",
        "Buy pita bread for the dip",
        "Bake homemade flatbread",
        "Make an arepa for breakfast",
        "Use lavash for a wrap",
        "Toast the flatbread before serving",
        "Dip flatbread in hummus",
        "Make a flatbread pizza",
        "Order naan from the Indian restaurant",
        "Serve warm flatbread with dinner",
    ],
    conv_en = [
        "Naan with curry!",
        "Bake flatbread",
        "Pita and hummus",
        "Flatbread time",
    ],
    typo_en = [
        "make naaan for curry",
        "buy pita berad",
        "bake flatbrad at home",
        "lavsah wrap recipe",
    ],
    bnd_en = [
        "Buy a stuffed pita with falafel",
        "Make a gyro wrap",
        "Toast a regular bread slice",
        "Make a sourdough loaf",
        "Bake a baguette",
        "Make a pizza on thick dough",
    ],
    valid_en = [
        "Bake flatbread at home",
        "Make naan with the curry",
        "Buy pita for the dip",
    ],
    test_en = [
        "Toast flatbread before serving",
        "Dip flatbread in hummus",
        "Make a flatbread pizza",
    ],
)

# ============================================================
# 179. flatbread-stuffed
# ============================================================
process_icon(
    "flatbread-stuffed",
    st_en = ["falafel", "gyro", "kebab", "pita", "sandwich"],
    pst_en = [
        "Make a stuffed pita with falafel", "Order a falafel pita wrap",
        "Try a Greek gyro for lunch", "Order a gyro at the restaurant",
        "Get a kebab wrap for dinner", "Make a homemade kebab wrap",
        "Stuff the pita with fillings", "Buy a pita wrap",
        "Make a pita sandwich for lunch", "Try a stuffed flatbread sandwich",
    ],
    reg_en = [
        "Order a gyro wrap for lunch",
        "Make a stuffed pita at home",
        "Try a kebab from the food truck",
        "Make a falafel wrap",
        "Fill pita bread with salad and meat",
        "Get a Mediterranean wrap",
        "Order a souvlaki pita",
        "Make a chicken shawarma wrap",
        "Pack a pita sandwich for lunch",
        "Try a stuffed flatbread at the restaurant",
    ],
    conv_en = [
        "Gyro time!",
        "Kebab wrap",
        "Stuffed pita",
        "Mediterranean lunch",
    ],
    typo_en = [
        "order a gyro warp",
        "make stuffed pitta",
        "kebab warp for dinner",
        "falafel pita sanwich",
    ],
    bnd_en = [
        "Make plain flatbread without stuffing",
        "Eat a burger with no wrapping",
        "Order a regular sandwich on bread",
        "Make a plain naan",
        "Eat hummus with plain pita",
        "Order a sub sandwich",
    ],
    valid_en = [
        "Order a gyro wrap for lunch",
        "Make a stuffed pita",
        "Try a kebab from the food truck",
    ],
    test_en = [
        "Make a falafel wrap",
        "Pack a pita sandwich for lunch",
        "Order a Mediterranean wrap",
    ],
)

print("\nAll 30 icons processed successfully!")
