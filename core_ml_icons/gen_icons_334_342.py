#!/usr/bin/env python3
"""Generate English training data for icons 334-342."""
from pathlib import Path
import csv, json

icons_dir = Path("icons")
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

# 334
process_icon("droplet",
    st_en=["blood", "cold", "color", "comic", "drop", "droplet", "raindrop", "sweat", "waterdrop"],
    pst_en=[
        "blood droplet from a finger prick", "blood drop for the medical test",
        "cold water droplet on the glass", "cold droplet falling from the tap",
        "color dropper picking a color", "color droplet in the design tool",
        "comic sweat drop on the face", "comic droplet symbol of surprise",
        "drop of water on the leaf", "drop falling from the faucet",
        "droplet of water on the surface", "single droplet in the air",
        "raindrop falling from the sky", "raindrop hitting the puddle",
        "sweat droplet on the forehead", "sweat drop after a workout",
        "waterdrop on the window pane", "waterdrop rolling down the glass",
    ],
    reg_en=[
        "single water droplet falling",
        "raindrop hitting the puddle",
        "sweat droplet after a hard workout",
        "blood drop for a medical test",
        "water drop on a green leaf",
        "color picker droplet in the design app",
        "dew droplet on the morning grass",
        "droplet icon for water or hydration",
        "teardrop falling from the eye",
        "ink droplet falling into the water",
    ],
    conv_en=[
        "I need a droplet icon for the hydration tracker",
        "add a water drop to the weather section",
        "show a droplet for the color picker tool",
        "use the drop icon for the blood test feature",
    ],
    typo_en=[
        "raindorp falling from sky",
        "watre droplet on glass",
        "sweatt drop after workout",
        "blod drop for test",
    ],
    bnd_en=[
        "rain cloud with drops falling below",
        "wave of water crashing on shore",
        "ice cube melting into water",
        "bucket filling with water",
        "swimming pool with clear water",
        "river flowing through the valley",
    ],
    valid_en=["water droplet falling", "raindrop on the glass", "droplet for hydration"],
    test_en=["droplet icon", "water drop symbol", "raindrop droplet"],
)

# 335
process_icon("ear",
    st_en=["body", "ear", "head", "hearing", "listen", "lobe"],
    pst_en=[
        "ear as a body part", "body ear anatomy",
        "human ear close-up", "ear icon for sound",
        "ear on the side of the head", "head ear hearing symbol",
        "hearing aid in the ear", "ear hearing check",
        "listen with your ear", "ear listen for sounds",
        "ear lobe with earring", "lobe of the ear",
    ],
    reg_en=[
        "human ear with lobe and canal",
        "ear icon for audio or sound settings",
        "hearing test at the audiologist",
        "ear with a hearing aid device",
        "ear listening to the music",
        "anatomy diagram of the ear",
        "ear symbol for accessibility settings",
        "ear pressed against the wall to listen",
        "earring hanging from the ear lobe",
        "ear protection worn at the loud event",
    ],
    conv_en=[
        "I need an ear icon for the hearing accessibility feature",
        "add an ear symbol to the audio settings",
        "show an ear for the listen button",
        "use the ear icon for the sound section",
    ],
    typo_en=[
        "huamn ear canal",
        "hrearing test today",
        "eear lobe earring",
        "listten with your ear",
    ],
    bnd_en=[
        "headphones covering both ears",
        "microphone for recording sound",
        "speaker playing music loudly",
        "eye icon for visibility",
        "nose above the lips on a face",
        "hand cupped behind the ear to hear",
    ],
    valid_en=["human ear with lobe", "ear icon for hearing", "listen with your ear"],
    test_en=["ear icon", "ear symbol for sound", "hearing ear"],
)

# 336
process_icon("engine",
    st_en=["car", "engine"],
    pst_en=[
        "car engine under the hood", "car engine warning light",
        "engine running in the vehicle", "engine power symbol",
    ],
    reg_en=[
        "car engine under the open hood",
        "engine warning light on the dashboard",
        "powerful engine roaring at startup",
        "engine maintenance at the garage",
        "diesel engine of the truck",
        "engine cylinder block in the shop",
        "electric engine of the EV",
        "engine oil check before the trip",
        "turbocharged engine for performance",
        "engine icon for the car settings",
    ],
    conv_en=[
        "I need an engine icon for the car diagnostics app",
        "add an engine symbol to the vehicle section",
        "show an engine for the car maintenance feature",
        "use the engine icon for the power settings",
    ],
    typo_en=[
        "car enigne warning light",
        "egnine under the hood",
        "enigne oil check",
        "car engien power",
    ],
    bnd_en=[
        "car wheel and tire on the road",
        "steering wheel in the cockpit",
        "fuel gauge showing low tank",
        "gear shift lever in the car",
        "exhaust pipe emitting smoke",
        "battery icon for the electric car",
    ],
    valid_en=["car engine under the hood", "engine warning light", "engine maintenance symbol"],
    test_en=["engine icon", "car engine symbol", "engine for vehicle"],
)

# 337
process_icon("fingerprint",
    st_en=["human", "id", "identification", "lock", "privacy", "smudge", "touch", "unique", "unlock"],
    pst_en=[
        "human fingerprint on the surface", "human fingerprint unique pattern",
        "ID fingerprint for identification", "fingerprint ID on the phone",
        "identification by fingerprint", "fingerprint identification system",
        "fingerprint lock on the device", "lock the phone with fingerprint",
        "privacy protected by fingerprint", "fingerprint for user privacy",
        "smudge fingerprint on the glass", "fingerprint smudge on the screen",
        "touch fingerprint sensor", "touch the fingerprint scanner",
        "unique fingerprint pattern", "unique fingerprint of every person",
        "unlock with fingerprint", "fingerprint to unlock the phone",
    ],
    reg_en=[
        "fingerprint scanner on the phone",
        "unique fingerprint pattern for identification",
        "fingerprint unlock on the lock screen",
        "biometric fingerprint for security",
        "fingerprint smudge left on the glass",
        "fingerprint reader at the office door",
        "fingerprint ID for border control",
        "touch ID fingerprint sensor",
        "fingerprint captured for the database",
        "forensic fingerprint on the evidence",
    ],
    conv_en=[
        "I need a fingerprint icon for the biometric login",
        "add a fingerprint symbol to the security settings",
        "show a fingerprint for the touch ID feature",
        "use the fingerprint icon for the unlock screen",
    ],
    typo_en=[
        "fingerpirnt scanner",
        "biometrc fingerprint",
        "uniqe fingerprint pattern",
        "fingerpint unlock",
    ],
    bnd_en=[
        "face ID scan for biometric login",
        "retina eye scan for identification",
        "PIN code entry on the keypad",
        "access card with magnetic strip",
        "password field on the login screen",
        "hand scan for biometric authentication",
    ],
    valid_en=["fingerprint scanner on phone", "unique fingerprint pattern", "fingerprint unlock"],
    test_en=["fingerprint icon", "fingerprint symbol for security", "touch fingerprint"],
)

# 338
process_icon("fire",
    st_en=["burn", "caliente", "fire", "flame", "heat", "hot", "popular", "tool"],
    pst_en=[
        "burn the wood with fire", "fire burning the logs",
        "caliente fire keeping warm", "caliente flame in the heat",
        "fire burning at the campsite", "fire icon for the app",
        "flame of the candle", "flame burning bright",
        "heat from the fire", "fire heat warming the room",
        "hot fire on the grill", "hot flame burning",
        "popular trending fire icon", "fire symbol for popular content",
        "fire as a tool for cooking", "tool fire for the campsite",
    ],
    reg_en=[
        "orange flame burning bright",
        "campfire flames crackling at night",
        "fire emoji for hot or trending",
        "fire burning in the fireplace",
        "flame icon for a spicy dish",
        "wildfire spreading through the forest",
        "fire on the gas stove burner",
        "fire hazard warning symbol",
        "fire showing popular or viral content",
        "birthday candle flame on the cake",
    ],
    conv_en=[
        "I need a fire icon for the trending section",
        "add a flame symbol to the hot items list",
        "show a fire for the spicy food category",
        "use the fire icon for the streak counter",
    ],
    typo_en=[
        "frie burning bright",
        "campfier flames",
        "flmae of the candle",
        "populr fire icon",
    ],
    bnd_en=[
        "campfire with logs burning at the campsite",
        "explosion with a burst of light",
        "sun radiating heat in the sky",
        "lava flowing from the volcano",
        "candle flame on the dinner table",
        "sparkler held at the celebration",
    ],
    valid_en=["fire flame burning bright", "fire icon for trending", "flame for hot content"],
    test_en=["fire icon", "flame symbol", "fire for popular"],
)

# 339
process_icon("headphones",
    st_en=["audio", "earbud", "headphone", "listen", "music", "sound", "speaker"],
    pst_en=[
        "audio headphones for the studio", "audio quality headphones",
        "earbud headphone for music", "earbud in the ear",
        "headphone over the ears", "headphone for the DJ set",
        "listen with headphones", "listen to music with headphones",
        "music headphones on", "music playing through headphones",
        "sound coming through headphones", "headphones for good sound",
        "speaker in the headphone", "headphone speaker quality",
    ],
    reg_en=[
        "over-ear headphones for the recording studio",
        "wireless headphones connected by Bluetooth",
        "DJ headphones at the mixing deck",
        "noise-cancelling headphones on the plane",
        "headphones resting around the neck",
        "in-ear headphones with a microphone",
        "headphones plugged into the audio jack",
        "headphones icon for music player",
        "gaming headset with surround sound",
        "headphones hung on the monitor stand",
    ],
    conv_en=[
        "I need a headphones icon for the music app",
        "add headphones to the audio settings section",
        "show headphones for the podcast feature",
        "use the headphones icon for the sound controls",
    ],
    typo_en=[
        "headphoens for music",
        "wireles headphones",
        "hsadphones on ears",
        "udio headphones quality",
    ],
    bnd_en=[
        "ear with a hearing aid",
        "speaker mounted on the wall",
        "microphone on the desk stand",
        "earbuds connected to the phone",
        "sound wave equalizer display",
        "radio with antenna playing music",
    ],
    valid_en=["headphones for music listening", "wireless headphones icon", "headphones for audio"],
    test_en=["headphones icon", "headphones symbol for music", "over-ear headphones"],
)

# 340
process_icon("hospital",
    st_en=["building", "covid-19", "doctor", "emergency room", "hospital", "medical center", "medicine"],
    pst_en=[
        "hospital building in the city", "building with a red cross hospital",
        "hospital during the covid-19 pandemic", "covid-19 patients in the hospital",
        "doctor at the hospital", "doctor working in the hospital ward",
        "emergency room at the hospital", "emergency room visit at night",
        "hospital icon on the map", "hospital building symbol",
        "medical center hospital", "medical center building",
        "medicine dispensed at the hospital", "hospital medicine cabinet",
    ],
    reg_en=[
        "large hospital building with a red cross",
        "emergency room entrance at the hospital",
        "hospital ward with patients and nurses",
        "hospital on the city map pin",
        "ambulance arriving at the hospital",
        "hospital reception desk with staff",
        "hospital icon for the health app",
        "children's hospital in the neighborhood",
        "hospital operating room for surgery",
        "hospital bed in the patient room",
    ],
    conv_en=[
        "I need a hospital icon for the health map",
        "add a hospital symbol to the emergency section",
        "show a hospital for the nearest clinic feature",
        "use the hospital icon for the medical center page",
    ],
    typo_en=[
        "hospitl building",
        "emregency room visit",
        "hosiptal on the map",
        "docter at hospital",
    ],
    bnd_en=[
        "pharmacy with a green cross sign",
        "clinic office building for appointments",
        "ambulance with sirens on the road",
        "first aid kit with red cross",
        "doctor's stethoscope on the desk",
        "church building with a steeple",
    ],
    valid_en=["hospital building with red cross", "emergency room at hospital", "hospital on the map"],
    test_en=["hospital icon", "hospital building symbol", "medical center hospital"],
)

# 341
process_icon("kettlebell",
    st_en=["exercise", "gym", "strength", "weight", "workout"],
    pst_en=[
        "exercise with the kettlebell", "kettlebell exercise routine",
        "gym kettlebell on the floor", "kettlebell in the gym",
        "strength training with kettlebell", "build strength with kettlebell",
        "kettlebell weight for lifting", "weight of the kettlebell",
        "workout with kettlebell swings", "kettlebell workout session",
    ],
    reg_en=[
        "cast iron kettlebell on the gym floor",
        "kettlebell swing exercise for strength",
        "kettlebell snatch at the crossfit gym",
        "row of kettlebells in different weights",
        "kettlebell pressed overhead",
        "kettlebell deadlift for the lower back",
        "kettlebell workout for endurance",
        "kettlebell goblet squat exercise",
        "kettlebell Turkish get-up movement",
        "home gym with kettlebells and dumbbells",
    ],
    conv_en=[
        "I need a kettlebell icon for the fitness app",
        "add a kettlebell symbol to the strength section",
        "show a kettlebell for the workout category",
        "use the kettlebell icon for the gym equipment list",
    ],
    typo_en=[
        "kettlebal swing",
        "kttlebell weight",
        "gymn kettlebell",
        "workuot with kettlebell",
    ],
    bnd_en=[
        "dumbbell pair on the weight rack",
        "barbell loaded with plates",
        "weight plate stacked on the floor",
        "medicine ball on the gym mat",
        "resistance band for stretching",
        "pull-up bar mounted in the doorway",
    ],
    valid_en=["kettlebell for strength training", "gym kettlebell workout", "kettlebell exercise"],
    test_en=["kettlebell icon", "kettlebell symbol for gym", "kettlebell workout"],
)

# 342
process_icon("lamp",
    st_en=["bright", "furniture", "light"],
    pst_en=[
        "bright lamp lighting the room", "bright light from the lamp",
        "lamp as a furniture piece", "furniture lamp in the living room",
        "lamp providing light at night", "light from the reading lamp",
    ],
    reg_en=[
        "floor lamp standing in the living room corner",
        "desk lamp lighting the work surface",
        "table lamp with a fabric shade",
        "reading lamp beside the bed",
        "adjustable lamp for the home office",
        "lamp turned on at dusk",
        "vintage lamp with a warm glow",
        "lamp icon for the lighting control",
        "lamp shade casting soft light",
        "smart lamp controlled from the phone",
    ],
    conv_en=[
        "I need a lamp icon for the smart home app",
        "add a lamp symbol to the lighting controls",
        "show a lamp for the room ambiance feature",
        "use the lamp icon for the reading mode",
    ],
    typo_en=[
        "desk lmap lighting",
        "flooor lamp corner",
        "bight lamp shade",
        "furniutre lamp",
    ],
    bnd_en=[
        "ceiling light fixture with bulbs",
        "light bulb with glowing filament",
        "candle flame on the table",
        "flashlight beam in the dark",
        "lantern hanging at the entrance",
        "street light on the pole at night",
    ],
    valid_en=["desk lamp lighting the room", "reading lamp by the bed", "lamp for light control"],
    test_en=["lamp icon", "lamp symbol for light", "floor lamp furniture"],
)
