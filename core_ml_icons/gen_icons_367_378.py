#!/usr/bin/env python3
"""Generate English training data for icons 367-378."""
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

# 367 — spa (f5bb)
process_icon("spa",
    st_en=["flora", "massage", "mindfulness", "plant", "wellness"],
    pst_en=[
        "tropical flora in a zen garden", "flora arrangement at the spa entrance",
        "deep tissue massage at the spa", "massage table with soft towels",
        "mindfulness meditation in a calm spa space", "mindfulness session for stress relief",
        "lush green plant in a spa lobby", "plant icon for a wellness or nature app",
        "wellness retreat at a luxury spa", "wellness icon for a health tracking app",
    ],
    reg_en=[
        "lotus flower or leaf icon in a tranquil setting",
        "book a spa treatment for relaxation",
        "wellness category icon in a self-care app",
        "delicate floral symbol suggesting peace and calm",
        "spa day for a birthday or anniversary gift",
        "beauty and wellness icon for a booking platform",
        "soft leaf or flower motif on a spa sign",
        "unwind with a spa massage after a stressful week",
        "holistic health icon representing relaxation services",
        "serene spa symbol with a botanical design",
    ],
    conv_en=[
        "I need a spa icon for my wellness booking app",
        "add a spa symbol to the relaxation section",
        "show a spa icon for the self-care category",
        "use the spa icon for the mindfulness feature",
    ],
    typo_en=[
        "sap treatment at the resort",
        "spaa for a relaxing weekend",
        "spa massge booking",
        "spa mindfulnes retreat",
    ],
    bnd_en=[
        "yoga pose silhouette in a meditation app",
        "person sitting in a lotus yoga pose",
        "scented candle flickering on a wooden surface",
        "aromatherapy candle with a calming fragrance",
        "hot spring pool with steam rising from the water",
        "steaming bath icon for a hot tub or sauna",
    ],
    valid_en=[
        "spa wellness icon with a botanical motif",
        "relaxing spa treatment booking",
        "spa symbol for a self-care app",
    ],
    test_en=[
        "spa icon for a wellness app",
        "massage and spa service",
        "spa leaf or flower motif",
    ],
)

# 368 — spider (f717)
process_icon("spider",
    st_en=["arachnid", "bug", "charlotte", "crawl", "eight", "halloween", "insect", "spider"],
    pst_en=[
        "eight-legged arachnid hanging from a web", "arachnid crawling across the ceiling",
        "creepy bug hanging on a spider web", "bug icon for a Halloween app",
        "charlotte the spider spinning her web", "charlotte's web famous literary spider",
        "spider crawl across the wall at night", "crawl of a spider down a silken thread",
        "eight legs spread wide on a web", "eight eyes staring from a dark corner",
        "halloween spider decoration hanging in the window", "spooky halloween spider on an orange background",
        "insect icon for a nature or science app", "creepy insect crawling on the floor",
        "large hairy spider in a web", "spider dangling from a single thread",
    ],
    reg_en=[
        "black spider with eight legs hanging from a web",
        "halloween decoration spider on a doorstep",
        "nature icon for a bug guide or science app",
        "spider silhouette with a round body and long legs",
        "fear of spiders warning symbol in an app",
        "arachnid icon in a science or biology app",
        "tiny spider suspended on a long silk thread",
        "spider spinning a spiral web between two branches",
        "halloween icon representing fear and the unknown",
        "hairy tarantula spider viewed from above",
    ],
    conv_en=[
        "I need a spider icon for my Halloween app",
        "add a spider symbol to the creepy crawlies section",
        "show a spider for the bug and insect category",
        "use the spider icon for the haunted house feature",
    ],
    typo_en=[
        "spidre on the ceiling",
        "spoder crawling across the wall",
        "sipder hanging from a web",
        "spiider with eight legs",
    ],
    bnd_en=[
        "scorpion with a curved stinger tail",
        "desert scorpion pinching with its claws",
        "ant carrying a crumb across the kitchen floor",
        "black ant marching in a trail",
        "intricate cobweb stretched between two corners",
        "sticky spider web with morning dew drops",
    ],
    valid_en=[
        "spider with eight legs on a web",
        "halloween spider decoration",
        "spider icon for a bug app",
    ],
    test_en=[
        "black spider hanging from a thread",
        "creepy spider for halloween",
        "spider in a nature app",
    ],
)

# 369 — stethoscope (f0f1)
process_icon("stethoscope",
    st_en=["covid-19", "diagnosis", "doctor", "general practitioner", "heart",
           "hospital", "infirmary", "medicine", "office", "outpatient", "stethoscope"],
    pst_en=[
        "covid-19 checkup with a stethoscope", "covid-19 diagnosis at the clinic",
        "diagnosis confirmed by a doctor with a stethoscope", "initial diagnosis during a medical exam",
        "doctor listening with a stethoscope", "doctor icon for a medical appointment app",
        "general practitioner checking your lungs", "general practitioner visit at the family clinic",
        "listening to the heart with a stethoscope", "heart rate check during a physical exam",
        "hospital staff wearing stethoscopes", "hospital icon for a healthcare app",
        "infirmary visit for a routine checkup", "school infirmary equipped with a stethoscope",
        "medicine and health icon in a doctor app", "practice medicine with the proper tools",
        "doctor's office with a stethoscope on the desk", "office visit icon for medical scheduling",
        "outpatient clinic for minor health checkups", "outpatient visit tracked in a health app",
        "stethoscope around the neck of a physician", "stethoscope placed on a patient's chest",
    ],
    reg_en=[
        "stethoscope with earpieces and a chest piece",
        "doctor listening to a patient's heartbeat",
        "medical icon for a healthcare or doctor app",
        "round chest piece of a stethoscope on skin",
        "checkup with a stethoscope at the annual physical",
        "health icon for a telemedicine platform",
        "coiled stethoscope tubing hanging from the neck",
        "nurse using a stethoscope in the hospital ward",
        "diagnostic tool icon in a medical records app",
        "classic stethoscope silhouette in a medical symbol",
    ],
    conv_en=[
        "I need a stethoscope icon for my doctor booking app",
        "add a stethoscope symbol to the health checkup section",
        "show a stethoscope for the medical diagnosis feature",
        "use the stethoscope icon for the doctor profile screen",
    ],
    typo_en=[
        "stethascope used by the doctor",
        "stethoscpe on the doctor's desk",
        "stethescope during a checkup",
        "stethoscape for listening to the heart",
    ],
    bnd_en=[
        "digital thermometer displaying a temperature reading",
        "glass thermometer in a child's mouth",
        "blood pressure cuff wrapped around an arm",
        "inflatable blood pressure monitor at the clinic",
        "medical syringe drawn up for an injection",
        "nurse holding a syringe ready to give a vaccine",
    ],
    valid_en=[
        "stethoscope around a doctor's neck",
        "stethoscope for a medical app",
        "doctor listening with a stethoscope",
    ],
    test_en=[
        "stethoscope on a white background",
        "medical stethoscope icon",
        "stethoscope for a health checkup",
    ],
)

# 370 — stomach (f623)
process_icon("stomach",
    st_en=["abdomen", "belly", "food", "gut", "hungry", "intestine", "organ", "tummy"],
    pst_en=[
        "pain in the abdomen after eating", "abdomen icon in a body anatomy app",
        "belly rumbling when hungry", "full belly after a big meal",
        "food digested in the stomach", "food tracker showing stomach capacity",
        "gut health tracked in a nutrition app", "healthy gut microbiome symbol",
        "stomach growling because you're hungry", "hungry icon for a food ordering app",
        "stomach connected to the intestine", "intestine diagram in a biology textbook",
        "organ diagram showing the stomach", "digestive organ icon in a health app",
        "tummy ache after eating too much", "tummy grumbling sound before lunch",
    ],
    reg_en=[
        "rounded stomach organ shape with an opening",
        "stomach pain tracker in a health journal",
        "digestive system icon in a body anatomy app",
        "stomach silhouette with folded walls inside",
        "log what you eat and how your stomach feels",
        "gastrointestinal health icon for a medical app",
        "simple outlined stomach icon with a J-shape",
        "hungry stomach symbol on a food delivery app",
        "anatomy icon representing the digestive organ",
        "stomach growling icon for a hunger reminder",
    ],
    conv_en=[
        "I need a stomach icon for my gut health tracker",
        "add a stomach symbol to the digestion section",
        "show a stomach for the hunger and meal tracking feature",
        "use the stomach icon for the body anatomy map",
    ],
    typo_en=[
        "stomache ache after dinner",
        "stomch pain in the morning",
        "stomack growling before lunch",
        "stoamch organ diagram",
    ],
    bnd_en=[
        "small and large intestine coiled together",
        "intestine diagram for a digestive health app",
        "liver organ shown in a body anatomy illustration",
        "liver shape used in a medical reference app",
        "heart organ beating in the chest cavity",
        "anatomical heart with arteries and chambers",
    ],
    valid_en=[
        "stomach organ icon",
        "stomach in a digestive health app",
        "stomach silhouette for anatomy",
    ],
    test_en=[
        "stomach ache tracker",
        "stomach organ in a health app",
        "hungry stomach icon",
    ],
)

# 371 — sword (f71c)
process_icon("sword",
    st_en=["blade", "d&d", "dagger", "dnd", "fantasy", "fight", "knife", "sharp", "weapon"],
    pst_en=[
        "sharp blade of a medieval sword", "blade glinting in the sunlight",
        "d&d character wielding a magic sword", "d&d campaign with legendary weapon drops",
        "dagger stabbed into a wooden table", "short dagger used for close combat",
        "dnd warrior equipped with a longsword", "dnd game icon for a dungeon master app",
        "fantasy sword with runes along the blade", "epic fantasy weapon for a video game",
        "fight scene with swords clashing", "fight icon for a combat strategy game",
        "knife-shaped blade for a hunting tool", "knife icon in a survival or camping app",
        "sharp sword edge that cuts through stone", "sharp tip of a finely crafted blade",
        "weapon icon for a game inventory", "medieval weapon in an RPG adventure game",
    ],
    reg_en=[
        "longsword with a cross guard and leather grip",
        "equip a sword in a role-playing game inventory",
        "combat weapon icon for a fantasy RPG app",
        "medieval sword with an ornate hilt and pommel",
        "knight brandishing a sword in battle",
        "game icon for a weapon or armory section",
        "straight double-edged sword on a dark background",
        "collecting legendary swords in a dungeon crawler",
        "fantasy game symbol for attack or combat",
        "ancient ceremonial sword mounted on a wall",
    ],
    conv_en=[
        "I need a sword icon for my RPG game app",
        "add a sword symbol to the weapons inventory section",
        "show a sword for the combat and battle feature",
        "use the sword icon for the fantasy adventure game",
    ],
    typo_en=[
        "swrod in the stone",
        "swordl of the knight",
        "soword with a sharp blade",
        "swod ready for battle",
    ],
    bnd_en=[
        "battle axe with a wide curved blade",
        "wood chopping axe stuck in a log",
        "round wooden shield with an iron boss",
        "knight's shield with a coat of arms",
        "bow and arrow drawn back ready to fire",
        "archery bow with a notched arrow",
    ],
    valid_en=[
        "medieval sword with a cross guard",
        "sword icon for an RPG game",
        "sharp blade weapon symbol",
    ],
    test_en=[
        "knight sword in a fantasy game",
        "sword in the stone",
        "sword icon for a combat app",
    ],
)

# 372 — telescope (e03e)
process_icon("telescope",
    st_en=["astronomy", "knowledge", "lens", "look", "microscope", "observatory",
           "science", "scope", "search", "space", "telescope", "tool", "view"],
    pst_en=[
        "astronomy club meeting to observe the stars", "astronomy app showing tonight's sky map",
        "knowledge gained by studying the cosmos", "knowledge icon for a science education app",
        "telescope lens magnifying distant galaxies", "precision lens inside a reflecting telescope",
        "look through the telescope at the moon", "look up at the stars through the eyepiece",
        "telescope and microscope both use optical lenses", "microscope for small things telescope for distant",
        "observatory dome housing a large telescope", "visit the observatory to view the planets",
        "science project with a small telescope", "science icon for an astronomy learning app",
        "scope trained on the night sky", "scope used to find distant star clusters",
        "search the galaxy with a powerful telescope", "search for exoplanets with a space telescope",
        "space telescope orbiting above the atmosphere", "space exploration icon in a NASA-themed app",
        "portable telescope set up in the backyard", "telescope pointed at the crescent moon",
        "optical tool for viewing distant objects", "tool icon for an astronomy equipment guide",
        "view the rings of Saturn through a telescope", "panoramic view of the Milky Way with a scope",
    ],
    reg_en=[
        "long cylindrical telescope on a tripod stand",
        "stargazing at night with a backyard telescope",
        "astronomy icon for a space or stargazing app",
        "refracting telescope with a long narrow tube",
        "point the telescope at Jupiter to see its moons",
        "science education icon for a sky observation app",
        "telescope angled upward toward a starry sky",
        "amateur astronomer setting up a telescope in the field",
        "space discovery icon for a solar system app",
        "eyepiece end of a gleaming brass telescope",
    ],
    conv_en=[
        "I need a telescope icon for my stargazing app",
        "add a telescope symbol to the astronomy section",
        "show a telescope for the space exploration feature",
        "use the telescope icon for the sky observation category",
    ],
    typo_en=[
        "telescpe pointed at the moon",
        "telesocpe for stargazing",
        "telecope in the backyard",
        "telascope at the observatory",
    ],
    bnd_en=[
        "pair of binoculars for birdwatching or sports",
        "binoculars raised to the eyes for a distant view",
        "laboratory microscope with glass slides and objective",
        "microscope used to view bacteria in a science class",
        "satellite dish pointed toward the sky",
        "orbital satellite transmitting signals to earth",
    ],
    valid_en=[
        "telescope pointed at the night sky",
        "astronomy telescope on a tripod",
        "telescope icon for a stargazing app",
    ],
    test_en=[
        "backyard telescope for stargazing",
        "telescope in an astronomy app",
        "view the stars through a telescope",
    ],
)

# 373 — tent (e57d)
process_icon("tent",
    st_en=["bivouac", "campground", "campsite", "refugee", "shelter", "tent"],
    pst_en=[
        "overnight bivouac on a mountain trail", "minimalist bivouac shelter in the forest",
        "campground map showing tent sites", "campground with a fire pit and picnic table",
        "campsite with a tent and sleeping bags", "reserve a campsite for the weekend",
        "refugee tent in an emergency relief camp", "refugee shelter set up by aid workers",
        "emergency shelter for disaster relief", "waterproof shelter from the rain on a hike",
        "dome tent pitched on flat ground", "tent glowing from a lantern inside at night",
    ],
    reg_en=[
        "triangular tent pitched on a grassy meadow",
        "camping overnight under the stars in a tent",
        "outdoor adventure icon for a camping or hiking app",
        "small dome tent with a zipped front entrance",
        "set up the tent before it gets dark outside",
        "campsite icon for a travel or outdoor activity app",
        "tent silhouette with stakes and guy lines",
        "backpacking tent packed into a compact carry bag",
        "emergency shelter icon for a disaster relief app",
        "family tent with multiple rooms and a rain fly",
    ],
    conv_en=[
        "I need a tent icon for my camping planner app",
        "add a tent symbol to the outdoor activities section",
        "show a tent for the campsite booking feature",
        "use the tent icon for the emergency shelter category",
    ],
    typo_en=[
        "tnet set up in the field",
        "tentt with a rain fly",
        "teny pitched for the night",
        "ten pitched at the campsite",
    ],
    bnd_en=[
        "wooden log cabin in the forest clearing",
        "rustic mountain cabin with a front porch",
        "camper van parked at a campground",
        "RV motorhome on a coastal road trip",
        "hammock strung between two palm trees",
        "camping hammock hanging over a forest stream",
    ],
    valid_en=[
        "dome tent pitched at a campsite",
        "tent icon for a camping app",
        "outdoor tent for overnight shelter",
    ],
    test_en=[
        "tent set up in the woods",
        "camping tent under the stars",
        "tent in a travel or camping app",
    ],
)

# 374 — ticket (f145)
process_icon("ticket",
    st_en=["admission", "coupon", "movie", "pass", "support", "ticket", "voucher"],
    pst_en=[
        "admission ticket to the art museum", "admission price printed on the ticket stub",
        "coupon code printed on a ticket", "discount coupon clipped from a newspaper",
        "movie ticket for the Friday night show", "scan the movie ticket at the theater entrance",
        "concert pass clipped to a lanyard", "day pass for unlimited rides at the theme park",
        "support ticket submitted to the help desk", "customer support ticket number for tracking",
        "print your ticket at home before the event", "digital ticket displayed on a phone screen",
        "gift voucher redeemable at the restaurant", "voucher code entered at checkout",
    ],
    reg_en=[
        "rectangular ticket with a perforation line on the side",
        "scan a QR code on a digital event ticket",
        "event ticketing icon in a booking or venue app",
        "torn ticket stub from a sold-out concert",
        "buy tickets online for a sports game",
        "customer support ticket icon in a help desk app",
        "brightly colored ticket roll for carnival rides",
        "admit one ticket with a star border design",
        "print and show your ticket at the gate",
        "ticketing symbol for an entertainment or travel app",
    ],
    conv_en=[
        "I need a ticket icon for my event booking app",
        "add a ticket symbol to the reservations section",
        "show a ticket for the purchase and checkout feature",
        "use the ticket icon for the support request screen",
    ],
    typo_en=[
        "tiket to the concert",
        "tickt scanned at the door",
        "ticekt for the movie tonight",
        "tiicket stub from last night",
    ],
    bnd_en=[
        "airline boarding pass with seat and gate info",
        "printed boarding pass folded in a passport",
        "store coupon with a barcode and expiration date",
        "discount coupon torn from a promotional mailer",
        "name badge on a lanyard at a conference",
        "event wristband with printed text and barcode",
    ],
    valid_en=[
        "event ticket with a perforation line",
        "ticket icon for a booking app",
        "digital ticket scanned at the door",
    ],
    test_en=[
        "movie ticket for tonight",
        "ticket stub from a concert",
        "ticket icon in an event app",
    ],
)

# 375 — tomato (e330)
process_icon("tomato",
    st_en=["blt", "fresh", "fruit", "garden", "salad", "summer", "tomato", "vegetable"],
    pst_en=[
        "blt sandwich with fresh tomato slices", "ripe tomato for a classic blt",
        "fresh tomato from the garden vine", "fresh tomato on a cutting board",
        "technically a fruit mistaken for a vegetable", "fruit salad with cherry tomatoes",
        "garden tomato picked at peak ripeness", "home garden with rows of tomato plants",
        "sliced tomato in a caprese salad", "salad with cherry tomatoes and basil",
        "summer harvest of red ripe tomatoes", "summer garden full of juicy tomatoes",
        "round red tomato with a green stem", "tomato juice squeezed fresh",
        "vegetable section with tomatoes in a grocery app", "vegetable icon for a recipe tracker",
    ],
    reg_en=[
        "round red tomato with a bright green stem",
        "slicing a fresh tomato for a salad",
        "food icon for a recipe or grocery app",
        "ripe tomato with a shiny smooth skin",
        "roasting cherry tomatoes with olive oil and garlic",
        "vegetable icon in a meal planning dashboard",
        "cluster of cherry tomatoes on the vine",
        "tomato sauce simmering for a pasta dinner",
        "ingredient icon for an Italian food recipe",
        "tomato cut in half showing the seeds inside",
    ],
    conv_en=[
        "I need a tomato icon for my recipe tracker app",
        "add a tomato symbol to the vegetable category",
        "show a tomato for the fresh produce section",
        "use the tomato icon for the garden harvest feature",
    ],
    typo_en=[
        "tomatoe ripening on the vine",
        "tomoto sliced for a salad",
        "tmoato in a pasta sauce",
        "tomato withoutt the stem",
    ],
    bnd_en=[
        "red bell pepper with a green stem and seeds inside",
        "roasted red pepper in a sandwich",
        "purple eggplant with a long green stem",
        "sliced eggplant grilling on a hot pan",
        "bunch of red cherries with stems attached",
        "cherry on top of an ice cream sundae",
    ],
    valid_en=[
        "round red tomato with green stem",
        "fresh tomato for a recipe app",
        "tomato vegetable icon",
    ],
    test_en=[
        "sliced tomato in a salad",
        "ripe tomato from the garden",
        "tomato icon in a cooking app",
    ],
)

# 376 — tooth (f5c9)
process_icon("tooth",
    st_en=["bicuspid", "dental", "dentist", "molar", "mouth", "teeth", "tooth"],
    pst_en=[
        "bicuspid tooth between the canines and molars", "bicuspid extracted at the dental clinic",
        "dental checkup every six months", "dental hygiene icon in a health app",
        "dentist appointment reminder notification", "dentist cleaning teeth with special tools",
        "molar tooth used for grinding food", "impacted wisdom molar causing pain",
        "tooth visible inside an open mouth", "mouth hygiene routine with brushing and flossing",
        "brush teeth twice a day for good hygiene", "teeth whitening treatment at the dentist",
        "single tooth icon for a dental app", "tooth fairy tradition for children's lost teeth",
    ],
    reg_en=[
        "white tooth with rounded bumps on top",
        "book a dentist appointment for a checkup",
        "dental health icon in a medical or hygiene app",
        "molar tooth with deep grooves on the surface",
        "brush and floss to keep teeth healthy",
        "dentist icon for a clinic appointment app",
        "simple tooth outline with a crown and two roots",
        "tooth pain alert in a dental health tracker",
        "oral hygiene category in a wellness app",
        "gleaming white tooth on a blue background",
    ],
    conv_en=[
        "I need a tooth icon for my dental reminder app",
        "add a tooth symbol to the oral health section",
        "show a tooth for the dentist appointment feature",
        "use the tooth icon for the teeth brushing tracker",
    ],
    typo_en=[
        "tooht ache after eating sweets",
        "tooh needs to be filled",
        "toth fairy left a coin",
        "toothh brushing reminder",
    ],
    bnd_en=[
        "toothbrush with bristles for brushing teeth",
        "electric toothbrush charging on a bathroom shelf",
        "mouth with lips slightly open showing teeth",
        "lips icon used in a beauty or cosmetics app",
        "panoramic dental x-ray for a full mouth scan",
        "x-ray image showing tooth roots and bone structure",
    ],
    valid_en=[
        "white tooth icon for a dental app",
        "molar tooth with rounded bumps",
        "tooth symbol for oral hygiene",
    ],
    test_en=[
        "tooth for a dentist appointment app",
        "tooth fairy symbol",
        "dental tooth icon",
    ],
)

# 377 — tractor (f722)
process_icon("tractor",
    st_en=["agriculture", "farm", "tractor", "vehicle"],
    pst_en=[
        "agriculture equipment used on a large farm", "agriculture icon for a farming tracker app",
        "farm tractor plowing a field", "farm vehicle parked in a barn",
        "red tractor driving across a wheat field", "old tractor with large rear wheels",
        "farm vehicle pulling a trailer", "heavy vehicle icon for an agricultural app",
    ],
    reg_en=[
        "large red tractor with big rear wheels in a field",
        "plowing the field with a tractor before planting",
        "agriculture icon for a farm management app",
        "tractor with an exhaust pipe and enclosed cab",
        "harvesting crops with a tractor and attachment",
        "farming equipment icon in a rural lifestyle app",
        "green tractor parked next to a red barn",
        "tractor pulling a plow through muddy soil",
        "vehicle icon for an agricultural machinery catalog",
        "tractor tire track left in a freshly plowed field",
    ],
    conv_en=[
        "I need a tractor icon for my farm management app",
        "add a tractor symbol to the agriculture section",
        "show a tractor for the equipment tracking feature",
        "use the tractor icon for the farm vehicle category",
    ],
    typo_en=[
        "tarctor plowing the soil",
        "tracor pulling a trailer",
        "trctor in a wheat field",
        "tractir with a powerful engine",
    ],
    bnd_en=[
        "combine harvester cutting through a grain field",
        "grain harvester with a wide cutting head",
        "flatbed truck hauling equipment on the highway",
        "pickup truck parked outside the farm store",
        "yellow bulldozer pushing soil on a construction site",
        "construction bulldozer leveling the ground",
    ],
    valid_en=[
        "red tractor with large rear wheels",
        "farm tractor in an agriculture app",
        "tractor plowing a field",
    ],
    test_en=[
        "tractor on a wheat farm",
        "agriculture tractor vehicle",
        "tractor icon for a farm app",
    ],
)

# 378 — train (f238)
process_icon("train",
    st_en=["bullet", "commute", "locomotive", "railway", "subway", "train"],
    pst_en=[
        "bullet train speeding at 300 km per hour", "japanese bullet train on the shinkansen",
        "daily commute on the train to work", "commute time tracked in a travel app",
        "steam locomotive pulling passenger cars", "diesel locomotive on a freight line",
        "railway station with multiple platforms", "railway map for a transit planning app",
        "subway train arriving at the underground station", "subway map icon for a city transit app",
        "passenger train crossing a bridge", "book a train ticket for the weekend trip",
    ],
    reg_en=[
        "side view of a passenger train with many windows",
        "take the train to skip the morning traffic jam",
        "transit icon for a railway or commuting app",
        "streamlined bullet train on an elevated track",
        "track departure times for the next train",
        "public transport icon for a city navigation app",
        "train engine at the front of a long passenger set",
        "ride the overnight train across the country",
        "railway schedule icon in a travel planner",
        "steam train with a smoke plume from the funnel",
    ],
    conv_en=[
        "I need a train icon for my commute tracker app",
        "add a train symbol to the public transport section",
        "show a train for the railway schedule feature",
        "use the train icon for the travel booking screen",
    ],
    typo_en=[
        "trian leaving the station now",
        "traiin arriving on platform three",
        "trein to the city center",
        "trani on the metro line",
    ],
    bnd_en=[
        "yellow tram on city rails in the street",
        "streetcar tram gliding along a busy avenue",
        "double-decker bus on a city road",
        "city bus pulling up to a bus stop",
        "underground metro train in a tiled station",
        "metro map showing colored lines and stations",
    ],
    valid_en=[
        "passenger train on a railway track",
        "train icon for a commuting app",
        "train arriving at the station",
    ],
    test_en=[
        "bullet train at high speed",
        "train schedule in a travel app",
        "locomotive pulling passenger cars",
    ],
)
