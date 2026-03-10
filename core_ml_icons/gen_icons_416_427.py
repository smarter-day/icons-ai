#!/usr/bin/env python3
"""Generate English training data for icons 416-427."""
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

# 416
process_icon("cucumber",
    st_en=["cuke", "pickle", "zucchini"],
    pst_en=[
        "fresh cuke sliced on a salad", "cuke harvested from the garden",
        "jar of pickle on the shelf", "sour pickle spear with dill",
        "zucchini grilled with olive oil", "zucchini spiral noodle dish",
    ],
    reg_en=[
        "long green cucumber with bumpy skin",
        "sliced cucumber rounds on a salad plate",
        "fresh cucumber from the vegetable garden",
        "cucumber used in cold gazpacho soup",
        "crisp cucumber stick for a healthy snack",
        "cucumber emoji for a recipe app",
        "whole cucumber vegetable ingredient",
        "cool cucumber slices on a spa towel",
        "pickled cucumber in a mason jar",
        "cucumber cross-section showing seeds inside",
    ],
    conv_en=[
        "I need a cucumber icon for my recipe app",
        "add a cucumber symbol to the vegetable category",
        "show a cucumber for the salad ingredient list",
        "use the cucumber icon for the fresh produce section",
    ],
    typo_en=[
        "cucumbre salad ingredient",
        "pickled cucmber in brine",
        "zukcchini grilled vegetable",
        "cuecumber garden harvest",
    ],
    bnd_en=[
        "green zucchini summer squash on cutting board",
        "coiled snake green serpent icon",
        "banana yellow curved fruit",
        "celery stalk with leafy top",
        "asparagus spear bundled together",
        "corn cob with yellow kernels",
    ],
    valid_en=["fresh cucumber vegetable", "cucumber sliced for salad", "garden cucumber icon"],
    test_en=["pickle jar icon", "cucumber produce section", "green vegetable cucumber"],
)

# 417
process_icon("football",
    st_en=["ball", "fall", "football", "nfl", "pigskin", "seasonal"],
    pst_en=[
        "oval ball thrown in a spiral", "ball kicked for a field goal",
        "football game in the fall season", "fall Sunday watching football",
        "football flying through the air", "throw a football to the receiver",
        "nfl game highlights on Sunday", "nfl logo with football laces",
        "classic pigskin tossed across the yard", "pigskin spiral pass downfield",
        "seasonal football decor for autumn", "seasonal sport icon for fall events",
    ],
    reg_en=[
        "brown oval football with white laces",
        "american football spiraling through the air",
        "football icon for a sports tracking app",
        "NFL game day with a leather pigskin",
        "football player throwing a long pass",
        "kicked football sailing between the goalposts",
        "football season kicking off in September",
        "deflated football on the grass sideline",
        "football used in yard game with friends",
        "pro football worn with scuff marks",
    ],
    conv_en=[
        "I need a football icon for my sports app",
        "add a football symbol to the game schedule screen",
        "show a football for the NFL news section",
        "use the football icon for the touchdown tracker",
    ],
    typo_en=[
        "footbal game on Sunday",
        "american fotball season",
        "pigsikn spiral throw",
        "footbll touchdown celebration",
    ],
    bnd_en=[
        "round black and white soccer ball kicked on a field",
        "oval rugby ball with pointed ends",
        "basketball orange sphere with black lines",
        "tennis ball yellow fuzzy sphere on court",
        "volleyball white and blue panel ball",
        "baseball white ball with red stitching",
    ],
    valid_en=["american football icon", "pigskin oval ball", "football for sports app"],
    test_en=["NFL football laces", "football game symbol", "oval football ball"],
)

# 418
process_icon("hands",
    st_en=["asl", "deaf", "hands"],
    pst_en=[
        "asl alphabet fingerspelling letter", "asl interpreter signing at event",
        "deaf community using sign language", "deaf awareness month symbol",
        "two hands open facing up", "hands raised in greeting gesture",
    ],
    reg_en=[
        "two open hands facing upward in sign language",
        "sign language interpreter hands in motion",
        "ASL hands spelling a word gesture",
        "deaf community hand communication symbol",
        "raised hands together for applause",
        "open palms facing each other for exchange",
        "hands icon for accessibility features",
        "two hands used in American Sign Language",
        "cupped hands holding something gently",
        "hands gesturing during conversation",
    ],
    conv_en=[
        "I need a hands icon for my accessibility settings",
        "add a hands symbol to the sign language section",
        "show hands for the ASL interpreter feature",
        "use the hands icon for the deaf community page",
    ],
    typo_en=[
        "hads signing asl gesture",
        "sign langauge hands icon",
        "asl hande spelling alphabet",
        "deaf communtiy hands signal",
    ],
    bnd_en=[
        "single hand waving hello gesture",
        "handshake two people greeting each other",
        "thumbs up approval like button",
        "praying hands pressed together emoji",
        "clapping hands applause celebration",
        "pointing finger cursor direction arrow",
    ],
    valid_en=["sign language hands", "ASL hands symbol", "two hands open gesture"],
    test_en=["deaf hands icon", "hands signing ASL", "accessibility hands symbol"],
)

# 419
process_icon("peach",
    st_en=["butt", "fruit", "peach", "pit", "stone"],
    pst_en=[
        "peach butt emoji cheeky symbol", "butt icon for playful messaging",
        "sweet summer fruit on the table", "tropical fruit basket with mango",
        "ripe peach fresh from the orchard", "peach jam spread on toast",
        "peach with the pit removed", "hard pit inside a ripe peach",
        "stone fruit like plum and cherry", "stone fruit drupe with fuzzy skin",
    ],
    reg_en=[
        "round fuzzy peach with pink and orange skin",
        "ripe peach dripping with sweet juice",
        "peach emoji for messaging and social apps",
        "fresh peach from the farmers market",
        "sliced peach on top of yogurt",
        "peach cobbler filling made from summer fruit",
        "whole peach with green leaf attached",
        "peach stone fruit in the orchard",
        "grilled peach half for a summer dessert",
        "peach icon for a fruit tracker app",
    ],
    conv_en=[
        "I need a peach icon for my recipe app",
        "add a peach symbol to the summer fruit section",
        "show a peach for the orchard produce page",
        "use the peach icon for the smoothie ingredient list",
    ],
    typo_en=[
        "ripe peche from the orchard",
        "fuzzy peack on the counter",
        "summer peeach dessert topping",
        "peach smothie blended drink",
    ],
    bnd_en=[
        "ripe mango yellow tropical fruit with seed",
        "fuzzy kiwi brown oval fruit with green inside",
        "apricot small orange stone fruit",
        "plum purple drupe fruit on branch",
        "nectarine smooth-skinned variety of peach",
        "orange citrus fruit round with dimpled skin",
    ],
    valid_en=["fresh peach fruit", "ripe peach icon", "peach summer fruit"],
    test_en=["peach emoji icon", "fuzzy peach orchard", "stone fruit peach"],
)

# 420
process_icon("seedling",
    st_en=["environment", "flora", "grow", "investment", "plant", "sapling", "seedling", "vegan", "young"],
    pst_en=[
        "protect the environment planting trees", "environment conservation green icon",
        "wild flora blooming in the meadow", "flora and fauna preservation effort",
        "watch a tiny plant grow over time", "grow your own herbs on the windowsill",
        "startup investment growing like a seedling", "investment portfolio growing steadily",
        "small plant emerging from the soil", "potted plant on a sunny windowsill",
        "young sapling planted in the forest", "sapling tree growing in spring",
        "seedling sprouting from the ground", "seedling planted in a paper cup",
        "vegan lifestyle represented by a plant", "vegan diet with fresh greens",
        "young plant just beginning to sprout", "young growth in the garden bed",
    ],
    reg_en=[
        "tiny green seedling with two leaves emerging from soil",
        "plant sprout just breaking through the ground",
        "seedling growing in a small biodegradable pot",
        "ecology icon showing new green growth",
        "reforestation seedling planted by volunteers",
        "spring gardening with seedlings in a tray",
        "sustainable farming with young plant starts",
        "growth metaphor seedling for startup apps",
        "vegan and eco-friendly seedling symbol",
        "baby plant icon for a gardening tracker",
    ],
    conv_en=[
        "I need a seedling icon for my garden app",
        "add a seedling symbol to the eco section",
        "show a seedling for the plant growth tracker",
        "use the seedling icon for the sustainability page",
    ],
    typo_en=[
        "small seeedling sprouting from soil",
        "saplign planted in the forest",
        "tiny seedlign with two leaves",
        "grwoing plant in a garden pot",
    ],
    bnd_en=[
        "full grown oak tree with spreading branches",
        "green leaf single smooth oval shape",
        "flower blossom with petals open in spring",
        "potted cactus succulent on a windowsill",
        "wheat stalk grain crop in a field",
        "herb bundle fresh basil tied together",
    ],
    valid_en=["seedling sprouting icon", "small plant growing", "eco seedling symbol"],
    test_en=["plant seedling green", "sapling sprout icon", "young plant growing"],
)

# 421
process_icon("snooze",
    st_en=["alarm", "comic", "nap", "rest", "siesta", "sleep", "zzz"],
    pst_en=[
        "alarm clock snooze button tapped", "morning alarm going off again",
        "comic book zzz sleeping bubble", "comic speech bubble with snoring",
        "afternoon nap on the couch", "power nap during lunch break",
        "rest after a long workout", "rest and recovery mode enabled",
        "midday siesta in warm weather", "siesta tradition in Spanish culture",
        "deep sleep overnight rest icon", "sleep tracking app badge",
        "zzz floating above sleeping character", "zzz bubbles drifting from a sleeper",
    ],
    reg_en=[
        "snooze button tapped on an alarm clock",
        "zzz bubbles floating above a sleeping person",
        "alarm dismissed for another ten minutes",
        "dozing off with heavy eyelids icon",
        "sleep mode icon for a wellness app",
        "nap time reminder notification badge",
        "snooze animation in a comic strip",
        "sleep tracking snooze counter feature",
        "rest period marked in daily schedule",
        "drowsy state shown with zzz symbol",
    ],
    conv_en=[
        "I need a snooze icon for my alarm app",
        "add a snooze symbol to the sleep tracker",
        "show a zzz for the rest reminder feature",
        "use the snooze icon for the nap timer",
    ],
    typo_en=[
        "snooze the alamr for ten minutes",
        "zzz sleepng bubble in comic",
        "tap snooze buton to delay alarm",
        "afternoon npa on the sofa",
    ],
    bnd_en=[
        "crescent moon night mode symbol",
        "bed with pillow and blanket for sleep",
        "hourglass timer counting down",
        "alarm clock face with ringing bells",
        "eye closed sleepy emoji expression",
        "night sky with stars and moon",
    ],
    valid_en=["snooze alarm icon", "zzz sleep symbol", "nap snooze button"],
    test_en=["alarm snooze tap", "zzz sleeping bubbles", "rest snooze icon"],
)

# 422
process_icon("stopwatch",
    st_en=["clock", "reminder", "stopwatch", "time", "waiting"],
    pst_en=[
        "wall clock showing the current hour", "analog clock face with hands",
        "reminder set to alert at noon", "daily reminder notification on phone",
        "stopwatch timing a race sprint", "press stopwatch to start the timer",
        "time elapsed on the scoreboard", "time management app feature",
        "waiting for the bus at the stop", "loading waiting spinner icon",
    ],
    reg_en=[
        "round stopwatch with a button on top to start and stop",
        "sports timing with a stopwatch clicking at the finish line",
        "lap timer stopwatch tracking split times",
        "stopwatch icon for a workout interval timer",
        "countdown from sixty seconds on a stopwatch",
        "coach holding a stopwatch at the track",
        "kitchen timer stopwatch for cooking intervals",
        "elapsed time displayed on a digital stopwatch",
        "stopwatch precision measuring milliseconds",
        "fitness app stopwatch for interval training",
    ],
    conv_en=[
        "I need a stopwatch icon for my workout app",
        "add a stopwatch symbol to the timer screen",
        "show a stopwatch for the lap tracking feature",
        "use the stopwatch icon for the race timing section",
    ],
    typo_en=[
        "stpwatch timing a sprint race",
        "stop wtach lap timer click",
        "sotpwatch measuring elapsed time",
        "stowatch counting down seconds",
    ],
    bnd_en=[
        "hourglass sand flowing through chambers",
        "clock alarm ringing with bells on top",
        "timer bar countdown progress indicator",
        "calendar date with event reminder",
        "metronome ticking tempo beat marker",
        "wristwatch analog face on a band",
    ],
    valid_en=["stopwatch timing icon", "sports stopwatch timer", "lap stopwatch symbol"],
    test_en=["stopwatch start stop", "timing stopwatch race", "stopwatch elapsed time"],
)

# 423
process_icon("strawberry",
    st_en=["berry", "fruit", "juice", "seed", "strawberry", "summer"],
    pst_en=[
        "fresh berry picked from the garden", "mixed berry smoothie in a blender",
        "tropical fruit salad in a bowl", "seasonal fruit at the farmers market",
        "strawberry juice in a chilled glass", "juice squeezed from ripe berries",
        "tiny seed dots on the strawberry skin", "seed embedded in the outer flesh",
        "ripe strawberry dipped in chocolate", "strawberry layered in a shortcake",
        "summer berry dessert on the patio", "summer fruit stand roadside pickup",
    ],
    reg_en=[
        "red heart-shaped strawberry with green leafy top",
        "ripe strawberry with tiny yellow seeds on the surface",
        "fresh strawberry for a smoothie recipe app",
        "chocolate-dipped strawberry for a dessert menu",
        "strawberry shortcake with whipped cream",
        "strawberry emoji icon for a food journal",
        "punnet of strawberries from the market stall",
        "sliced strawberry topping on a yogurt bowl",
        "summer strawberry picking in the field",
        "strawberry jam spread on a slice of bread",
    ],
    conv_en=[
        "I need a strawberry icon for my recipe app",
        "add a strawberry symbol to the fruit category",
        "show a strawberry for the summer dessert section",
        "use the strawberry icon for the smoothie builder",
    ],
    typo_en=[
        "ripe straberry dipped in chocolate",
        "fresh strawbery from the garden",
        "strwaberry shortcake dessert recipe",
        "summmer strawberry picking season",
    ],
    bnd_en=[
        "red cherry pair on a stem",
        "raspberry textured red berry cluster",
        "watermelon slice with black seeds",
        "blueberry small round dark berry",
        "apple red round fruit with stem and leaf",
        "tomato red round fruit on the vine",
    ],
    valid_en=["fresh strawberry icon", "red strawberry fruit", "strawberry berry symbol"],
    test_en=["ripe strawberry produce", "strawberry summer fruit", "strawberry for recipe app"],
)

# 424
process_icon("teeth",
    st_en=["bite", "dental", "dentist", "gums", "mouth", "smile", "tooth"],
    pst_en=[
        "bite force measured in dental study", "bite into a crisp apple",
        "dental hygiene brushing twice daily", "dental checkup reminder icon",
        "dentist office appointment booked", "dentist cleaning and x-ray visit",
        "healthy pink gums surrounding teeth", "gums bleeding sign of gingivitis",
        "open mouth showing upper and lower teeth", "mouth diagram for dental app",
        "bright smile with clean white teeth", "smile makeover with whitening treatment",
        "single tooth with root canal icon", "wisdom tooth extracted by dentist",
    ],
    reg_en=[
        "row of white teeth in an open mouth",
        "upper and lower teeth shown together",
        "dental health icon showing clean teeth",
        "teeth whitening before and after result",
        "set of straight teeth after orthodontic treatment",
        "molar and incisor dental diagram",
        "teeth brushing twice daily reminder",
        "dentist checkup with teeth and gums check",
        "tooth decay warning shown on teeth icon",
        "bright smile teeth symbol for wellness app",
    ],
    conv_en=[
        "I need a teeth icon for my dental app",
        "add a teeth symbol to the oral health section",
        "show teeth for the dentist appointment reminder",
        "use the teeth icon for the smile tracker feature",
    ],
    typo_en=[
        "brush your teech twice a day",
        "dental chekup with teeth cleaning",
        "healthy tehth and gums icon",
        "denist appointment for tooth exam",
    ],
    bnd_en=[
        "single tooth with root showing for dentist",
        "lips closed smile expression emoji",
        "tongue sticking out playful gesture",
        "toothbrush with toothpaste bristles",
        "mouthwash bottle for oral rinse",
        "skull with jaw bones anatomy diagram",
    ],
    valid_en=["teeth dental icon", "row of teeth smile", "teeth health symbol"],
    test_en=["dental teeth checkup", "teeth whitening icon", "upper lower teeth symbol"],
)

# 425
process_icon("unlock",
    st_en=["admin", "lock", "open", "padlock", "password", "privacy", "private", "protect", "unlock", "unlocked"],
    pst_en=[
        "admin panel access unlocked", "admin privileges granted to user",
        "lock removed to grant access", "broken lock security breach icon",
        "open padlock letting user through", "open access no longer restricted",
        "padlock shackle open position", "padlock clicked open icon",
        "password entered to unlock screen", "forgotten password reset unlock",
        "privacy setting toggled off", "privacy mode disabled for sharing",
        "private folder access opened", "private document shared with team",
        "protect account with two-factor code", "protect data by unlocking securely",
        "unlock the phone with fingerprint", "unlock account after verification",
        "unlocked state shown in green icon", "unlocked padlock confirming access",
    ],
    reg_en=[
        "open padlock with shackle lifted up",
        "unlocked icon indicating access is granted",
        "security padlock in the open unlocked state",
        "unlock screen gesture on a mobile device",
        "account unlocked after password reset",
        "file permission changed to unlocked",
        "unlock feature for premium content access",
        "door lock turned to the open position",
        "unlocked badge showing unrestricted content",
        "admin unlocking a protected resource",
    ],
    conv_en=[
        "I need an unlock icon for my security settings",
        "add an unlock symbol to the access control screen",
        "show an unlock for the premium feature gate",
        "use the unlock icon for the password-reset confirmation",
    ],
    typo_en=[
        "unlocke the phone with your pin",
        "padlokc open after authentication",
        "unlocked acesss granted to user",
        "passwrod entered to unlock account",
    ],
    bnd_en=[
        "closed padlock locked and secured icon",
        "key inserted into a lock cylinder",
        "shield with checkmark security badge",
        "fingerprint biometric scan icon",
        "lock chain wrapped around a gate",
        "door knob turning to open position",
    ],
    valid_en=["unlocked padlock icon", "open lock symbol", "unlock access granted"],
    test_en=["unlock screen icon", "padlock open unlocked", "unlock security feature"],
)

# 426
process_icon("van",
    st_en=["airport", "bus", "minibus", "transportation", "travel", "vehicle"],
    pst_en=[
        "airport shuttle van picking up passengers", "airport van transfer to the terminal",
        "city bus route on the schedule", "bus service running every ten minutes",
        "minibus hired for a group tour", "minibus carrying passengers downtown",
        "public transportation van on route", "transportation fleet management icon",
        "travel van packed for a road trip", "travel by van across the country",
        "cargo vehicle for delivery service", "vehicle fleet tracked by GPS",
    ],
    reg_en=[
        "passenger van with sliding side door",
        "white minivan used for airport shuttles",
        "delivery van driving through city streets",
        "camper van parked at a national park",
        "van icon for a ride-sharing app",
        "family road trip in a large van",
        "school mini-bus van with children",
        "courier service van making deliveries",
        "shuttle van service between hotel and airport",
        "cargo van loaded for a moving day",
    ],
    conv_en=[
        "I need a van icon for my transport app",
        "add a van symbol to the fleet management screen",
        "show a van for the shuttle booking feature",
        "use the van icon for the vehicle tracking section",
    ],
    typo_en=[
        "airprot shuttle van service",
        "passneger minivan for hire",
        "cargo vna delivery route",
        "trnaport van fleet tracking",
    ],
    bnd_en=[
        "large bus coach with many passenger windows",
        "pickup truck with open flatbed cargo area",
        "semi truck eighteen-wheeler on the highway",
        "taxi yellow cab urban transport",
        "ambulance emergency medical vehicle",
        "minivan station wagon family car",
    ],
    valid_en=["passenger van icon", "minivan transport symbol", "shuttle van vehicle"],
    test_en=["van delivery icon", "airport shuttle van", "transportation van symbol"],
)

# 427
process_icon("violin",
    st_en=["bow", "cello", "fiddle", "instrument", "music", "orchestra", "string", "violin"],
    pst_en=[
        "bow drawn across the strings smoothly", "rosin applied to the horsehair bow",
        "cello played in a string quartet", "cello section in a symphony orchestra",
        "country fiddle music at a hoedown", "fiddle player at a folk festival",
        "stringed instrument tuned to concert pitch", "instrument case carried by a musician",
        "classical music performed on stage", "music stand with sheet music notes",
        "orchestra warming up before the concert", "orchestra string section playing in unison",
        "violin string plucked for pizzicato effect", "high E string on the violin snapped",
        "violin solo played by a concert master", "violinist with chin rest under jaw",
    ],
    reg_en=[
        "wooden violin with f-holes and scroll",
        "bow drawn across violin strings making a melody",
        "classical violin instrument for orchestra",
        "violin solo performing a concerto on stage",
        "fiddle played at a bluegrass jam session",
        "violin bridge and tailpiece close-up detail",
        "rosin powdered on the horsehair bow",
        "violin tuned with fine tuners at the tailpiece",
        "string quartet with two violins viola and cello",
        "violin icon for a music practice app",
    ],
    conv_en=[
        "I need a violin icon for my music app",
        "add a violin symbol to the orchestra section",
        "show a violin for the classical music category",
        "use the violin icon for the string instrument selector",
    ],
    typo_en=[
        "clasical violen concert solo",
        "violine played in the orchestra",
        "fiddel music at the festival",
        "vioin bow drawn across strings",
    ],
    bnd_en=[
        "acoustic guitar six strings with sound hole",
        "cello large bowed string instrument between the knees",
        "viola slightly larger than violin mid-range tone",
        "harp vertical strings plucked with fingers",
        "double bass upright bass in jazz ensemble",
        "ukulele small four-string instrument from Hawaii",
    ],
    valid_en=["violin string instrument", "classical violin icon", "violin orchestra symbol"],
    test_en=["violin bow strings", "fiddle folk music icon", "violin music app"],
)

print("\nDone! All 12 icons processed.")
