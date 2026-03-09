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
# 210. hat-chef
# ============================================================
process_icon(
    "hat-chef",
    st_en = ["cook", "cuisine", "culinary", "dining", "kitchen"],
    pst_en = [
        "Cook a new recipe tonight", "Learn to cook from scratch",
        "Try a new cuisine this week", "Explore international cuisine",
        "Take a culinary class", "Improve culinary skills",
        "Book a fine dining experience", "Enjoy a dining experience",
        "Organize the kitchen", "Cook in a professional kitchen",
    ],
    reg_en = [
        "Take a cooking class",
        "Wear the chef hat at the event",
        "Cook a professional meal at home",
        "Try a new recipe from scratch",
        "Watch a cooking show for inspiration",
        "Follow a culinary course online",
        "Host a dinner party",
        "Learn French cuisine techniques",
        "Cook a gourmet meal",
        "Prepare a multi-course dinner",
    ],
    conv_en = [
        "Chef mode on",
        "Cook something fancy",
        "Culinary adventure",
        "Kitchen time!",
    ],
    typo_en = [
        "take a cookin class",
        "weare the chef hat",
        "cook a profesional meal",
        "try a new recpie",
    ],
    bnd_en = [
        "Order from a professional chef online",
        "Buy a cooking apron",
        "Watch a restaurant review show",
        "Set a dinner table with cutlery",
        "Use a kitchen timer",
        "Buy kitchen utensils",
    ],
    valid_en = [
        "Take a cooking class",
        "Cook a gourmet meal at home",
        "Try a new culinary technique",
    ],
    test_en = [
        "Host a dinner party",
        "Follow a culinary course",
        "Cook a professional meal",
    ],
)

# ============================================================
# 211. heading
# ============================================================
process_icon(
    "heading",
    st_en = ["format", "header", "text", "title"],
    pst_en = [
        "Apply the correct text format", "Format the document",
        "Add a header to the document", "Edit the page header",
        "Style the text in the editor", "Increase the text size",
        "Add a title to the article", "Edit the page title",
    ],
    reg_en = [
        "Add a heading to the document",
        "Format text as a header",
        "Use H1 for the main title",
        "Apply heading style in Word",
        "Add a section heading",
        "Set the page title",
        "Use heading tags in HTML",
        "Organize content with headings",
        "Change the heading font size",
        "Format the blog post heading",
    ],
    conv_en = [
        "Add a heading",
        "Set the title",
        "Format the header",
        "Big title text",
    ],
    typo_en = [
        "add a headin to the doc",
        "formatt text as header",
        "use h1 for main ttile",
        "apply headign stlye",
    ],
    bnd_en = [
        "Add a paragraph of body text",
        "Create a bullet list",
        "Insert a table in the document",
        "Add a caption below the image",
        "Write a footnote",
        "Apply bold formatting to the text",
    ],
    valid_en = [
        "Add a heading to the document",
        "Format text as a title",
        "Use H1 for the main heading",
    ],
    test_en = [
        "Apply heading style in Word",
        "Organize content with headings",
        "Format the blog post heading",
    ],
)

# ============================================================
# 212. headset
# ============================================================
process_icon(
    "headset",
    st_en = ["audio", "gaming", "listen", "microphone", "sound", "support"],
    pst_en = [
        "Plug in audio for the call", "Buy good audio equipment",
        "Use the headset for gaming", "Play games with the headset on",
        "Listen to music with the headset", "Listen to the meeting recording",
        "Use the microphone for the call", "Mute the microphone",
        "Hear the sound clearly", "Adjust the sound volume",
        "Contact customer support", "Work in customer support",
    ],
    reg_en = [
        "Use the headset for a video call",
        "Buy a gaming headset",
        "Connect the headset to the computer",
        "Use headset for the customer support shift",
        "Listen to music while working",
        "Join the online meeting with headset",
        "Adjust the headset microphone",
        "Use a noise-canceling headset",
        "Set up the headset for the podcast",
        "Charge the wireless headset",
    ],
    conv_en = [
        "Headset on",
        "Join the call",
        "Gaming time",
        "Support shift",
    ],
    typo_en = [
        "use the headste for call",
        "buy a gamign headset",
        "lsiten with headphones",
        "connet headset to pc",
    ],
    bnd_en = [
        "Listen with earbuds",
        "Use speakers for the meeting",
        "Use a standalone microphone",
        "Wear noise-canceling headphones",
        "Use a Bluetooth earpiece",
        "Connect to a speakerphone",
    ],
    valid_en = [
        "Use the headset for a video call",
        "Buy a gaming headset",
        "Use headset for customer support",
    ],
    test_en = [
        "Connect the headset to the computer",
        "Adjust the headset microphone",
        "Use a noise-canceling headset",
    ],
)

# ============================================================
# 213. heart-pulse
# ============================================================
process_icon(
    "heart-pulse",
    st_en = ["ekg", "health", "lifeline", "vital signs"],
    pst_en = [
        "Get an EKG test done", "Check the EKG results",
        "Monitor heart health", "Check overall health",
        "Check the patient's lifeline", "Track fitness lifeline",
        "Check vital signs at the clinic", "Record vital signs",
    ],
    reg_en = [
        "Check heart rate at the doctor",
        "Monitor heart health with a smartwatch",
        "Get an EKG test",
        "Track fitness and heart rate",
        "Go to cardiology appointment",
        "Check blood pressure and pulse",
        "Measure heart rate after exercise",
        "Book a heart health checkup",
        "Monitor vital signs at the hospital",
        "Use a fitness tracker for heart rate",
    ],
    conv_en = [
        "Check heart rate",
        "Cardio check",
        "Health checkup",
        "Vital signs",
    ],
    typo_en = [
        "chekc heart rat at doctor",
        "moniotr heart helath",
        "get an ekeg test",
        "track fitnes heart rate",
    ],
    bnd_en = [
        "Measure blood pressure",
        "Check oxygen saturation",
        "Monitor blood sugar levels",
        "Track steps on the fitness app",
        "Get a full body health scan",
        "Check body temperature",
    ],
    valid_en = [
        "Check heart rate at the doctor",
        "Get an EKG test",
        "Monitor vital signs",
    ],
    test_en = [
        "Track heart health with a smartwatch",
        "Book a cardiology appointment",
        "Measure heart rate after exercise",
    ],
)

# ============================================================
# 214. helmet-battle
# ============================================================
process_icon(
    "helmet-battle",
    st_en = ["armor", "d&d", "fantasy", "knight", "paladin"],
    pst_en = [
        "Equip armor for the battle", "Find better armor in the dungeon",
        "Play D&D as a knight", "Set up the D&D campaign",
        "Build a fantasy character", "Read a fantasy novel",
        "Play as the noble knight", "Knight the character in the game",
        "Choose the paladin class", "Level up the paladin",
    ],
    reg_en = [
        "Play a knight character in D&D",
        "Build a paladin for the campaign",
        "Equip battle armor in the game",
        "Read a medieval fantasy book",
        "Watch a knights and dragons movie",
        "Design a knight costume for Halloween",
        "Visit a medieval castle exhibit",
        "Play a tabletop RPG as a knight",
        "Write a fantasy story with knights",
        "Play a video game with medieval armor",
    ],
    conv_en = [
        "D&D night",
        "Knight character",
        "Fantasy game",
        "Suit up for battle",
    ],
    typo_en = [
        "equip armro for battle",
        "play a kngiht in dnd",
        "chooese the paldin class",
        "fantsy character creation",
    ],
    bnd_en = [
        "Play as a rogue in the game",
        "Wear a wizard hat for D&D",
        "Use a hood cloak for stealth",
        "Equip a dagger instead of armor",
        "Cast spells as a mage",
        "Wear a hockey helmet for sport",
    ],
    valid_en = [
        "Play a knight in the D&D campaign",
        "Equip battle armor in the game",
        "Choose the paladin class",
    ],
    test_en = [
        "Build a knight character for D&D",
        "Read a medieval fantasy story",
        "Design a knight costume",
    ],
)

# ============================================================
# 215. hockey-mask
# ============================================================
process_icon(
    "hockey-mask",
    st_en = ["halloween", "ice", "nhl", "protection", "sport"],
    pst_en = [
        "Wear a hockey mask for Halloween", "Get the Jason hockey mask costume",
        "Skate on ice at the rink", "Book ice time for practice",
        "Watch the NHL playoffs", "Follow the NHL season",
        "Wear protection gear for hockey", "Buy face protection for hockey",
        "Try an ice sport this winter", "Sign up for a sport league",
    ],
    reg_en = [
        "Wear a hockey goalie mask",
        "Buy protective gear for hockey",
        "Watch the NHL game tonight",
        "Use a hockey mask as a Halloween costume",
        "Play goalie in the hockey game",
        "Order a custom hockey mask",
        "Practice hockey with proper protection",
        "Attend an NHL game live",
        "Buy hockey safety equipment",
        "Train as a hockey goaltender",
    ],
    conv_en = [
        "Hockey game!",
        "Goalie gear",
        "Halloween mask",
        "NHL tonight",
    ],
    typo_en = [
        "ware a hocky mask",
        "wacth the nhl gamee",
        "buy protectoin gear",
        "hocky goalie massk",
    ],
    bnd_en = [
        "Wear a football helmet",
        "Use a face shield for protection",
        "Wear a ski helmet on the slopes",
        "Put on a motorcycle helmet",
        "Wear a boxing headguard",
        "Use a Halloween pumpkin mask",
    ],
    valid_en = [
        "Wear a hockey goalie mask",
        "Watch the NHL game",
        "Buy protective gear for hockey",
    ],
    test_en = [
        "Play goalie with a hockey mask",
        "Use a hockey mask for Halloween",
        "Attend an NHL game live",
    ],
)

# ============================================================
# 216. hockey-puck
# ============================================================
process_icon(
    "hockey-puck",
    st_en = ["ice", "nhl", "sport"],
    pst_en = [
        "Skate on the ice rink", "Clear the ice before the game",
        "Watch the NHL match tonight", "Follow the NHL playoffs",
        "Play an ice sport this winter", "Sign up for hockey as a sport",
    ],
    reg_en = [
        "Shoot the puck on goal",
        "Watch the hockey game on TV",
        "Buy a hockey puck for practice",
        "Play street hockey with a puck",
        "Attend an NHL game",
        "Collect a signed hockey puck",
        "Use the puck for hockey drills",
        "Practice slap shots at the rink",
        "Join a hockey league",
        "Buy hockey equipment",
    ],
    conv_en = [
        "Shoot the puck!",
        "Hockey tonight",
        "Puck drop",
        "NHL game",
    ],
    typo_en = [
        "shott the puck on goaal",
        "wacth the hocky game",
        "buy a hocky pukc",
        "practce slap shots",
    ],
    bnd_en = [
        "Hit the hockey sticks together",
        "Use a soccer ball instead",
        "Play with a lacrosse ball",
        "Shoot a basketball",
        "Hit a baseball pitch",
        "Use a tennis ball for practice",
    ],
    valid_en = [
        "Shoot the puck on goal",
        "Watch the NHL game",
        "Buy a hockey puck",
    ],
    test_en = [
        "Play hockey drills with the puck",
        "Join a hockey league",
        "Attend an NHL game",
    ],
)

# ============================================================
# 217. hockey-sticks
# ============================================================
process_icon(
    "hockey-sticks",
    st_en = ["ice", "nhl", "sport"],
    pst_en = [
        "Skate on the ice with the team", "Practice on ice",
        "Watch the NHL match", "Follow NHL standings",
        "Play hockey as a sport", "Train for the sport",
    ],
    reg_en = [
        "Buy a new hockey stick",
        "Practice stick handling drills",
        "Choose the right hockey stick flex",
        "Tape the hockey stick blade",
        "Join a hockey team",
        "Play street hockey with sticks",
        "Watch the hockey game",
        "Sign kids up for hockey",
        "Find a good hockey stick for beginners",
        "Repair the cracked hockey stick",
    ],
    conv_en = [
        "Hockey drills",
        "Tape the stick",
        "New hockey stick",
        "Stick handling",
    ],
    typo_en = [
        "buy a new hocky stikc",
        "pratice stick handlign",
        "tape the hocky stick blaed",
        "jion a hocky team",
    ],
    bnd_en = [
        "Shoot the puck with the stick",
        "Use a lacrosse stick instead",
        "Swing a baseball bat",
        "Use a golf club on the course",
        "Hit with a tennis racket",
        "Use a cricket bat",
    ],
    valid_en = [
        "Buy a new hockey stick",
        "Practice stick handling",
        "Join a hockey team",
    ],
    test_en = [
        "Tape the hockey stick blade",
        "Play street hockey with sticks",
        "Sign kids up for hockey",
    ],
)

# ============================================================
# 218. hood-cloak
# ============================================================
process_icon(
    "hood-cloak",
    st_en = ["clothing", "d&d", "fantasy", "rogue", "stealth"],
    pst_en = [
        "Wear a hood cloak costume", "Buy a cloak for the costume party",
        "Play D&D tonight", "Set up the D&D session",
        "Design a fantasy character", "Build a fantasy world",
        "Play the rogue class in the campaign", "Sneak as a rogue",
        "Use stealth to pass the enemy", "Move in stealth mode",
    ],
    reg_en = [
        "Play a rogue character in D&D",
        "Wear a cloak for the Halloween costume",
        "Design a hooded character in the game",
        "Use stealth in the RPG game",
        "Build a rogue for the D&D campaign",
        "Read a fantasy book with a hooded hero",
        "Watch a fantasy movie tonight",
        "Find a cloak prop for the costume",
        "Write a fantasy story with a rogue",
        "Play as the shadowy rogue class",
    ],
    conv_en = [
        "Rogue character",
        "D&D stealth",
        "Cloak up",
        "Fantasy game",
    ],
    typo_en = [
        "play a rogu in dnd",
        "weare a cloak costume",
        "use stealth in rpg gamme",
        "fantsy rogue character",
    ],
    bnd_en = [
        "Wear battle armor as a knight",
        "Use a wizard hat for magic",
        "Equip a paladin helmet",
        "Wear a party hat for the celebration",
        "Use a winter coat outdoors",
        "Wear a raincoat in the rain",
    ],
    valid_en = [
        "Play a rogue in the D&D campaign",
        "Wear a hood cloak for Halloween",
        "Use stealth in the fantasy game",
    ],
    test_en = [
        "Design a hooded character",
        "Build a rogue for D&D",
        "Read a fantasy book with a hooded hero",
    ],
)

# ============================================================
# 219. horse
# ============================================================
process_icon(
    "horse",
    st_en = ["equestrian", "fauna", "horse", "mare", "pony", "racehorse", "racing"],
    pst_en = [
        "Take equestrian lessons", "Watch the equestrian event",
        "Observe fauna on the ranch", "See fauna at the stables",
        "Ride a horse on the trail", "Feed the horse at the stable",
        "Brush the mare after riding", "Care for the mare at the farm",
        "Ride a pony at the fair", "Buy a pony for the kids",
        "Watch the racehorse at the track", "Bet on a racehorse",
        "Watch horse racing on TV", "Go to the horse racing event",
    ],
    reg_en = [
        "Take horse riding lessons",
        "Visit a horse ranch",
        "Go horseback riding on the trail",
        "Watch the Kentucky Derby",
        "Feed and groom the horse",
        "Book a horseback riding tour",
        "Attend a horse show",
        "Take the kids to see ponies",
        "Watch horses race at the track",
        "Volunteer at the horse sanctuary",
    ],
    conv_en = [
        "Horseback riding!",
        "Visit the stable",
        "Race day",
        "Horse show",
    ],
    typo_en = [
        "take hrose riding lesosns",
        "vist a hrose ranch",
        "go horsebakc riding",
        "wacth the kenutcky derby",
    ],
    bnd_en = [
        "Ride a horse with a saddle",
        "Visit a donkey sanctuary",
        "See zebras at the safari",
        "Watch cows graze at the farm",
        "Ride a camel in the desert",
        "See a moose in the wild",
    ],
    valid_en = [
        "Take horse riding lessons",
        "Go horseback riding on the trail",
        "Watch the horse race",
    ],
    test_en = [
        "Visit a horse ranch",
        "Book a horseback riding tour",
        "Attend a horse show",
    ],
)

# ============================================================
# 220. horse-saddle
# ============================================================
process_icon(
    "horse-saddle",
    st_en = ["cowboy", "fauna", "mare", "pony", "rodeo", "western"],
    pst_en = [
        "Dress as a cowboy for the event", "Buy cowboy boots and hat",
        "Observe fauna at the ranch", "Wildlife and fauna on the western plains",
        "Brush the mare before saddling", "Ride the mare on the trail",
        "Ride a pony with a saddle", "Saddle up the pony",
        "Watch the rodeo event", "Compete in the rodeo",
        "Watch a western movie", "Enjoy a western-style dinner",
    ],
    reg_en = [
        "Saddle up the horse for a ride",
        "Attend a rodeo event",
        "Take a western horseback riding tour",
        "Watch a classic western movie",
        "Buy a leather saddle",
        "Clean and oil the saddle",
        "Visit a dude ranch",
        "Dress in western wear for the event",
        "Watch bull riding at the rodeo",
        "Learn to lasso at the ranch",
    ],
    conv_en = [
        "Saddle up!",
        "Rodeo time",
        "Western ride",
        "Cowboy mode",
    ],
    typo_en = [
        "sadle up the horse",
        "watcch the rodeo evnet",
        "take a westenr ride",
        "buy a learther saddle",
    ],
    bnd_en = [
        "Ride a horse without a saddle",
        "Put the bridle on the horse",
        "Use a riding helmet for safety",
        "Visit a farm to see horses",
        "Watch horse racing at the track",
        "Buy horseshoes for the stable",
    ],
    valid_en = [
        "Saddle up the horse",
        "Attend a rodeo event",
        "Take a western horseback tour",
    ],
    test_en = [
        "Buy a leather saddle",
        "Visit a dude ranch",
        "Watch bull riding at the rodeo",
    ],
)

# ============================================================
# 221. hose-reel
# ============================================================
process_icon(
    "hose-reel",
    st_en = ["fire", "irrigation", "water"],
    pst_en = [
        "Check the fire hose reel location", "Unroll the fire hose",
        "Set up the irrigation system", "Water the garden with irrigation",
        "Water the garden with the hose", "Coil the hose on the reel",
    ],
    reg_en = [
        "Water the garden with the hose",
        "Roll up the garden hose",
        "Buy a hose reel for the garden",
        "Set up the irrigation system",
        "Check the fire hose in the building",
        "Connect the hose to the outdoor tap",
        "Wash the car with the garden hose",
        "Unravel the garden hose",
        "Replace the leaking hose",
        "Install a retractable hose reel",
    ],
    conv_en = [
        "Water the garden",
        "Roll up the hose",
        "Garden hose",
        "Irrigation time",
    ],
    typo_en = [
        "watr the garden with hoes",
        "rol up the garden hoes",
        "buy a hose reel fo garden",
        "set up the irigation",
    ],
    bnd_en = [
        "Use a watering can for plants",
        "Set up a sprinkler system",
        "Water flowers with a bottle",
        "Use drip irrigation for plants",
        "Use a pressure washer for the driveway",
        "Fill the pool with a hose",
    ],
    valid_en = [
        "Water the garden with the hose",
        "Roll up the hose on the reel",
        "Set up the irrigation system",
    ],
    test_en = [
        "Buy a hose reel for the garden",
        "Connect the hose to the outdoor tap",
        "Install a retractable hose reel",
    ],
)

# ============================================================
# 222. hospital-user
# ============================================================
process_icon(
    "hospital-user",
    st_en = ["doctor", "patient", "primary care"],
    pst_en = [
        "See the doctor for a checkup", "Schedule an appointment with the doctor",
        "Register as a new patient", "Check patient records",
        "Visit primary care for a routine checkup", "Find a primary care physician",
    ],
    reg_en = [
        "Book an appointment with the doctor",
        "Visit the family doctor",
        "Get a referral from the primary care doctor",
        "Check in as a patient at the clinic",
        "Review patient health history",
        "Get a physical exam",
        "See the doctor about the symptoms",
        "Register at the new clinic",
        "Follow up with the primary care doctor",
        "Schedule a telehealth appointment",
    ],
    conv_en = [
        "Doctor visit",
        "See the doc",
        "Patient checkup",
        "Primary care",
    ],
    typo_en = [
        "book an appointemnt with doctr",
        "vist the famly doctor",
        "get a referrl from doctor",
        "se the doctor about symtoms",
    ],
    bnd_en = [
        "Go to the emergency room",
        "Visit the specialist",
        "Check into the hospital",
        "Call the nurse station",
        "See the dentist",
        "Visit the pharmacy",
    ],
    valid_en = [
        "Book a doctor appointment",
        "Visit the primary care physician",
        "Follow up with the doctor",
    ],
    test_en = [
        "Get a physical exam",
        "Register as a new patient",
        "Schedule a telehealth appointment",
    ],
)

# ============================================================
# 223. hospitals
# ============================================================
process_icon(
    "hospitals",
    st_en = ["emergency", "insurance", "network"],
    pst_en = [
        "Go to the emergency room", "Call emergency services",
        "Check the health insurance coverage", "Submit an insurance claim",
        "Find hospitals in the insurance network", "Check the hospital network",
    ],
    reg_en = [
        "Find the nearest hospital",
        "Call the hospital emergency line",
        "Check hospital visiting hours",
        "Navigate to the hospital",
        "Check if the hospital accepts insurance",
        "Find a hospital in the network",
        "Submit a hospital insurance claim",
        "Look up hospital ratings",
        "Find a specialist at the hospital",
        "Check in at the hospital reception",
    ],
    conv_en = [
        "Find a hospital",
        "Emergency room",
        "Hospital network",
        "Check insurance",
    ],
    typo_en = [
        "find the nearset hosptial",
        "call the hosptal emergeny",
        "chek hosptal visitng hours",
        "submitt an insurace claim",
    ],
    bnd_en = [
        "Visit a single family doctor",
        "Go to the urgent care clinic",
        "Call the ambulance",
        "Visit the pharmacy for medication",
        "See the specialist at the clinic",
        "Use a telemedicine service",
    ],
    valid_en = [
        "Find the nearest hospital",
        "Check hospital insurance coverage",
        "Navigate to the emergency room",
    ],
    test_en = [
        "Find a hospital in the network",
        "Submit a hospital insurance claim",
        "Look up hospital ratings",
    ],
)

# ============================================================
# 224. hotdog
# ============================================================
process_icon(
    "hotdog",
    st_en = ["bun", "chili", "hot dog", "hotdog", "sausage", "sandwich"],
    pst_en = [
        "Toast the bun before serving", "Buy hotdog buns at the store",
        "Make chili dogs for the party", "Top the hotdog with chili",
        "Grill hot dogs at the BBQ", "Order a hot dog at the game",
        "Make a hotdog for lunch", "Buy hotdog toppings",
        "Grill sausages at the cookout", "Buy bratwurst sausages",
        "Make a sausage sandwich", "Eat a sandwich for lunch",
    ],
    reg_en = [
        "Grill hotdogs at the BBQ",
        "Buy hotdogs for the cookout",
        "Make chili dogs at home",
        "Get a hotdog at the baseball game",
        "Top the hotdog with mustard and ketchup",
        "Cook hotdogs on the stove",
        "Make a corn dog batter",
        "Serve hotdogs at the kids party",
        "Order a hotdog from the food cart",
        "Make a Chicago-style hotdog",
    ],
    conv_en = [
        "Hotdog time!",
        "Grill the dogs",
        "Chili dog",
        "BBQ sausages",
    ],
    typo_en = [
        "gril hotdogs at the barbeque",
        "buy hotodgs for cookoout",
        "make chilli dogs at home",
        "get a hotdgo at the game",
    ],
    bnd_en = [
        "Make a burger at the grill",
        "Order a bratwurst at the fair",
        "Cook a corn dog in oil",
        "Make a breakfast sausage wrap",
        "Grill chicken wings instead",
        "Make a sandwich with deli meat",
    ],
    valid_en = [
        "Grill hotdogs at the BBQ",
        "Make chili dogs at home",
        "Top the hotdog with mustard",
    ],
    test_en = [
        "Get a hotdog at the baseball game",
        "Serve hotdogs at the party",
        "Order a hotdog from the food cart",
    ],
)

# ============================================================
# 225. hotel
# ============================================================
process_icon(
    "hotel",
    st_en = ["hotel", "inn", "lodging", "motel", "resort", "travel"],
    pst_en = [
        "Book a hotel for the trip", "Check hotel availability",
        "Stay at a cozy inn", "Find a bed and breakfast inn",
        "Book lodging for the trip", "Compare lodging options",
        "Reserve a room at the motel", "Stay at a motel on the road trip",
        "Book a resort for the vacation", "Relax at an all-inclusive resort",
        "Plan the travel accommodations", "Book travel and hotel together",
    ],
    reg_en = [
        "Book a hotel room online",
        "Check into the hotel",
        "Find a hotel near the venue",
        "Compare hotel prices",
        "Order room service at the hotel",
        "Request a late checkout",
        "Book a resort for the honeymoon",
        "Find pet-friendly hotel",
        "Stay at a boutique hotel",
        "Use hotel points for a free night",
    ],
    conv_en = [
        "Book the hotel",
        "Check in time",
        "Hotel tonight",
        "Resort vacation",
    ],
    typo_en = [
        "book a hotle for trip",
        "chekc into the hotell",
        "find a hotle nera the venue",
        "comprae hotle prices",
    ],
    bnd_en = [
        "Rent an Airbnb apartment",
        "Stay at a hostel",
        "Book a camping site",
        "Stay with family",
        "Rent a vacation home",
        "Book a cruise cabin",
    ],
    valid_en = [
        "Book a hotel room online",
        "Check into the hotel",
        "Find a hotel near the venue",
    ],
    test_en = [
        "Compare hotel prices",
        "Book a resort for vacation",
        "Request a late checkout",
    ],
)

# ============================================================
# 226. house
# ============================================================
process_icon(
    "house",
    st_en = ["building", "home", "house", "residence"],
    pst_en = [
        "Inspect the building before buying", "Maintain the building",
        "Go home after work", "Stay home today",
        "Buy a house this year", "Sell the house",
        "Register the new residence", "Change the residence address",
    ],
    reg_en = [
        "Go home after work",
        "Clean the house this weekend",
        "Pay the mortgage",
        "Fix something in the house",
        "Decorate the home for the holidays",
        "Mow the lawn at home",
        "Welcome guests to the house",
        "Buy a new home",
        "Renovate the house",
        "Add a security system to the house",
    ],
    conv_en = [
        "Heading home",
        "Home sweet home",
        "House chores",
        "Back home",
    ],
    typo_en = [
        "go hoem after wrok",
        "clen the hose",
        "pay the mortagge",
        "fix somethign in the house",
    ],
    bnd_en = [
        "Book a hotel for the trip",
        "Rent an apartment downtown",
        "Stay at a friend's place",
        "Visit the office building",
        "Buy a condo in the city",
        "Rent a vacation cabin",
    ],
    valid_en = [
        "Go home after work",
        "Clean the house",
        "Pay the mortgage",
    ],
    test_en = [
        "Decorate the home for the holidays",
        "Buy a new house",
        "Add a security system at home",
    ],
)

# ============================================================
# 227. hryvnia-sign
# ============================================================
process_icon(
    "hryvnia-sign",
    st_en = ["Hryvnia Sign", "currency"],
    pst_en = [
        "Pay in hryvnia in Ukraine", "Check the hryvnia exchange rate",
        "Exchange currency to hryvnia", "Convert hryvnia to dollars",
    ],
    reg_en = [
        "Exchange money to Ukrainian hryvnia",
        "Check the UAH exchange rate",
        "Pay in hryvnia while in Ukraine",
        "Send money in hryvnia",
        "Convert hryvnia to euros",
        "Find the best hryvnia exchange rate",
        "Budget the trip in hryvnia",
        "Withdraw hryvnia from the ATM",
        "Pay the invoice in hryvnia",
        "Transfer hryvnia internationally",
    ],
    conv_en = [
        "Ukraine trip budget",
        "Convert to hryvnia",
        "Pay in UAH",
        "Check UAH rate",
    ],
    typo_en = [
        "exchagne to hryvnai",
        "pay in hrivnia",
        "check uah excahnge rate",
        "convrt hryvnia to euros",
    ],
    bnd_en = [
        "Pay in euros",
        "Exchange to US dollars",
        "Use Russian rubles",
        "Pay in Polish zloty",
        "Exchange for British pounds",
        "Use a credit card abroad",
    ],
    valid_en = [
        "Exchange money to hryvnia",
        "Pay in hryvnia in Ukraine",
        "Check the UAH exchange rate",
    ],
    test_en = [
        "Convert hryvnia to euros",
        "Withdraw hryvnia from the ATM",
        "Budget the Ukraine trip",
    ],
)

# ============================================================
# 228. ice-skate
# ============================================================
process_icon(
    "ice-skate",
    st_en = ["figure skating", "hockey", "ice", "ice skate", "seasonal", "shoe", "skate"],
    pst_en = [
        "Watch figure skating at the Olympics", "Practice figure skating moves",
        "Play hockey on the ice", "Buy hockey ice skates",
        "Book ice time at the rink", "Skate on the outdoor ice rink",
        "Learn to ice skate", "Rent ice skates at the rink",
        "Enjoy a seasonal activity in winter", "Ice skate as a seasonal activity",
        "Buy ice skate shoes", "Get the right shoe size for skates",
        "Glide on the ice with skates", "Practice stopping on skates",
    ],
    reg_en = [
        "Go ice skating at the rink",
        "Rent ice skates at the venue",
        "Take ice skating lessons",
        "Buy ice skates for the winter",
        "Skate on the outdoor rink",
        "Watch figure skating competition",
        "Practice hockey skating",
        "Ice skate with the family",
        "Sharpen the ice skate blades",
        "Pack warm clothes for ice skating",
    ],
    conv_en = [
        "Ice skating!",
        "Hit the rink",
        "Winter skate",
        "Figure skating",
    ],
    typo_en = [
        "go ice skatign at the rnik",
        "rent ice skatse",
        "take ice skaitng lessons",
        "wach figure skatign",
    ],
    bnd_en = [
        "Go skiing on the mountain",
        "Try snowboarding this winter",
        "Play ice hockey without skates",
        "Go roller skating instead",
        "Wear snow boots for winter",
        "Go curling on the ice",
    ],
    valid_en = [
        "Go ice skating at the rink",
        "Take ice skating lessons",
        "Watch figure skating competition",
    ],
    test_en = [
        "Buy ice skates for winter",
        "Skate on the outdoor rink",
        "Ice skate with the family",
    ],
)

# ============================================================
# 229. image
# ============================================================
process_icon(
    "image",
    st_en = ["album", "landscape", "photo", "picture"],
    pst_en = [
        "Create a photo album", "Browse the photo album",
        "Take a landscape photo", "Edit the landscape shot",
        "Take a photo at the event", "Edit the photo before sharing",
        "Print the picture", "Frame the picture for the wall",
    ],
    reg_en = [
        "Take a photo with the camera",
        "Edit the image in Lightroom",
        "Share a photo on social media",
        "Print a photo for the album",
        "Set a photo as the wallpaper",
        "Crop the image for the post",
        "Upload a photo to the profile",
        "Browse vacation photos",
        "Back up photos to the cloud",
        "Create a photo collage",
    ],
    conv_en = [
        "Take a photo",
        "Nice picture",
        "Edit the image",
        "Share the photo",
    ],
    typo_en = [
        "take a potho at the event",
        "edit the imge in lightroom",
        "shrae a photo on social medai",
        "pritn a pictuer",
    ],
    bnd_en = [
        "Record a video instead",
        "Draw an illustration",
        "Scan a document",
        "Create an animated GIF",
        "Take a screenshot",
        "Download an icon from the web",
    ],
    valid_en = [
        "Take a photo at the event",
        "Edit the image before sharing",
        "Print a photo for the album",
    ],
    test_en = [
        "Share a photo on social media",
        "Back up photos to the cloud",
        "Create a photo collage",
    ],
)

# ============================================================
# 230. inbox
# ============================================================
process_icon(
    "inbox",
    st_en = ["archive", "email", "mail", "message"],
    pst_en = [
        "Archive old emails", "Move emails to the archive folder",
        "Check the email inbox", "Clear the email inbox",
        "Check the mail inbox", "Sort the incoming mail",
        "Reply to the message in inbox", "Check unread messages",
    ],
    reg_en = [
        "Check the inbox for new emails",
        "Clear out the inbox",
        "Reply to unread messages",
        "Sort emails into folders",
        "Check for new messages",
        "Archive old emails",
        "Mark all as read in the inbox",
        "Search the inbox for the email",
        "Set up an auto-reply for the inbox",
        "Check the inbox first thing in the morning",
    ],
    conv_en = [
        "Check inbox",
        "New messages",
        "Clear the inbox",
        "Unread emails",
    ],
    typo_en = [
        "chekc the inbxo",
        "clera out the inbox",
        "repyl to unread mesages",
        "sort emials into foldrers",
    ],
    bnd_en = [
        "Send an email from the outbox",
        "Check the spam folder",
        "Read messages in the sent folder",
        "Check the notification tray",
        "Read texts on the phone",
        "Check the physical mailbox outside",
    ],
    valid_en = [
        "Check inbox for new emails",
        "Clear out the inbox",
        "Reply to unread messages",
    ],
    test_en = [
        "Archive old emails",
        "Sort emails into folders",
        "Search the inbox for an email",
    ],
)

# ============================================================
# 231. industry
# ============================================================
process_icon(
    "industry",
    st_en = ["building", "factory", "industrial", "manufacturing", "mill", "warehouse"],
    pst_en = [
        "Visit the industrial building", "Inspect the building structure",
        "Tour the factory floor", "Work at the factory",
        "Work in an industrial zone", "Move to an industrial area",
        "Monitor the manufacturing line", "Improve manufacturing efficiency",
        "Visit the old mill", "Restore the historic mill",
        "Manage the warehouse operations", "Organize the warehouse floor",
    ],
    reg_en = [
        "Visit the manufacturing plant",
        "Inspect the factory equipment",
        "Work on the production line",
        "Manage warehouse operations",
        "Monitor industrial output",
        "Schedule a factory tour",
        "Improve industrial efficiency",
        "Order supplies for the factory",
        "Check safety at the industrial site",
        "Transport goods from the warehouse",
    ],
    conv_en = [
        "Factory tour",
        "Industrial site",
        "Warehouse check",
        "Production line",
    ],
    typo_en = [
        "viist the manufacurting plant",
        "inspekt the factroy",
        "work on productin line",
        "managge warehous operations",
    ],
    bnd_en = [
        "Visit an office building",
        "Manage a retail store",
        "Work from a home office",
        "Run a small restaurant",
        "Open a retail shop",
        "Manage a farm operation",
    ],
    valid_en = [
        "Visit the manufacturing plant",
        "Inspect the factory floor",
        "Manage warehouse operations",
    ],
    test_en = [
        "Work on the production line",
        "Monitor industrial output",
        "Schedule a factory tour",
    ],
)

# ============================================================
# 232. jar
# ============================================================
process_icon(
    "jar",
    st_en = ["jam", "jelly", "storage"],
    pst_en = [
        "Make homemade jam", "Buy strawberry jam at the store",
        "Make grape jelly", "Spread jelly on toast",
        "Use a jar for food storage", "Store leftovers in a jar",
    ],
    reg_en = [
        "Open the jar of jam",
        "Make homemade fruit jam",
        "Buy a jar of peanut butter",
        "Store herbs in a glass jar",
        "Seal a jar for canning",
        "Buy a mason jar set",
        "Make preserves in a jar",
        "Store dry goods in jars",
        "Use a jar to store change",
        "Gift a jar of homemade jam",
    ],
    conv_en = [
        "Open the jar",
        "Jar of jam",
        "Mason jar",
        "Store in a jar",
    ],
    typo_en = [
        "open the jra of jam",
        "make homemad fuit jam",
        "stoer herbs in a glas jar",
        "seall a jar for canning",
    ],
    bnd_en = [
        "Store flour in a jar with wheat",
        "Use a bottle for storing liquids",
        "Put leftovers in a plastic container",
        "Use a can for food storage",
        "Store food in a Tupperware box",
        "Use a ceramic pot for cooking",
    ],
    valid_en = [
        "Open the jar of jam",
        "Make homemade fruit jam",
        "Store herbs in a glass jar",
    ],
    test_en = [
        "Buy a mason jar set",
        "Make preserves in a jar",
        "Gift a jar of homemade jam",
    ],
)

# ============================================================
# 233. jar-wheat
# ============================================================
process_icon(
    "jar-wheat",
    st_en = ["flour", "storage"],
    pst_en = [
        "Buy whole wheat flour", "Store flour in the jar",
        "Organize dry goods storage", "Use the storage jar for grains",
    ],
    reg_en = [
        "Store flour in an airtight jar",
        "Buy a bag of whole wheat flour",
        "Measure flour for baking",
        "Keep flour in a sealed jar",
        "Buy flour for the bread recipe",
        "Store grain and flour in jars",
        "Label the flour storage jar",
        "Use a flour jar for the pantry",
        "Keep the flour jar in the cabinet",
        "Refill the flour storage container",
    ],
    conv_en = [
        "Flour jar",
        "Store the grain",
        "Wheat storage",
        "Fill the flour jar",
    ],
    typo_en = [
        "stoer flour in the jra",
        "by a bag of weat flour",
        "measuer flour for bakign",
        "kep flour in a seled jar",
    ],
    bnd_en = [
        "Store jam in a jar",
        "Keep sugar in a canister",
        "Store coffee beans in a jar",
        "Use a bin for bulk grains",
        "Keep spices in small jars",
        "Store rice in a large container",
    ],
    valid_en = [
        "Store flour in an airtight jar",
        "Buy whole wheat flour",
        "Label the flour storage jar",
    ],
    test_en = [
        "Keep flour in a sealed jar",
        "Measure flour for baking",
        "Refill the flour storage container",
    ],
)

# ============================================================
# 234. joystick
# ============================================================
process_icon(
    "joystick",
    st_en = ["arcade", "atari", "controller", "game", "joystick", "retro", "video game", "vintage"],
    pst_en = [
        "Play at the arcade", "Find an old-school arcade",
        "Collect an Atari console", "Play Atari games",
        "Buy a joystick controller", "Plug in the joystick",
        "Play a game with a joystick", "Win the game with a joystick",
        "Use the joystick for the game", "Learn to use a joystick",
        "Find retro gaming equipment", "Play retro video games",
        "Play a classic video game", "Try a vintage video game",
        "Find vintage gaming gear", "Buy a vintage joystick",
    ],
    reg_en = [
        "Play a retro arcade game",
        "Buy a joystick for the PC",
        "Set up an Atari console",
        "Play classic video games",
        "Visit a retro gaming arcade",
        "Collect vintage game controllers",
        "Use a joystick for flight simulation",
        "Play an old-school game",
        "Set up the joystick for gaming",
        "Stream retro gaming on Twitch",
    ],
    conv_en = [
        "Retro gaming!",
        "Joystick time",
        "Arcade fun",
        "Classic game",
    ],
    typo_en = [
        "play a retro arcad game",
        "buy a joystkc for pc",
        "set up an atari consoel",
        "play clasic video gaems",
    ],
    bnd_en = [
        "Use a modern game controller",
        "Play on a gamepad",
        "Use a keyboard and mouse for gaming",
        "Play a board game instead",
        "Use a touchscreen to play",
        "Play a mobile phone game",
    ],
    valid_en = [
        "Play a retro arcade game",
        "Buy a joystick controller",
        "Set up an Atari console",
    ],
    test_en = [
        "Visit a retro gaming arcade",
        "Use a joystick for flight simulation",
        "Collect vintage game controllers",
    ],
)

# ============================================================
# 235. jug-bottle
# ============================================================
process_icon(
    "jug-bottle",
    st_en = ["collect", "container", "jug", "plastics", "recycle"],
    pst_en = [
        "Collect empty bottles for recycling", "Collect cans and bottles",
        "Reuse the container", "Buy a reusable container",
        "Fill the jug with water", "Buy a large water jug",
        "Recycle plastics at the depot", "Separate plastics for recycling",
        "Recycle the plastic bottles", "Put plastics in the recycling bin",
    ],
    reg_en = [
        "Recycle plastic bottles",
        "Take bottles to the recycling center",
        "Buy a reusable water jug",
        "Fill the jug with drinking water",
        "Separate plastics for recycling",
        "Reduce plastic waste at home",
        "Return empty bottles for deposit",
        "Buy a BPA-free water container",
        "Use a refillable jug instead of bottles",
        "Collect recyclable plastics",
    ],
    conv_en = [
        "Recycle the bottles",
        "Water jug",
        "Plastic recycling",
        "Fill the jug",
    ],
    typo_en = [
        "recycle platsic botles",
        "take bottes to recycilng center",
        "buy a reusabel water jug",
        "sepaarte plastics for recycilng",
    ],
    bnd_en = [
        "Use a detergent jug for laundry",
        "Store jam in a glass jar",
        "Use a metal water bottle",
        "Fill a thermos with hot coffee",
        "Reuse a glass bottle",
        "Put juice in the carafe",
    ],
    valid_en = [
        "Recycle plastic bottles",
        "Buy a reusable water jug",
        "Fill the jug with drinking water",
    ],
    test_en = [
        "Take bottles to the recycling center",
        "Separate plastics for recycling",
        "Return empty bottles for deposit",
    ],
)

# ============================================================
# 236. jug-detergent
# ============================================================
process_icon(
    "jug-detergent",
    st_en = ["detergent", "laundry", "soap", "wash"],
    pst_en = [
        "Buy laundry detergent", "Use the right amount of detergent",
        "Do a load of laundry", "Sort the laundry before washing",
        "Use liquid soap for washing", "Buy dish soap at the store",
        "Wash clothes in the machine", "Wash by hand with soap",
    ],
    reg_en = [
        "Buy laundry detergent at the store",
        "Use the right amount of detergent",
        "Run the laundry with detergent",
        "Buy eco-friendly laundry soap",
        "Refill the detergent dispenser",
        "Use fabric softener with detergent",
        "Spot clean with a little detergent",
        "Check the detergent is safe for colors",
        "Use detergent pods for convenience",
        "Add detergent before the laundry",
    ],
    conv_en = [
        "Get more detergent",
        "Laundry time",
        "Buy soap",
        "Washing day",
    ],
    typo_en = [
        "buy laudnry detergnet",
        "use the rigt amoun of detergnet",
        "run the laudnry",
        "buy eco-firendly soap",
    ],
    bnd_en = [
        "Use dish soap for washing dishes",
        "Buy hand soap for the bathroom",
        "Use shampoo for the hair",
        "Use a water jug for drinking water",
        "Fill the jug with juice",
        "Use fabric softener alone",
    ],
    valid_en = [
        "Buy laundry detergent",
        "Use the right amount of detergent",
        "Run the laundry with detergent",
    ],
    test_en = [
        "Buy eco-friendly laundry soap",
        "Use detergent pods for convenience",
        "Add detergent before the laundry",
    ],
)

# ============================================================
# 237. kazoo
# ============================================================
process_icon(
    "kazoo",
    st_en = ["buzz", "instrument", "music"],
    pst_en = [
        "Make a buzzing sound with the kazoo", "Buzz along to the music",
        "Play a simple instrument", "Buy a cheap instrument for fun",
        "Play music at the party", "Make music with the kids",
    ],
    reg_en = [
        "Play the kazoo at the party",
        "Buy a kazoo for the kids",
        "Learn a simple tune on the kazoo",
        "Make music with a kazoo",
        "Use a kazoo in the sing-along",
        "Bring a kazoo to the parade",
        "Play the kazoo as a joke instrument",
        "Give kazoos as party favors",
        "Hum a melody through the kazoo",
        "Use a kazoo in a fun band",
    ],
    conv_en = [
        "Play the kazoo!",
        "Kazoo time",
        "Fun instrument",
        "Party music",
    ],
    typo_en = [
        "play the kazoo at pary",
        "buy a kazoo fo the kids",
        "lern a tune on kazoo",
        "make musci with a kazoo",
    ],
    bnd_en = [
        "Play the harmonica",
        "Use a recorder for music class",
        "Play the flute",
        "Use a whistle to signal",
        "Blow a party horn",
        "Play the trumpet",
    ],
    valid_en = [
        "Play the kazoo at the party",
        "Buy a kazoo for the kids",
        "Give kazoos as party favors",
    ],
    test_en = [
        "Use a kazoo in the sing-along",
        "Hum a melody through the kazoo",
        "Bring a kazoo to the parade",
    ],
)

# ============================================================
# 238. keyboard
# ============================================================
process_icon(
    "keyboard",
    st_en = ["computer", "edit", "input", "keyboard", "text", "type", "write"],
    pst_en = [
        "Connect to the computer", "Set up the computer workspace",
        "Edit the document", "Edit the code",
        "Set up the input device", "Configure the input settings",
        "Buy a mechanical keyboard", "Clean the keyboard",
        "Type the report", "Type faster",
        "Write a blog post", "Write an email",
    ],
    reg_en = [
        "Buy a new mechanical keyboard",
        "Connect the keyboard to the laptop",
        "Clean the keyboard keys",
        "Type a document in Word",
        "Write an email to the client",
        "Set up a wireless keyboard",
        "Use keyboard shortcuts to work faster",
        "Replace a broken keyboard key",
        "Adjust the keyboard height",
        "Buy a compact keyboard for travel",
    ],
    conv_en = [
        "New keyboard!",
        "Type faster",
        "Keyboard setup",
        "Write it out",
    ],
    typo_en = [
        "buy a new mechancial keybord",
        "conect the keybaord",
        "clena the keyborad keys",
        "tpye the docuemnt",
    ],
    bnd_en = [
        "Use a computer mouse instead",
        "Type on the touchscreen",
        "Use voice input instead of typing",
        "Connect a drawing tablet",
        "Use a trackpad to navigate",
        "Set up a number pad",
    ],
    valid_en = [
        "Buy a mechanical keyboard",
        "Connect the keyboard to the laptop",
        "Type a document in Word",
    ],
    test_en = [
        "Clean the keyboard keys",
        "Set up a wireless keyboard",
        "Write an email to the client",
    ],
)

# ============================================================
# 239. kit-medical
# ============================================================
process_icon(
    "kit-medical",
    st_en = ["emergency", "emt", "health", "medical", "rescue"],
    pst_en = [
        "Use the first aid kit in an emergency", "Check the emergency supplies",
        "Call an EMT for help", "Work as an EMT",
        "Maintain good health habits", "Go to a health checkup",
        "Pack a medical kit for the trip", "Stock the medical cabinet",
        "Call rescue services", "Train for rescue situations",
    ],
    reg_en = [
        "Pack a first aid kit for the trip",
        "Stock the home first aid kit",
        "Use the first aid kit for a cut",
        "Check the expiry date on medical supplies",
        "Call emergency services",
        "Learn basic first aid",
        "Buy bandages and antiseptic",
        "Take a first aid course",
        "Keep a first aid kit in the car",
        "Restock the first aid kit",
    ],
    conv_en = [
        "First aid kit",
        "Medical supplies",
        "Emergency kit",
        "Health kit ready",
    ],
    typo_en = [
        "pak a fisrt aid kit",
        "stokc the home frist aid kit",
        "use fisrt aid kit for a cut",
        "call emeregency servicces",
    ],
    bnd_en = [
        "Go to the hospital emergency room",
        "Visit the doctor for treatment",
        "Take medicine from the pharmacy",
        "Use a defibrillator",
        "Call the ambulance",
        "Use a thermometer to check temperature",
    ],
    valid_en = [
        "Pack a first aid kit for the trip",
        "Stock the home first aid kit",
        "Learn basic first aid",
    ],
    test_en = [
        "Check expiry date on medical supplies",
        "Keep a first aid kit in the car",
        "Take a first aid course",
    ],
)

# ============================================================
# 240. kitchen-set
# ============================================================
process_icon(
    "kitchen-set",
    st_en = ["chef", "cook", "kitchen", "pan", "pot", "skillet"],
    pst_en = [
        "Cook like a professional chef", "Watch a chef demonstrate",
        "Cook a new recipe tonight", "Learn to cook at home",
        "Organize the kitchen drawers", "Clean the kitchen counters",
        "Buy a non-stick pan", "Season the pan before use",
        "Boil water in the pot", "Make soup in the pot",
        "Sear meat in the skillet", "Cook eggs in the skillet",
    ],
    reg_en = [
        "Cook dinner in the kitchen",
        "Buy a new pot and pan set",
        "Season the cast iron skillet",
        "Organize kitchen utensils",
        "Cook a stir-fry in the wok",
        "Boil pasta in a large pot",
        "Fry eggs in the skillet",
        "Replace old pots and pans",
        "Clean the kitchen after cooking",
        "Set up the kitchen for meal prep",
    ],
    conv_en = [
        "Cook dinner!",
        "New pan set",
        "Kitchen time",
        "Meal prep",
    ],
    typo_en = [
        "cook dinnre in the kitchn",
        "buy a new pot and pna set",
        "seasson the casst iron",
        "organizee kicthen utensilss",
    ],
    bnd_en = [
        "Wear a chef hat for the event",
        "Use the microwave to heat food",
        "Use the oven to bake",
        "Set up the dining table",
        "Use a blender for smoothies",
        "Buy kitchen appliances",
    ],
    valid_en = [
        "Cook dinner in the kitchen",
        "Buy a new pot and pan set",
        "Season the cast iron skillet",
    ],
    test_en = [
        "Organize kitchen utensils",
        "Boil pasta in a large pot",
        "Clean the kitchen after cooking",
    ],
)

# ============================================================
# 241. knife
# ============================================================
process_icon(
    "knife",
    st_en = ["cut", "cutlery", "dining", "equipment", "silverware", "tool"],
    pst_en = [
        "Cut the vegetables with the knife", "Cut the steak",
        "Buy a complete cutlery set", "Set the cutlery on the table",
        "Set the table for dining", "Book a dining experience",
        "Buy the right equipment for cooking", "Use sharp equipment",
        "Polish the silverware", "Wash the silverware after dinner",
        "Use a knife as a cooking tool", "Sharpen the knife tool",
    ],
    reg_en = [
        "Sharpen the kitchen knife",
        "Use a chef's knife for chopping",
        "Buy a new knife set",
        "Slice bread with a bread knife",
        "Cut vegetables for the stir-fry",
        "Use a paring knife for peeling",
        "Wash knives by hand",
        "Store knives on a magnetic strip",
        "Use a steak knife at dinner",
        "Learn proper knife technique",
    ],
    conv_en = [
        "Sharpen the knife",
        "Chop it up",
        "New knife set",
        "Slice and dice",
    ],
    typo_en = [
        "sharpne the kitchn knife",
        "use a chefs knofe",
        "buy a new knive set",
        "sliice bread wiht knife",
    ],
    bnd_en = [
        "Set the table with fork and knife together",
        "Use a spoon to stir the soup",
        "Use scissors to cut wrapping paper",
        "Use a peeler instead of a knife",
        "Chop with a cleaver",
        "Use a mandoline slicer",
    ],
    valid_en = [
        "Sharpen the kitchen knife",
        "Use a chef's knife for chopping",
        "Buy a new knife set",
    ],
    test_en = [
        "Slice bread with a bread knife",
        "Wash knives by hand",
        "Learn proper knife technique",
    ],
)

# ============================================================
# 242. laptop
# ============================================================
process_icon(
    "laptop",
    st_en = ["computer", "laptop", "mac", "macbook", "pc"],
    pst_en = [
        "Buy a new computer for work", "Fix the computer issue",
        "Buy a lightweight laptop", "Set up the new laptop",
        "Get a new Mac for the studio", "Set up the Mac at home",
        "Buy a MacBook Pro", "Configure the MacBook settings",
        "Buy a PC laptop", "Use the PC for work",
    ],
    reg_en = [
        "Buy a new laptop for work",
        "Set up the MacBook",
        "Work on the laptop at the cafe",
        "Update the laptop software",
        "Back up the laptop files",
        "Fix the slow laptop",
        "Connect the laptop to the monitor",
        "Charge the laptop battery",
        "Clean the laptop screen",
        "Replace the laptop battery",
    ],
    conv_en = [
        "New laptop!",
        "MacBook setup",
        "Work from laptop",
        "Laptop upgrade",
    ],
    typo_en = [
        "buy a new laotop",
        "set up the macbok",
        "work on lpatop at cafe",
        "updat the laptpo software",
    ],
    bnd_en = [
        "Set up a desktop computer",
        "Use a tablet for work",
        "Work on a smartphone",
        "Use a Chromebook instead",
        "Set up a gaming PC",
        "Use a server for computing",
    ],
    valid_en = [
        "Buy a new laptop for work",
        "Set up the MacBook",
        "Work on the laptop at the cafe",
    ],
    test_en = [
        "Update the laptop software",
        "Connect the laptop to the monitor",
        "Replace the laptop battery",
    ],
)

# ============================================================
# 243. lasso-sparkles
# ============================================================
process_icon(
    "lasso-sparkles",
    st_en = ["automatic", "magic", "select"],
    pst_en = [
        "Use automatic selection in Photoshop", "Apply automatic background removal",
        "Use the magic wand tool", "Apply a magic effect to the design",
        "Select the object automatically", "Use lasso to select the area",
    ],
    reg_en = [
        "Use the magic select tool in Photoshop",
        "Auto-select the background",
        "Use AI to select the object",
        "Apply magic removal to the background",
        "Select all similar colors automatically",
        "Use lasso tool to trace the outline",
        "Use smart select in the design app",
        "Auto-crop the subject from the background",
        "Use AI-powered selection tool",
        "Select and remove background automatically",
    ],
    conv_en = [
        "Magic select",
        "Auto remove background",
        "AI selection",
        "Smart select",
    ],
    typo_en = [
        "use the magci select tool",
        "auto-selcet the backgrond",
        "aply magic removel",
        "use ai to selcet object",
    ],
    bnd_en = [
        "Use the regular lasso tool",
        "Select manually with the pen tool",
        "Crop the image manually",
        "Use the eraser tool",
        "Use the marquee selection tool",
        "Use the magic wand without sparkles",
    ],
    valid_en = [
        "Use magic select in Photoshop",
        "Auto-remove the background",
        "Use AI-powered selection tool",
    ],
    test_en = [
        "Select the object automatically",
        "Apply smart background removal",
        "Use lasso to trace the outline",
    ],
)

# ============================================================
# 244. light-ceiling
# ============================================================
process_icon(
    "light-ceiling",
    st_en = ["bright", "furniture", "light", "overhead"],
    pst_en = [
        "Turn on the bright ceiling light", "Dim the bright lights",
        "Replace the ceiling light fixture", "Buy new furniture for the room",
        "Turn on the light in the room", "Fix the light that won't turn on",
        "Install an overhead light fixture", "Adjust the overhead brightness",
    ],
    reg_en = [
        "Replace the ceiling light bulb",
        "Install a new ceiling light fixture",
        "Dim the lights for dinner",
        "Turn on the overhead light",
        "Buy a LED ceiling light",
        "Fix the flickering ceiling light",
        "Add a dimmer switch for the ceiling light",
        "Paint the room before replacing the light",
        "Set up smart ceiling lights",
        "Choose the right light temperature",
    ],
    conv_en = [
        "Turn on the light",
        "New ceiling light",
        "Fix the light",
        "Dim the lights",
    ],
    typo_en = [
        "replcae the celing light bulb",
        "instlal a new ceeling light",
        "trun on the overhad light",
        "fix the flickerign light",
    ],
    bnd_en = [
        "Turn on a floor lamp",
        "Use a desk lamp for reading",
        "Turn on the night light",
        "Install outdoor lighting",
        "Put up Christmas string lights",
        "Use a flashlight in the dark",
    ],
    valid_en = [
        "Replace the ceiling light bulb",
        "Install a new ceiling light fixture",
        "Turn on the overhead light",
    ],
    test_en = [
        "Dim the lights for dinner",
        "Add a dimmer switch",
        "Set up smart ceiling lights",
    ],
)

# ============================================================
# 245. lightbulb
# ============================================================
process_icon(
    "lightbulb",
    st_en = ["bulb", "electric", "energy", "idea", "innovation", "inspiration", "light"],
    pst_en = [
        "Replace the old light bulb", "Buy LED bulbs for the home",
        "Use an electric light", "Check the electric circuit",
        "Save energy with LED bulbs", "Reduce energy consumption",
        "Get a great idea", "Write down the idea",
        "Start an innovation project", "Work on an innovation challenge",
        "Find inspiration for the project", "Get inspired by a new concept",
        "Turn on the light", "Fix the broken light",
    ],
    reg_en = [
        "Replace the light bulb",
        "Switch to LED for energy savings",
        "Come up with a new idea",
        "Brainstorm ideas for the project",
        "Find inspiration online",
        "Write down a creative idea",
        "Buy smart light bulbs",
        "Fix the lamp that won't turn on",
        "Install a dimmer for the bulb",
        "Get a brainwave for the solution",
    ],
    conv_en = [
        "Great idea!",
        "Light bulb moment",
        "New idea",
        "Change the bulb",
    ],
    typo_en = [
        "replcae the lgiht bulb",
        "swich to led blubs",
        "com up with a new ieda",
        "brainstrom idaes",
    ],
    bnd_en = [
        "Turn on the ceiling light",
        "Use a flashlight instead",
        "Hang string lights for decoration",
        "Set up a neon sign",
        "Turn on the desk lamp",
        "Buy a lava lamp for decoration",
    ],
    valid_en = [
        "Replace the light bulb",
        "Switch to LED for energy savings",
        "Come up with a new idea",
    ],
    test_en = [
        "Brainstorm ideas for the project",
        "Find inspiration online",
        "Install smart light bulbs",
    ],
)

# ============================================================
# 246. lights-holiday
# ============================================================
process_icon(
    "lights-holiday",
    st_en = ["christmas", "decoration", "holiday", "string", "xmas"],
    pst_en = [
        "Hang Christmas lights outside", "Buy LED Christmas lights",
        "Put up holiday decorations", "Take down the holiday decorations",
        "Celebrate the holiday season", "Plan a holiday party",
        "Hang string lights around the tree", "Buy string lights for the patio",
        "Decorate for Xmas", "Xmas light display",
    ],
    reg_en = [
        "Hang Christmas lights on the house",
        "Decorate the tree with string lights",
        "Set up holiday lights in the yard",
        "Buy new Christmas lights",
        "Put up the Christmas decorations",
        "Take down lights after the holidays",
        "Hang string lights on the patio",
        "Use timer for the holiday lights",
        "Replace broken Christmas lights",
        "Add lights to the holiday wreath",
    ],
    conv_en = [
        "Holiday lights!",
        "Xmas decorating",
        "Put up the lights",
        "String lights up",
    ],
    typo_en = [
        "hang chrismas lights outsdie",
        "put up holdiay decoratinos",
        "by new chrsitmas lights",
        "decroate for xmas",
    ],
    bnd_en = [
        "Replace the ceiling light bulb",
        "Set up a regular lamp",
        "Light candles for the dinner",
        "Hang a holiday wreath",
        "Decorate with tinsel",
        "Set up a lighted nativity scene",
    ],
    valid_en = [
        "Hang Christmas lights on the house",
        "Decorate with string lights",
        "Buy new holiday lights",
    ],
    test_en = [
        "Set up holiday lights in the yard",
        "Use a timer for Christmas lights",
        "Take down lights after the holidays",
    ],
)

# ============================================================
# 247. lira-sign
# ============================================================
process_icon(
    "lira-sign",
    st_en = ["Lira Sign", "currency"],
    pst_en = [
        "Pay in lira while in Turkey", "Check the Turkish lira rate",
        "Exchange currency to lira", "Convert lira to euros",
    ],
    reg_en = [
        "Exchange money to Turkish lira",
        "Check the TRY exchange rate",
        "Pay in lira while in Turkey",
        "Convert lira to dollars",
        "Budget the Turkey trip in lira",
        "Find the best lira exchange rate",
        "Withdraw lira from the ATM",
        "Pay the bill in lira",
        "Transfer money in lira",
        "Check lira to euro conversion",
    ],
    conv_en = [
        "Turkey trip budget",
        "Convert to lira",
        "Pay in TRY",
        "Check lira rate",
    ],
    typo_en = [
        "pay in lria in turkey",
        "chekc try exchagne rate",
        "convrt lira to euros",
        "exchagne to turksh lira",
    ],
    bnd_en = [
        "Pay in euros",
        "Exchange to US dollars",
        "Use hryvnia in Ukraine",
        "Pay in British pounds",
        "Exchange for Swiss francs",
        "Use a credit card abroad",
    ],
    valid_en = [
        "Exchange money to lira",
        "Pay in lira in Turkey",
        "Check the TRY exchange rate",
    ],
    test_en = [
        "Convert lira to euros",
        "Withdraw lira from the ATM",
        "Budget the Turkey trip",
    ],
)

# ============================================================
# 248. list-check
# ============================================================
process_icon(
    "list-check",
    st_en = ["checklist", "progress", "project management", "settings", "summary", "to do", "working"],
    pst_en = [
        "Create a project checklist", "Follow the checklist step by step",
        "Track the download progress", "Monitor the progress bar",
        "Use a project management tool", "Plan with project management software",
        "Open the app settings checklist", "Complete the settings checklist",
        "Write a project summary", "Review the completion summary",
        "Make a to-do list", "Check off the to-do items",
        "Stay working on the task", "Keep working through the list",
    ],
    reg_en = [
        "Check off completed tasks",
        "Create a project task list",
        "Track progress on the checklist",
        "Mark items as done on the list",
        "Review the checklist before submitting",
        "Make a shopping checklist",
        "Follow the setup checklist",
        "Keep track of project milestones",
        "Use a checklist for the process",
        "Complete all items on the list",
    ],
    conv_en = [
        "Check it off",
        "Task list",
        "Mark as done",
        "Track progress",
    ],
    typo_en = [
        "chekc off completd tasks",
        "creat a projet task lsit",
        "trakc progres on checkist",
        "mark itmes as doen",
    ],
    bnd_en = [
        "Write a grocery list without checks",
        "Plan using a Gantt chart",
        "Use a calendar for scheduling",
        "Write notes in the journal",
        "Use a kanban board for tasks",
        "Draft a project proposal",
    ],
    valid_en = [
        "Check off completed tasks",
        "Track progress on the checklist",
        "Create a project task list",
    ],
    test_en = [
        "Mark items as done on the list",
        "Follow the setup checklist",
        "Complete all items on the list",
    ],
)

# ============================================================
# 249. litecoin-sign
# ============================================================
process_icon(
    "litecoin-sign",
    st_en = ["currency"],
    pst_en = [
        "Buy Litecoin cryptocurrency", "Check Litecoin price",
    ],
    reg_en = [
        "Buy Litecoin on the exchange",
        "Check the Litecoin price",
        "Transfer Litecoin to the wallet",
        "Invest in Litecoin",
        "Trade Litecoin for Bitcoin",
        "Set up a Litecoin wallet",
        "Sell Litecoin on the exchange",
        "Track Litecoin portfolio",
        "Convert Litecoin to dollars",
        "Learn about Litecoin cryptocurrency",
    ],
    conv_en = [
        "Buy Litecoin",
        "Crypto trade",
        "LTC price check",
        "Litecoin wallet",
    ],
    typo_en = [
        "buy litcoin on exchagne",
        "chekc liteocin price",
        "transefr litecoin to walelt",
        "invets in litecoin",
    ],
    bnd_en = [
        "Buy Bitcoin instead",
        "Trade Ethereum",
        "Use a regular bank currency",
        "Exchange for US dollars",
        "Invest in Dogecoin",
        "Use a stablecoin",
    ],
    valid_en = [
        "Buy Litecoin on the exchange",
        "Check the Litecoin price",
        "Transfer Litecoin to the wallet",
    ],
    test_en = [
        "Invest in Litecoin",
        "Set up a Litecoin wallet",
        "Convert Litecoin to dollars",
    ],
)

print("\nAll 40 icons processed successfully!")
