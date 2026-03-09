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
# 180. floppy-disk
# ============================================================
process_icon(
    "floppy-disk",
    st_en = ["computer", "disk", "download", "floppy", "floppy disk"],
    pst_en = [
        "Save the file on the computer", "Fix the computer storage",
        "Save data to a disk", "Back up data to a disk",
        "Download the file to the device", "Download the update",
        "Find an old floppy drive", "Collect retro floppy disks",
        "Save to a floppy disk", "Transfer files via floppy disk",
    ],
    reg_en = [
        "Save the document before closing",
        "Click save to keep the changes",
        "Back up the project file",
        "Download the installer file",
        "Collect old floppy disks",
        "Find a USB floppy drive reader",
        "Transfer old files from floppy disk",
        "Save work frequently",
        "Download and save the attachment",
        "Preserve old computer files",
    ],
    conv_en = [
        "Save the file",
        "Hit save now",
        "Old floppy disk",
        "Download it",
    ],
    typo_en = [
        "sav the documnet",
        "donwload the flie",
        "backup to a dkis",
        "old floppy diks",
    ],
    bnd_en = [
        "Save to a USB flash drive",
        "Upload to cloud storage",
        "Burn data to a CD",
        "Copy to an external hard drive",
        "Save to an SD card",
        "Upload the file to Google Drive",
    ],
    valid_en = [
        "Save the document",
        "Download the file",
        "Back up to a disk",
    ],
    test_en = [
        "Click save before closing",
        "Transfer files from floppy disk",
        "Download and save the file",
    ],
)

# ============================================================
# 181. fork
# ============================================================
process_icon(
    "fork",
    st_en = ["cutlery", "dining", "food", "fork", "silverware"],
    pst_en = [
        "Set the table with cutlery", "Buy a cutlery set",
        "Book a table for dining", "Enjoy a quiet dining experience",
        "Order food at the restaurant", "Cook food at home",
        "Eat with a fork", "Pick up the fork to eat",
        "Polish the silverware", "Buy sterling silverware",
    ],
    reg_en = [
        "Set the table with a fork",
        "Eat dinner with a fork",
        "Buy a new cutlery set",
        "Set out the silverware for guests",
        "Use a fork for the salad",
        "Wash the forks after dinner",
        "Pack a fork for the lunch box",
        "Find a fork in the kitchen drawer",
        "Use the right fork at the formal dinner",
        "Set the fork on the left side of the plate",
    ],
    conv_en = [
        "Pass the fork",
        "Need a fork",
        "Table setting",
        "Cutlery out",
    ],
    typo_en = [
        "set the tabel with fork",
        "eat dinne with a frork",
        "buy a cutlrery set",
        "wahs the forks",
    ],
    bnd_en = [
        "Set the table with fork and knife together",
        "Use a spoon for the soup",
        "Pick up the chopsticks for sushi",
        "Use a dessert fork for the cake",
        "Eat with a fork and knife at dinner",
        "Use a ladle to serve the stew",
    ],
    valid_en = [
        "Set the table with a fork",
        "Eat dinner with a fork",
        "Buy a new cutlery set",
    ],
    test_en = [
        "Use the fork for the salad",
        "Wash the forks after dinner",
        "Pack a fork for the lunch box",
    ],
)

# ============================================================
# 182. fork-knife
# ============================================================
process_icon(
    "fork-knife",
    st_en = ["cutlery", "dining", "dinner", "eat", "food", "fork", "knife", "restaurant"],
    pst_en = [
        "Buy a complete cutlery set", "Polish the cutlery for the party",
        "Reserve a table for dining", "Enjoy a fine dining experience",
        "Make dinner reservations", "Cook dinner at home",
        "Sit down to eat", "Ready to eat dinner",
        "Order food at the restaurant", "Cook food for the family",
        "Set the fork for the meal", "Pick up the fork and start eating",
        "Sharpen the kitchen knife", "Use a knife to cut the meat",
        "Book a table at the restaurant", "Find a good restaurant nearby",
    ],
    reg_en = [
        "Go out for dinner",
        "Book a restaurant for the anniversary",
        "Set the table with fork and knife",
        "Cook a three-course dinner",
        "Find a restaurant near me",
        "Make a dinner reservation",
        "Try the new restaurant downtown",
        "Eat out tonight",
        "Prepare a home-cooked dinner",
        "Order a meal at the restaurant",
    ],
    conv_en = [
        "Dinner time!",
        "Eat out tonight",
        "Book a restaurant",
        "Table for two",
    ],
    typo_en = [
        "book a restrant for dinner",
        "go out fo dinner",
        "set the tabel for dining",
        "find a resturant nearby",
    ],
    bnd_en = [
        "Set the table with just a fork",
        "Use chopsticks for Asian food",
        "Order takeout instead of dining out",
        "Have a quick lunch at home",
        "Use a spoon and fork for dessert",
        "Eat breakfast with just a spoon",
    ],
    valid_en = [
        "Go out for dinner",
        "Book a restaurant for the evening",
        "Set the table with fork and knife",
    ],
    test_en = [
        "Make a dinner reservation",
        "Try the new restaurant downtown",
        "Cook a three-course dinner",
    ],
)

# ============================================================
# 183. forklift
# ============================================================
process_icon(
    "forklift",
    st_en = ["archive", "inventory", "lorry", "maintenance", "pallet", "shipping", "tractor", "warehouse"],
    pst_en = [
        "Archive old stock in the warehouse", "Move archived items",
        "Do a full inventory count", "Update the inventory system",
        "Drive the lorry to the warehouse", "Load the lorry for delivery",
        "Schedule forklift maintenance", "Check forklift maintenance log",
        "Load a pallet with boxes", "Move the pallet to the dock",
        "Arrange shipping from the warehouse", "Track the shipping pallet",
        "Use the tractor to move goods", "Drive the warehouse tractor",
        "Organize the warehouse floor", "Manage warehouse operations",
    ],
    reg_en = [
        "Operate the forklift in the warehouse",
        "Load pallets with the forklift",
        "Move heavy goods with the forklift",
        "Get forklift certification",
        "Drive the forklift safely",
        "Stack pallets in the warehouse",
        "Unload the delivery truck with the forklift",
        "Inspect the forklift before use",
        "Use the forklift to stock shelves",
        "Check forklift safety procedures",
    ],
    conv_en = [
        "Forklift time",
        "Move that pallet",
        "Warehouse work",
        "Load the goods",
    ],
    typo_en = [
        "oprate the forklfit",
        "load pallets in warehuose",
        "moov heavy goods",
        "get foklift certfication",
    ],
    bnd_en = [
        "Move boxes with a hand dolly",
        "Use a conveyor belt to move goods",
        "Push a pallet jack manually",
        "Drive a delivery truck",
        "Use a hand truck to carry boxes",
        "Operate a crane at the construction site",
    ],
    valid_en = [
        "Operate the forklift in the warehouse",
        "Load pallets with the forklift",
        "Get forklift certification",
    ],
    test_en = [
        "Move heavy goods with the forklift",
        "Stack pallets in the warehouse",
        "Inspect the forklift before use",
    ],
)

# ============================================================
# 184. frame
# ============================================================
process_icon(
    "frame",
    st_en = ["artboard", "crop", "grid", "group", "viewbox"],
    pst_en = [
        "Set up the artboard in the design tool", "Resize the artboard",
        "Crop the image to the frame", "Crop the design to size",
        "Use a grid for layout alignment", "Set up a grid in Figma",
        "Group the elements together", "Group layers in the design",
        "Set the viewbox dimensions", "Adjust the SVG viewbox",
    ],
    reg_en = [
        "Create a new artboard in the design tool",
        "Frame the content for the layout",
        "Set up the design canvas",
        "Arrange elements within the frame",
        "Group UI components together",
        "Use a frame for the app screen layout",
        "Set up a frame for the presentation slide",
        "Resize the design frame",
        "Nest frames in the design file",
        "Export the frame as an image",
    ],
    conv_en = [
        "New frame",
        "Design frame",
        "Set the canvas",
        "Artboard ready",
    ],
    typo_en = [
        "set up the artboadr",
        "creat a new desgin frame",
        "grup the elements",
        "adjsut the viewbx",
    ],
    bnd_en = [
        "Crop the photo",
        "Add a photo frame on the wall",
        "Use a border on the document",
        "Draw a rectangle in the design",
        "Set the page margins",
        "Use a grid for the spreadsheet",
    ],
    valid_en = [
        "Set up the artboard in the design tool",
        "Create a new design frame",
        "Group elements in the frame",
    ],
    test_en = [
        "Resize the design frame",
        "Export the frame as an image",
        "Set up a frame for the app screen",
    ],
)

# ============================================================
# 185. french-fries
# ============================================================
process_icon(
    "french-fries",
    st_en = ["chips", "fast food", "french fries", "fried", "fries", "ketchup", "potato", "poutine"],
    pst_en = [
        "Order chips with the burger", "Eat chips as a snack",
        "Stop at a fast food place", "Order fast food for the family",
        "Order a large french fries", "Make french fries at home",
        "Deep fry potatoes for fries", "Bake fried potatoes in the oven",
        "Make crispy fries", "Get a side of fries",
        "Dip the fries in ketchup", "Buy ketchup for the fries",
        "Make mashed potato for dinner", "Buy potatoes at the store",
        "Try Canadian poutine", "Order poutine with gravy",
    ],
    reg_en = [
        "Order fries with the burger",
        "Make homemade french fries",
        "Stop at McDonald's for fries",
        "Bake oven fries instead of frying",
        "Get a side of fries with lunch",
        "Dip fries in ketchup or mayo",
        "Make sweet potato fries",
        "Order poutine in Canada",
        "Cook frozen fries in the oven",
        "Get curly fries at the restaurant",
    ],
    conv_en = [
        "Fries please!",
        "Side of fries",
        "Fast food run",
        "Fries and ketchup",
    ],
    typo_en = [
        "order freis with burger",
        "make homemade frnech fries",
        "bake oven freis",
        "diip fries in kechup",
    ],
    bnd_en = [
        "Order onion rings instead",
        "Get a side salad with the meal",
        "Make potato wedges in the oven",
        "Cook mashed potatoes for dinner",
        "Get a baked potato at the steakhouse",
        "Order potato chips from the bag",
    ],
    valid_en = [
        "Order fries with the burger",
        "Make homemade french fries",
        "Dip fries in ketchup",
    ],
    test_en = [
        "Stop at fast food for fries",
        "Bake oven fries",
        "Get a side of fries with lunch",
    ],
)

# ============================================================
# 186. frog
# ============================================================
process_icon(
    "frog",
    st_en = ["amphibian", "bullfrog", "fauna", "hop", "ribbit", "toad"],
    pst_en = [
        "Learn about amphibians", "See amphibians at the nature center",
        "Hear a bullfrog at the pond", "Spot a bullfrog in the wetlands",
        "Observe local fauna", "Find fauna near the pond",
        "Watch the frog hop", "Hop like a frog for fun",
        "Hear frogs ribbit at night", "Imitate a frog ribbit",
        "Spot a toad in the garden", "Move a toad out of the path",
    ],
    reg_en = [
        "See frogs at the pond",
        "Listen to frogs ribbit at night",
        "Find a frog in the garden",
        "Watch a frog jump into the water",
        "Take the kids to see frogs",
        "Photograph a frog in the wild",
        "Observe frogs at the nature park",
        "Spot a tree frog",
        "Keep a pet frog",
        "Learn about frog life cycles",
    ],
    conv_en = [
        "Ribbit ribbit",
        "Found a frog!",
        "Frog in the garden",
        "Pond frog",
    ],
    typo_en = [
        "see frosg at the pnod",
        "litsne to frogs ribbit",
        "find a frgo in garden",
        "wach frog jump",
    ],
    bnd_en = [
        "See a salamander in the creek",
        "Spot a lizard in the yard",
        "Watch a turtle sunbathe",
        "Find a snake in the grass",
        "See a newt near the pond",
        "Watch a chameleon change color",
    ],
    valid_en = [
        "See frogs at the pond",
        "Listen to frogs ribbit at night",
        "Spot a frog in the garden",
    ],
    test_en = [
        "Watch a frog jump into the water",
        "Photograph a frog in the wild",
        "Take kids to see frogs",
    ],
)

# ============================================================
# 187. futbol
# ============================================================
process_icon(
    "futbol",
    st_en = ["ball", "football", "soccer", "soccer ball"],
    pst_en = [
        "Kick the ball in practice", "Buy a new ball for the game",
        "Watch the football match", "Play football with friends",
        "Join a soccer league", "Coach a soccer team",
        "Buy a new soccer ball", "Pump up the soccer ball",
    ],
    reg_en = [
        "Play soccer at the park",
        "Watch the World Cup match",
        "Sign the kids up for soccer",
        "Buy soccer cleats",
        "Practice penalty kicks",
        "Join a local soccer league",
        "Watch the Champions League game",
        "Take the kids to soccer practice",
        "Play a pickup soccer game",
        "Buy a soccer jersey",
    ],
    conv_en = [
        "Soccer night!",
        "Kick the ball",
        "World Cup time",
        "Soccer practice",
    ],
    typo_en = [
        "play soccre at the park",
        "wathc the footbal match",
        "jion soccer leauge",
        "buy soccre cleats",
    ],
    bnd_en = [
        "Throw the American football",
        "Shoot a basketball hoop",
        "Hit a baseball pitch",
        "Serve a tennis ball",
        "Score a goal in hockey",
        "Play volleyball on the beach",
    ],
    valid_en = [
        "Play soccer at the park",
        "Watch the soccer match",
        "Sign up for a soccer league",
    ],
    test_en = [
        "Buy soccer cleats",
        "Take kids to soccer practice",
        "Watch the Champions League game",
    ],
)

# ============================================================
# 188. game-board
# ============================================================
process_icon(
    "game-board",
    st_en = ["checkers", "chess", "gaming", "grid", "tabletop"],
    pst_en = [
        "Play checkers with a friend", "Set up the checkers board",
        "Play chess online", "Learn chess openings",
        "Try a new gaming experience", "Gaming session tonight",
        "Draw a grid for the game", "Set up the grid on the board",
        "Play a tabletop game", "Organize a tabletop gaming night",
    ],
    reg_en = [
        "Play a board game with the family",
        "Host a game night",
        "Set up the chess board",
        "Play checkers with the kids",
        "Try a new tabletop game",
        "Buy a new board game",
        "Play Scrabble on game night",
        "Organize a board game tournament",
        "Play a strategy board game",
        "Invite friends for a tabletop session",
    ],
    conv_en = [
        "Game night!",
        "Chess time",
        "Board game fun",
        "Set up the board",
    ],
    typo_en = [
        "play chekers with frined",
        "set up the chsess board",
        "tabletpo gaming night",
        "buy a new bord game",
    ],
    bnd_en = [
        "Play a video game on the console",
        "Roll the dice for a dice game",
        "Play cards for poker night",
        "Play a word game on the phone",
        "Use a gamepad for the video game",
        "Play an arcade game",
    ],
    valid_en = [
        "Set up the chess board",
        "Host a board game night",
        "Play checkers with the kids",
    ],
    test_en = [
        "Try a new tabletop game",
        "Organize a board game tournament",
        "Play a strategy game",
    ],
)

# ============================================================
# 189. gamepad
# ============================================================
process_icon(
    "gamepad",
    st_en = ["arcade", "controller", "d-pad", "joystick", "video", "video game"],
    pst_en = [
        "Visit the arcade", "Play at the arcade with coins",
        "Buy a new game controller", "Pair the controller to the console",
        "Use the d-pad for movement", "Press the d-pad to navigate",
        "Use the joystick to aim", "Calibrate the joystick",
        "Stream video game footage", "Record a video game session",
        "Play the video game all night", "Buy a new video game",
    ],
    reg_en = [
        "Play video games after work",
        "Buy a new game controller",
        "Set up the gaming console",
        "Play multiplayer with friends online",
        "Download a new video game",
        "Charge the controller battery",
        "Stream gameplay on Twitch",
        "Beat the final boss in the game",
        "Try the new game release",
        "Play a co-op game with family",
    ],
    conv_en = [
        "Game on!",
        "Play a video game",
        "Controller charged",
        "Gaming session",
    ],
    typo_en = [
        "play viedo games",
        "buy a new controler",
        "set up the gamign console",
        "dowload a new gaem",
    ],
    bnd_en = [
        "Play a board game instead",
        "Use the keyboard for PC gaming",
        "Play a card game with friends",
        "Use the mouse for a PC game",
        "Play a mobile game on the phone",
        "Use a joystick for flight simulation",
    ],
    valid_en = [
        "Play video games after work",
        "Buy a new game controller",
        "Set up the gaming console",
    ],
    test_en = [
        "Download a new video game",
        "Play multiplayer with friends",
        "Beat the final boss",
    ],
)

# ============================================================
# 190. garage
# ============================================================
process_icon(
    "garage",
    st_en = ["auto", "car", "door", "storage", "structure", "warehouse"],
    pst_en = [
        "Fix the auto in the garage", "Park the auto in the garage",
        "Park the car in the garage", "Take the car out of the garage",
        "Open the garage door", "Replace the garage door opener",
        "Organize garage storage", "Use the garage for extra storage",
        "Build a garage structure", "Reinforce the garage structure",
        "Convert the garage into a workshop", "Use the garage as a warehouse",
    ],
    reg_en = [
        "Clean out the garage",
        "Park the car in the garage",
        "Organize the garage shelves",
        "Fix the garage door opener",
        "Set up a workshop in the garage",
        "Store seasonal items in the garage",
        "Epoxy coat the garage floor",
        "Install shelving in the garage",
        "Park both cars in the garage",
        "Use the garage for the home gym",
    ],
    conv_en = [
        "Clean the garage",
        "Park in the garage",
        "Garage door broke",
        "Garage workshop",
    ],
    typo_en = [
        "clen out the gaarge",
        "park the cra in garage",
        "fix the garaged oor",
        "ogranize the gaargae",
    ],
    bnd_en = [
        "Park the car in the driveway",
        "Store items in a storage unit",
        "Fix the car at the auto shop",
        "Park in the underground parking",
        "Use a carport instead of a garage",
        "Organize the basement storage",
    ],
    valid_en = [
        "Park the car in the garage",
        "Clean out the garage",
        "Fix the garage door opener",
    ],
    test_en = [
        "Organize the garage shelves",
        "Set up a workshop in the garage",
        "Store seasonal items in the garage",
    ],
)

# ============================================================
# 191. gauge
# ============================================================
process_icon(
    "gauge",
    st_en = ["dashboard", "fast", "odometer", "speed", "speedometer"],
    pst_en = [
        "Check the car dashboard", "Review the analytics dashboard",
        "Drive fast on the highway", "Keep driving fast to make it on time",
        "Read the odometer before selling", "Check the odometer reading",
        "Watch the speed on the speedometer", "Drive at the right speed",
        "Check the speedometer in the car", "Monitor the speedometer",
    ],
    reg_en = [
        "Check the car speed",
        "Monitor the speedometer while driving",
        "Check tire pressure on the dashboard",
        "Read the fuel gauge",
        "Watch the engine temperature gauge",
        "Review the website speed metrics",
        "Check the app performance dashboard",
        "Monitor CPU usage on the dashboard",
        "Keep track of speed on the highway",
        "Calibrate the speedometer",
    ],
    conv_en = [
        "Check the speed",
        "Dashboard check",
        "Too fast!",
        "Speed limit",
    ],
    typo_en = [
        "chekc the spedometer",
        "read the dashboadr",
        "moniotr the speed",
        "check odmoeter reading",
    ],
    bnd_en = [
        "Check the fuel level indicator",
        "Read the thermometer temperature",
        "Monitor the battery charge level",
        "Use a ruler to measure distance",
        "Check the compass direction",
        "Read the pressure gauge on the tire",
    ],
    valid_en = [
        "Check the speedometer while driving",
        "Monitor the dashboard",
        "Read the odometer",
    ],
    test_en = [
        "Review the performance dashboard",
        "Check the car gauges",
        "Monitor speed on the highway",
    ],
)

# ============================================================
# 192. gear
# ============================================================
process_icon(
    "gear",
    st_en = ["configuration", "gear", "mechanical", "modify", "settings", "tool"],
    pst_en = [
        "Open the app configuration", "Update the system configuration",
        "Switch to a lower gear on the bike", "Check the gear in the car",
        "Fix the mechanical issue", "Inspect the mechanical parts",
        "Modify the app behavior", "Modify the settings",
        "Open the settings menu", "Change the app settings",
        "Use the right tool for the job", "Pack the tools for the repair",
    ],
    reg_en = [
        "Open the app settings",
        "Configure the system preferences",
        "Adjust the settings for the device",
        "Change the notification settings",
        "Update app settings",
        "Fix the mechanical problem",
        "Set up preferences in the app",
        "Tweak the configuration file",
        "Manage the app permissions",
        "Customize the display settings",
    ],
    conv_en = [
        "Open settings",
        "Change the config",
        "Tweak the settings",
        "Settings menu",
    ],
    typo_en = [
        "oen the app settnigs",
        "conifgure the systme",
        "adjsut the sttings",
        "fix the mechancial issue",
    ],
    bnd_en = [
        "Use a wrench to tighten the bolt",
        "Open the control panel",
        "Use a hammer to fix the problem",
        "Adjust the dial on the device",
        "Change the app theme",
        "Use a screwdriver for the repair",
    ],
    valid_en = [
        "Open the app settings",
        "Configure the system preferences",
        "Adjust the notification settings",
    ],
    test_en = [
        "Change the display settings",
        "Update app configuration",
        "Fix the mechanical problem",
    ],
)

# ============================================================
# 193. gif
# ============================================================
process_icon(
    "gif",
    st_en = ["animation", "img"],
    pst_en = [
        "Add an animation to the message", "Create a looping animation",
        "Insert an img tag in the HTML", "Add the img to the page",
    ],
    reg_en = [
        "Send a funny GIF in the chat",
        "Find a GIF to express a reaction",
        "Create an animated GIF",
        "Add a GIF to the presentation",
        "Search for a GIF on Giphy",
        "Make a GIF from a video clip",
        "Add a GIF sticker to the message",
        "Use a GIF as a profile banner",
        "Save a GIF from the internet",
        "Compress a GIF to reduce size",
    ],
    conv_en = [
        "Send a GIF",
        "Funny GIF",
        "GIF reaction",
        "Animated image",
    ],
    typo_en = [
        "sned a funy GIF",
        "find a GIf to react",
        "cretae an animated gfi",
        "seacrh for a gif on giphy",
    ],
    bnd_en = [
        "Send a static image",
        "Share a meme photo",
        "Send a short video clip",
        "Add a PNG image to the document",
        "Attach a JPEG photo to the email",
        "Use an emoji instead of a GIF",
    ],
    valid_en = [
        "Send a GIF in the chat",
        "Create an animated GIF",
        "Search for a reaction GIF",
    ],
    test_en = [
        "Find a funny GIF",
        "Make a GIF from a video",
        "Add a GIF to the presentation",
    ],
)

# ============================================================
# 194. gingerbread-man
# ============================================================
process_icon(
    "gingerbread-man",
    st_en = ["cookie", "decoration", "frosting", "holiday"],
    pst_en = [
        "Bake gingerbread cookies", "Decorate gingerbread man cookies",
        "Put up holiday decorations", "Buy Christmas decorations",
        "Add frosting to the gingerbread", "Pipe frosting on the cookie",
        "Celebrate the holiday season", "Plan holiday activities",
    ],
    reg_en = [
        "Bake gingerbread men for Christmas",
        "Decorate gingerbread cookies with frosting",
        "Make a gingerbread house",
        "Give gingerbread cookies as gifts",
        "Bake holiday cookies with the kids",
        "Use cookie cutters for the gingerbread",
        "Make gingerbread men for the school party",
        "Decorate gingerbread with icing",
        "Bake cookies for the holiday swap",
        "Pack gingerbread cookies in a tin",
    ],
    conv_en = [
        "Bake gingerbread!",
        "Holiday baking",
        "Gingerbread time",
        "Christmas cookies",
    ],
    typo_en = [
        "bake gingerberd men",
        "decorate gingerbeard cookies",
        "make a gingerbread hous",
        "holdiay bakign",
    ],
    bnd_en = [
        "Bake regular sugar cookies",
        "Decorate a Christmas cake",
        "Make a holiday pie",
        "Bake chocolate chip cookies",
        "Make a snowman out of felt",
        "Hang Christmas ornaments on the tree",
    ],
    valid_en = [
        "Bake gingerbread men for Christmas",
        "Decorate gingerbread with frosting",
        "Make a gingerbread house",
    ],
    test_en = [
        "Give gingerbread cookies as gifts",
        "Bake holiday cookies with the kids",
        "Pack gingerbread cookies in a tin",
    ],
)

# ============================================================
# 195. glasses
# ============================================================
process_icon(
    "glasses",
    st_en = ["nerd", "reading", "sight", "spectacles", "vision"],
    pst_en = [
        "Wear glasses like a nerd", "Embrace the nerd look",
        "Put on reading glasses", "Buy reading glasses at the pharmacy",
        "Get an eye test for sight", "Check the sight prescription",
        "Clean the spectacles", "Buy a case for the spectacles",
        "Get a vision test", "Improve vision with glasses",
    ],
    reg_en = [
        "Book an eye exam",
        "Pick up new glasses from the optician",
        "Buy reading glasses",
        "Clean the glasses lenses",
        "Get a new prescription",
        "Order glasses online",
        "Replace the broken glasses frame",
        "Adjust the glasses at the optician",
        "Try contact lenses instead of glasses",
        "Keep glasses in the case",
    ],
    conv_en = [
        "Need new glasses",
        "Eye test time",
        "Glasses update",
        "Clean the specs",
    ],
    typo_en = [
        "boko an eye exam",
        "pik up new glasess",
        "buy readign glasses",
        "clen the glasess lenses",
    ],
    bnd_en = [
        "Wear sunglasses outside",
        "Buy contact lenses",
        "Get laser eye surgery",
        "Wear safety goggles at work",
        "Use a magnifying glass to read",
        "Put on swimming goggles",
    ],
    valid_en = [
        "Book an eye exam",
        "Pick up new glasses",
        "Get a new prescription",
    ],
    test_en = [
        "Buy reading glasses",
        "Clean the glasses lenses",
        "Order glasses online",
    ],
)

# ============================================================
# 196. globe-pointer
# ============================================================
process_icon(
    "globe-pointer",
    st_en = ["globe", "internet", "link", "net", "search", "website", "www"],
    pst_en = [
        "See the globe in the geography class", "Spin the globe",
        "Connect to the internet", "Check the internet connection",
        "Copy the link to share", "Click the link in the email",
        "Browse the net for information", "Search on the net",
        "Search for the answer online", "Use a search engine",
        "Visit the company website", "Build a new website",
        "Type the www address in the browser", "Open the www link",
    ],
    reg_en = [
        "Search for information online",
        "Visit a website",
        "Share a link with the team",
        "Check the website for updates",
        "Browse the internet for ideas",
        "Open the web browser",
        "Search for a restaurant online",
        "Visit the online store",
        "Copy the web link",
        "Bookmark the website",
    ],
    conv_en = [
        "Google it",
        "Check the website",
        "Send the link",
        "Browse the web",
    ],
    typo_en = [
        "seach for it online",
        "viist the websit",
        "sned the lnik",
        "brwose the internet",
    ],
    bnd_en = [
        "Use a VPN to browse safely",
        "Check the map for directions",
        "Open the app instead of the website",
        "Navigate using GPS",
        "Open the browser settings",
        "Use offline maps for travel",
    ],
    valid_en = [
        "Search for information online",
        "Visit the company website",
        "Share a link with the team",
    ],
    test_en = [
        "Browse the internet for ideas",
        "Bookmark the website",
        "Copy the web link",
    ],
)

# ============================================================
# 197. goal-net
# ============================================================
process_icon(
    "goal-net",
    st_en = ["goal", "goal net", "hockey", "lacrosse", "net", "penalty", "soccer"],
    pst_en = [
        "Score a goal in the match", "Celebrate the goal",
        "Shoot the puck into the goal net", "Hit the goal net",
        "Watch an NHL hockey game", "Play hockey on the ice",
        "Play lacrosse this weekend", "Join a lacrosse team",
        "Set up the net for practice", "Replace the torn net",
        "Take a penalty kick", "Save the penalty shot",
        "Play soccer in the park", "Practice soccer drills",
    ],
    reg_en = [
        "Score a goal in the soccer match",
        "Watch the hockey game tonight",
        "Practice penalty kicks",
        "Set up the goal net for practice",
        "Buy a goal net for the backyard",
        "Watch the goalie block the shot",
        "Play a soccer match with friends",
        "Sign up for a hockey league",
        "Try lacrosse for the first time",
        "Practice shooting on goal",
    ],
    conv_en = [
        "GOAL!",
        "Score a goal",
        "Hockey night",
        "Penalty kick",
    ],
    typo_en = [
        "scroe a goal in soccre",
        "wacth the hokcy game",
        "practce penalty kicks",
        "set up the goaal net",
    ],
    bnd_en = [
        "Throw the ball in the basketball hoop",
        "Hit the target in archery",
        "Score a touchdown in American football",
        "Hit a home run in baseball",
        "Serve an ace in tennis",
        "Bowl a strike in bowling",
    ],
    valid_en = [
        "Score a goal in the match",
        "Practice penalty kicks",
        "Watch the hockey game tonight",
    ],
    test_en = [
        "Set up the goal net for practice",
        "Play a soccer match with friends",
        "Try lacrosse for the first time",
    ],
)

# ============================================================
# 198. golf-club
# ============================================================
process_icon(
    "golf-club",
    st_en = ["caddy", "eagle", "putt", "tee"],
    pst_en = [
        "Hire a caddy for the round", "Ask the caddy for advice",
        "Score an eagle on hole 5", "Aim for an eagle",
        "Sink the putt on the green", "Practice putting",
        "Place the ball on the tee", "Hit off the tee",
    ],
    reg_en = [
        "Play a round of golf",
        "Book a tee time at the course",
        "Practice at the driving range",
        "Buy new golf clubs",
        "Take a golf lesson",
        "Play golf with colleagues",
        "Watch the PGA tournament",
        "Improve the golf swing",
        "Play mini golf with the kids",
        "Check the golf course weather",
    ],
    conv_en = [
        "Golf day!",
        "Tee off time",
        "Golf round",
        "Hit the links",
    ],
    typo_en = [
        "play a rounf of golf",
        "book a tee tiem",
        "practce at the drivng range",
        "buy new gollf clubs",
    ],
    bnd_en = [
        "Hit a tennis ball on the court",
        "Swing the baseball bat",
        "Play croquet in the garden",
        "Hit a hockey puck",
        "Play badminton in the park",
        "Putt in mini golf",
    ],
    valid_en = [
        "Play a round of golf",
        "Book a tee time",
        "Practice at the driving range",
    ],
    test_en = [
        "Buy new golf clubs",
        "Take a golf lesson",
        "Watch the PGA tournament",
    ],
)

# ============================================================
# 199. grill
# ============================================================
process_icon(
    "grill",
    st_en = ["barbecue", "bbq", "burger", "charcoal", "cook", "cookout", "hot", "smoke"],
    pst_en = [
        "Host a backyard barbecue", "Buy a new barbecue grill",
        "Organize a summer BBQ party", "Invite friends to the BBQ",
        "Grill burgers for the cookout", "Make smash burgers on the grill",
        "Light the charcoal grill", "Use charcoal for the BBQ",
        "Cook steaks on the grill", "Cook chicken on the grill",
        "Plan a cookout for the weekend", "Get supplies for the cookout",
        "Stay safe around the hot grill", "Don't touch the hot grill",
        "Add wood chips for smoke flavor", "Smoke ribs on the grill",
    ],
    reg_en = [
        "Host a BBQ party",
        "Grill burgers for the family",
        "Light the charcoal grill",
        "Marinate the meat before grilling",
        "Buy propane for the grill",
        "Clean the grill grates",
        "Grill vegetables as a side",
        "Cook ribs on the smoker grill",
        "Invite neighbors to the cookout",
        "Grill corn on the cob",
    ],
    conv_en = [
        "BBQ time!",
        "Fire up the grill",
        "Cookout today",
        "Grill master",
    ],
    typo_en = [
        "host a backyard barbeque",
        "gril burgers for famiy",
        "lgiht the charcaol grill",
        "clena the grill graets",
    ],
    bnd_en = [
        "Bake a chicken in the oven",
        "Cook burgers in the pan",
        "Use a slow cooker for the ribs",
        "Fry food on the stovetop",
        "Roast vegetables in the oven",
        "Use an air fryer for chicken",
    ],
    valid_en = [
        "Host a BBQ party",
        "Grill burgers for the family",
        "Light the charcoal grill",
    ],
    test_en = [
        "Marinate the meat before grilling",
        "Clean the grill grates",
        "Cook ribs on the smoker",
    ],
)

# ============================================================
# 200. guitar-electric
# ============================================================
process_icon(
    "guitar-electric",
    st_en = ["guitar", "instrument", "music", "rock", "rock and roll", "song", "strings"],
    pst_en = [
        "Play the guitar solo", "Learn to play guitar",
        "Tune the instrument", "Buy a new instrument",
        "Listen to live music", "Play music at the event",
        "Play rock music all night", "Go to a rock concert",
        "Play rock and roll classics", "Cover a rock and roll song",
        "Write a new song on the guitar", "Record a song in the studio",
        "Restring the guitar strings", "Buy new guitar strings",
    ],
    reg_en = [
        "Practice guitar every day",
        "Take guitar lessons",
        "Learn a new guitar song",
        "Play guitar at the open mic night",
        "Record a guitar cover",
        "Buy a new electric guitar",
        "Set up guitar amp and pedals",
        "Join a band",
        "Play guitar at the campfire",
        "Watch a guitar tutorial online",
    ],
    conv_en = [
        "Guitar practice!",
        "Rock out",
        "Play a riff",
        "Jam session",
    ],
    typo_en = [
        "practce guitar everydya",
        "take guittar lessosn",
        "lern a new guitr song",
        "reocrd a guitar covre",
    ],
    bnd_en = [
        "Play the acoustic guitar",
        "Learn to play the piano",
        "Practice drums in the garage",
        "Play bass guitar in the band",
        "Strum the ukulele",
        "Play violin in the orchestra",
    ],
    valid_en = [
        "Practice guitar every day",
        "Take guitar lessons",
        "Play guitar at the open mic",
    ],
    test_en = [
        "Buy a new electric guitar",
        "Record a guitar cover",
        "Join a band",
    ],
)

# ============================================================
# 201. gun
# ============================================================
process_icon(
    "gun",
    st_en = ["firearm", "pistol", "weapon"],
    pst_en = [
        "Clean the firearm safely", "Store the firearm securely",
        "Practice with the pistol at the range", "Buy a holster for the pistol",
        "Handle the weapon responsibly", "Lock up the weapon at home",
    ],
    reg_en = [
        "Go to the shooting range",
        "Clean the gun after use",
        "Store the gun safely at home",
        "Take a gun safety course",
        "Renew the firearms license",
        "Buy ammunition at the store",
        "Lock the gun in the safe",
        "Practice target shooting",
        "Join a shooting sports club",
        "Inspect the pistol before use",
    ],
    conv_en = [
        "Shooting range trip",
        "Gun safety",
        "Target practice",
        "Clean the pistol",
    ],
    typo_en = [
        "go to the shootign range",
        "clen the gun after use",
        "strore the gun safly",
        "take a gun safty course",
    ],
    bnd_en = [
        "Use a bow and arrow for archery",
        "Play a laser tag game",
        "Use a slingshot for target practice",
        "Shoot with a paintball gun",
        "Play a shooting video game",
        "Use a crossbow for sport",
    ],
    valid_en = [
        "Go to the shooting range",
        "Store the gun safely",
        "Take a gun safety course",
    ],
    test_en = [
        "Clean the gun after use",
        "Practice target shooting",
        "Renew the firearms license",
    ],
)

# ============================================================
# 202. hammer
# ============================================================
process_icon(
    "hammer",
    st_en = ["equipment", "fix", "hammer", "maintenance", "repair", "settings", "tool"],
    pst_en = [
        "Use the right equipment for the job", "Buy equipment for the renovation",
        "Fix the broken shelf", "Fix the loose cabinet hinge",
        "Hang a picture with a hammer", "Use the hammer to nail",
        "Schedule home maintenance", "Do regular maintenance on the house",
        "Repair the fence", "Repair the broken step",
        "Open the settings to adjust", "Update settings for the repair tool",
        "Use the right tool for the job", "Buy a new set of tools",
    ],
    reg_en = [
        "Hang a picture on the wall",
        "Fix the broken fence",
        "Nail the boards together",
        "Use a hammer for the home repair",
        "Build a shelf for the garage",
        "Repair the loose floorboard",
        "Renovate the bathroom",
        "Hang shelves in the bedroom",
        "Build a birdhouse",
        "Fix the squeaky stair",
    ],
    conv_en = [
        "Nail it!",
        "Fix it up",
        "Home repair",
        "Hammer time",
    ],
    typo_en = [
        "hang a picturre on the wal",
        "fix the brokne fence",
        "use a hamemr for repair",
        "buid a shleving unit",
    ],
    bnd_en = [
        "Use a screwdriver to fix the screw",
        "Apply paint with a brush",
        "Use a wrench to tighten the bolt",
        "Saw the wood to size",
        "Use a drill for the hole",
        "Fix with a staple gun",
    ],
    valid_en = [
        "Hang a picture with a hammer",
        "Fix the broken fence",
        "Build a shelf for the garage",
    ],
    test_en = [
        "Use a hammer for the home repair",
        "Nail the boards together",
        "Repair the loose floorboard",
    ],
)

# ============================================================
# 203. hammer-brush
# ============================================================
process_icon(
    "hammer-brush",
    st_en = ["art", "fix", "hammer", "maintenance", "paint", "remodel", "repair", "tool"],
    pst_en = [
        "Use art tools for the project", "Create art with tools",
        "Fix and paint the wall", "Fix the surface before painting",
        "Use a hammer to prep the surface", "Hammer down loose nails before painting",
        "Do regular maintenance on the home", "Schedule home maintenance",
        "Paint the living room walls", "Apply a fresh coat of paint",
        "Remodel the kitchen", "Plan the bathroom remodel",
        "Repair and repaint the fence", "Repair the damaged wall",
        "Pick the right tool for painting", "Buy the right tools for the project",
    ],
    reg_en = [
        "Renovate the living room",
        "Paint the walls and fix the trim",
        "Repair and paint the fence",
        "Do a home improvement project",
        "Buy paint and tools for the renovation",
        "Prep the wall before painting",
        "Touch up the paint in the hallway",
        "Fix cracks and repaint the wall",
        "Hire a handyman for repairs",
        "Remodel the bathroom",
    ],
    conv_en = [
        "Home reno",
        "Fix and paint",
        "DIY project",
        "Handyman time",
    ],
    typo_en = [
        "renovte the livign room",
        "paint the wallls",
        "fix and repiant the fence",
        "home imporvement project",
    ],
    bnd_en = [
        "Use only a hammer for nailing",
        "Use only a paintbrush for art",
        "Hire a plumber for pipe repair",
        "Use a screwdriver to fix screws",
        "Sweep the floor with a broom",
        "Use a roller to paint the ceiling",
    ],
    valid_en = [
        "Renovate and repaint the living room",
        "Repair and paint the fence",
        "Do a home improvement project",
    ],
    test_en = [
        "Prep the wall before painting",
        "Fix cracks and repaint",
        "Buy paint and tools for the renovation",
    ],
)

# ============================================================
# 204. hand-heart
# ============================================================
process_icon(
    "hand-heart",
    st_en = ["care", "charity", "donate", "help", "wishlist"],
    pst_en = [
        "Care for others in need", "Show care and kindness",
        "Donate to charity this month", "Support a local charity",
        "Donate clothes to the shelter", "Donate money to the cause",
        "Help a neighbor in need", "Help the community",
        "Add a gift to the wishlist", "Check the holiday wishlist",
    ],
    reg_en = [
        "Donate to a local charity",
        "Volunteer at the food bank",
        "Give blood at the donation center",
        "Support a crowdfunding campaign",
        "Help a friend move",
        "Donate old clothes to the shelter",
        "Participate in a charity run",
        "Raise money for a good cause",
        "Give a gift to someone in need",
        "Sponsor a child's education",
    ],
    conv_en = [
        "Give back",
        "Help others",
        "Donate today",
        "Care for someone",
    ],
    typo_en = [
        "donatte to chrity",
        "volnteer at food bank",
        "give blood at dontion center",
        "help a freind in need",
    ],
    bnd_en = [
        "Buy a gift for a friend",
        "Pay for someone's meal",
        "Write a thank-you card",
        "Send flowers to someone",
        "Give a compliment",
        "Cook dinner for a neighbor",
    ],
    valid_en = [
        "Donate to a local charity",
        "Volunteer at the food bank",
        "Help a friend in need",
    ],
    test_en = [
        "Support a crowdfunding campaign",
        "Donate old clothes to the shelter",
        "Participate in a charity run",
    ],
)

# ============================================================
# 205. hand-holding
# ============================================================
process_icon(
    "hand-holding",
    st_en = ["carry", "lift"],
    pst_en = [
        "Carry the box to the new room", "Carry groceries from the car",
        "Lift the heavy bag", "Lift the box onto the shelf",
    ],
    reg_en = [
        "Carry the groceries inside",
        "Hold the baby safely",
        "Lift the heavy box onto the shelf",
        "Carry the laundry basket",
        "Hold the door open for someone",
        "Carry the equipment to the venue",
        "Lift the suitcase into the overhead bin",
        "Hand something to a colleague",
        "Carry the tray of food",
        "Hold the package securely",
    ],
    conv_en = [
        "Carry that",
        "Hold it",
        "Lift it up",
        "Hand it over",
    ],
    typo_en = [
        "carrey the groceries",
        "lfit the heavy box",
        "holdd the baby",
        "caryr the laundrey",
    ],
    bnd_en = [
        "Use a dolly to move boxes",
        "Ask for help lifting",
        "Put the item down on the table",
        "Use a forklift for the heavy pallet",
        "Set the box on the conveyor belt",
        "Use both hands to hold the item",
    ],
    valid_en = [
        "Carry the groceries inside",
        "Lift the heavy box",
        "Hold the package securely",
    ],
    test_en = [
        "Carry the laundry basket",
        "Hand something to a colleague",
        "Lift the suitcase into the bin",
    ],
)

# ============================================================
# 206. hand-pointer
# ============================================================
process_icon(
    "hand-pointer",
    st_en = ["arrow", "cursor", "select"],
    pst_en = [
        "Click the arrow to proceed", "Follow the arrow to the exit",
        "Move the cursor to the button", "Click the cursor on the link",
        "Select the option from the menu", "Select all the items",
    ],
    reg_en = [
        "Click the button on the screen",
        "Point to the correct option",
        "Select the file to open",
        "Click the link to open the page",
        "Use the pointer to highlight",
        "Select items in the list",
        "Click the icon to launch the app",
        "Point the cursor to the right area",
        "Select all and copy",
        "Click the submit button",
    ],
    conv_en = [
        "Click here",
        "Point to it",
        "Select that",
        "Tap to open",
    ],
    typo_en = [
        "cilck the buton",
        "selecct the optoin",
        "moev the cursro",
        "ponit to the icon",
    ],
    bnd_en = [
        "Use the arrow keys to navigate",
        "Drag and drop the file",
        "Right-click to open the menu",
        "Use a touchscreen to tap",
        "Use a stylus to draw",
        "Scroll to see more options",
    ],
    valid_en = [
        "Click the button on the screen",
        "Select the file to open",
        "Point the cursor to the right area",
    ],
    test_en = [
        "Click the link to open the page",
        "Select all and copy",
        "Click the submit button",
    ],
)

# ============================================================
# 207. hands-bubbles
# ============================================================
process_icon(
    "hands-bubbles",
    st_en = ["hygiene", "soap", "wash"],
    pst_en = [
        "Practice good hygiene habits", "Teach kids about hygiene",
        "Use soap to wash hands", "Buy antibacterial soap",
        "Wash hands before eating", "Wash hands after using the bathroom",
    ],
    reg_en = [
        "Wash hands before cooking",
        "Use soap and water to wash hands",
        "Wash hands for 20 seconds",
        "Buy hand soap for the bathroom",
        "Teach kids to wash hands properly",
        "Wash hands after the gym",
        "Use hand sanitizer when soap is unavailable",
        "Wash hands after handling raw meat",
        "Keep soap near the sink",
        "Wash hands before eating",
    ],
    conv_en = [
        "Wash your hands!",
        "Soap up",
        "Hygiene first",
        "Clean hands",
    ],
    typo_en = [
        "wahs hands before eaitng",
        "use saop to wash hads",
        "clen hands wiht soap",
        "teahc kids to was hands",
    ],
    bnd_en = [
        "Take a shower",
        "Brush your teeth",
        "Use hand lotion after washing",
        "Use a hand dryer after washing",
        "Sanitize the kitchen counter",
        "Clean the bathroom sink",
    ],
    valid_en = [
        "Wash hands before cooking",
        "Use soap for 20 seconds",
        "Buy hand soap for the bathroom",
    ],
    test_en = [
        "Teach kids to wash hands",
        "Wash hands after the gym",
        "Keep soap near the sink",
    ],
)

# ============================================================
# 208. hands-holding
# ============================================================
process_icon(
    "hands-holding",
    st_en = ["carry", "hold", "lift"],
    pst_en = [
        "Carry the item with both hands", "Carry groceries with both hands",
        "Hold the baby with care", "Hold the fragile item gently",
        "Lift the box together", "Lift the sofa with help",
    ],
    reg_en = [
        "Hold the newborn baby",
        "Carry the large box together",
        "Support a friend in need",
        "Hold the dish with both hands",
        "Lift the furniture with a partner",
        "Carry the heavy equipment",
        "Hold the gift with both hands",
        "Pass the item carefully",
        "Hold the door open with both hands",
        "Lift the mattress upstairs",
    ],
    conv_en = [
        "Hold it together",
        "Both hands needed",
        "Carry together",
        "Lift with help",
    ],
    typo_en = [
        "holdd with boht hands",
        "carrey the large boks",
        "lfit the furniutre together",
        "supprot a freind",
    ],
    bnd_en = [
        "Carry with one hand only",
        "Use a cart to transport goods",
        "Use a crane to lift heavy items",
        "Ask for help lifting",
        "Use a dolly to move boxes",
        "Put the item on a trolley",
    ],
    valid_en = [
        "Hold the newborn with both hands",
        "Carry the large box together",
        "Lift the furniture with a partner",
    ],
    test_en = [
        "Support a friend in need",
        "Pass the fragile item carefully",
        "Lift the mattress upstairs",
    ],
)

# ============================================================
# 209. hard-drive
# ============================================================
process_icon(
    "hard-drive",
    st_en = ["hard drive", "machine", "save", "storage"],
    pst_en = [
        "Replace the old hard drive", "Upgrade the hard drive capacity",
        "Fix the machine that won't start", "Service the machine",
        "Save the work to the hard drive", "Save a backup to the drive",
        "Add more storage to the computer", "Buy external storage",
    ],
    reg_en = [
        "Back up files to the hard drive",
        "Replace the failing hard drive",
        "Buy an external hard drive",
        "Format the hard drive",
        "Transfer files to the new hard drive",
        "Check how much storage is left",
        "Delete old files to free up space",
        "Recover deleted files from the drive",
        "Upgrade to a solid state drive",
        "Clone the hard drive before replacing",
    ],
    conv_en = [
        "Back up the drive",
        "Storage full",
        "New hard drive",
        "Free up space",
    ],
    typo_en = [
        "bakcup fiels to hard driv",
        "replcae the failign drive",
        "buy an extenral hard driv",
        "formatt the hard drive",
    ],
    bnd_en = [
        "Save to a USB flash drive",
        "Upload to cloud storage",
        "Save to an SD card",
        "Use a NAS for network storage",
        "Back up to the floppy disk",
        "Store files on a DVD disc",
    ],
    valid_en = [
        "Back up files to the hard drive",
        "Replace the failing hard drive",
        "Check how much storage is left",
    ],
    test_en = [
        "Buy an external hard drive",
        "Delete old files to free up space",
        "Upgrade to a solid state drive",
    ],
)

print("\nAll 30 icons processed successfully!")
