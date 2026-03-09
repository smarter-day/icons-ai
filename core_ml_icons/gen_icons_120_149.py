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
# 120. conveyor-belt
# ============================================================
process_icon(
    "conveyor-belt",
    st_en = ["carousel", "inventory", "manufacture", "packaging", "shipping"],
    pst_en = [
        "Watch bags on the luggage carousel", "Pick up suitcase from the carousel",
        "Update the warehouse inventory", "Do a full inventory count",
        "Tour the manufacture facility", "Monitor the manufacture process",
        "Set up the packaging line", "Speed up the packaging process",
        "Track the shipping order", "Optimize shipping workflow",
    ],
    reg_en = [
        "Pick up luggage at the airport",
        "Monitor the production line",
        "Inspect items on the assembly line",
        "Speed up the packaging process",
        "Check goods moving through the factory",
        "Optimize the warehouse workflow",
        "Set up automated sorting",
        "Track items through the assembly line",
        "Manage the production schedule",
        "Visit the manufacturing plant",
    ],
    conv_en = [
        "Watch the belt",
        "Factory line check",
        "Grab it off the belt",
        "Production running",
    ],
    typo_en = [
        "conveyro belt speed",
        "packagin line setup",
        "inventroy on the belt",
        "manufcature process",
    ],
    bnd_en = [
        "Pack boxes and send to warehouse",
        "Ship goods in a container",
        "Sort documents in the filing cabinet",
        "Unload the delivery truck",
        "Organize items on warehouse shelves",
        "Track the package delivery",
    ],
    valid_en = [
        "Monitor the conveyor belt",
        "Pick up luggage from the carousel",
        "Check the production line speed",
    ],
    test_en = [
        "Inspect the assembly line",
        "Set up the packaging belt",
        "Track items on the factory belt",
    ],
)

# ============================================================
# 121. cookie
# ============================================================
process_icon(
    "cookie",
    st_en = ["baked good", "chips", "chocolate", "cookie", "dessert", "eat", "snack", "sweet", "treat"],
    pst_en = [
        "Bake a batch of baked goods", "Buy baked goods at the store",
        "Add chocolate chips to the dough", "Chocolate chips for baking",
        "Melt chocolate for the cookies", "Make chocolate chip cookies",
        "Bake homemade cookies", "Buy cookies from the bakery",
        "Make a dessert for the party", "Pick a dessert from the menu",
        "Eat cookies after dinner", "Eat a snack between meals",
        "Grab a snack from the pantry", "Have a snack before the movie",
        "Satisfy the sweet tooth", "Make something sweet today",
        "Give a treat to the kids", "Get a treat from the bakery",
    ],
    reg_en = [
        "Bake chocolate chip cookies",
        "Make cookies for the school bake sale",
        "Buy cookies at the grocery store",
        "Decorate cookies for the holidays",
        "Try a new cookie recipe",
        "Pack cookies for the road trip",
        "Give cookies as a gift",
        "Make peanut butter cookies",
        "Bake snickerdoodles",
        "Grab a cookie with coffee",
    ],
    conv_en = [
        "Cookie time!",
        "Bake some cookies",
        "Need a sweet snack",
        "Grab a cookie",
    ],
    typo_en = [
        "bake choclate chip cooikes",
        "cokie recipe",
        "buy cooikes at the store",
        "make dessetr cookies",
    ],
    bnd_en = [
        "Eat a cookie with a bite taken out",
        "Bake a birthday cake",
        "Make a brownie from scratch",
        "Buy a cupcake at the bakery",
        "Make muffins for breakfast",
        "Bake a pie for dessert",
    ],
    valid_en = [
        "Bake homemade cookies",
        "Buy cookies as a snack",
        "Make chocolate chip cookies",
    ],
    test_en = [
        "Grab a cookie for dessert",
        "Bake cookies for the holidays",
        "Pack cookies for a snack",
    ],
)

# ============================================================
# 122. cookie-bite
# ============================================================
process_icon(
    "cookie-bite",
    st_en = ["baked good", "bitten", "chips", "chocolate", "eat", "snack", "sweet", "treat"],
    pst_en = [
        "Take a bite out of the baked good", "Half-eaten baked good on the plate",
        "Cookie with a bitten piece", "Half bitten cookie on the desk",
        "Chocolate chips in the half-eaten cookie", "Chocolate chip cookie with a bite",
        "Bite into the chocolate cookie", "Chocolate cookie half eaten",
        "Start eating the snack", "Eat just a bit of the snack",
        "Quick snack between tasks", "Nibble on a snack",
        "Bite into something sweet", "Take a small sweet bite",
        "Give the kids a treat", "Taste the treat",
    ],
    reg_en = [
        "Take a bite of the cookie",
        "Leave a half-eaten cookie on the plate",
        "Snack on a cookie while working",
        "Eat just one cookie",
        "Try a bite of the dessert",
        "Nibble on a chocolate cookie",
        "Have a cookie break at work",
        "Share a cookie with a friend",
        "Eat a cookie in between meetings",
        "Bite into a fresh cookie",
    ],
    conv_en = [
        "Just one bite",
        "Half a cookie",
        "Quick nibble",
        "Bite that cookie",
    ],
    typo_en = [
        "half eaten cooike",
        "bitten choclate cookie",
        "cokie with a bite",
        "snakc on a cookie",
    ],
    bnd_en = [
        "Eat a whole unbitten cookie",
        "Bake a full batch of cookies",
        "Have a piece of cake",
        "Eat a full brownie",
        "Share a whole cookie",
        "Buy a bag of cookies at the store",
    ],
    valid_en = [
        "Take a bite of the cookie",
        "Half-eaten cookie on the desk",
        "Nibble on a chocolate cookie",
    ],
    test_en = [
        "Snack on a bitten cookie",
        "Eat just a piece of the cookie",
        "Cookie with one bite taken",
    ],
)

# ============================================================
# 123. copy
# ============================================================
process_icon(
    "copy",
    st_en = ["clone", "duplicate", "file", "paper", "paste"],
    pst_en = [
        "Clone the repository", "Clone the existing template",
        "Duplicate the document", "Duplicate the layer in the design",
        "Copy the file to another folder", "Attach the file to the email",
        "Print on paper", "Scan the paper document",
        "Copy and paste the text", "Paste the copied content",
    ],
    reg_en = [
        "Copy the text from the document",
        "Paste the link into the message",
        "Duplicate the file before editing",
        "Make a backup copy of the document",
        "Copy the template for a new project",
        "Clone the design for a new version",
        "Copy the code snippet",
        "Paste the address into the form",
        "Duplicate the spreadsheet",
        "Make a copy of the contract",
    ],
    conv_en = [
        "Copy that",
        "Duplicate it",
        "Just copy-paste",
        "Make a copy",
    ],
    typo_en = [
        "coppy the text",
        "duplciate the file",
        "paste the copeid text",
        "mak a copy of the doc",
    ],
    bnd_en = [
        "Move the file to the new folder",
        "Cut and paste the paragraph",
        "Share the document with the team",
        "Delete the original file",
        "Archive the old version",
        "Export the document as PDF",
    ],
    valid_en = [
        "Copy the document",
        "Duplicate the file",
        "Paste the copied text",
    ],
    test_en = [
        "Make a backup copy",
        "Clone the template",
        "Copy and paste the content",
    ],
)

# ============================================================
# 124. couch
# ============================================================
process_icon(
    "couch",
    st_en = ["chair", "cushion", "furniture", "relax", "sofa"],
    pst_en = [
        "Buy a comfortable chair", "Sit in the chair after work",
        "Replace the old cushions", "Fluff the sofa cushions",
        "Buy new furniture for the living room", "Rearrange the furniture",
        "Relax after a long day", "Find time to relax this weekend",
        "Pick a new sofa for the apartment", "Clean the sofa upholstery",
    ],
    reg_en = [
        "Watch TV on the couch",
        "Buy a new sofa for the living room",
        "Rearrange the living room furniture",
        "Take a nap on the couch",
        "Clean the couch cushions",
        "Order a couch online",
        "Find a sectional sofa that fits",
        "Relax on the sofa after work",
        "Set up the living room",
        "Get a couch cover to protect it",
    ],
    conv_en = [
        "Couch time",
        "Sofa nap",
        "Relax on the couch",
        "Lazy day in",
    ],
    typo_en = [
        "realx on the couch",
        "buy a new soaf",
        "clena the cusions",
        "furnituer for living room",
    ],
    bnd_en = [
        "Buy an office chair for the desk",
        "Set up a bed in the guest room",
        "Get a recliner chair",
        "Buy a dining table and chairs",
        "Place a rug in the living room",
        "Hang curtains in the living room",
    ],
    valid_en = [
        "Relax on the couch after work",
        "Buy a new sofa",
        "Clean the couch cushions",
    ],
    test_en = [
        "Watch a movie on the couch",
        "Take a nap on the sofa",
        "Rearrange the living room furniture",
    ],
)

# ============================================================
# 125. cow
# ============================================================
process_icon(
    "cow",
    st_en = ["agriculture", "animal", "beef", "bovine", "cow", "farm", "fauna", "livestock", "mammal", "milk", "moo"],
    pst_en = [
        "Visit an agriculture fair", "Learn about modern agriculture",
        "See the farm animals", "Feed the animals at the farm",
        "Buy beef at the butcher", "Cook a beef steak for dinner",
        "Learn about bovine farming", "Bovine health check",
        "See the cows in the field", "Pet the cow at the farm",
        "Visit the local farm", "Take kids to the farm",
        "Spot wildlife and fauna", "Learn about local fauna",
        "Buy livestock at the auction", "Care for livestock",
        "See the large mammals at the farm", "Feed the mammals",
        "Buy fresh milk at the farm", "Pick up milk from the store",
        "Hear the cow moo", "Imitate a cow moo",
    ],
    reg_en = [
        "Visit a dairy farm",
        "Buy fresh milk from the farm",
        "Cook beef burgers for the BBQ",
        "Take kids to a petting zoo",
        "Learn about dairy farming",
        "Watch cows graze in the field",
        "Buy grass-fed beef at the market",
        "Visit a ranch this weekend",
        "Make a beef stew for dinner",
        "Feed cows at the farm",
    ],
    conv_en = [
        "Farm visit!",
        "Got milk?",
        "Moo!",
        "Beef for dinner",
    ],
    typo_en = [
        "visitt the dairy fam",
        "buy freesh milk",
        "cook beeef burger",
        "see the cows int he field",
    ],
    bnd_en = [
        "Feed pigs at the farm",
        "Ride a horse at the stable",
        "See the goats at the petting zoo",
        "Visit a sheep farm",
        "Buy chicken at the butcher",
        "Watch deer graze in the meadow",
    ],
    valid_en = [
        "Visit a dairy farm",
        "Buy fresh milk",
        "Cook beef for dinner",
    ],
    test_en = [
        "Take kids to a farm",
        "Buy grass-fed beef",
        "Watch cows in the field",
    ],
)

# ============================================================
# 126. crab
# ============================================================
process_icon(
    "crab",
    st_en = ["claws", "crabmeat", "crustacean", "seafood", "shellfish", "zodiac"],
    pst_en = [
        "Watch out for the crab claws", "Pick crab claws for dinner",
        "Buy fresh crabmeat at the fish market", "Cook crabmeat pasta",
        "Learn about crustaceans", "Cook a crustacean dinner",
        "Order seafood at the restaurant", "Buy fresh seafood",
        "Try a shellfish platter", "Avoid shellfish if allergic",
        "Check your zodiac sign Cancer", "Read about the Cancer zodiac",
    ],
    reg_en = [
        "Order crab legs at the restaurant",
        "Cook fresh crab for dinner",
        "Go crabbing at the beach",
        "Buy live crabs at the market",
        "Make crab cakes",
        "Pick crab meat from the shell",
        "Find out if seafood is fresh",
        "Try a crab bisque soup",
        "Make seafood pasta with crab",
        "Visit the seafood market",
    ],
    conv_en = [
        "Crab dinner!",
        "Seafood night",
        "Go crabbing",
        "Fresh crab tonight",
    ],
    typo_en = [
        "order crab lesg",
        "buy freesh crab",
        "make craab cakes",
        "seafood nigt at the restaurant",
    ],
    bnd_en = [
        "Order lobster at the restaurant",
        "Buy fresh shrimp at the market",
        "Make a clam chowder",
        "Grill fish for dinner",
        "Try oysters for the first time",
        "Buy mussels at the fish market",
    ],
    valid_en = [
        "Cook crab for dinner",
        "Buy fresh crabmeat",
        "Order seafood at the restaurant",
    ],
    test_en = [
        "Make crab cakes",
        "Go crabbing at the beach",
        "Try a crab bisque",
    ],
)

# ============================================================
# 127. croissant
# ============================================================
process_icon(
    "croissant",
    st_en = ["bakery", "bread", "breakfast", "butter", "crescent", "croissant", "dough", "french", "pastry", "roll"],
    pst_en = [
        "Visit the local bakery", "Buy fresh pastries from the bakery",
        "Buy a fresh loaf of bread", "Bake bread at home",
        "Make a light breakfast", "Have a croissant for breakfast",
        "Spread butter on the croissant", "Butter the warm croissant",
        "Shape the dough into a crescent", "Crescent-shaped pastry for breakfast",
        "Buy a fresh croissant", "Warm up the croissant",
        "Knead the dough for pastry", "Let the dough rise overnight",
        "Try French cuisine", "Get a French pastry for breakfast",
        "Buy pastries for the meeting", "Make homemade pastry",
        "Make a buttery bread roll", "Serve warm rolls at dinner",
    ],
    reg_en = [
        "Buy croissants at the bakery",
        "Make homemade croissants",
        "Have a croissant with coffee",
        "Try almond croissants",
        "Pack a croissant for breakfast",
        "Get a ham and cheese croissant",
        "Order croissants for the office",
        "Visit a French bakery",
        "Make a croissant sandwich",
        "Bake croissants for the weekend",
    ],
    conv_en = [
        "Croissant time",
        "Fresh bakery run",
        "French breakfast",
        "Buttery croissant",
    ],
    typo_en = [
        "buy a fresh corissant",
        "croissent from the bakery",
        "frech pastry breakfast",
        "make homemade criossant",
    ],
    bnd_en = [
        "Buy a fresh bagel",
        "Get a baguette from the bakery",
        "Make a blueberry muffin",
        "Toast an English muffin",
        "Buy a sourdough loaf",
        "Make a cinnamon roll for breakfast",
    ],
    valid_en = [
        "Buy croissants at the bakery",
        "Have a croissant with coffee",
        "Make a croissant sandwich",
    ],
    test_en = [
        "Order croissants for the office",
        "Visit a French bakery",
        "Pack a croissant for breakfast",
    ],
)

# ============================================================
# 128. crop
# ============================================================
process_icon(
    "crop",
    st_en = ["design", "frame", "mask", "modify", "resize", "shrink"],
    pst_en = [
        "Crop the image for the design", "Adjust the design canvas",
        "Set the photo frame size", "Frame the image for Instagram",
        "Apply a mask to the photo layer", "Mask out the background",
        "Modify the photo before posting", "Modify the image dimensions",
        "Resize the image for the web", "Resize the photo before uploading",
        "Shrink the image file size", "Shrink the photo to fit the screen",
    ],
    reg_en = [
        "Crop the profile photo",
        "Trim the video clip",
        "Crop the screenshot before sending",
        "Resize image for the presentation",
        "Adjust the aspect ratio",
        "Crop out unwanted background",
        "Edit the photo before sharing",
        "Prepare the image for the blog",
        "Crop the banner to the right size",
        "Trim the edges of the photo",
    ],
    conv_en = [
        "Crop that photo",
        "Trim the image",
        "Quick crop",
        "Edit the pic",
    ],
    typo_en = [
        "croop the profile photo",
        "rezise the image",
        "tirm the photo edges",
        "modfiy the photo size",
    ],
    bnd_en = [
        "Rotate the photo 90 degrees",
        "Adjust brightness and contrast",
        "Apply a filter to the photo",
        "Resize the canvas in Photoshop",
        "Flip the image horizontally",
        "Add a border to the photo",
    ],
    valid_en = [
        "Crop the profile photo",
        "Resize image for the web",
        "Trim the screenshot before sharing",
    ],
    test_en = [
        "Crop the banner image",
        "Adjust the photo aspect ratio",
        "Crop out the background",
    ],
)

# ============================================================
# 129. crosshairs
# ============================================================
process_icon(
    "crosshairs",
    st_en = ["aim", "bullseye", "picker", "position"],
    pst_en = [
        "Aim at the target", "Aim precisely at the center",
        "Hit the bullseye on the target", "Bullseye shot",
        "Use the color picker tool", "Pick an exact color with the picker",
        "Mark the position on the map", "Find the exact position",
    ],
    reg_en = [
        "Find my current GPS location",
        "Pin the exact position on the map",
        "Use the color picker in the design tool",
        "Target the precise area",
        "Lock on to the location",
        "Center the crosshairs on the target",
        "Navigate to the exact coordinates",
        "Pick the right color for the design",
        "Set the focus point on the camera",
        "Locate the exact spot on the map",
    ],
    conv_en = [
        "Lock on target",
        "Find the spot",
        "Aim right there",
        "Dead center",
    ],
    typo_en = [
        "find my currnet location",
        "aim at the taregt",
        "use the colro picker",
        "postion on the map",
    ],
    bnd_en = [
        "Hit the bullseye on the archery target",
        "Navigate with a compass",
        "Set a map pin for the destination",
        "Use GPS to find the route",
        "Zoom in on the target area",
        "Focus the camera on the subject",
    ],
    valid_en = [
        "Find the precise location",
        "Use the color picker tool",
        "Aim at the exact target",
    ],
    test_en = [
        "Pin the position on the map",
        "Center the aim on the target",
        "Pick the exact color",
    ],
)

# ============================================================
# 130. crow
# ============================================================
process_icon(
    "crow",
    st_en = ["bird", "fauna", "halloween", "holiday"],
    pst_en = [
        "Watch a bird perch on the fence", "Spot a bird in the yard",
        "Learn about local fauna", "Observe fauna in the park",
        "Decorate for halloween", "Buy halloween decorations",
        "Plan for the holiday", "Celebrate the holiday with family",
    ],
    reg_en = [
        "Spot a crow on the rooftop",
        "Listen to crows cawing outside",
        "Decorate the yard for Halloween",
        "Set up spooky decorations",
        "Photograph the crow in the park",
        "Watch birds from the window",
        "See crows gathering in the trees",
        "Put out a scarecrow in the garden",
        "Watch the crows fly at sunset",
        "Learn about crow behavior",
    ],
    conv_en = [
        "Halloween vibes",
        "Spooky bird",
        "Crows everywhere",
        "Creepy crow",
    ],
    typo_en = [
        "haloween decorations",
        "spot a crwo in the yard",
        "spooky halowwen bird",
        "crows on the rooftpo",
    ],
    bnd_en = [
        "Feed pigeons in the park",
        "Watch a dove flying",
        "Spot an eagle in the sky",
        "Hear an owl hoot at night",
        "Watch seagulls at the beach",
        "Observe a parrot in the tree",
    ],
    valid_en = [
        "Spot a crow in the park",
        "Decorate for Halloween",
        "Listen to crows cawing",
    ],
    test_en = [
        "Watch crows gather in the yard",
        "Set up Halloween decorations",
        "Photograph the crow at sunset",
    ],
)

# ============================================================
# 131. cup-togo
# ============================================================
process_icon(
    "cup-togo",
    st_en = ["beverage", "breakfast", "cafe", "drink", "latte", "morning", "mug", "starbucks", "takeout", "tea", "travel"],
    pst_en = [
        "Order a hot beverage to go", "Get a takeout beverage",
        "Grab breakfast on the way to work", "Pick up a breakfast drink",
        "Visit the local cafe", "Order from the cafe drive-through",
        "Get a drink for the commute", "Pick up a drink before the meeting",
        "Order a latte to go", "Try a vanilla latte",
        "Get morning coffee on the go", "Morning coffee before work",
        "Buy a travel mug", "Bring a reusable mug to the cafe",
        "Order a Starbucks drink", "Pick up Starbucks on the way",
        "Get takeout coffee", "Takeout tea from the shop",
        "Order tea to go", "Get a cup of herbal tea",
        "Coffee for the travel day", "Grab coffee for the road trip",
    ],
    reg_en = [
        "Grab a coffee on the way to work",
        "Order a latte from the coffee shop",
        "Pick up tea for the commute",
        "Get a drink from the drive-through",
        "Buy a to-go cup of coffee",
        "Order a hot chocolate to go",
        "Pick up drinks for the team",
        "Grab an iced coffee from the cafe",
        "Get a travel cup of green tea",
        "Stop at the coffee shop before work",
    ],
    conv_en = [
        "Coffee to go!",
        "Grab a cup",
        "Drive-through run",
        "Tea for the road",
    ],
    typo_en = [
        "grab a coffe on the way",
        "ordr a latte to go",
        "pick up tee for commute",
        "starbukcs order",
    ],
    bnd_en = [
        "Brew coffee at home in the coffee pot",
        "Drink coffee from a ceramic mug",
        "Make tea in the kettle at home",
        "Use a French press for coffee",
        "Sit and drink coffee at the cafe",
        "Make a smoothie at home",
    ],
    valid_en = [
        "Order coffee to go",
        "Grab a latte for the commute",
        "Pick up tea from the cafe",
    ],
    test_en = [
        "Stop at the coffee shop drive-through",
        "Get a to-go drink before work",
        "Order a hot drink for the road",
    ],
)

# ============================================================
# 132. curling-stone
# ============================================================
process_icon(
    "curling-stone",
    st_en = ["curling stone", "game", "ice", "olympics", "rock", "sport", "stone"],
    pst_en = [
        "Throw the curling stone on the ice", "Practice the curling stone slide",
        "Play a new game this weekend", "Find a new game to try",
        "Book ice time at the rink", "Skate on the ice",
        "Watch the winter Olympics", "Follow the Olympics events",
        "Roll the rock down the ice", "Slide the rock to the target",
        "Try a winter sport", "Sign up for a winter sport class",
        "Smooth the stone before delivery", "Aim the stone at the target",
    ],
    reg_en = [
        "Watch curling at the Olympics",
        "Try curling for the first time",
        "Join a curling league",
        "Book a curling session at the rink",
        "Learn the rules of curling",
        "Sweep the ice in front of the stone",
        "Aim for the center of the target",
        "Practice the curling delivery",
        "Watch the curling team strategy",
        "Go curling with friends",
    ],
    conv_en = [
        "Try curling!",
        "Ice sport fun",
        "Olympic curling",
        "Throw the stone",
    ],
    typo_en = [
        "wach curling at hte olympics",
        "try curlign for first time",
        "book a curlng session",
        "sweap the iec",
    ],
    bnd_en = [
        "Go ice skating at the rink",
        "Play ice hockey with friends",
        "Try bobsled at the winter games",
        "Ski down the mountain slope",
        "Go snowboarding this winter",
        "Watch figure skating at the Olympics",
    ],
    valid_en = [
        "Try curling at the ice rink",
        "Watch curling at the Olympics",
        "Join a curling league",
    ],
    test_en = [
        "Book a curling session",
        "Practice the curling delivery",
        "Watch the curling competition",
    ],
)

# ============================================================
# 133. dagger
# ============================================================
process_icon(
    "dagger",
    st_en = ["blade", "d&d", "fantasy", "rogue", "weapon"],
    pst_en = [
        "Buy a dagger for the costume", "Collect a dagger as decoration",
        "Use a dagger in the D&D campaign", "Play D&D this weekend",
        "Create a fantasy character", "Build a fantasy world",
        "Play the rogue character in the game", "Level up the rogue class",
        "Craft a weapon in the game", "Find a rare weapon in the dungeon",
    ],
    reg_en = [
        "Play Dungeons and Dragons",
        "Design a fantasy RPG character",
        "Find a rare dagger in the dungeon",
        "Buy a costume prop for Halloween",
        "Write a fantasy story",
        "Set up the D&D campaign",
        "Choose the rogue class in the game",
        "Watch a fantasy movie tonight",
        "Collect fantasy memorabilia",
        "Play a tabletop RPG game",
    ],
    conv_en = [
        "D&D night",
        "Fantasy game",
        "Rogue class",
        "Dungeon run",
    ],
    typo_en = [
        "play dungeons and draogns",
        "fantsy character creation",
        "roug class in the game",
        "use a dagegr in battle",
    ],
    bnd_en = [
        "Wield a sword in the RPG",
        "Use a bow and arrow",
        "Fight with an axe in the game",
        "Equip a shield for defense",
        "Cast a spell as a wizard",
        "Use a staff as a mage",
    ],
    valid_en = [
        "Play D&D with friends",
        "Use a dagger in the RPG",
        "Design a rogue character",
    ],
    test_en = [
        "Set up a D&D campaign",
        "Find a dagger in the dungeon",
        "Play the rogue class tonight",
    ],
)

# ============================================================
# 134. database
# ============================================================
process_icon(
    "database",
    st_en = ["computer", "development", "directory", "memory", "mysql", "sql", "storage"],
    pst_en = [
        "Set up the computer database", "Fix the computer storage issue",
        "Work on the development database", "Set up the development environment",
        "Search the company directory", "Create a new directory structure",
        "Expand the server memory", "Free up memory on the database server",
        "Optimize the MySQL database", "Connect to the MySQL server",
        "Run a SQL query", "Write an SQL script to update data",
        "Add storage to the database server", "Backup the database to storage",
    ],
    reg_en = [
        "Set up the database for the app",
        "Run a SQL query on the database",
        "Backup the database",
        "Optimize slow database queries",
        "Add new records to the database",
        "Create a new database table",
        "Connect the app to the database",
        "Migrate data to the new database",
        "Monitor database performance",
        "Grant access to the database",
    ],
    conv_en = [
        "Database work",
        "Run the query",
        "DB backup",
        "Check the database",
    ],
    typo_en = [
        "bakcup the databse",
        "run sql queery",
        "optimze database",
        "conect to mysql",
    ],
    bnd_en = [
        "Write code for the new feature",
        "Set up a file server",
        "Use cloud storage for files",
        "Create a spreadsheet in Excel",
        "Manage files in the directory",
        "Set up a NoSQL database",
    ],
    valid_en = [
        "Backup the database",
        "Run a SQL query",
        "Optimize the database performance",
    ],
    test_en = [
        "Set up the app database",
        "Create a new database table",
        "Connect the app to MySQL",
    ],
)

# ============================================================
# 135. deer
# ============================================================
process_icon(
    "deer",
    st_en = ["animal", "antlers", "deer", "fauna", "mammal", "reindeer"],
    pst_en = [
        "Spot a wild animal on the hike", "See animals at the wildlife park",
        "Admire the deer's antlers", "Draw the deer antlers",
        "Watch deer in the forest", "Photograph a deer in the meadow",
        "Learn about local fauna", "Observe fauna on the nature trail",
        "See the large mammals at the wildlife park", "Feed mammals at the sanctuary",
        "Watch Santa's reindeer", "Read about reindeer for Christmas",
    ],
    reg_en = [
        "Watch deer graze in the meadow",
        "Spot deer on the hiking trail",
        "Take photos of deer in the wild",
        "Visit a deer sanctuary",
        "See reindeer at the Christmas market",
        "Feed deer at the nature park",
        "Watch for deer crossing the road",
        "Learn about deer behavior",
        "Photograph wildlife in the forest",
        "See fawns in the spring",
    ],
    conv_en = [
        "Deer in the yard!",
        "Spotted a deer",
        "Watch the deer",
        "Wildlife sighting",
    ],
    typo_en = [
        "spot a deerr on the trail",
        "see wild animlas in the forest",
        "watch deeer graze",
        "photographh wildlife",
    ],
    bnd_en = [
        "Visit a farm to see cows",
        "Watch horses at the stable",
        "See moose in the wild",
        "Spot an elk on the trail",
        "Visit a petting zoo with goats",
        "Watch rabbits in the field",
    ],
    valid_en = [
        "Watch deer graze in the field",
        "Spot deer on the hiking trail",
        "See reindeer at the Christmas market",
    ],
    test_en = [
        "Photograph deer in the wild",
        "Visit a deer sanctuary",
        "Watch for deer crossing the road",
    ],
)

# ============================================================
# 136. desktop
# ============================================================
process_icon(
    "desktop",
    st_en = ["computer", "cpu", "desktop", "desktop computer", "device", "imac", "machine", "monitor", "pc", "screen"],
    pst_en = [
        "Set up the computer at home", "Repair the computer",
        "Upgrade the CPU for better performance", "Replace the CPU",
        "Clean up the desktop", "Organize the desktop icons",
        "Buy a new desktop computer", "Configure the desktop computer",
        "Connect a new device to the network", "Set up the device",
        "Get a new iMac for the studio", "Set up the iMac at work",
        "Repair the machine", "Service the machine regularly",
        "Adjust the monitor brightness", "Position the monitor ergonomically",
        "Build a gaming PC", "Set up the new PC",
        "Clean the screen", "Replace the cracked screen",
    ],
    reg_en = [
        "Set up the iMac on the desk",
        "Buy a new desktop computer for work",
        "Upgrade the RAM in the desktop",
        "Install software on the desktop PC",
        "Clean the monitor screen",
        "Connect an external monitor",
        "Back up data from the desktop",
        "Replace the old desktop with a new one",
        "Configure the display settings",
        "Set up the home office desktop",
    ],
    conv_en = [
        "New iMac day",
        "Desktop upgrade",
        "Set up the PC",
        "New screen",
    ],
    typo_en = [
        "set up the desktpo computer",
        "by a new imac",
        "clen the monitr screen",
        "upgarde the pc",
    ],
    bnd_en = [
        "Buy a new laptop for travel",
        "Set up a tablet for the kids",
        "Connect a keyboard to the laptop",
        "Use a gaming console",
        "Set up a second monitor for the laptop",
        "Configure a server machine",
    ],
    valid_en = [
        "Set up the desktop computer",
        "Buy a new iMac for the office",
        "Configure the PC display",
    ],
    test_en = [
        "Upgrade the desktop PC",
        "Install software on the desktop",
        "Clean the computer screen",
    ],
)

# ============================================================
# 137. diagram-project
# ============================================================
process_icon(
    "diagram-project",
    st_en = ["chart", "graph", "network", "pert", "statistics"],
    pst_en = [
        "Build a project chart", "Review the project chart with the team",
        "Create a bar graph for the report", "Read the graph results",
        "Map out the network diagram", "Design the network topology",
        "Use a PERT chart for planning", "Create a PERT diagram for the project",
        "Analyze project statistics", "Share statistics in the presentation",
    ],
    reg_en = [
        "Create a project flow diagram",
        "Map the dependencies between tasks",
        "Plan the project phases",
        "Build a network chart for the project",
        "Review the project diagram with the team",
        "Use a PERT chart for scheduling",
        "Visualize the project timeline",
        "Draw the task dependency chart",
        "Plan milestones on the diagram",
        "Update the project workflow diagram",
    ],
    conv_en = [
        "Map the project",
        "Draw the workflow",
        "Project diagram",
        "Task flow chart",
    ],
    typo_en = [
        "creat a project charrt",
        "plan the prject flow",
        "netwrok diagram",
        "pert chartt for planning",
    ],
    bnd_en = [
        "Create a pie chart for the budget",
        "Make a Gantt chart for the schedule",
        "Draw a Venn diagram",
        "Build a bar chart for statistics",
        "Make a line graph of the trend",
        "Create a spreadsheet table",
    ],
    valid_en = [
        "Map the project dependencies",
        "Create a project flow diagram",
        "Build a network chart",
    ],
    test_en = [
        "Plan the project phases with a diagram",
        "Draw the task dependency chart",
        "Use PERT for project scheduling",
    ],
)

# ============================================================
# 138. diagram-venn
# ============================================================
process_icon(
    "diagram-venn",
    st_en = ["chart", "intersection", "logic", "overlap"],
    pst_en = [
        "Create a chart to compare options", "Build a comparison chart",
        "Find the intersection of two sets", "Show the intersection in the diagram",
        "Apply logic to the problem", "Use logic to categorize items",
        "Show where two groups overlap", "Highlight the overlap between categories",
    ],
    reg_en = [
        "Draw a Venn diagram to compare",
        "Use a Venn diagram in the presentation",
        "Show the overlap between two ideas",
        "Compare two groups with a Venn diagram",
        "Teach logic with a Venn diagram",
        "Find common ground between options",
        "Visualize intersecting categories",
        "Map out shared features of two products",
        "Use Venn diagram for brainstorming",
        "Compare two data sets with a diagram",
    ],
    conv_en = [
        "Venn diagram it",
        "Find the overlap",
        "Compare the two",
        "Logic diagram",
    ],
    typo_en = [
        "draw a venn daigram",
        "find the intersecton",
        "compair two groups",
        "show the overalp",
    ],
    bnd_en = [
        "Make a pie chart for the budget",
        "Create a bar graph for the report",
        "Build a network flow diagram",
        "Use a PERT chart for the project",
        "Create a Gantt chart timeline",
        "Draw a mind map for brainstorming",
    ],
    valid_en = [
        "Draw a Venn diagram to compare",
        "Show the overlap between two groups",
        "Use a Venn diagram in the presentation",
    ],
    test_en = [
        "Compare two options with a Venn diagram",
        "Find the intersection of categories",
        "Visualize shared features",
    ],
)

# ============================================================
# 139. dial
# ============================================================
process_icon(
    "dial",
    st_en = ["dial", "level"],
    pst_en = [
        "Turn the dial to adjust the volume", "Set the dial to the right setting",
        "Check the level on the gauge", "Set the difficulty level",
    ],
    reg_en = [
        "Adjust the settings on the device",
        "Turn up the volume on the stereo",
        "Set the temperature on the oven dial",
        "Tune the radio dial to the station",
        "Adjust the thermostat",
        "Set the correct level for the task",
        "Turn the knob to the right setting",
        "Calibrate the instrument dial",
        "Fine-tune the audio settings",
        "Adjust the brightness level",
    ],
    conv_en = [
        "Turn the dial",
        "Adjust the level",
        "Crank it up",
        "Set the knob",
    ],
    typo_en = [
        "asjust the sttings dial",
        "trun up the volum",
        "set the tempreture dial",
        "tune the raido",
    ],
    bnd_en = [
        "Use a slider to adjust the volume",
        "Press a button to change settings",
        "Adjust the brightness with a tap",
        "Use a gauge to measure pressure",
        "Set the speed on the treadmill",
        "Use a toggle switch to turn on",
    ],
    valid_en = [
        "Adjust the dial settings",
        "Turn the knob to the right level",
        "Calibrate the instrument",
    ],
    test_en = [
        "Set the temperature on the dial",
        "Tune the radio dial",
        "Adjust the volume level",
    ],
)

# ============================================================
# 140. dice
# ============================================================
process_icon(
    "dice",
    st_en = ["chance", "dice", "die", "gambling", "game", "game die", "roll"],
    pst_en = [
        "Take a chance on the game", "Leave it to chance",
        "Roll the dice to move", "Buy a set of dice for the game",
        "Roll the die for your turn", "Throw the die and move",
        "Try your luck at gambling", "Avoid gambling problems",
        "Play a board game tonight", "Set up the game for family night",
        "Roll the game die for your turn", "Use the game die to decide",
        "Roll the dice at the start", "Roll again for a double",
    ],
    reg_en = [
        "Play a board game with the family",
        "Roll the dice for your turn",
        "Host a game night",
        "Buy a new board game",
        "Set up Dungeons and Dragons",
        "Decide who goes first by rolling",
        "Play Yahtzee tonight",
        "Try a new dice game",
        "Bring dice to the camping trip",
        "Play a casino game",
    ],
    conv_en = [
        "Roll the dice!",
        "Game night",
        "Take a chance",
        "Board game time",
    ],
    typo_en = [
        "rol the diec",
        "borad game night",
        "play with dise",
        "gambling at the casnio",
    ],
    bnd_en = [
        "Play a card game with friends",
        "Spin the wheel on the game show",
        "Play chess with a partner",
        "Flip a coin to decide",
        "Play dominoes",
        "Deal cards for poker night",
    ],
    valid_en = [
        "Roll the dice for your turn",
        "Host a board game night",
        "Play Yahtzee with friends",
    ],
    test_en = [
        "Buy a new board game",
        "Set up the dice game",
        "Play a dice game tonight",
    ],
)

# ============================================================
# 141. diploma
# ============================================================
process_icon(
    "diploma",
    st_en = ["award", "certificate", "college", "education", "graduate", "graduation", "scholar", "university"],
    pst_en = [
        "Win an award for best performance", "Give out awards at the ceremony",
        "Get a certificate of completion", "Hang the certificate on the wall",
        "Apply to college", "Choose the right college",
        "Invest in education", "Support education programs",
        "Graduate from the program", "Celebrate the graduate",
        "Attend the graduation ceremony", "Plan the graduation party",
        "Become a scholar in the field", "Apply for a scholarship",
        "Graduate from university", "Apply to university programs",
    ],
    reg_en = [
        "Attend the graduation ceremony",
        "Frame the diploma",
        "Apply for a scholarship",
        "Celebrate finishing the degree",
        "Send graduation announcements",
        "Plan a graduation party",
        "Pick up the diploma from school",
        "Apply to graduate school",
        "Order a graduation cap and gown",
        "Share the graduation photo",
    ],
    conv_en = [
        "Graduation day!",
        "Got my diploma",
        "School's done",
        "Grad party time",
    ],
    typo_en = [
        "gradution ceremony",
        "fram the diplom",
        "apply for scholrship",
        "celebarte graduation",
    ],
    bnd_en = [
        "Win a sports trophy",
        "Earn a work promotion",
        "Receive an employee award",
        "Get a participation medal",
        "Frame a family photo",
        "Hang a certificate of appreciation",
    ],
    valid_en = [
        "Attend the graduation ceremony",
        "Frame the diploma",
        "Celebrate finishing the degree",
    ],
    test_en = [
        "Plan a graduation party",
        "Apply for a scholarship",
        "Pick up the diploma from school",
    ],
)

# ============================================================
# 142. display
# ============================================================
process_icon(
    "display",
    st_en = ["Screen", "computer", "desktop", "imac"],
    pst_en = [
        "Adjust the screen brightness", "Replace the cracked screen",
        "Connect a computer to the display", "Set up dual computer screens",
        "Set up a clean desktop workspace", "Organize the desktop",
        "Buy a new iMac for the studio", "Set up the iMac on the desk",
    ],
    reg_en = [
        "Adjust the display resolution",
        "Clean the computer screen",
        "Connect to an external display",
        "Mirror the screen to the TV",
        "Change the wallpaper on the screen",
        "Set up dual displays for work",
        "Adjust the screen refresh rate",
        "Fix the flickering screen",
        "Buy a widescreen monitor",
        "Calibrate the display colors",
    ],
    conv_en = [
        "New screen day",
        "Screen setup",
        "Dual monitors",
        "Fix the display",
    ],
    typo_en = [
        "adujst the scren brightness",
        "by a new monitr",
        "conect to external displaly",
        "set up duel screens",
    ],
    bnd_en = [
        "Buy a new laptop screen",
        "Fix the phone display",
        "Set up a projector for the room",
        "Connect the TV to the PC",
        "Use a tablet as a second screen",
        "Fix the broken desktop monitor",
    ],
    valid_en = [
        "Adjust the display settings",
        "Clean the computer screen",
        "Connect to an external display",
    ],
    test_en = [
        "Set up dual display screens",
        "Calibrate the display colors",
        "Fix the flickering screen",
    ],
)

# ============================================================
# 143. dog
# ============================================================
process_icon(
    "dog",
    st_en = ["animal", "canine", "dog", "fauna", "mammal", "pet", "pooch", "puppy", "woof"],
    pst_en = [
        "See the wild animal at the sanctuary", "Take kids to see animals",
        "Train the canine to sit", "Canine obedience class",
        "Walk the dog in the park", "Buy food for the dog",
        "Observe the local fauna", "Learn about fauna in the park",
        "Pet the friendly mammal", "Learn about mammals at the zoo",
        "Take the pet to the vet", "Buy a toy for the pet",
        "Give the pooch a bath", "Brush the pooch",
        "Adopt a puppy from the shelter", "Train the new puppy",
        "Hear the dog woof", "Teach the dog not to woof at strangers",
    ],
    reg_en = [
        "Walk the dog in the morning",
        "Take the dog to the vet",
        "Buy dog food at the pet store",
        "Train the dog to sit and stay",
        "Groom the dog",
        "Play fetch with the dog in the park",
        "Adopt a dog from the shelter",
        "Sign up for dog training classes",
        "Buy a dog bed",
        "Take the dog to the dog park",
    ],
    conv_en = [
        "Dog walk time",
        "Puppy cuddles",
        "Vet appointment",
        "Good doggo",
    ],
    typo_en = [
        "wlak the dgo",
        "take dog to vett",
        "buy dgo food",
        "adoppt a puppy",
    ],
    bnd_en = [
        "Take the dog for a walk on the leash",
        "Feed the cat",
        "Clean the fish tank",
        "Buy food for the hamster",
        "Take the rabbit to the vet",
        "Watch the dog with a guide harness",
    ],
    valid_en = [
        "Walk the dog in the park",
        "Take the dog to the vet",
        "Adopt a puppy from the shelter",
    ],
    test_en = [
        "Buy dog food at the store",
        "Train the dog to sit",
        "Play fetch with the dog",
    ],
)

# ============================================================
# 144. dog-leashed
# ============================================================
process_icon(
    "dog-leashed",
    st_en = ["animal", "canine", "guide dog", "mammal", "pet", "puppy", "walk"],
    pst_en = [
        "See the animal on the leash", "Keep the animal on a leash in public",
        "Train the canine on a leash", "Canine leash training class",
        "Get a guide dog for assistance", "Work with a guide dog trainer",
        "Walk with the mammal on a leash", "Mammals must be on leash in the park",
        "Buy a harness for the pet", "Register the pet at the vet",
        "Train the puppy to walk on a leash", "Take the puppy on a leash walk",
        "Go for a walk with the dog", "Walk the dog on the trail",
    ],
    reg_en = [
        "Walk the dog on a leash",
        "Buy a new dog leash",
        "Train the dog to heel on leash",
        "Keep the dog leashed in the park",
        "Get a retractable leash",
        "Practice loose leash walking",
        "Use a harness instead of a collar",
        "Walk the dog twice a day",
        "Sign up for leash training class",
        "Keep the dog leashed on the trail",
    ],
    conv_en = [
        "Leash the dog",
        "Dog walk time",
        "On the leash",
        "Morning walk",
    ],
    typo_en = [
        "walk the dgo on leash",
        "buy a new lesah",
        "trian dog to heel",
        "kep dog on leahs",
    ],
    bnd_en = [
        "Let the dog run off leash at the park",
        "Walk the dog without a leash",
        "Train the dog to come when called",
        "Take the cat for a walk in a carrier",
        "Walk with the dog freely in the yard",
        "Teach the dog to fetch",
    ],
    valid_en = [
        "Walk the dog on a leash",
        "Buy a new dog leash",
        "Train the dog to walk on leash",
    ],
    test_en = [
        "Keep the dog leashed in public",
        "Practice leash training",
        "Walk the dog on the trail",
    ],
)

# ============================================================
# 145. dollar-sign
# ============================================================
process_icon(
    "dollar-sign",
    st_en = ["coupon", "currency", "dollar", "investment", "money", "premium", "revenue", "salary"],
    pst_en = [
        "Use a coupon at the store", "Find a coupon for the restaurant",
        "Exchange currency at the bank", "Check the currency rate",
        "Pay with a dollar bill", "Count the dollar bills",
        "Make an investment decision", "Research investment options",
        "Save money this month", "Budget the money carefully",
        "Upgrade to a premium plan", "Get premium features",
        "Track monthly revenue", "Report on annual revenue",
        "Negotiate the salary", "Ask for a salary raise",
    ],
    reg_en = [
        "Check the price of the item",
        "Pay the bill",
        "Budget for the month",
        "Track expenses and income",
        "Negotiate a higher salary",
        "Invest money in savings",
        "Find a discount or coupon",
        "Split the bill with friends",
        "Transfer money to savings",
        "Check the bank balance",
    ],
    conv_en = [
        "Money talk",
        "Check the price",
        "Pay up",
        "Dollar day",
    ],
    typo_en = [
        "pay the bil",
        "budgte for the month",
        "negociate a sallary",
        "investt money in savigns",
    ],
    bnd_en = [
        "Count coins in the jar",
        "Use a credit card for payment",
        "Get a discount badge",
        "Pay with a check",
        "Transfer money via bank app",
        "Check the price tag on the item",
    ],
    valid_en = [
        "Budget for the month",
        "Negotiate a salary raise",
        "Track monthly revenue",
    ],
    test_en = [
        "Pay the bill",
        "Find a coupon for the store",
        "Check the investment options",
    ],
)

# ============================================================
# 146. dolly
# ============================================================
process_icon(
    "dolly",
    st_en = ["carry", "shipping", "transport"],
    pst_en = [
        "Carry heavy boxes with the dolly", "Use a dolly to carry equipment",
        "Ship the heavy items via freight", "Arrange shipping for the boxes",
        "Transport furniture with the dolly", "Use the dolly to transport goods",
    ],
    reg_en = [
        "Use a dolly to move heavy boxes",
        "Load boxes on the hand truck",
        "Move furniture with the dolly",
        "Transport equipment to the venue",
        "Use a hand truck to carry appliances",
        "Move boxes during the office move",
        "Unload the delivery truck",
        "Wheel the luggage to the room",
        "Load the dolly at the warehouse",
        "Move heavy items without strain",
    ],
    conv_en = [
        "Use the dolly",
        "Move the boxes",
        "Hand truck time",
        "Heavy load move",
    ],
    typo_en = [
        "use the dolley for boxes",
        "carrey heavy stuff",
        "moove furniture with dolly",
        "shiping heavy items",
    ],
    bnd_en = [
        "Push the shopping cart in the store",
        "Use a forklift at the warehouse",
        "Ship items in a container",
        "Pack boxes for the storage unit",
        "Use a luggage trolley at the airport",
        "Carry a backpack for the move",
    ],
    valid_en = [
        "Use the dolly to move boxes",
        "Load equipment on the hand truck",
        "Transport heavy items with a dolly",
    ],
    test_en = [
        "Move furniture with the dolly",
        "Unload boxes from the truck",
        "Use a dolly at the warehouse",
    ],
)

# ============================================================
# 147. dolphin
# ============================================================
process_icon(
    "dolphin",
    st_en = ["aquarium", "dolphin", "fish", "flipper", "mammal", "marine", "maritime", "porpoise"],
    pst_en = [
        "Visit the aquarium this weekend", "Buy tickets to the aquarium",
        "Watch dolphins jump", "See a dolphin in the wild",
        "Watch the fish in the tank", "Feed the fish at the aquarium",
        "Watch the dolphin use its flipper", "Flipper the dolphin show",
        "See the marine mammals at the show", "Learn about marine mammals",
        "Go on a marine wildlife tour", "Learn about marine ecosystems",
        "Take a maritime tour", "Enjoy a maritime experience",
        "Learn about porpoises", "Spot a porpoise in the water",
    ],
    reg_en = [
        "Visit an aquarium",
        "Watch the dolphin show",
        "Go whale watching",
        "Swim with dolphins",
        "See dolphins at the beach",
        "Book a dolphin watching tour",
        "Learn about marine life",
        "Take kids to the aquarium",
        "Watch dolphins play in the waves",
        "See dolphins from the boat",
    ],
    conv_en = [
        "Dolphin show!",
        "Aquarium visit",
        "Swim with dolphins",
        "Marine life fun",
    ],
    typo_en = [
        "see dolhpins at the beach",
        "visit the aquareum",
        "wach the dolpin show",
        "swm with dolphins",
    ],
    bnd_en = [
        "Watch whales on the ocean tour",
        "See sharks at the aquarium",
        "Watch sea lions perform",
        "Go scuba diving to see fish",
        "See penguins at the zoo",
        "Watch an octopus at the aquarium",
    ],
    valid_en = [
        "Visit the aquarium",
        "Watch the dolphin show",
        "Go on a dolphin watching tour",
    ],
    test_en = [
        "Swim with dolphins",
        "Take kids to the aquarium",
        "See dolphins from the boat",
    ],
)

# ============================================================
# 148. door-closed
# ============================================================
process_icon(
    "door-closed",
    st_en = ["door", "enter", "exit", "locked", "privacy"],
    pst_en = [
        "Close the door behind you", "Install a new door",
        "Enter the building through the door", "Hold the door open",
        "Exit through the back door", "Use the emergency exit",
        "Check if the door is locked", "Lock the door before leaving",
        "Keep the door closed for privacy", "Respect the closed door",
    ],
    reg_en = [
        "Lock the front door before leaving",
        "Close the office door for a meeting",
        "Install a new door lock",
        "Replace the worn door handle",
        "Check that the door is locked",
        "Keep the bedroom door closed",
        "Use the back door to exit",
        "Install a smart door lock",
        "Knock before entering the closed door",
        "Keep the door shut to save heat",
    ],
    conv_en = [
        "Lock the door",
        "Close the door",
        "Door's closed",
        "Privacy please",
    ],
    typo_en = [
        "lok the front dorr",
        "clsoe the door behnd you",
        "chek if door is lokced",
        "instal a new door lok",
    ],
    bnd_en = [
        "Open the door to let guests in",
        "Leave the door ajar",
        "Open the window for fresh air",
        "Install a window lock",
        "Use the revolving door at the office",
        "Unlock the gate to the yard",
    ],
    valid_en = [
        "Lock the front door",
        "Close the office door for privacy",
        "Check that the door is locked",
    ],
    test_en = [
        "Install a new door lock",
        "Keep the door closed during the meeting",
        "Use the back door to exit",
    ],
)

# ============================================================
# 149. dove
# ============================================================
process_icon(
    "dove",
    st_en = ["bird", "dove", "fauna", "fly", "flying", "peace", "war"],
    pst_en = [
        "Watch a bird soar overhead", "Spot a bird in the garden",
        "Release a dove at the ceremony", "See a dove perched on the branch",
        "Observe local fauna", "Photograph fauna in the park",
        "Watch the bird fly away", "See a bird fly across the sky",
        "Watch the dove flying", "Flying dove at the wedding",
        "Promote peace in the community", "Send a peace message",
        "Pray for peace in times of war", "Oppose war and support peace",
    ],
    reg_en = [
        "Release doves at the wedding",
        "Watch doves in the park",
        "Feed doves in the garden",
        "Use a dove as a peace symbol",
        "Photograph a dove in the wild",
        "Watch doves nest on the balcony",
        "Draw a dove as a peace symbol",
        "Send a peace message with a dove",
        "See doves at the church",
        "Observe doves flying at sunset",
    ],
    conv_en = [
        "Peace out",
        "Release the doves",
        "White dove",
        "Symbol of peace",
    ],
    typo_en = [
        "relese doves at wedidng",
        "wach doves in the aprk",
        "doove as peace symbl",
        "fotografph a dove",
    ],
    bnd_en = [
        "Spot a crow on the rooftop",
        "See an eagle soar overhead",
        "Watch a pigeon in the city",
        "Feed sparrows in the park",
        "Observe a hawk hunting",
        "See a flamingo at the zoo",
    ],
    valid_en = [
        "Release doves at the wedding",
        "Watch doves in the garden",
        "Use a dove as a peace symbol",
    ],
    test_en = [
        "See doves flying at sunset",
        "Feed doves in the park",
        "Draw a peace dove",
    ],
)

print("\nAll 30 icons processed successfully!")
