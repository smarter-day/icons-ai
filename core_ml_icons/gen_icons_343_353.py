#!/usr/bin/env python3
"""Generate English training data for icons 343-353."""
from pathlib import Path
import csv, json

icons_dir = Path("icons_data")
icons_dir.mkdir(exist_ok=True)

def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        w.writerows(rows)

def process_icon(icon, st_en, pst_en, reg_en, conv_en, typo_en, bnd_en, valid_en, test_en):
    icon_dir = icons_dir / icon
    icon_dir.mkdir(parents=True, exist_ok=True)
    train_en = [(t, icon) for t in st_en + pst_en + reg_en + conv_en + typo_en + bnd_en]
    write_csv(icon_dir / "train_en.csv", train_en)
    write_csv(icon_dir / "valid_en.csv", [(t, icon) for t in valid_en])
    write_csv(icon_dir / "test_en.csv",  [(t, icon) for t in test_en])
    log = {
        "icon": icon, "search_terms": st_en, "phrase_per_search_term": pst_en,
        "regular": reg_en, "conversational": conv_en, "typo": typo_en,
        "boundary": bnd_en, "valid": valid_en, "test": test_en,
    }
    with open(icon_dir / "icon_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    n_st = len(st_en); n_pst = len(pst_en)
    print(f"  {icon}: {len(train_en)} train rows  ({n_st} st + {n_pst} pst + 24)")

# 343 — avocado (e0aa)
process_icon("avocado",
    st_en=["avocado", "food", "fruit", "green", "guacamole", "hass", "pit"],
    pst_en=[
        "ripe avocado cut in half", "avocado toast with sea salt",
        "healthy food for meal prep", "food icon for a nutrition tracker",
        "tropical fruit with a creamy texture", "fruit salad with avocado slices",
        "deep green skin of a ripe avocado", "green vegetable with rich flavor",
        "fresh guacamole made from scratch", "guacamole dip served with chips",
        "california hass avocado in season", "hass variety with dark pebbly skin",
        "large round pit in the center", "removing the pit from an avocado",
    ],
    reg_en=[
        "halved avocado showing the large seed inside",
        "creamy green fruit used in salads and sandwiches",
        "avocado icon for a health and nutrition app",
        "ripe avocado with bumpy dark green skin",
        "spread avocado on toast for a healthy breakfast",
        "symbol for a vegan-friendly restaurant menu",
        "cross-section of an avocado revealing pale green flesh",
        "avocado as a source of healthy fats in diet tracking",
        "fresh avocado sliced on a wooden cutting board",
        "tropical fruit grown in warm sunny climates",
    ],
    conv_en=[
        "I need an avocado icon for my healthy eating app",
        "add an avocado symbol to the recipe section",
        "show an avocado for the vegan food category",
        "use the avocado icon for the smoothie bowl feature",
    ],
    typo_en=[
        "avacado toast recipe",
        "avocdo with sea salt",
        "avocafo spread on bread",
        "avocadoo sliced in half",
    ],
    bnd_en=[
        "bright yellow lemon cut in half showing the pulp",
        "fresh lemon wedge for a citrus drink",
        "round green lime on a kitchen counter",
        "lime slice garnishing a cocktail glass",
        "red apple with a green leaf on top",
        "whole apple fruit sitting on a wooden surface",
    ],
    valid_en=[
        "ripe avocado cut open showing the pit",
        "avocado for a healthy meal tracker",
        "creamy green avocado fruit",
    ],
    test_en=[
        "avocado sliced in half on a plate",
        "fresh avocado for guacamole",
        "avocado icon in a nutrition app",
    ],
)

# 344 — broccoli (e3e2)
process_icon("broccoli",
    st_en=["bush", "cauliflower", "tree", "wild cabbage"],
    pst_en=[
        "dense green bush-shaped vegetable", "broccoli head looks like a miniature bush",
        "cauliflower and broccoli are both brassicas", "roasted cauliflower on a baking sheet",
        "broccoli floret resembling a tiny tree", "tiny tree vegetable kids love to avoid",
        "wild cabbage grown into a cultivated vegetable", "brassica descended from wild cabbage",
    ],
    reg_en=[
        "dark green broccoli floret with a thick stalk",
        "steamed broccoli for a healthy side dish",
        "broccoli icon for a vegetable or grocery app",
        "tree-shaped green vegetable packed with vitamins",
        "roasting broccoli with olive oil and garlic",
        "broccoli as part of a balanced diet tracker",
        "tightly packed green florets on a white background",
        "fresh broccoli from the farmer's market",
        "vegetable icon for a meal planning dashboard",
        "crunchy raw broccoli florets in a salad bowl",
    ],
    conv_en=[
        "I need a broccoli icon for my veggie tracking app",
        "add a broccoli symbol to the healthy food category",
        "show a broccoli for the vegetables section",
        "use the broccoli icon for the garden meal planner",
    ],
    typo_en=[
        "brocoli florets with garlic",
        "brocolli stir fry",
        "broccili with cheese sauce",
        "brococli crowns",
    ],
    bnd_en=[
        "white cauliflower head surrounded by green leaves",
        "roasted cauliflower in a baking dish",
        "round green cabbage head cut in half",
        "fresh cabbage leaves for coleslaw",
        "leafy green kale in a salad bowl",
        "bundle of kale stems at a grocery store",
    ],
    valid_en=[
        "green broccoli floret on a plate",
        "fresh broccoli for a healthy dinner",
        "broccoli vegetable icon",
    ],
    test_en=[
        "broccoli stalk and florets",
        "steamed broccoli with seasoning",
        "broccoli in a meal planning app",
    ],
)

# 345 — capsules (f46b)
process_icon("capsules",
    st_en=["drugs", "medicine", "pills", "prescription"],
    pst_en=[
        "prescription drugs in a pharmacy bag", "controlled drugs tracked in a medication app",
        "daily medicine reminder for patients", "over the counter medicine in a blister pack",
        "pills scattered on a white surface", "bottle of pills on a nightstand",
        "prescription from a doctor for antibiotics", "fill prescription at the local pharmacy",
    ],
    reg_en=[
        "two-tone gel capsules in a medicine bottle",
        "daily medication capsules for a health tracker",
        "pharmacy icon for medication management",
        "red and blue capsule on a white background",
        "taking capsules with a full glass of water",
        "capsule icon for a drug reminder application",
        "capsules lined up in a pill organizer tray",
        "supplement capsules for vitamins and minerals",
        "medical icon representing drug dosage forms",
        "gelatin capsule containing powdered medication",
    ],
    conv_en=[
        "I need a capsules icon for my medication tracker",
        "add a capsule symbol to the prescriptions screen",
        "show a capsule for the daily medicine section",
        "use the capsules icon for the pharmacy feature",
    ],
    typo_en=[
        "capusles medication reminder",
        "capsuls in a pill bottle",
        "cappules with vitamins",
        "capslues daily dose",
    ],
    bnd_en=[
        "two round white tablets in a blister pack",
        "white circular pill cut in half on a surface",
        "plastic syringe with a metal needle",
        "medical syringe being filled with medication",
        "mortar and pestle grinding herbs for medicine",
        "pharmacy pestle blending compounds in a bowl",
    ],
    valid_en=[
        "gel capsules in a medicine bottle",
        "capsule for a prescription medication",
        "drug capsules in a health app",
    ],
    test_en=[
        "two-tone capsule pill",
        "capsules for daily supplements",
        "medication capsule icon",
    ],
)

# 346 — carrot (f787)
process_icon("carrot",
    st_en=["bugs bunny", "carrot", "food", "orange", "vegan", "vegetable"],
    pst_en=[
        "bugs bunny nibbling on a long carrot", "classic bugs bunny carrot snack",
        "fresh carrot with green leafy tops", "baby carrot snack pack",
        "healthy food for meal prep tracking", "food icon on a nutrition label",
        "bright orange root vegetable in the ground", "orange carrot freshly pulled from the soil",
        "popular vegan snack idea for a plant-based diet", "common vegan ingredient in soups and stews",
        "root vegetable high in beta carotene", "vegetable icon for a grocery list app",
    ],
    reg_en=[
        "long orange carrot with feathery green top",
        "sliced carrots in a warm soup or stew",
        "food icon for a vegan recipe app",
        "whole carrot with a dark green leafy stem",
        "crunchy raw carrot sticks for a healthy snack",
        "vegetable icon in a grocery delivery app",
        "orange root vegetable growing in garden soil",
        "shredded carrot in a salad or carrot cake",
        "nutrition tracker with vitamin A rich vegetables",
        "carrot as a symbol of healthy eating habits",
    ],
    conv_en=[
        "I need a carrot icon for my vegetable tracking app",
        "add a carrot symbol to the healthy snacks section",
        "show a carrot for the garden harvest feature",
        "use the carrot icon for the vegan food category",
    ],
    typo_en=[
        "carot sticks and hummus",
        "carott salad recipe",
        "carort juice freshly squeezed",
        "caarrot soup for winter",
    ],
    bnd_en=[
        "round red radish with a short white tail",
        "fresh radish sliced thinly in a salad",
        "yellow corn cob with green husk",
        "sweet corn grilled on the barbecue",
        "purple turnip on a wooden surface",
        "roasted turnip with herbs and butter",
    ],
    valid_en=[
        "orange carrot with green top",
        "fresh carrot for a healthy meal",
        "carrot vegetable icon",
    ],
    test_en=[
        "carrot stick snack",
        "whole carrot with leafy stem",
        "carrot in a recipe app",
    ],
)

# 347 — donut (e406)
process_icon("donut",
    st_en=["donut", "doughnut", "frosting", "homer simpson", "jimmies", "sprinkles"],
    pst_en=[
        "glazed donut from the bakery", "donut box with a dozen inside",
        "classic doughnut with a hole in the middle", "freshly fried doughnut with powdered sugar",
        "pink frosting drizzled over a donut", "thick chocolate frosting on a ring donut",
        "homer simpson reaching for a pink frosted donut", "homer simpson's favorite glazed donut treat",
        "rainbow jimmies on a glazed donut", "chocolate jimmies sprinkled across the top",
        "colorful sprinkles covering a donut", "donut covered in rainbow sprinkles",
    ],
    reg_en=[
        "round donut with a hole and pink frosting on top",
        "sweet treat icon for a bakery menu",
        "dessert symbol in a food delivery app",
        "glazed donut with colorful rainbow sprinkles",
        "morning coffee and a fresh donut from the shop",
        "bakery icon for a pastry shop website",
        "ring-shaped fried dough with chocolate drizzle",
        "donut for celebrating milestones and birthdays",
        "sweet food icon for a cheat day tracker",
        "cream-filled donut cut in half showing the filling",
    ],
    conv_en=[
        "I need a donut icon for my bakery ordering app",
        "add a donut symbol to the sweet treats section",
        "show a donut for the desserts category",
        "use the donut icon for the cheat meal tracker",
    ],
    typo_en=[
        "dount with sprinkles on top",
        "donnut glazed with chocolate",
        "donat from the bakery",
        "dounut with pink frosting",
    ],
    bnd_en=[
        "round chocolate chip cookie on a plate",
        "freshly baked sugar cookie with white icing",
        "layered birthday cake with candles on top",
        "slice of wedding cake with white frosting",
        "round bagel with sesame seeds on top",
        "toasted bagel with cream cheese spread",
    ],
    valid_en=[
        "glazed donut with colorful sprinkles",
        "donut with pink frosting and a hole",
        "sweet donut for a dessert app",
    ],
    test_en=[
        "ring shaped donut from the bakery",
        "donut covered in sprinkles",
        "donut icon for a food app",
    ],
)

# 348 — message (f27a)
process_icon("message",
    st_en=["answer", "bubble", "chat", "commenting", "conversation", "discussion",
           "feedback", "message", "note", "notification", "sms", "speech", "talk",
           "talking", "texting"],
    pst_en=[
        "waiting for an answer to my question", "quick answer in a chat thread",
        "speech bubble popping up in a chat", "thought bubble floating above a character",
        "chat icon for a messaging app", "live chat support button on a website",
        "commenting on a post in a social feed", "enable commenting on the article",
        "ongoing conversation between two people", "start a conversation with a new contact",
        "group discussion in a team channel", "open discussion thread in a forum",
        "submit feedback about the app experience", "feedback form for user reviews",
        "new message from a friend notification", "send a message to the support team",
        "leave a note for your teammate", "sticky note reminder on the dashboard",
        "notification badge on the chat icon", "push notification for a new message",
        "sms text message from your bank", "receive an sms alert on your phone",
        "speech bubble in a comic strip", "speech icon for a voice-to-text feature",
        "talk to a friend over text", "tap to talk in a walkie-talkie app",
        "two people talking in a chat window", "talking bubble animation in a messenger",
        "texting your friend about the party", "stop texting while driving reminder",
    ],
    reg_en=[
        "rounded chat bubble with a tail pointing down",
        "chat icon for a real-time messaging feature",
        "customer support chat widget for a website",
        "speech bubble with three dots indicating typing",
        "send and receive messages from friends",
        "messaging icon in a social media dashboard",
        "white speech bubble on a green background",
        "new message alert with unread count badge",
        "in-app chat system for team collaboration",
        "conversation bubble icon for a comment section",
    ],
    conv_en=[
        "I need a message icon for my chat application",
        "add a chat bubble symbol to the inbox screen",
        "show a message bubble for the notifications panel",
        "use the message icon for the support chat feature",
    ],
    typo_en=[
        "messge from a friend",
        "mesage notification on my phone",
        "messgae icon for the app",
        "massege bubble in the chat",
    ],
    bnd_en=[
        "email envelope icon in an inbox folder",
        "unopened letter envelope with a red wax seal",
        "phone call icon with a handset silhouette",
        "incoming call notification with a ringing icon",
        "comment bubble with horizontal text lines inside",
        "forum post comment thread with reply arrows",
    ],
    valid_en=[
        "chat message bubble icon",
        "send a message to a contact",
        "messaging feature in an app",
    ],
    test_en=[
        "text message notification",
        "speech bubble for a chat app",
        "message icon with unread badge",
    ],
)

# 349 — moon (f186)
process_icon("moon",
    st_en=["contrast", "crescent", "crescent moon", "dark", "lunar", "moon", "night"],
    pst_en=[
        "high contrast mode toggle icon", "dark light contrast switch in display settings",
        "crescent shape hanging in the night sky", "crescent symbol on a Turkish flag",
        "crescent moon rising over the horizon", "crescent moon phase during a clear night",
        "dark mode switch for the app theme", "dark sky at midnight with stars visible",
        "lunar calendar showing moon phases", "lunar orbit around the earth",
        "full moon glowing in the night sky", "moon phase tracker for astronomy",
        "night mode enabled at sunset automatically", "quiet night with a bright crescent moon",
    ],
    reg_en=[
        "crescent moon silhouette against a dark sky",
        "night mode toggle icon in display settings",
        "moon phase icon for a weather or astronomy app",
        "thin crescent shape curving to the right",
        "tap the moon icon to enable dark theme",
        "lunar symbol used in sleep and wellness apps",
        "pale white moon with craters on the surface",
        "moon icon appearing at nighttime in a schedule",
        "dark mode indicator in mobile app settings",
        "glowing crescent moon floating in a starry sky",
    ],
    conv_en=[
        "I need a moon icon for my sleep tracking app",
        "add a moon symbol to the night mode toggle",
        "show a moon for the dark theme settings section",
        "use the moon icon for the do not disturb feature",
    ],
    typo_en=[
        "moom phase tonight",
        "mooon rising over the hills",
        "cresent moon in the evening",
        "luanr calendar for moon phases",
    ],
    bnd_en=[
        "bright yellow sun with rays radiating outward",
        "sunrise icon for morning routine reminders",
        "five-pointed star glowing in the night sky",
        "gold star badge for achievement or rating",
        "circular ring of light during a solar eclipse",
        "total solar eclipse with the corona visible",
    ],
    valid_en=[
        "crescent moon for a sleep app",
        "moon icon in night mode settings",
        "lunar crescent shape",
    ],
    test_en=[
        "moon rising in the evening sky",
        "moon phase icon for astronomy",
        "dark mode toggle with moon symbol",
    ],
)

# 350 — mountain (f6fc)
process_icon("mountain",
    st_en=["cold", "glacier", "hiking", "hill", "landscape", "mountain", "snow",
           "snow-capped mountain", "travel", "view"],
    pst_en=[
        "cold alpine air on a mountain peak", "cold weather gear for mountain trekking",
        "glacier slowly moving down the valley", "ancient glacier carved the valley below",
        "hiking trail winding up the mountain", "hiking boots on a rocky mountain path",
        "rolling hill in the countryside", "hill climb route for mountain bikers",
        "dramatic mountain landscape at sunrise", "landscape photography of jagged peaks",
        "mountain range stretching across the horizon", "mountain peak covered in white snow",
        "snow covered summit of a tall mountain", "fresh snow falling on mountain slopes",
        "snow-capped mountain visible from the valley", "iconic snow-capped mountain on a clear day",
        "travel adventure to the mountains this summer", "travel icon for a hiking or camping app",
        "panoramic view from the top of the mountain", "breathtaking view of the mountain summit",
    ],
    reg_en=[
        "jagged mountain peak with a snow-capped summit",
        "hiking trail leading up to a mountain summit",
        "outdoor adventure icon for a travel app",
        "triangular mountain silhouette against a blue sky",
        "ski resort on a snow-covered mountain slope",
        "landscape icon for a wallpaper or photography app",
        "rugged rocky mountain rising above the clouds",
        "mountain climbing route for experienced trekkers",
        "terrain elevation icon for a topography app",
        "misty mountain range at dawn with fog below",
    ],
    conv_en=[
        "I need a mountain icon for my hiking tracker app",
        "add a mountain symbol to the outdoor adventures section",
        "show a mountain for the travel destinations feature",
        "use the mountain icon for the nature and landscape category",
    ],
    typo_en=[
        "mountian peak covered in snow",
        "mountan trail for hiking",
        "moutain range in the distance",
        "mountaim summit with a glacier",
    ],
    bnd_en=[
        "erupting volcano with lava flowing down the side",
        "volcano peak with smoke billowing from the top",
        "camping tent pitched on a flat meadow",
        "small dome tent under a starry sky",
        "gently rolling green hills in the countryside",
        "smooth grassy hill without any snow or peaks",
    ],
    valid_en=[
        "snow-capped mountain peak",
        "mountain range for a hiking app",
        "mountain silhouette landscape",
    ],
    test_en=[
        "tall mountain with snow on top",
        "mountain trail for outdoor adventures",
        "mountain icon in a travel app",
    ],
)

# 351 — mushroom (e425)
process_icon("mushroom",
    st_en=["1-up", "fungus", "toadstool"],
    pst_en=[
        "1-up mushroom granting an extra life in the game", "collect the 1-up mushroom for bonus lives",
        "wild fungus growing on a fallen log", "fungus found in damp shaded forest areas",
        "red toadstool with white polka dots", "poisonous toadstool in the forest undergrowth",
    ],
    reg_en=[
        "round mushroom cap on a thick white stem",
        "wild mushroom foraged from the forest floor",
        "ingredient icon for a recipe or cooking app",
        "red mushroom with white spots like in a fairy tale",
        "sautéed mushrooms as a savory side dish topping",
        "nature icon representing fungi in a science app",
        "button mushroom in a grocery shopping list",
        "mushroom growing on the floor of a dense forest",
        "game icon inspired by classic video game power-ups",
        "flat umbrella cap mushroom on a short stalk",
    ],
    conv_en=[
        "I need a mushroom icon for my recipe app",
        "add a mushroom symbol to the foraging guide section",
        "show a mushroom for the forest nature category",
        "use the mushroom icon for the cooking ingredients feature",
    ],
    typo_en=[
        "mushrom growing in the forest",
        "muhsroom cap with white spots",
        "moshroom found in the woods",
        "mushroon on the forest floor",
    ],
    bnd_en=[
        "tall oak tree with a wide canopy of leaves",
        "pine tree with pointed branches in a forest",
        "green maple leaf in autumn colors",
        "fallen autumn leaf on a wooden surface",
        "round acorn with a ridged cap on a branch",
        "acorn dropped from an oak tree in autumn",
    ],
    valid_en=[
        "mushroom with a round cap and white stem",
        "wild mushroom from the forest",
        "mushroom ingredient in a recipe",
    ],
    test_en=[
        "toadstool mushroom in the woods",
        "mushroom cap on a thick stem",
        "mushroom icon for a cooking app",
    ],
)

# 352 — pills (f484)
process_icon("pills",
    st_en=["drugs", "medicine", "prescription", "tablets"],
    pst_en=[
        "prescription drugs dispensed at the pharmacy", "tracking drugs with a medication reminder app",
        "take medicine on time with this reminder", "daily medicine routine for chronic patients",
        "pick up prescription at the local drug store", "doctor prescription for a seven day course",
        "tablets in a blister pack for daily use", "small white tablets taken twice a day",
    ],
    reg_en=[
        "two round tablets on a white surface",
        "daily pill reminder for morning and evening doses",
        "medication icon for a health management app",
        "small white and yellow circular tablets side by side",
        "take your pills with a full glass of water",
        "pharmaceutical icon for a drug reference app",
        "round flat tablet and an oval capsule together",
        "prescription tablets in a weekly pill organizer",
        "health icon representing over the counter medication",
        "two pills resting on an open palm",
    ],
    conv_en=[
        "I need a pills icon for my medication reminder app",
        "add a pills symbol to the daily dose tracker",
        "show pills for the prescription management screen",
        "use the pills icon for the pharmacy section",
    ],
    typo_en=[
        "pils taken twice a day",
        "pillas with a glass of water",
        "piils scattered on the counter",
        "plils for the evening dose",
    ],
    bnd_en=[
        "red and blue gel capsule on a white background",
        "transparent gelatin capsule with powder inside",
        "medical syringe with a needle for injection",
        "disposable plastic syringe being prepared",
        "digital thermometer displaying a temperature reading",
        "glass thermometer with a red mercury line",
    ],
    valid_en=[
        "round white tablets on a surface",
        "pills for a daily medication tracker",
        "prescription pills in a health app",
    ],
    test_en=[
        "two pills side by side",
        "daily pills for medication reminder",
        "pill icon in a pharmacy app",
    ],
)

# 353 — radio (f8d7)
process_icon("radio",
    st_en=["am", "broadcast", "fm", "frequency", "music", "news", "radio",
           "receiver", "transmitter", "tuner", "video"],
    pst_en=[
        "am radio station playing oldies", "am frequency for talk radio programs",
        "live broadcast on a national radio station", "broadcast tower transmitting audio signals",
        "fm radio playing pop music in the car", "tuning into an fm station on the stereo",
        "adjusting the frequency dial on the radio", "frequency band for shortwave radio",
        "listening to music on the radio while driving", "music streaming from a vintage radio receiver",
        "morning news on the AM radio", "breaking news update on the radio broadcast",
        "portable radio on a kitchen counter", "battery powered radio for camping trips",
        "shortwave radio receiver for international signals", "stereo receiver tuned to a local station",
        "radio transmitter tower broadcasting signals", "handheld transmitter for walkie talkie use",
        "car stereo tuner searching for stations", "digital tuner presets for favorite radio channels",
        "video and radio broadcast from the same tower", "video radio combo in a news studio",
    ],
    reg_en=[
        "boxy retro radio with a dial and telescopic antenna",
        "listen to the news on a portable radio",
        "broadcast media icon for a streaming or radio app",
        "vintage radio with rounded corners and a tuning knob",
        "tuning a car radio to the local FM station",
        "radio icon for a podcast or audio streaming platform",
        "compact handheld AM FM radio with telescopic antenna",
        "emergency weather updates on a battery powered radio",
        "shortwave radio icon for a ham radio application",
        "classic tabletop radio with a fabric speaker grille",
    ],
    conv_en=[
        "I need a radio icon for my audio streaming app",
        "add a radio symbol to the music player section",
        "show a radio for the broadcast news feature",
        "use the radio icon for the FM tuner screen",
    ],
    typo_en=[
        "raido tuned to a local station",
        "radioo playing in the kitchen",
        "rdaio broadcast on AM frequency",
        "redio for morning news",
    ],
    bnd_en=[
        "professional microphone on a stand in a podcast studio",
        "condenser microphone for recording audio",
        "large loudspeaker cone projecting sound waves",
        "bluetooth speaker on a desk playing music",
        "tall broadcast antenna tower with signal waves",
        "cellular tower transmitting wireless signals",
    ],
    valid_en=[
        "vintage radio with a dial and speaker",
        "portable AM FM radio receiver",
        "radio icon for a music streaming app",
    ],
    test_en=[
        "classic tabletop radio tuning to a station",
        "radio broadcast icon",
        "FM radio for a car stereo app",
    ],
)
