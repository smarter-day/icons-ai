#!/usr/bin/env python3
"""Generate English training data for icons 428-440."""
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

# 428
process_icon("banana",
    st_en=["banana", "fruit", "peel", "plantain", "potassium"],
    pst_en=[
        "ripe yellow banana from the bunch", "banana split dessert with ice cream",
        "tropical fruit salad with mango", "fruit basket with assorted produce",
        "slippery banana peel on the floor", "peel back the banana skin to eat",
        "green plantain fried as a side dish", "plantain chips seasoned and baked",
        "potassium-rich banana for athletes", "potassium source in a healthy diet",
    ],
    reg_en=[
        "yellow curved banana with a brown spot",
        "bunch of bananas hanging in the market",
        "peeled banana half eaten as a snack",
        "banana emoji icon for a food diary",
        "ripe banana mashed for banana bread",
        "frozen banana blended into a smoothie",
        "banana split with chocolate sauce and nuts",
        "plantain roasted beside the main course",
        "athlete eating a banana at halftime",
        "tropical banana palm fruit for recipe app",
    ],
    conv_en=[
        "I need a banana icon for my fruit tracker",
        "add a banana symbol to the smoothie ingredients",
        "show a banana for the tropical fruit section",
        "use the banana icon for the healthy snack list",
    ],
    typo_en=[
        "ripe banna from the fruit bowl",
        "ellow banaana on the counter",
        "bananna peel slipping hazard",
        "potasium-rich banan for runners",
    ],
    bnd_en=[
        "curved yellow crescent moon night icon",
        "pineapple tropical fruit with spiky crown",
        "mango yellow tropical stone fruit",
        "yellow lemon citrus fruit for cooking",
        "corn cob yellow with husk peeled back",
        "hot dog sausage in a bun on a plate",
    ],
    valid_en=["yellow banana fruit", "ripe banana icon", "banana for smoothie app"],
    test_en=["banana peel symbol", "bunch of bananas", "banana fruit produce"],
)

# 429
process_icon("bandage",
    st_en=["bandage", "boo boo", "first aid", "ouch"],
    pst_en=[
        "adhesive bandage covering a small cut", "bandage wrapped around a sprained wrist",
        "kiss the boo boo to make it better", "cartoon boo boo with bandage on",
        "first aid kit stocked with bandages", "first aid station at the sports event",
        "ouch that cut needs a bandage fast", "ouch sticker on a child's wound",
    ],
    reg_en=[
        "beige adhesive bandage strip on a finger",
        "bandage crossed diagonally on a wound",
        "first aid bandage for minor cuts and scrapes",
        "wound covered with a sterile bandage",
        "waterproof bandage for swimming after injury",
        "bandage icon for a health and wellness app",
        "emergency bandage applied to a bleeding cut",
        "cartoon-style bandage with crossed lines",
        "bandage pack from the medicine cabinet",
        "medical bandage symbolizing healing and care",
    ],
    conv_en=[
        "I need a bandage icon for my first aid app",
        "add a bandage symbol to the health tracker",
        "show a bandage for the injury log section",
        "use the bandage icon for the wound care reminder",
    ],
    typo_en=[
        "adhesive bandge on the finger",
        "put a bnadage on that cut now",
        "frist aid bandage in the kit",
        "ouch I need a bandege fast",
    ],
    bnd_en=[
        "red cross medical symbol on a white background",
        "syringe needle for an injection icon",
        "pill tablet medication capsule shape",
        "heart pulse heartbeat medical monitor",
        "thermometer reading a fever temperature",
        "hospital bed patient resting icon",
    ],
    valid_en=["adhesive bandage icon", "bandage first aid symbol", "wound bandage strip"],
    test_en=["bandage medical icon", "first aid bandage", "bandage health app"],
)

# 430
process_icon("blueberries",
    st_en=["berry", "bilberry", "blue", "blueberries", "blueberry", "juice"],
    pst_en=[
        "mixed berry smoothie in the blender", "berry picking in the summer field",
        "bilberry growing wild in the forest", "bilberry jam spread on morning toast",
        "blue fruit staining fingers while picking", "blue round berries in a punnet",
        "blueberries scattered on yogurt bowl", "blueberries baked into a muffin",
        "single blueberry plucked from the bush", "blueberry pancakes for Sunday brunch",
        "fresh blueberry juice in a tall glass", "juice pressed from ripe blueberries",
    ],
    reg_en=[
        "cluster of small round blue-purple berries",
        "handful of blueberries in an open palm",
        "blueberry smoothie bowl topped with granola",
        "fresh blueberries at the farmers market stall",
        "blueberry muffin fresh from the oven",
        "antioxidant-rich blueberries in a fruit salad",
        "blueberry bush with ripe fruit in summer",
        "frozen blueberries for a winter smoothie",
        "blueberry pie filling in a pastry shell",
        "blueberries icon for a nutrition tracking app",
    ],
    conv_en=[
        "I need a blueberries icon for my diet app",
        "add a blueberries symbol to the fruit section",
        "show blueberries for the antioxidant foods list",
        "use the blueberries icon for the smoothie builder",
    ],
    typo_en=[
        "fresh blueberirs on the yogurt",
        "bluberries baked in the muffin",
        "blueberies smoothie for breakfast",
        "ripe bluebrries from the garden",
    ],
    bnd_en=[
        "red raspberries clustered on a cane",
        "dark purple grapes in a bunch on the vine",
        "blackberries deep-colored clustered fruit",
        "red cherries pair hanging on a stem",
        "small green peas in a pod",
        "red cranberries in a sauce for Thanksgiving",
    ],
    valid_en=["blueberries fruit icon", "fresh blueberries symbol", "blueberry bowl"],
    test_en=["blueberries smoothie icon", "ripe blueberries produce", "blueberries antioxidant food"],
)

# 431
process_icon("cherries",
    st_en=["berries", "cherries", "cherry", "fruit", "red", "stem"],
    pst_en=[
        "assorted berries in a summer dessert", "wild berries picked from the hedgerow",
        "bowl of cherries on the kitchen counter", "cherries dipped in dark chocolate",
        "cherry on top of an ice cream sundae", "maraschino cherry in a cocktail glass",
        "stone fruit harvest in early summer", "fruit tart topped with fresh cherries",
        "red cherry gleaming with ripe color", "red round cherries hanging on the tree",
        "stem attached to a pair of cherries", "tie the cherry stem with your tongue",
    ],
    reg_en=[
        "two red cherries hanging from a shared green stem",
        "ripe cherry glossy red with a long stem",
        "cherry pair emoji for messaging apps",
        "bowl of sweet cherries fresh from the orchard",
        "cherry blossoms falling like pink snow",
        "sour cherries used for pie filling",
        "cherry on top of a layered sundae",
        "cherry juice dark red in a small glass",
        "cherry season arriving in late spring",
        "cherry icon for a food journaling app",
    ],
    conv_en=[
        "I need a cherries icon for my recipe app",
        "add a cherries symbol to the fruit category",
        "show cherries for the dessert topping section",
        "use the cherries icon for the fresh produce page",
    ],
    typo_en=[
        "pair of cherreis on a green stem",
        "red cheries dipped in chocolate",
        "maraschino chery in the cocktail",
        "fresh cherryes from the orchard",
    ],
    bnd_en=[
        "red strawberry heart-shaped berry with seeds",
        "grapes purple cluster hanging from vine",
        "tomato red round fruit on the vine",
        "apple red round fruit with a stem",
        "cranberries red tart berries in sauce",
        "pomegranate red seeded fruit cut in half",
    ],
    valid_en=["red cherries fruit icon", "pair of cherries on stem", "cherries produce symbol"],
    test_en=["cherries emoji fruit", "fresh cherries icon", "cherry pair dessert"],
)

# 432
process_icon("citrus",
    st_en=["fruit", "grapefruit", "juice", "mandarin", "orange", "tangerine"],
    pst_en=[
        "tropical fruit salad with citrus slices", "fruit basket with lemons and oranges",
        "pink grapefruit halved on the counter", "grapefruit juice squeezed for breakfast",
        "freshly squeezed citrus juice in a glass", "juice bar serving fresh orange and lemon",
        "mandarin orange easy to peel snack", "mandarin segments in a lunchbox",
        "fresh orange cross-section showing segments", "orange peel zested for baking",
        "tangerine small sweet citrus fruit", "tangerine peeled and separated into segments",
    ],
    reg_en=[
        "orange citrus fruit sliced to show juicy segments",
        "cross-section of a grapefruit with pink flesh",
        "pile of ripe citrus fruits on a market stall",
        "citrus juicer squeezing an orange half",
        "vitamin C-rich citrus for a health app",
        "mandarin peeled into segments for a snack",
        "citrus zest grated over a dessert",
        "lemon lime orange tangerine citrus variety",
        "citrus slice icon for a juice bar app",
        "fresh citrus scent icon for a home care product",
    ],
    conv_en=[
        "I need a citrus icon for my nutrition app",
        "add a citrus symbol to the vitamin C section",
        "show a citrus fruit for the juice recipe list",
        "use the citrus icon for the fresh produce category",
    ],
    typo_en=[
        "fresh citurus fruit on the counter",
        "sliced cirtus on a cutting board",
        "grapefruti juice for breakfast",
        "mandaring orange easy to peel",
    ],
    bnd_en=[
        "yellow lemon wedge on a cocktail rim",
        "green lime slice for guacamole",
        "pineapple tropical fruit with spiky leaves",
        "pomelo large pale citrus variety",
        "peach fuzzy stone fruit in summer",
        "mango yellow tropical drupe fruit",
    ],
    valid_en=["citrus fruit icon", "orange citrus slice", "citrus produce symbol"],
    test_en=["citrus juice icon", "grapefruit citrus fruit", "mandarin citrus segment"],
)

# 433
process_icon("dna",
    st_en=["biologist", "dna", "evolution", "gene", "genetic", "genetics", "helix", "life", "molecule", "protein"],
    pst_en=[
        "biologist studying cell samples under a microscope", "biologist sequencing the genome in the lab",
        "dna strand extracted from a blood sample", "dna test revealing ancestry results",
        "evolution from single cell to complex life", "evolution tree showing species divergence",
        "gene expression regulated by enzymes", "gene editing with CRISPR technology",
        "genetic mutation causing inherited disease", "genetic testing for cancer risk",
        "genetics course at the university biology department", "genetics determines eye color and height",
        "double helix structure of the DNA strand", "helix coil rotating animation in a science app",
        "life encoded in a long DNA sequence", "life sciences research in the genomics lab",
        "water molecule with two hydrogen atoms", "molecule bonding in a chemistry diagram",
        "protein folding simulation on a supercomputer", "protein structure determined by gene sequence",
    ],
    reg_en=[
        "double helix DNA strand spiraling upward",
        "colorful DNA illustration with base pairs",
        "genetic code visualized as a twisted ladder",
        "DNA sequencing result in a genomics app",
        "biology textbook diagram of a DNA molecule",
        "ancestry DNA test kit icon for consumer app",
        "CRISPR gene editing tool represented by DNA",
        "protein synthesis shown with DNA and RNA",
        "forensic DNA evidence collected at the scene",
        "DNA icon for a health and genomics platform",
    ],
    conv_en=[
        "I need a DNA icon for my genetics app",
        "add a DNA symbol to the biology section",
        "show a DNA helix for the ancestry feature",
        "use the DNA icon for the genome sequencing tool",
    ],
    typo_en=[
        "double helix DNA stnad spiraling up",
        "gentic testing ancestry results",
        "dna sequencing the gemone sample",
        "double hleix structure of dna",
    ],
    bnd_en=[
        "microscope lab instrument for viewing cells",
        "atom nucleus with electron orbits",
        "test tube with chemical reaction inside",
        "chromosome X shape from cell division",
        "petri dish with bacterial colony growing",
        "flask beaker laboratory glassware icon",
    ],
    valid_en=["DNA double helix icon", "genetics DNA strand", "DNA biology symbol"],
    test_en=["DNA sequencing icon", "helix gene symbol", "DNA molecule science app"],
)

# 434
process_icon("handshake",
    st_en=["agreement", "greeting", "meeting", "partnership"],
    pst_en=[
        "business agreement sealed with a handshake", "agreement signed after negotiation",
        "friendly greeting with a firm handshake", "greeting colleagues at the conference",
        "formal meeting opened with a handshake", "first meeting between two team leads",
        "startup partnership formed with a handshake", "partnership deal announced at the summit",
    ],
    reg_en=[
        "two hands clasped together in a handshake",
        "firm business handshake sealing a deal",
        "friendly greeting handshake at a networking event",
        "handshake icon for a contracts and agreements app",
        "partnership represented by two joined hands",
        "diplomatic handshake between two parties",
        "handshake emoji for approval or deal confirmation",
        "client and consultant shaking hands after a meeting",
        "trust and cooperation symbolized by a handshake",
        "handshake for a collaboration or team-building feature",
    ],
    conv_en=[
        "I need a handshake icon for my partnership app",
        "add a handshake symbol to the deals section",
        "show a handshake for the agreement confirmation screen",
        "use the handshake icon for the networking feature",
    ],
    typo_en=[
        "firm handshake selaing the deal",
        "busniess handshake at the meeting",
        "partnershi confirmed with a handshake",
        "greeting handshke at the conference",
    ],
    bnd_en=[
        "fist bump casual greeting between friends",
        "high five celebration slap hands upward",
        "waving hand hello or goodbye gesture",
        "thumbs up approval like or agree icon",
        "clapping hands applause celebration gesture",
        "praying hands pressed together emoji",
    ],
    valid_en=["handshake agreement icon", "business handshake symbol", "handshake partnership"],
    test_en=["two hands handshake", "handshake deal icon", "greeting handshake symbol"],
)

# 435
process_icon("pump",
    st_en=["drain", "flood", "pump", "sump", "water"],
    pst_en=[
        "drain the flooded basement with a pump", "drain pipe clearing a blocked channel",
        "flood water rising in the street", "flood relief pump deployed by emergency team",
        "water pump transferring liquid between tanks", "pump running to empty the pool",
        "sump pump activating in heavy rain", "sump pit with float switch trigger",
        "water pump station for municipal supply", "water flowing through the pump outlet",
    ],
    reg_en=[
        "mechanical water pump with inlet and outlet",
        "sump pump in the basement keeping it dry",
        "flood control pump running continuously",
        "electric pump moving water uphill",
        "garden water pump for irrigation system",
        "pump icon for a plumbing services app",
        "fire truck pump delivering water at high pressure",
        "hand pump drawing water from a well",
        "drain pump clearing standing water after a storm",
        "industrial pump for liquid transfer operations",
    ],
    conv_en=[
        "I need a pump icon for my home maintenance app",
        "add a pump symbol to the plumbing section",
        "show a pump for the flood control feature",
        "use the pump icon for the water management tool",
    ],
    typo_en=[
        "supm pump running in the basement",
        "flood watr pump at the drain",
        "watter pump moving liquid uphill",
        "draining the floood with a pump",
    ],
    bnd_en=[
        "faucet tap dripping water from a sink",
        "water droplet single blue teardrop icon",
        "pipe wrench plumbing repair tool",
        "fire hydrant red street emergency water supply",
        "water tower large storage tank on stilts",
        "swimming pool with lane dividers aerial view",
    ],
    valid_en=["water pump icon", "sump pump symbol", "pump drainage tool"],
    test_en=["flood pump icon", "pump water transfer", "drain pump symbol"],
)

# 436
process_icon("refrigerator",
    st_en=["cold", "cool", "freezer", "fridge", "icebox", "kitchen"],
    pst_en=[
        "keep food cold in the refrigerator", "cold storage for fresh vegetables",
        "cool environment preserving dairy products", "cool air circulating inside the fridge",
        "freezer compartment holding frozen meals", "freezer full of ice cream and peas",
        "fridge door opened to grab a snack", "fridge stocked with leftovers and drinks",
        "old icebox before modern refrigeration", "icebox keeps drinks cold on a summer day",
        "kitchen appliance lineup including the refrigerator", "kitchen fridge next to the oven",
    ],
    reg_en=[
        "tall white refrigerator with two doors",
        "stainless steel fridge in a modern kitchen",
        "refrigerator full of fresh produce and drinks",
        "fridge door covered with family photos and magnets",
        "smart refrigerator with a touchscreen panel",
        "mini fridge in a dorm room or office",
        "refrigerator icon for a grocery or meal app",
        "freezer drawer at the bottom of the fridge",
        "energy-efficient refrigerator with A++ rating",
        "refrigerator compressor humming in the kitchen",
    ],
    conv_en=[
        "I need a refrigerator icon for my kitchen app",
        "add a fridge symbol to the food storage section",
        "show a refrigerator for the grocery tracker",
        "use the fridge icon for the meal planning feature",
    ],
    typo_en=[
        "stock the refirgerator with fresh food",
        "frideg door left open accidentally",
        "frezer compartment full of ice cream",
        "kicthen refridgerator stainless steel",
    ],
    bnd_en=[
        "microwave oven with rotating turntable",
        "washing machine front-loading laundry appliance",
        "dishwasher kitchen appliance with clean dishes",
        "oven range with burners on top",
        "air conditioner wall unit cooling the room",
        "chest freezer large standalone deep freeze",
    ],
    valid_en=["refrigerator kitchen appliance", "fridge food storage icon", "refrigerator symbol"],
    test_en=["fridge icon for kitchen", "refrigerator cold storage", "fridge appliance symbol"],
)

# 437
process_icon("signature",
    st_en=["cursive", "name", "username", "writing"],
    pst_en=[
        "cursive script flowing across the page", "cursive handwriting in a personal letter",
        "sign your name at the bottom of the form", "name written in a stylized signature",
        "create a username for your profile", "username displayed on the login screen",
        "writing a signature on the dotted line", "writing your autograph on a document",
    ],
    reg_en=[
        "handwritten signature on a contract document",
        "stylized cursive signature with a flourish",
        "e-signature captured on a touch screen",
        "doctor's illegible signature on a prescription",
        "autograph signed by a celebrity on a photo",
        "digital signature field in a PDF form",
        "signature icon for a document signing app",
        "ink pen signing a legal agreement",
        "signature verification for identity check",
        "unique handwritten name as a personal mark",
    ],
    conv_en=[
        "I need a signature icon for my contract app",
        "add a signature symbol to the document signing screen",
        "show a signature for the approval workflow",
        "use the signature icon for the e-sign feature",
    ],
    typo_en=[
        "sign your signaure on the dotted line",
        "cursive signtaure on the contract",
        "handwriten signatre looks unique",
        "digital signture captured on the pad",
    ],
    bnd_en=[
        "pen writing on paper open notepad",
        "pencil sketching a drawing on paper",
        "stamp seal impression on a document",
        "fingerprint unique biometric identifier",
        "certificate with ribbon and wax seal",
        "handwriting text flowing cursive script",
    ],
    valid_en=["handwritten signature icon", "e-signature symbol", "cursive signature mark"],
    test_en=["signature contract icon", "sign document symbol", "signature writing icon"],
)

# 438
process_icon("siren",
    st_en=["alarm", "alert", "ambulance", "loud", "police", "warning"],
    pst_en=[
        "alarm sounding at the fire station", "alarm triggered by smoke detector",
        "emergency alert notification on the phone", "weather alert siren outdoors",
        "ambulance siren blaring through traffic", "ambulance arriving at the accident scene",
        "loud siren echoing through the city", "loud horn warning pedestrians",
        "police siren flashing blue and red lights", "police car speeding with siren on",
        "warning siren activated during tornado drill", "warning light spinning on the rooftop",
    ],
    reg_en=[
        "rotating red emergency siren on a vehicle roof",
        "flashing police siren with blue and red light",
        "ambulance siren blaring at full volume",
        "tornado warning siren mounted on a pole",
        "fire alarm siren ringing in the building",
        "siren icon for an emergency alert app",
        "civil defense siren during a public test",
        "loud warning siren for evacuation order",
        "security alarm siren triggered by intruder",
        "rotating beacon siren on a construction vehicle",
    ],
    conv_en=[
        "I need a siren icon for my emergency alert app",
        "add a siren symbol to the alarm section",
        "show a siren for the warning notification feature",
        "use the siren icon for the emergency mode screen",
    ],
    typo_en=[
        "police siren flahsing red and blue",
        "emergency sirne blaring loudly",
        "ambulancce siren through traffic",
        "warning siren durign tornado drill",
    ],
    bnd_en=[
        "bell ringing for a notification alert",
        "megaphone announcement loudspeaker icon",
        "horn blowing instrument or boat signal",
        "fire extinguisher red canister safety tool",
        "traffic light red yellow green signal",
        "speaker audio sound output icon",
    ],
    valid_en=["emergency siren icon", "police siren alarm", "warning siren symbol"],
    test_en=["siren alert symbol", "ambulance siren icon", "rotating siren warning"],
)

# 439
process_icon("sunglasses",
    st_en=["bright", "cool", "dark", "eye", "eyewear", "glasses", "shades", "sunglasses"],
    pst_en=[
        "bright sunshine calling for shades", "bright UV rays blocked by tinted lenses",
        "cool look with retro sunglasses on", "cool celebrity wearing oversized shades",
        "dark tinted lenses filtering sunlight", "dark lenses reducing glare on water",
        "eye protection from harmful UV rays", "eye care icon for an optometry app",
        "fashionable eyewear on the beach", "prescription eyewear with tinted lenses",
        "glasses frames without lenses for style", "reading glasses versus sunglasses",
        "designer shades on a summer holiday", "retro shades with mirrored lenses",
        "sunglasses emoji showing a cool expression", "sunglasses left on the dashboard in summer",
    ],
    reg_en=[
        "pair of sunglasses with dark oval lenses",
        "retro wayfarer-style sunglasses in black",
        "sunglasses resting on the nose at the beach",
        "mirrored aviator sunglasses for outdoor sports",
        "UV-blocking sunglasses for sunny weather",
        "cool emoji face with sunglasses on",
        "fashionable sunglasses in a style app",
        "sunglasses hanging on a shirt collar",
        "polarized sunglasses reducing glare on water",
        "sunglasses icon for a travel or summer app",
    ],
    conv_en=[
        "I need a sunglasses icon for my style app",
        "add a sunglasses symbol to the summer essentials list",
        "show sunglasses for the UV protection reminder",
        "use the sunglasses icon for the cool look badge",
    ],
    typo_en=[
        "stylish sunglases at the beach",
        "retro sungalsses with mirrored lens",
        "dark shades blokcing UV rays",
        "cool sunglasess emoji expression",
    ],
    bnd_en=[
        "reading glasses clear lens for close-up text",
        "safety goggles sealed protective eyewear",
        "monocle single lens on a chain",
        "ski goggles foam-sealed winter eye protection",
        "magnifying glass with a handle for inspection",
        "VR headset virtual reality goggles device",
    ],
    valid_en=["sunglasses UV protection icon", "shades summer symbol", "sunglasses eyewear icon"],
    test_en=["sunglasses cool emoji", "dark shades sunglasses", "sunglasses beach symbol"],
)

# 440
process_icon("wave",
    st_en=["barrel", "beach", "break", "shore", "surf", "tsunami", "water", "wave"],
    pst_en=[
        "barrel wave forming a perfect tube", "barrel roll inside a breaking wave",
        "beach waves crashing on the sand", "beach vacation with rolling surf",
        "wave breaking on the rocky shore", "break point where surfers wait",
        "foamy shore where waves meet land", "shore walk watching waves roll in",
        "surf session catching big waves", "surf forecast showing swell height",
        "massive tsunami wave approaching the coast", "tsunami warning issued for coastal areas",
        "water ripple expanding outward", "water current moving in the ocean",
        "ocean wave crest rising and falling", "wave pattern decorative border",
    ],
    reg_en=[
        "curling ocean wave with white foam crest",
        "surfer riding inside the barrel of a big wave",
        "wave icon for a beach or surf forecast app",
        "tsunami alert shown with a massive wave symbol",
        "gentle shore waves lapping on the sand",
        "ocean swell building offshore before breaking",
        "wave pattern used as a decorative divider",
        "blue water wave emoji for messaging",
        "storm wave crashing against the sea wall",
        "wave height measurement on a surf report",
    ],
    conv_en=[
        "I need a wave icon for my surf app",
        "add a wave symbol to the ocean conditions section",
        "show a wave for the beach forecast feature",
        "use the wave icon for the tsunami alert page",
    ],
    typo_en=[
        "surfing the bareel wave at the point",
        "ocean waev crashing on the beach",
        "tusnami wave warning on the coast",
        "suft forecast for big wave conditions",
    ],
    bnd_en=[
        "water droplet single blue teardrop falling",
        "swimming person doing laps in a pool",
        "sailboat on calm water with white sail",
        "rain cloud with water drops falling",
        "river winding through a landscape",
        "wind turbine spinning in a coastal breeze",
    ],
    valid_en=["ocean wave icon", "surf wave symbol", "wave beach icon"],
    test_en=["wave crashing shore", "tsunami wave alert", "wave surf forecast icon"],
)

print("\nDone! All 13 icons processed.")
