#!/usr/bin/env python3
"""Generate English training data for icons 379-391."""
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

# 379 — jeans (e6d2)
process_icon("jeans",
    st_en=["denim", "dungaree", "jean", "legs", "pants", "pockets"],
    pst_en=[
        "blue denim jeans with a worn wash", "denim fabric used in classic jeans",
        "dungaree overalls with a denim bib", "striped dungaree for kids",
        "a pair of jean trousers on a mannequin", "slim fit jean in a dark indigo wash",
        "jeans covering both legs to the ankle", "straight leg jeans with a simple cut",
        "casual pants made from denim fabric", "denim pants folded on a store shelf",
        "jeans with five pockets in a classic cut", "front pockets on a pair of blue jeans",
    ],
    reg_en=[
        "blue denim jeans with a button fly",
        "pick out a pair of jeans for a casual outing",
        "clothing icon for a fashion or wardrobe app",
        "slim fit jeans with a faded wash",
        "roll up the cuffs of your jeans for summer",
        "bottoms category icon in an e-commerce store",
        "classic five-pocket denim jeans",
        "jeans and a t-shirt for a relaxed everyday look",
        "wardrobe icon for a personal styling app",
        "dark indigo straight leg jeans on a hanger",
    ],
    conv_en=[
        "I need a jeans icon for my wardrobe tracker app",
        "add a jeans symbol to the clothing category",
        "show jeans for the casual wear section",
        "use the jeans icon for the outfit planner feature",
    ],
    typo_en=[
        "jenas washed and folded",
        "jeasn hanging on a hook",
        "jeanz with a worn look",
        "jaens in a slim fit",
    ],
    bnd_en=[
        "denim cutoff shorts frayed above the knee",
        "athletic shorts with a drawstring waist",
        "chino pants in a khaki color",
        "fitted dress pants with a crease down the front",
        "floral print summer skirt below the knee",
        "pleated midi skirt paired with a blouse",
    ],
    valid_en=[
        "blue denim jeans on a hanger",
        "jeans icon for a clothing app",
        "classic five-pocket jeans",
    ],
    test_en=[
        "slim fit jeans in a dark wash",
        "jeans for a wardrobe tracker",
        "denim jeans folded on a shelf",
    ],
)

# 380 — lemon (f094)
process_icon("lemon",
    st_en=["citrus", "fruit", "lemon", "lemonade", "lime", "tart"],
    pst_en=[
        "citrus fruit with a bright yellow skin", "citrus scent used in cleaning products",
        "fruit bowl with lemons and oranges", "fresh fruit icon for a grocery app",
        "sliced lemon in a glass of water", "squeeze a lemon over the fish",
        "fresh lemonade with ice and mint", "homemade lemonade for a summer day",
        "lemon and lime sliced on a cutting board", "lime and lemon in a citrus cocktail",
        "sharp tart flavor of freshly squeezed lemon", "lemon tart pastry from the bakery",
    ],
    reg_en=[
        "bright yellow oval lemon with a pointed tip",
        "squeeze lemon juice over a grilled fish fillet",
        "food icon for a recipe or grocery app",
        "lemon sliced in half showing the juicy segments",
        "make fresh lemonade on a hot summer afternoon",
        "citrus icon in a nutrition or smoothie app",
        "shiny yellow lemon with a leafy stem attached",
        "lemon zest grated over a pasta dish",
        "ingredient icon for a cocktail or beverage app",
        "glossy lemon sitting on a white marble surface",
    ],
    conv_en=[
        "I need a lemon icon for my recipe tracker app",
        "add a lemon symbol to the citrus fruits section",
        "show a lemon for the fresh produce category",
        "use the lemon icon for the cocktail ingredient feature",
    ],
    typo_en=[
        "lemno juice for the dressing",
        "lemom squeezed on the salad",
        "lmeon in a glass of water",
        "lemon juicce freshly squeezed",
    ],
    bnd_en=[
        "small round lime with a green bumpy skin",
        "wedge of lime garnishing a margarita glass",
        "round orange with a dimpled skin",
        "orange cut in half showing the juicy segments",
        "large pink grapefruit sliced in half",
        "grapefruit half with a spoon for scooping",
    ],
    valid_en=[
        "bright yellow lemon with a pointed tip",
        "fresh lemon for a recipe app",
        "lemon citrus fruit icon",
    ],
    test_en=[
        "sliced lemon in a glass",
        "lemon for lemonade",
        "lemon icon in a food app",
    ],
)

# 381 — lobster (e421)
process_icon("lobster",
    st_en=["bisque", "crustacean", "lobster", "seafood", "shellfish"],
    pst_en=[
        "lobster bisque served in a warm bowl", "rich bisque made from lobster shells",
        "large crustacean from the cold Atlantic waters", "crustacean with two large front claws",
        "red boiled lobster on a seafood platter", "fresh lobster caught off the Maine coast",
        "seafood restaurant icon with a lobster", "seafood platter with lobster and shrimp",
        "shellfish allergy warning on a menu", "shellfish section in a seafood market",
    ],
    reg_en=[
        "red lobster with large claws and a segmented tail",
        "cracking open a fresh lobster at a seafood dinner",
        "seafood icon for a restaurant or food delivery app",
        "boiled lobster with bright red shell on a white plate",
        "order lobster for a special occasion dinner",
        "premium seafood category in a menu or recipe app",
        "lobster with long antennae and five pairs of legs",
        "lobster dipped in melted butter with lemon",
        "marine creature icon for an ocean-themed app",
        "side view of a lobster with claws extended",
    ],
    conv_en=[
        "I need a lobster icon for my seafood restaurant app",
        "add a lobster symbol to the seafood menu section",
        "show a lobster for the premium dining category",
        "use the lobster icon for the ocean food feature",
    ],
    typo_en=[
        "lobstre with large front claws",
        "lobsetr on a seafood platter",
        "lobster bisqeu soup",
        "lboster from Maine",
    ],
    bnd_en=[
        "red crab with wide claws on a beach",
        "crab claw cracking open at a seafood restaurant",
        "pink shrimp curled on a plate of cocktail sauce",
        "grilled shrimp skewer at a barbecue",
        "octopus with eight tentacles floating in water",
        "grilled octopus tentacle on a Mediterranean plate",
    ],
    valid_en=[
        "red lobster with large claws",
        "lobster for a seafood restaurant app",
        "boiled lobster on a platter",
    ],
    test_en=[
        "fresh lobster from the ocean",
        "lobster on a seafood menu",
        "lobster icon for a dining app",
    ],
)

# 382 — mug (f874)
process_icon("mug",
    st_en=["coffee", "cup", "drink", "hot chocolate", "tea"],
    pst_en=[
        "morning coffee in a ceramic mug", "coffee mug on a wooden desk",
        "large cup for hot beverages", "cup of tea steaming on the table",
        "hot drink to start the morning", "warm drink icon in a café app",
        "hot chocolate with marshmallows in a mug", "rich hot chocolate on a cold winter night",
        "herbal tea in a tall ceramic mug", "tea with honey in a cozy mug",
    ],
    reg_en=[
        "ceramic mug with steam rising from the top",
        "grab a mug of coffee before the morning meeting",
        "beverage icon for a café or coffee shop app",
        "large round mug with a curved handle",
        "fill the mug with hot tea and a slice of lemon",
        "hot drinks category icon in a menu app",
        "branded mug sitting on an office desk",
        "sip a mug of hot chocolate after playing in the snow",
        "café ordering icon in a beverage delivery app",
        "mug with a cozy knitted sleeve for winter drinks",
    ],
    conv_en=[
        "I need a mug icon for my coffee tracker app",
        "add a mug symbol to the hot drinks section",
        "show a mug for the café order feature",
        "use the mug icon for the morning routine category",
    ],
    typo_en=[
        "mgu of hot coffee in the morning",
        "mug fo hot tea",
        "mugg on the office desk",
        "mug cofefe in the morning",
    ],
    bnd_en=[
        "tall glass of iced coffee with a straw",
        "clear glass cup filled with lemonade and ice",
        "ceramic teapot with a bamboo handle",
        "round teapot with a whistling spout on the stove",
        "stainless steel thermos keeping coffee warm",
        "travel tumbler with a lid for commuting",
    ],
    valid_en=[
        "ceramic mug with steam on top",
        "mug for a coffee or tea app",
        "hot drink mug icon",
    ],
    test_en=[
        "coffee mug on a wooden desk",
        "mug of hot tea with honey",
        "mug in a café ordering app",
    ],
)

# 383 — music (f001)
process_icon("music",
    st_en=["lyrics", "melody", "music", "musical note", "note", "sing", "sound"],
    pst_en=[
        "song lyrics displayed in a music player", "lyrics scroll as the song plays",
        "hum a catchy melody stuck in your head", "melody recognized by a music identification app",
        "music streaming from a phone speaker", "background music playing during a workout",
        "musical note icon for a song or audio app", "musical note symbol on a sheet of paper",
        "written note on a musical staff", "eighth note floating above the music player",
        "sing along to your favorite song", "sing icon for a karaoke feature",
        "rich sound coming from the music player", "sound wave icon in an audio app",
    ],
    reg_en=[
        "single eighth note or a pair of beamed notes",
        "play a song in a music streaming app",
        "audio icon for a music player or playlist",
        "black musical note floating on a white background",
        "tap the music note to browse songs by genre",
        "music library icon in a media or streaming app",
        "beamed pair of eighth notes on a music staff",
        "background music setting in a game or app",
        "sound and media icon in a phone settings menu",
        "musical note symbol representing any audio content",
    ],
    conv_en=[
        "I need a music note icon for my playlist app",
        "add a music symbol to the audio player section",
        "show a music note for the sound settings feature",
        "use the music icon for the media library screen",
    ],
    typo_en=[
        "muisc playing in the background",
        "msuic streaming app",
        "musci note icon",
        "musik player on the phone",
    ],
    bnd_en=[
        "microphone on a boom stand for recording vocals",
        "handheld microphone at a karaoke night",
        "over-ear headphones resting on a desk",
        "wireless earbuds in a white charging case",
        "loudspeaker volume icon with sound waves",
        "phone volume slider in audio settings",
    ],
    valid_en=[
        "musical note icon",
        "music symbol for a playlist app",
        "eighth note floating above a staff",
    ],
    test_en=[
        "music icon in a streaming app",
        "tap the music note to play a song",
        "music note symbol for audio content",
    ],
)

# 384 — mustache (e5bc)
process_icon("mustache",
    st_en=["beard", "face", "hair", "lumberjack", "shave", "walrus", "whiskers"],
    pst_en=[
        "thick beard and mustache combo", "beard icon for a barber or grooming app",
        "face with a handlebar mustache", "face hair icon in a character customization screen",
        "facial hair styled into a twirled mustache", "hair icon for a barber shop menu",
        "bushy lumberjack mustache with a beard", "lumberjack style facial hair",
        "shave off the mustache for a new look", "shave styling kit for mustache grooming",
        "walrus-style drooping mustache", "thick walrus mustache hanging over the lip",
        "long whiskers of a twirled mustache", "waxed whiskers curling at the ends",
    ],
    reg_en=[
        "curly handlebar mustache on a white background",
        "grow a mustache for Movember awareness",
        "barber shop icon for a grooming or hairstyle app",
        "thick dark mustache sitting above the upper lip",
        "style a mustache with wax for a sharp curl",
        "facial hair category in a character creator app",
        "classic pencil-thin mustache in a silhouette",
        "mustache disguise prop for a photo booth app",
        "men's grooming icon for a shaving products app",
        "bushy full mustache covering the upper lip",
    ],
    conv_en=[
        "I need a mustache icon for my barber app",
        "add a mustache symbol to the facial hair section",
        "show a mustache for the grooming category",
        "use the mustache icon for the character customization feature",
    ],
    typo_en=[
        "mustahce waxed for a curl",
        "mustace grooming kit",
        "moustahce style for Movember",
        "mustche trimmed neatly",
    ],
    bnd_en=[
        "full thick beard covering the jaw and chin",
        "neatly trimmed short beard on a man's face",
        "red lips in a kissing expression",
        "lipstick mark on a cheek as a kiss",
        "curly wig icon for a costume or disguise",
        "top hat and monocle for a fancy disguise",
    ],
    valid_en=[
        "handlebar mustache icon",
        "mustache for a grooming app",
        "curly mustache above the lip",
    ],
    test_en=[
        "twirled mustache on a white background",
        "mustache icon for a barber app",
        "thick mustache for Movember",
    ],
)

# 385 — nose (e5bd)
process_icon("nose",
    st_en=["face", "nasal", "nostril", "smell", "sniff", "snout"],
    pst_en=[
        "nose in the center of the face", "face icon highlighting the nose feature",
        "nasal passage blocked during a cold", "nasal spray for allergy relief",
        "nostril flare when smelling something strong", "twin nostril openings in a nose icon",
        "smell the freshly baked bread", "ability to smell diminished during illness",
        "sniff the wine to detect the aroma", "dog sniff behavior icon for a pet app",
        "cartoon snout for an animal character", "pig snout design in a children's app",
    ],
    reg_en=[
        "simple outline of a human nose from the side",
        "nose icon for a health symptom tracker",
        "body part icon in a medical or anatomy app",
        "front-facing nose with rounded nostrils",
        "track nasal congestion in a cold symptom log",
        "face anatomy icon in a healthcare app",
        "rounded nose shape with a slight bump on the bridge",
        "nose sensitivity icon for an allergy tracking app",
        "sense of smell icon in a food or fragrance app",
        "cartoon nose icon in a facial expression set",
    ],
    conv_en=[
        "I need a nose icon for my symptom tracker app",
        "add a nose symbol to the face anatomy section",
        "show a nose for the allergy and cold tracker",
        "use the nose icon for the sense of smell feature",
    ],
    typo_en=[
        "noes running after coming in from the cold",
        "noze sensitivity to strong smells",
        "nosse blocked from the cold",
        "sniff with your noe",
    ],
    bnd_en=[
        "open mouth with visible teeth and tongue",
        "simple mouth or lips outline for a face icon",
        "ear with a curved outer shell and canal",
        "hearing ear symbol for an audio or accessibility app",
        "round eye with a colored iris and dark pupil",
        "eye outline for a visibility or view icon",
    ],
    valid_en=[
        "nose icon for a face or anatomy app",
        "human nose with two nostrils",
        "nose symbol for a smell tracker",
    ],
    test_en=[
        "nose in a health symptom app",
        "nasal icon for allergy tracking",
        "cartoon nose for a face emoji",
    ],
)

# 386 — pear (e20c)
process_icon("pear",
    st_en=["fruit", "pear"],
    pst_en=[
        "sweet pear fruit in a fruit bowl", "fresh fruit icon for a recipe app",
        "ripe green or yellow pear on a table", "juicy pear ready to eat",
    ],
    reg_en=[
        "rounded pear shape narrowing toward the stem",
        "bite into a ripe pear for a sweet snack",
        "fruit icon for a grocery or recipe app",
        "yellow-green pear with a curved stem on top",
        "poached pear in a red wine sauce for dessert",
        "fresh produce icon in a meal planning app",
        "smooth teardrop-shaped pear with a small leaf",
        "slice a pear into wedges for a cheese board",
        "healthy snack icon for a nutrition tracker",
        "glossy pear on a white background",
    ],
    conv_en=[
        "I need a pear icon for my fruit tracker app",
        "add a pear symbol to the fresh produce section",
        "show a pear for the healthy snacks category",
        "use the pear icon for the fruit and vegetables feature",
    ],
    typo_en=[
        "paer with a sweet juicy bite",
        "pear wiht a leafy stem",
        "pear fuit for a healthy snack",
        "prear from the orchard",
    ],
    bnd_en=[
        "red apple with a leaf and stem",
        "green apple sliced on a cutting board",
        "halved avocado showing the large pit inside",
        "ripe avocado with dark bumpy skin",
        "dried fig cut in half showing the pink seeds",
        "fresh fig with a purple skin and honey drizzle",
    ],
    valid_en=[
        "ripe pear with a curved stem",
        "pear icon for a fruit app",
        "yellow pear fruit",
    ],
    test_en=[
        "fresh pear from the orchard",
        "pear in a grocery app",
        "juicy pear as a healthy snack",
    ],
)

# 387 — pepper (e432)
process_icon("pepper",
    st_en=["bell pepper", "capsicum"],
    pst_en=[
        "red bell pepper sliced for a salad", "stuffed bell pepper baked in the oven",
        "capsicum used in a stir fry dish", "capsicum pepper in a grocery list",
    ],
    reg_en=[
        "bright red bell pepper with a green stem on top",
        "slice bell peppers for a stir fry or salad",
        "vegetable icon for a recipe or grocery app",
        "green yellow and red peppers arranged together",
        "roast whole bell peppers in the oven until charred",
        "ingredient icon for a Mexican or Italian recipe",
        "glossy bell pepper with a dimpled base",
        "stuff a bell pepper with rice and ground meat",
        "fresh produce icon in a meal planning app",
        "bell pepper with four lobes on the bottom",
    ],
    conv_en=[
        "I need a pepper icon for my recipe app",
        "add a pepper symbol to the vegetable section",
        "show a bell pepper for the fresh produce category",
        "use the pepper icon for the cooking ingredients feature",
    ],
    typo_en=[
        "peppr sliced for the stir fry",
        "pepepr chopped for the salad",
        "peper stuffed with rice and meat",
        "peppper roasted in the oven",
    ],
    bnd_en=[
        "thin red chili pepper with a fiery pointed tip",
        "dried chili pepper used as a spicy seasoning",
        "round red tomato with a bright green stem",
        "cherry tomatoes on a vine in a garden",
        "purple eggplant with a long green stem",
        "eggplant sliced and grilled on a hot skillet",
    ],
    valid_en=[
        "red bell pepper with a green stem",
        "bell pepper for a recipe app",
        "colorful capsicum vegetable icon",
    ],
    test_en=[
        "bell pepper sliced for cooking",
        "pepper in a grocery app",
        "stuffed bell pepper for a recipe",
    ],
)

# 388 — pumpkin (f707)
process_icon("pumpkin",
    st_en=["autumn", "gourd", "halloween", "harvest", "squash", "thanksgiving", "vegetable"],
    pst_en=[
        "round orange pumpkin in an autumn display", "autumn harvest icon with pumpkin and leaves",
        "large orange gourd on a wooden porch", "decorative gourd used for fall centerpieces",
        "carved halloween pumpkin with a glowing face", "jack-o-lantern pumpkin at the front door",
        "pumpkin harvest at a fall farm", "harvest festival pumpkin picking event",
        "pumpkin squash grown in a garden patch", "winter squash variety with a thick orange skin",
        "pumpkin centerpiece on a Thanksgiving table", "pumpkin pie served at Thanksgiving dinner",
        "pumpkin as a winter vegetable in soups", "vegetable icon including pumpkin in fall cooking",
    ],
    reg_en=[
        "round orange pumpkin with a ribbed surface",
        "carve a pumpkin for Halloween night",
        "autumn icon for a seasonal or holiday app",
        "pumpkin with a thick brown curved stem on top",
        "bake a pumpkin pie from scratch for Thanksgiving",
        "Halloween decoration icon for an event planning app",
        "small to medium orange pumpkin on a porch step",
        "pick a pumpkin at the local pumpkin patch",
        "fall season icon for a harvest or farming app",
        "jack-o-lantern pumpkin with a carved smiling face",
    ],
    conv_en=[
        "I need a pumpkin icon for my Halloween app",
        "add a pumpkin symbol to the autumn season section",
        "show a pumpkin for the harvest festival feature",
        "use the pumpkin icon for the Thanksgiving category",
    ],
    typo_en=[
        "pumpikn carving for Halloween",
        "pumkin picked at the farm",
        "pumpkon on the porch step",
        "pumpkin piee at Thanksgiving",
    ],
    bnd_en=[
        "yellow butternut squash with a long curved neck",
        "acorn squash with a dark green ridged surface",
        "corn cob with yellow kernels and green husk",
        "dried corn hanging on a fall decoration wreath",
        "scarecrow in a field dressed in old clothes",
        "straw-stuffed scarecrow in a vegetable garden",
    ],
    valid_en=[
        "round orange pumpkin with a ribbed surface",
        "pumpkin icon for a Halloween app",
        "carved pumpkin jack-o-lantern",
    ],
    test_en=[
        "pumpkin at the fall harvest",
        "carved Halloween pumpkin",
        "pumpkin pie for Thanksgiving",
    ],
)

# 389 — sailboat (e445)
process_icon("sailboat",
    st_en=["dinghy", "mast", "sailboat", "sailing", "yacht"],
    pst_en=[
        "small dinghy with a single white sail", "sailing dinghy on a calm lake",
        "tall mast with a billowing sail in the wind", "mast snapped during a storm at sea",
        "sailboat gliding across a blue ocean", "classic sailboat with a white triangular sail",
        "sailing on the open sea on a summer day", "sailing trip across the harbor",
        "luxury yacht with multiple sails hoisted", "sleek racing yacht in a regatta",
    ],
    reg_en=[
        "white triangular sail on a small sailboat",
        "sailing across the harbor on a sunny afternoon",
        "transport icon for a sailing or nautical app",
        "sailboat hull cutting through calm blue waves",
        "take a sailboat out for the weekend on the bay",
        "travel icon for a coastal or marina booking app",
        "single-mast sailboat viewed from the side",
        "learn to sail on a small dinghy in the harbor",
        "recreation icon for an outdoor water sports app",
        "sailboat with a colorful spinnaker sail deployed",
    ],
    conv_en=[
        "I need a sailboat icon for my marina booking app",
        "add a sailboat symbol to the water sports section",
        "show a sailboat for the sailing trips feature",
        "use the sailboat icon for the nautical activities category",
    ],
    typo_en=[
        "sailbota crossing the bay",
        "slaiboat on a calm lake",
        "sailboatt with a white sail",
        "sailbat in the harbor",
    ],
    bnd_en=[
        "speedboat racing across the water with a wake",
        "motor boat pulling a water skier",
        "large cruise ship on the open ocean",
        "cargo ship loaded with shipping containers",
        "narrow canoe paddled across a calm river",
        "two people kayaking on a lake",
    ],
    valid_en=[
        "white sailboat on the open water",
        "sailboat icon for a marina app",
        "sailing trip on a sunny day",
    ],
    test_en=[
        "sailboat crossing the bay",
        "dinghy with a white triangular sail",
        "sailboat in a water sports app",
    ],
)

# 390 — scarf (f7c1)
process_icon("scarf",
    st_en=["clothing", "knitted", "neck", "scarf", "seasonal", "warmth"],
    pst_en=[
        "winter clothing including a warm scarf", "clothing icon for cold weather accessories",
        "knitted scarf in a chunky wool pattern", "hand-knitted scarf as a holiday gift",
        "scarf wrapped around the neck for warmth", "neck warmer wrapped tightly on a cold day",
        "woolen scarf in a striped pattern", "scarf tied loosely around the collar",
        "seasonal accessory for cold winter months", "seasonal winter icon for a weather app",
        "wrap a scarf for warmth in the cold", "warmth and comfort of a thick wool scarf",
    ],
    reg_en=[
        "long striped scarf wrapped around a neck",
        "tie a scarf before heading out into the cold",
        "winter clothing icon in a fashion or wardrobe app",
        "chunky knit scarf with fringe at the ends",
        "scarf as a cozy accessory for a winter outfit",
        "seasonal accessory icon in a cold weather app",
        "brightly colored wool scarf looped once around",
        "add a scarf to the laundry or packing list",
        "clothing category icon for cold weather accessories",
        "plaid scarf neatly folded on a store shelf",
    ],
    conv_en=[
        "I need a scarf icon for my wardrobe tracker app",
        "add a scarf symbol to the winter accessories section",
        "show a scarf for the cold weather clothing category",
        "use the scarf icon for the seasonal fashion feature",
    ],
    typo_en=[
        "scraf tied around the neck",
        "scaarf for a cold winter day",
        "scafr wrapping around the collar",
        "scarft with a fringe at the end",
    ],
    bnd_en=[
        "woolly beanie hat pulled down over the ears",
        "winter knit hat with a pom pom on top",
        "pair of leather gloves for cold weather",
        "knitted mittens hanging from a clothesline",
        "long wool coat with large buttons",
        "warm parka jacket zipped up to the chin",
    ],
    valid_en=[
        "knitted scarf wrapped around the neck",
        "scarf icon for a winter wardrobe app",
        "striped wool scarf for cold weather",
    ],
    test_en=[
        "scarf tied before going out in the cold",
        "chunky knit scarf on a hanger",
        "scarf in a fashion or clothing app",
    ],
)

# 391 — scooter (e7c3)
process_icon("scooter",
    st_en=["scooter", "wheels"],
    pst_en=[
        "electric scooter parked on the sidewalk", "ride a scooter to work in the city",
        "scooter wheels rolling on the pavement", "small wheels on a kick scooter",
    ],
    reg_en=[
        "electric kick scooter with two small wheels",
        "rent a shared scooter for a quick city ride",
        "micro-mobility icon for a transport or city app",
        "folded kick scooter leaned against a wall",
        "commute across town on a shared e-scooter",
        "electric vehicle icon for a ride-sharing app",
        "standing rider on a scooter in a busy street",
        "lock the e-scooter at the station after your ride",
        "green transport icon for an eco-friendly commuting app",
        "motorized scooter with a digital display panel",
    ],
    conv_en=[
        "I need a scooter icon for my ride-sharing app",
        "add a scooter symbol to the transport section",
        "show a scooter for the city mobility feature",
        "use the scooter icon for the micro-mobility category",
    ],
    typo_en=[
        "scootre parked on the sidewalk",
        "scootr left at the station",
        "scoooter on the pavement",
        "scooer on the bike lane",
    ],
    bnd_en=[
        "bicycle with two equal wheels and handlebars",
        "person riding a bicycle in a bike lane",
        "motorcycle parked on a city street",
        "sports motorcycle leaning in a curve",
        "skateboard with four wheels and grip tape",
        "person riding a skateboard at a skate park",
    ],
    valid_en=[
        "electric kick scooter on the pavement",
        "scooter for a city mobility app",
        "shared e-scooter for commuting",
    ],
    test_en=[
        "scooter parked at the station",
        "ride a scooter across town",
        "scooter icon in a transport app",
    ],
)
