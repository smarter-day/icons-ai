#!/usr/bin/env python3
"""Generate English training data for icons 392-403."""
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

# 392 — server (f233)
process_icon("server",
    st_en=["computer", "cpu", "database", "hardware", "mysql", "network", "sql"],
    pst_en=[
        "rack-mounted computer server in a data center", "dedicated computer server for web hosting",
        "cpu processing requests from multiple clients", "server cpu running at high utilization",
        "database server storing user records", "query the database hosted on the server",
        "server hardware rack installed in the cabinet", "hardware maintenance on the production server",
        "mysql database running on a server instance", "mysql server for a web application backend",
        "network server handling incoming connections", "network traffic routed through the server",
        "sql server database for enterprise applications", "run sql queries on the hosted server",
    ],
    reg_en=[
        "tall server rack with blinking indicator lights",
        "host a website on a dedicated server",
        "infrastructure icon for a DevOps or cloud app",
        "black server chassis with multiple drive bays",
        "scale the server to handle more traffic",
        "backend icon for a system administration app",
        "row of servers in a climate-controlled data center",
        "monitor server uptime and performance metrics",
        "IT icon for a network management dashboard",
        "stacked server units with glowing status LEDs",
    ],
    conv_en=[
        "I need a server icon for my cloud dashboard app",
        "add a server symbol to the infrastructure section",
        "show a server for the backend services feature",
        "use the server icon for the database management screen",
    ],
    typo_en=[
        "sever rack in the data center",
        "srever crashing during peak traffic",
        "serveer overloaded with requests",
        "serevr hosting the website",
    ],
    bnd_en=[
        "cylindrical database with stacked layers icon",
        "structured database icon for storing records",
        "cloud icon for remote storage or computing",
        "cloud upload symbol for syncing data online",
        "home router with antennas broadcasting wifi",
        "network router with blinking ethernet ports",
    ],
    valid_en=[
        "server rack in a data center",
        "server icon for a cloud app",
        "dedicated server for web hosting",
    ],
    test_en=[
        "server hosting a website",
        "server infrastructure icon",
        "SQL server for a database app",
    ],
)

# 393 — ship (f21a)
process_icon("ship",
    st_en=["boat", "passenger", "sea", "ship", "water"],
    pst_en=[
        "large ocean-going boat with multiple decks", "boat icon for a maritime travel app",
        "passenger ship crossing the Atlantic", "passenger ferry docking at the port",
        "ship sailing across the open sea", "sea voyage on a merchant vessel",
        "cargo ship loaded with containers at the dock", "ship icon for a shipping or logistics app",
        "water vessel navigating through ocean waves", "water route planned for the cargo ship",
    ],
    reg_en=[
        "large ocean vessel with a tall smokestack",
        "cargo ship delivering goods across the ocean",
        "shipping icon for a logistics or freight app",
        "side view of a ship with multiple decks",
        "book a cruise ship voyage across the Mediterranean",
        "maritime transport icon for a port management app",
        "ship hull cutting through blue ocean waves",
        "container ship departing from a busy seaport",
        "naval vessel icon in a geography or travel app",
        "silhouette of a large ship on the horizon",
    ],
    conv_en=[
        "I need a ship icon for my shipping tracker app",
        "add a ship symbol to the maritime transport section",
        "show a ship for the ocean freight feature",
        "use the ship icon for the cruise booking screen",
    ],
    typo_en=[
        "shpi crossing the Atlantic",
        "shiip arriving at the port",
        "shup docking at the harbor",
        "shio on the open sea",
    ],
    bnd_en=[
        "white triangular sail on a small sailboat",
        "sailboat gliding across a calm harbor",
        "car ferry loading vehicles on the lower deck",
        "passenger ferry crossing a river channel",
        "submarine submerging beneath the ocean surface",
        "military submarine with a periscope",
    ],
    valid_en=[
        "large ocean ship on the water",
        "ship icon for a logistics app",
        "cargo ship at the port",
    ],
    test_en=[
        "ship crossing the ocean",
        "container ship for a shipping app",
        "maritime vessel silhouette",
    ],
)

# 394 — shoe (e6d8)
process_icon("shoe",
    st_en=["formal", "laces", "shoe", "sole"],
    pst_en=[
        "formal dress shoe polished to a shine", "formal shoe for a business or wedding outfit",
        "leather shoe with tied laces", "laces knotted at the top of the shoe",
        "single shoe icon for a footwear app", "classic shoe silhouette on a white background",
        "rubber sole on the bottom of the shoe", "worn sole indicating it needs replacement",
    ],
    reg_en=[
        "classic oxford shoe with a rounded toe",
        "shine your shoes before a formal event",
        "footwear icon for a fashion or shoe store app",
        "leather dress shoe with a low heel",
        "pick the right shoes for a job interview",
        "clothing accessory icon in a wardrobe app",
        "side-profile shoe with a structured toe box",
        "shoe fitting at the store before purchase",
        "shoe size and style selector in a shopping app",
        "polished black shoe with a narrow toe cap",
    ],
    conv_en=[
        "I need a shoe icon for my wardrobe tracker app",
        "add a shoe symbol to the footwear category",
        "show a shoe for the formal clothing section",
        "use the shoe icon for the outfit planner feature",
    ],
    typo_en=[
        "sheo laced up and ready to wear",
        "shoee polished for a formal event",
        "suoe with a rubber sole",
        "shoe solee worn down",
    ],
    bnd_en=[
        "white running sneaker with a thick cushioned sole",
        "athletic sneaker with colored accents",
        "tall leather boot with a zipper up the side",
        "ankle boot with a low block heel",
        "flat sandal with straps across the foot",
        "open-toe sandal for a beach or summer outfit",
    ],
    valid_en=[
        "classic leather dress shoe",
        "shoe icon for a footwear app",
        "formal shoe with tied laces",
    ],
    test_en=[
        "polished shoe for a formal event",
        "shoe silhouette in a wardrobe app",
        "dress shoe with a rubber sole",
    ],
)

# 395 — shovel (f713)
process_icon("shovel",
    st_en=["construction", "dig", "equipment", "excavate", "maintenance", "tool", "trench"],
    pst_en=[
        "construction worker using a shovel on site", "construction tool for moving soil and gravel",
        "dig a hole with a pointed shovel", "dig the garden bed before planting",
        "gardening equipment including a shovel and rake", "heavy equipment including a mechanical shovel",
        "excavate a trench for water pipes", "excavate the foundation for a new building",
        "maintenance crew shoveling debris from the road", "routine maintenance with a shovel and wheelbarrow",
        "essential garden tool for digging and moving soil", "tool icon for a home improvement app",
        "dig a trench for a drainage pipe", "trench dug with a long-handled shovel",
    ],
    reg_en=[
        "shovel with a long handle and flat blade",
        "dig a garden bed with a spade shovel",
        "construction tool icon for a work or project app",
        "metal blade shovel stuck in a pile of soil",
        "shovel snow from the driveway after a blizzard",
        "outdoor maintenance icon for a home services app",
        "pointed shovel leaning against a garden wall",
        "scoop dirt into a wheelbarrow with a shovel",
        "landscaping tool icon for a gardening app",
        "round blade garden shovel with a d-grip handle",
    ],
    conv_en=[
        "I need a shovel icon for my home maintenance app",
        "add a shovel symbol to the gardening tools section",
        "show a shovel for the construction category",
        "use the shovel icon for the digging and excavation feature",
    ],
    typo_en=[
        "shovle stuck in the ground",
        "shoevl leaning against the wall",
        "shoval digging the garden bed",
        "shovell for the construction site",
    ],
    bnd_en=[
        "steel pickaxe breaking rocky ground",
        "pickaxe and hammer for mining or construction",
        "garden rake spreading mulch across the bed",
        "metal rake with tines for collecting leaves",
        "garden hoe chopping weeds between rows",
        "long-handled hoe used for tilling the soil",
    ],
    valid_en=[
        "shovel with a long handle and metal blade",
        "shovel icon for a gardening app",
        "digging shovel for construction",
    ],
    test_en=[
        "shovel stuck in a pile of soil",
        "dig with a shovel in the garden",
        "shovel tool icon for a maintenance app",
    ],
)

# 396 — smoking (f48d)
process_icon("smoking",
    st_en=["cancer", "cigarette", "nicotine", "smoking", "tobacco"],
    pst_en=[
        "lung cancer risk associated with smoking", "cancer warning label on a cigarette pack",
        "lit cigarette with smoke rising", "cigarette pack on a wooden table",
        "nicotine patch as a smoking cessation aid", "nicotine dependence tracked in a health app",
        "no smoking sign at the entrance", "smoking icon for a designated smoking area",
        "tobacco smoke filling a room", "tobacco product warning label",
    ],
    reg_en=[
        "cigarette with a lit tip and rising smoke trail",
        "no smoking zone indicator at a public venue",
        "health warning icon for a smoking cessation app",
        "cigarette silhouette with a burning orange tip",
        "track cigarettes smoked in a quit smoking app",
        "tobacco and health icon in a medical reference app",
        "cigarette stub in an ashtray",
        "log your smoking habit to help quit gradually",
        "addiction and wellness icon for a health dashboard",
        "smoking symbol shown on a restricted area sign",
    ],
    conv_en=[
        "I need a smoking icon for my quit smoking tracker",
        "add a smoking symbol to the health habits section",
        "show a smoking icon for the no smoking area sign",
        "use the smoking icon for the tobacco usage feature",
    ],
    typo_en=[
        "smoikng habit tracker",
        "smokign cigarette in a no smoking zone",
        "smoknig outside the building",
        "smoming in a restricted area",
    ],
    bnd_en=[
        "orange flame burning on a candle wick",
        "campfire with logs and glowing embers",
        "e-cigarette vape pen with a vapor cloud",
        "electronic cigarette charging on a cable",
        "warning triangle with an exclamation mark",
        "danger hazard sign on a restricted zone",
    ],
    valid_en=[
        "cigarette with smoke rising",
        "smoking icon for a health tracker",
        "no smoking symbol",
    ],
    test_en=[
        "cigarette icon in a quit smoking app",
        "smoking warning sign",
        "tobacco smoking habit tracker",
    ],
)

# 397 — sneaker (e6da)
process_icon("sneaker",
    st_en=["feet", "laces", "run", "running", "shoe", "tennis shoe"],
    pst_en=[
        "sneakers on two feet ready for a run", "comfortable sneakers for tired feet",
        "sneaker laces tied in a double knot", "untied laces dangling from a white sneaker",
        "run a marathon in lightweight sneakers", "run icon for a fitness tracker app",
        "running sneaker with cushioned heel support", "running shoes laid out before a morning jog",
        "athletic shoe with a breathable mesh upper", "casual shoe worn for everyday comfort",
        "tennis shoe with a non-slip sole", "classic white tennis shoe on a court",
    ],
    reg_en=[
        "white athletic sneaker with colored accents",
        "lace up your sneakers for the morning run",
        "footwear icon for a fitness or sports app",
        "sneaker with a thick rubber sole and mesh upper",
        "buy a new pair of sneakers for gym workouts",
        "shoe category icon in a sportswear shopping app",
        "low-top sneaker with a flat canvas design",
        "wear sneakers for comfort on a long walking day",
        "athletic footwear icon in a training tracker",
        "classic retro sneaker in a side profile view",
    ],
    conv_en=[
        "I need a sneaker icon for my fitness tracker app",
        "add a sneaker symbol to the sports footwear section",
        "show a sneaker for the running gear category",
        "use the sneaker icon for the workout outfit feature",
    ],
    typo_en=[
        "sneakre with a thick rubber sole",
        "snaeker laced up tight",
        "snekaer for the morning run",
        "sneeaker worn for the gym",
    ],
    bnd_en=[
        "polished leather dress shoe with a low heel",
        "formal oxford shoe with a pointed toe cap",
        "rubber rain boot for wet weather",
        "hiking boot with thick lug sole for trails",
        "lightweight flip flop sandal for the beach",
        "leather sandal with ankle strap closure",
    ],
    valid_en=[
        "athletic sneaker with colored laces",
        "sneaker icon for a fitness app",
        "running sneaker with cushioned sole",
    ],
    test_en=[
        "white sneaker for a morning jog",
        "sneaker in a sports shopping app",
        "classic sneaker side profile",
    ],
)

# 398 — snowman (f7d0)
process_icon("snowman",
    st_en=["cold", "decoration", "frost", "frosty", "holiday", "snow", "snowman"],
    pst_en=[
        "cold winter day perfect for building a snowman", "cold weather icon for a weather forecast app",
        "snowman decoration in a holiday window display", "yard decoration snowman with a scarf and hat",
        "frost on the ground the morning after a snowstorm", "frosty the snowman standing in the yard",
        "frosty snowman with coal eyes and a carrot nose", "frosty winter icon for a holiday greeting card",
        "holiday snowman decoration for Christmas", "winter holiday icon in a seasonal app",
        "snow packed into a round snowman body", "snow covering the ground on a winter morning",
        "classic three-ball snowman with a top hat", "build a snowman with the kids after school",
    ],
    reg_en=[
        "three stacked snowballs making a classic snowman",
        "build a snowman after a heavy snowfall",
        "winter holiday icon for a seasonal or Christmas app",
        "snowman with a carrot nose and coal buttons",
        "snowman wearing a scarf and top hat outside",
        "festive decoration icon for a holiday app",
        "cheerful snowman with stick arms and a smile",
        "children rolling snowballs to build a snowman",
        "winter season icon in a weather or calendar app",
        "glowing snowman ornament on a snowy lawn",
    ],
    conv_en=[
        "I need a snowman icon for my winter app",
        "add a snowman symbol to the holiday season section",
        "show a snowman for the winter activities feature",
        "use the snowman icon for the Christmas decoration category",
    ],
    typo_en=[
        "snowmaan wearing a top hat",
        "snoman standing in the yard",
        "snowamn built in the yard",
        "snoaman with a carrot nose",
    ],
    bnd_en=[
        "tall decorated Christmas tree with a star on top",
        "green Christmas tree with ornaments and lights",
        "santa claus with a red hat and white beard",
        "jolly Santa holding a bag of presents",
        "dome-shaped igloo made from packed snow blocks",
        "arctic igloo with an entrance tunnel",
    ],
    valid_en=[
        "classic three-ball snowman with a top hat",
        "snowman icon for a winter app",
        "frosty snowman in the yard",
    ],
    test_en=[
        "snowman with a carrot nose",
        "build a snowman after snowfall",
        "winter snowman decoration",
    ],
)

# 399 — toothbrush (f635)
process_icon("toothbrush",
    st_en=["bathroom", "bicuspid", "brush", "clean", "dental", "dentist",
           "hygiene", "molar", "mouth", "teeth", "toothbrush"],
    pst_en=[
        "toothbrush in a bathroom cup on the sink", "bathroom hygiene routine with a toothbrush",
        "brush the bicuspid teeth with a soft bristle", "bicuspid area cleaned with the back of the brush",
        "brush your teeth for two minutes each time", "electric brush head spinning against the enamel",
        "clean teeth after every meal", "keep your mouth clean with regular brushing",
        "dental hygiene kit with a toothbrush", "dental routine starting with the toothbrush",
        "dentist recommends brushing twice daily", "dentist appointment reminder icon in a health app",
        "oral hygiene icon for a wellness tracker", "daily hygiene checklist with toothbrushing",
        "scrub the molar surface with a toothbrush", "molar cleaning with the back of the brush head",
        "brush every surface of the mouth carefully", "mouth health icon in a dental tracking app",
        "brush teeth in circular motions", "teeth cleaning icon for a kids' hygiene app",
        "soft toothbrush for sensitive gums", "toothbrush standing in a holder on the counter",
    ],
    reg_en=[
        "toothbrush with colored bristles on a white handle",
        "brush your teeth every morning and night",
        "dental hygiene icon for an oral health app",
        "electric toothbrush with a rotating brush head",
        "two-minute toothbrush timer for proper cleaning",
        "health icon in a personal care routine tracker",
        "toothbrush leaning in a ceramic bathroom holder",
        "replace your toothbrush every three months",
        "oral health icon in a wellness habit tracker",
        "toothbrush with toothpaste squeezed on the bristles",
    ],
    conv_en=[
        "I need a toothbrush icon for my oral health app",
        "add a toothbrush symbol to the dental hygiene section",
        "show a toothbrush for the morning routine feature",
        "use the toothbrush icon for the hygiene tracker",
    ],
    typo_en=[
        "toothbrsuh twice a day",
        "toothrush with soft bristles",
        "toothbruhs used every morning",
        "toohtbrush standing on the counter",
    ],
    bnd_en=[
        "white tooth icon with rounded bumps on top",
        "single tooth silhouette for a dental app",
        "dental floss container with a cutting edge",
        "floss threaded between two teeth",
        "mouthwash bottle with a blue liquid inside",
        "rinse with mouthwash for fresh breath",
    ],
    valid_en=[
        "toothbrush with soft bristles",
        "toothbrush icon for an oral health app",
        "brush your teeth twice a day",
    ],
    test_en=[
        "electric toothbrush for daily cleaning",
        "toothbrush in a bathroom holder",
        "dental hygiene toothbrush icon",
    ],
)

# 400 — tornado (f76f)
process_icon("tornado",
    st_en=["cloud", "cyclone", "dorothy", "landspout", "tornado",
           "toto", "twister", "waterspout", "weather", "whirlwind"],
    pst_en=[
        "dark storm cloud spawning a tornado below", "rotating cloud funnel descending from the sky",
        "cyclone warning issued for the coastal region", "tropical cyclone spinning in the ocean",
        "dorothy swept away by a Kansas tornado", "wizard of Oz Dorothy and the twister",
        "landspout tornado forming over flat terrain", "short-lived landspout dust devil",
        "tornado touching down in a field", "tornado siren going off in the town",
        "toto the dog in the tornado scene", "toto swept up in Dorothy's tornado",
        "twister tornado spinning across the plains", "twister game board with colorful spots",
        "waterspout tornado rising from the ocean surface", "waterspout seen off the Florida coast",
        "severe weather warning for tornado activity", "weather icon for a storm alert app",
        "whirlwind spinning debris into the air", "whirlwind effect icon in a weather app",
    ],
    reg_en=[
        "funnel-shaped tornado descending from a dark cloud",
        "tornado warning siren activated in the county",
        "severe weather icon for a storm alert app",
        "narrow spinning vortex touching the ground below",
        "take shelter when a tornado watch is issued",
        "natural disaster icon in an emergency preparedness app",
        "tornado silhouette with debris swirling at the base",
        "tornado path tracked on a storm chaser map",
        "weather hazard icon in a radar or forecast app",
        "spinning funnel cloud narrowing toward the earth",
    ],
    conv_en=[
        "I need a tornado icon for my weather alert app",
        "add a tornado symbol to the severe weather section",
        "show a tornado for the natural disaster feature",
        "use the tornado icon for the storm tracking screen",
    ],
    typo_en=[
        "torando warning for the county",
        "tornaod touching down in the field",
        "torndo funnel cloud",
        "tornadoo spinning across the plains",
    ],
    bnd_en=[
        "hurricane spiral viewed from satellite above",
        "tropical hurricane making landfall on the coast",
        "lightning bolt striking during a thunderstorm",
        "dark storm cloud with heavy rain below",
        "whirlpool drain spinning in a body of water",
        "ocean whirlpool pulling objects in a spiral",
    ],
    valid_en=[
        "tornado funnel touching down",
        "tornado icon for a weather app",
        "spinning tornado vortex",
    ],
    test_en=[
        "tornado warning for a storm app",
        "tornado funnel cloud descending",
        "severe weather tornado symbol",
    ],
)

# 401 — tree (f1bb)
process_icon("tree",
    st_en=["bark", "evergreen tree", "fall", "flora", "forest",
           "investment", "nature", "plant", "seasonal", "tree"],
    pst_en=[
        "bark texture on the trunk of a tall oak", "tree bark peeling off in strips",
        "evergreen tree staying green all winter", "classic evergreen tree silhouette for nature",
        "fall tree with orange and red leaves", "fall foliage season on a tree-lined street",
        "local flora featuring native trees and shrubs", "flora icon for a nature identification app",
        "dense forest of towering trees", "forest walk on a trail surrounded by trees",
        "tree as a long-term investment in the environment", "planting a tree as a green investment",
        "nature icon featuring a tall green tree", "nature walk icon in an outdoor activity app",
        "plant a tree to offset carbon emissions", "tree icon for a gardening or plant care app",
        "seasonal tree with changing leaves throughout the year", "seasonal nature icon for a calendar app",
        "tall tree with a full leafy canopy", "lone tree on a hilltop at sunset",
    ],
    reg_en=[
        "single tree with a round leafy canopy on top",
        "plant a tree to help the environment",
        "nature and environment icon for an eco app",
        "tall oak tree with a wide spreading canopy",
        "hike through the forest under towering trees",
        "park or outdoor icon in a maps or travel app",
        "simple tree silhouette with a triangular crown",
        "water the tree weekly during the dry season",
        "green icon representing sustainability in an app",
        "leafy deciduous tree in full summer bloom",
    ],
    conv_en=[
        "I need a tree icon for my nature tracking app",
        "add a tree symbol to the environment section",
        "show a tree for the outdoor activities feature",
        "use the tree icon for the sustainability category",
    ],
    typo_en=[
        "tre with a large canopy",
        "tere with orange fall leaves",
        "treee on a hilltop at sunset",
        "trea growing in the forest",
    ],
    bnd_en=[
        "lush green forest of pine trees",
        "dense woodland with overlapping tree canopies",
        "low rounded bush or shrub in a garden",
        "flowering garden shrub along a walkway",
        "tall palm tree with long fronds on a tropical beach",
        "coconut palm leaning over the ocean waves",
    ],
    valid_en=[
        "tree with a round leafy canopy",
        "tree icon for a nature app",
        "tall tree in the park",
    ],
    test_en=[
        "plant a tree for the environment",
        "forest tree silhouette",
        "tree icon in an outdoor app",
    ],
)

# 402 — truck (f0d1)
process_icon("truck",
    st_en=["cargo", "delivery", "shipping", "truck", "vehicle"],
    pst_en=[
        "cargo truck transporting goods across the country", "heavy cargo load on a flatbed truck",
        "delivery truck parked outside the warehouse", "delivery truck icon in a shipping tracker",
        "shipping truck leaving the distribution center", "shipping icon for a logistics platform",
        "big rig truck on a highway", "truck driver icon for a transport app",
        "commercial vehicle tracking in a fleet app", "heavy vehicle driving on the interstate",
    ],
    reg_en=[
        "large box truck with a roll-up rear door",
        "track a delivery truck with the shipping app",
        "logistics icon for a freight or shipping platform",
        "semi-truck pulling a trailer on the highway",
        "order arrives in a delivery truck tomorrow",
        "transport icon for a supply chain dashboard",
        "flat-nose truck with a tall cargo box",
        "fleet of delivery trucks dispatched from the hub",
        "commercial vehicle icon in a route planning app",
        "delivery truck with a company logo on the side",
    ],
    conv_en=[
        "I need a truck icon for my delivery tracking app",
        "add a truck symbol to the shipping section",
        "show a truck for the logistics and freight feature",
        "use the truck icon for the vehicle fleet screen",
    ],
    typo_en=[
        "trucck on the highway",
        "truk delivering packages",
        "trcuk parked at the dock",
        "truock with a heavy load",
    ],
    bnd_en=[
        "white delivery van driving through the city",
        "cargo van with a sliding side door open",
        "large red farm tractor with big rear wheels",
        "tractor pulling a plow through a muddy field",
        "city bus with passengers at a bus stop",
        "double-decker bus on a busy street",
    ],
    valid_en=[
        "delivery truck on the road",
        "truck icon for a logistics app",
        "cargo truck on the highway",
    ],
    test_en=[
        "delivery truck tracked in a shipping app",
        "semi-truck hauling freight",
        "truck icon for a transport app",
    ],
)

# 403 — trumpet (f8e3)
process_icon("trumpet",
    st_en=["brass", "bugle", "classical", "cornet", "instrument", "jazz", "music", "orchestra", "trumpet"],
    pst_en=[
        "brass instrument with a bright golden finish", "brass section of a marching band",
        "bugle sounding a military reveille call", "simple bugle with no valves",
        "classical trumpet solo in a concert hall", "classical orchestra featuring trumpets and horns",
        "cornet similar to a trumpet but shorter", "brass cornet used in a brass band",
        "wind instrument requiring strong breath control", "brass instrument icon for a music app",
        "jazz trumpet player in a smoky club", "jazz solo improvised on the trumpet",
        "music played on a shiny brass trumpet", "music icon featuring a trumpet",
        "orchestra trumpet section playing forte", "orchestra pit with a row of trumpet players",
        "gleaming trumpet with three valves on top", "play the trumpet in a marching band",
    ],
    reg_en=[
        "gold trumpet with three valves and a wide bell",
        "play the trumpet in a jazz quartet",
        "music instrument icon for a band or orchestra app",
        "shiny brass trumpet viewed from the side",
        "practice the trumpet scales every morning",
        "brass section icon in a music education app",
        "trumpet bell flaring outward at the end",
        "fanfare trumpet announcing an important event",
        "instrument icon for a music learning platform",
        "classic trumpet silhouette in a musical context",
    ],
    conv_en=[
        "I need a trumpet icon for my music app",
        "add a trumpet symbol to the brass instruments section",
        "show a trumpet for the jazz music feature",
        "use the trumpet icon for the orchestra category",
    ],
    typo_en=[
        "trupmte solo in a jazz bar",
        "trumpt in the marching band",
        "trumept player in the orchestra",
        "trumpett with a golden finish",
    ],
    bnd_en=[
        "curved saxophone with a wide flared bell",
        "jazz saxophonist playing on stage",
        "trombone with a long sliding tube",
        "brass trombone player in a marching band",
        "round French horn coiled in a circle",
        "French horn player in an orchestra pit",
    ],
    valid_en=[
        "gold trumpet with three valves",
        "trumpet icon for a music app",
        "brass trumpet for a jazz band",
    ],
    test_en=[
        "trumpet solo in a jazz club",
        "trumpet in a marching band",
        "trumpet instrument icon",
    ],
)
