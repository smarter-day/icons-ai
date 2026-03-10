#!/usr/bin/env python3
"""Generate English training data for icons 441-451."""
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

# 441
process_icon("apple-whole",
    st_en=["apple", "fall", "fruit", "fuji", "green", "orchard", "red", "seasonal", "vegan"],
    pst_en=[
        "red apple polished and ready to eat", "apple slice in a lunchbox",
        "fall harvest apple picking season", "fall seasonal fruit at the market",
        "fresh fruit bowl with apples and pears", "fruit smoothie with apple and ginger",
        "fuji apple crisp and sweet variety", "fuji apple grown in Japanese orchards",
        "green granny smith apple tart flavor", "green apple sliced for a cheese board",
        "apple orchard rows in autumn color", "orchard ladder leaning against a tree",
        "red delicious apple shiny and round", "red apple core after taking a bite",
        "seasonal apple cider pressed in autumn", "seasonal fruit available in fall only",
        "vegan snack of apple slices with almond butter", "vegan diet includes whole fruits like apple",
    ],
    reg_en=[
        "whole red apple with a green leaf and stem",
        "shiny apple sitting on a wooden desk",
        "apple icon for a nutrition and diet app",
        "teacher's desk with an apple on the corner",
        "orchard-fresh apple crisp with caramel",
        "apple cross-section showing core and seeds",
        "granny smith green apple for a tart pie",
        "apple cider pressed from fall harvest",
        "apple emoji for healthy snack reminders",
        "whole apple produce icon in a food journal",
    ],
    conv_en=[
        "I need an apple icon for my diet tracker",
        "add an apple symbol to the healthy snack section",
        "show an apple for the orchard produce page",
        "use the apple icon for the nutrition log",
    ],
    typo_en=[
        "ripe red aple from the orchard",
        "fuji aplpe crisp and sweet",
        "granny smtih green apple pie",
        "seaosnal apple cider in the fall",
    ],
    bnd_en=[
        "pear green teardrop-shaped fruit with a stem",
        "orange round citrus fruit with dimpled skin",
        "tomato red round fruit on the vine",
        "peach fuzzy round stone fruit with a pit",
        "cherry small red fruit pair on a stem",
        "computer apple logo monochrome brand mark",
    ],
    valid_en=["whole apple fruit icon", "red apple produce symbol", "apple orchard icon"],
    test_en=["green apple snack", "whole apple nutrition", "apple fall harvest icon"],
)

# 442
process_icon("bolt-lightning",
    st_en=["electricity", "flash", "lightning", "weather", "zap"],
    pst_en=[
        "electricity bolt from a power station", "electricity surging through the power grid",
        "camera flash fired in a dark room", "flash of light before the thunder",
        "lightning bolt striking a tall tree", "lightning illuminating the storm clouds",
        "severe weather alert lightning warning", "weather forecast showing thunderstorms",
        "zap icon for a quick action button", "zap sound effect in a comic strip",
    ],
    reg_en=[
        "jagged lightning bolt striking downward",
        "electric flash symbol for a power icon",
        "lightning bolt badge on a superhero costume",
        "thunderstorm lightning bolt in dark sky",
        "fast action zap icon for an app",
        "electric vehicle charging bolt symbol",
        "lightning bolt warning on electrical equipment",
        "bright white lightning bolt in a storm",
        "energy and power represented by a bolt",
        "lightning bolt icon for a fitness or speed app",
    ],
    conv_en=[
        "I need a lightning bolt icon for my energy app",
        "add a bolt symbol to the fast-action button",
        "show a lightning bolt for the power indicator",
        "use the bolt icon for the electric charge feature",
    ],
    typo_en=[
        "jagged ligthning bolt in the storm",
        "electric ligntning striking the tree",
        "thunderstorm lihgtning bolt warning",
        "zpa quick action icon button",
    ],
    bnd_en=[
        "sun bright yellow circle with rays",
        "cloud with rain drops falling",
        "tornado funnel rotating storm column",
        "electric plug two-prong power connector",
        "battery charged indicator with fill level",
        "fire flame burning orange and red",
    ],
    valid_en=["lightning bolt icon", "electric bolt symbol", "lightning bolt weather"],
    test_en=["bolt lightning strike", "zap bolt icon", "lightning bolt power symbol"],
)

# 443
process_icon("bow-arrow",
    st_en=["archer", "archery", "arrow", "bow", "fantasy", "ranger", "weapon", "zodiac"],
    pst_en=[
        "skilled archer aiming at the target", "archer drawing the bowstring back",
        "archery competition at the summer games", "archery range with targets in a field",
        "arrow flying toward the bullseye", "arrow notched on the bowstring",
        "bow drawn taut before the release", "bow and arrow carried by a hunter",
        "fantasy RPG ranger using a bow", "fantasy world archer in enchanted forest",
        "wilderness ranger tracking prey silently", "ranger class chosen in the adventure game",
        "ranged weapon bow for long-distance attack", "weapon of choice for the elven archer",
        "Sagittarius zodiac sign bow and arrow", "zodiac symbol for the archer constellation",
    ],
    reg_en=[
        "curved bow with an arrow notched and aimed",
        "archery target hit by a flying arrow",
        "hunter in the forest with a longbow",
        "medieval archer defending the castle walls",
        "bow and arrow icon for a fantasy game app",
        "Olympic archery athlete at the shooting line",
        "compound bow with pulleys for extra power",
        "arrow released from a recurve bow",
        "Sagittarius zodiac bow and arrow symbol",
        "ranger character carrying a bow in an RPG",
    ],
    conv_en=[
        "I need a bow and arrow icon for my game app",
        "add a bow-arrow symbol to the weapons section",
        "show a bow and arrow for the archery event",
        "use the bow-arrow icon for the ranger class",
    ],
    typo_en=[
        "arcery bow and arrow at the range",
        "skilled archar drawing the bowstring",
        "arrow notched on the bwo string",
        "sagittarius zodiacs bow and arrow",
    ],
    bnd_en=[
        "sword long blade medieval melee weapon",
        "crossbow mechanical bolt-firing weapon",
        "spear thrown weapon long wooden shaft",
        "slingshot Y-shaped band weapon",
        "target bullseye with concentric rings",
        "quiver holding a bundle of arrows",
    ],
    valid_en=["bow and arrow icon", "archery bow symbol", "bow-arrow fantasy weapon"],
    test_en=["archer bow arrow", "bow and arrow zodiac", "archery range icon"],
)

# 444
process_icon("burger-cheese",
    st_en=["bacon", "beef", "burger", "grill", "hamburger", "sandwich", "slider"],
    pst_en=[
        "crispy bacon strip on the burger", "bacon cheeseburger with extra sauce",
        "juicy beef patty on the grill", "beef burger stacked with toppings",
        "cheeseburger with melted cheddar on top", "burger served with fries at the diner",
        "grill marks on a freshly cooked patty", "grill fired up for the backyard barbecue",
        "classic hamburger at the fast food counter", "hamburger bun toasted before assembly",
        "club sandwich stacked on a plate", "sandwich wrap for a lunch on the go",
        "mini slider with a small beef patty", "slider trio at the happy hour menu",
    ],
    reg_en=[
        "cheeseburger with melted cheese dripping over a beef patty",
        "double burger stacked with lettuce tomato and cheese",
        "smash burger pressed thin on a flat-top grill",
        "fast food burger icon for a delivery app",
        "gourmet burger with brioche bun and caramelized onions",
        "burger and fries combo on a tray",
        "grilled beef patty with cheddar slice melting",
        "burger emoji for a food ordering interface",
        "bacon cheeseburger in the restaurant menu",
        "slider row of three mini burgers on a platter",
    ],
    conv_en=[
        "I need a burger icon for my food delivery app",
        "add a cheeseburger symbol to the fast food section",
        "show a burger for the restaurant menu item",
        "use the burger icon for the grill category",
    ],
    typo_en=[
        "juicy cheeseburge with extra bacon",
        "beef burrger grilled to perfection",
        "hambruger with lettuce and tomato",
        "double burgr stacked with cheese",
    ],
    bnd_en=[
        "hot dog sausage in a bun with mustard",
        "pizza slice with mozzarella and tomato",
        "taco folded shell with meat and salsa",
        "sandwich club with three bread layers",
        "fried chicken sandwich in a brioche bun",
        "wrap tortilla rolled with salad filling",
    ],
    valid_en=["cheeseburger icon", "burger beef patty symbol", "hamburger food icon"],
    test_en=["burger cheese fast food", "grilled hamburger icon", "beef burger delivery app"],
)

# 445
process_icon("car-bolt",
    st_en=["auto", "automobile", "electric", "ev", "sedan", "transportation", "travel", "vehicle"],
    pst_en=[
        "auto body repair shop for EVs", "auto dealership showing electric models",
        "automobile with a charging port open", "automobile fleet transitioning to electric",
        "electric car charging at the station", "electric motor powering a quiet sedan",
        "ev range shown on the dashboard", "ev charger installed in the garage",
        "sedan silhouette with a lightning bolt", "sedan electric vehicle on the highway",
        "public transportation going electric", "transportation app tracking EV routes",
        "travel by electric car on a road trip", "travel range estimator for electric vehicles",
        "electric vehicle registered in the fleet", "vehicle log with charging history",
    ],
    reg_en=[
        "car with a lightning bolt symbol for electric vehicle",
        "EV sedan charging at a public station",
        "electric car icon with a bolt on the side",
        "zero-emission vehicle badge for a clean car",
        "electric car range indicator on the screen",
        "EV charging port opened on the door",
        "green energy electric car on the road",
        "Tesla-style sedan with electric bolt logo",
        "fleet management app for electric vehicles",
        "electric car symbol for a transport booking app",
    ],
    conv_en=[
        "I need an electric car icon for my EV app",
        "add a car-bolt symbol to the charging section",
        "show an EV icon for the green transport feature",
        "use the car-bolt icon for the electric fleet tracker",
    ],
    typo_en=[
        "electirc car charging at the station",
        "ev sedna with a lightning bolt icon",
        "electic vehicle fleet management app",
        "car-blt symbol for electric transport",
    ],
    bnd_en=[
        "gas pump fuel nozzle at a station",
        "regular car sedan without electric badge",
        "bicycle cycling green transport icon",
        "bus electric public transport vehicle",
        "scooter electric ride-sharing symbol",
        "charging station plug connector icon",
    ],
    valid_en=["electric car icon", "EV car bolt symbol", "car-bolt charging icon"],
    test_en=["electric vehicle bolt", "EV sedan charging", "car bolt electric icon"],
)

# 446
process_icon("champagne-glass",
    st_en=["alcohol", "bar", "beverage", "celebration", "champagne", "drink", "holiday", "party"],
    pst_en=[
        "alcohol-free version with sparkling juice", "alcohol served responsibly at the event",
        "bar menu featuring champagne by the glass", "bar cart stocked for the New Year party",
        "cold beverage poured into a tall flute", "beverage menu at the upscale restaurant",
        "celebration toast with champagne flutes", "celebration marking the big anniversary",
        "champagne bubbling in a crystal flute", "champagne cork popping at midnight",
        "drink responsibly message on the label", "festive drink poured for the guests",
        "holiday gathering with champagne toasts", "holiday season cheers with glasses raised",
        "party starting with a champagne toast", "party decoration with confetti and flutes",
    ],
    reg_en=[
        "tall champagne flute filled with bubbly",
        "champagne glass clinking at a celebration toast",
        "New Year's Eve countdown with champagne",
        "wedding reception champagne glasses on the table",
        "champagne bottle popped at the victory party",
        "sparkling wine in an elegant flute glass",
        "celebration icon with a champagne flute",
        "holiday party champagne toast at midnight",
        "anniversary dinner champagne for two",
        "champagne glass emoji for events and party apps",
    ],
    conv_en=[
        "I need a champagne glass icon for my event app",
        "add a champagne symbol to the celebration section",
        "show a champagne flute for the party RSVP screen",
        "use the champagne glass icon for the toast reminder",
    ],
    typo_en=[
        "chamagne glass clinking at the party",
        "champgne flute filled with bubbles",
        "celebartion toast with champagn",
        "New Year champagne glas at midnight",
    ],
    bnd_en=[
        "wine glass with red wine swirled inside",
        "cocktail glass with ice and garnish",
        "beer mug with a frothy head",
        "martini glass with olive on a toothpick",
        "juice glass with orange slices",
        "water glass clear tumbler on a table",
    ],
    valid_en=["champagne flute icon", "celebration champagne glass", "champagne toast symbol"],
    test_en=["champagne party icon", "New Year champagne glass", "bubbly champagne flute"],
)

# 447
process_icon("court-sport",
    st_en=["basketball", "court", "field", "football", "soccer", "sport"],
    pst_en=[
        "basketball court with painted three-point line", "basketball game played on the hardwood",
        "court layout diagram for a sports app", "court lines marked on the gymnasium floor",
        "football field with yard markers and end zones", "field goal kicked between the uprights",
        "football played on a grass field", "football stadium aerial view of the field",
        "soccer match on a green outdoor pitch", "soccer training drills on the field",
        "team sport played on a court or field", "sport facility booking app interface",
    ],
    reg_en=[
        "top-down view of a basketball court with lane markings",
        "sports court diagram showing field layout",
        "court lines for tennis or basketball",
        "multi-sport facility map with courts",
        "soccer field with center circle and goals",
        "sport venue booking icon for a recreation app",
        "basketball half-court used for practice drills",
        "court sport icon showing field boundaries",
        "football field diagram with goal posts",
        "sport court icon for a gym scheduling app",
    ],
    conv_en=[
        "I need a court-sport icon for my booking app",
        "add a court symbol to the sports facility section",
        "show a court for the game schedule feature",
        "use the court-sport icon for the field map screen",
    ],
    typo_en=[
        "baskeball court with painted lane lines",
        "soccar field with center circle marked",
        "footbll field yard markers and end zone",
        "spost court layout for the facility map",
    ],
    bnd_en=[
        "golf course green with flag in the hole",
        "swimming pool lane dividers aerial view",
        "ice rink oval surface with boards",
        "baseball diamond with base paths",
        "tennis racket and ball for match play",
        "running track oval lanes for athletics",
    ],
    valid_en=["sport court icon", "court field layout symbol", "court sport diagram"],
    test_en=["basketball court icon", "soccer field layout", "court sport facility"],
)

# 448
process_icon("language",
    st_en=["dialect", "idiom", "localize", "speech", "translate", "vernacular"],
    pst_en=[
        "regional dialect spoken in the countryside", "dialect differences between cities",
        "common idiom used in everyday conversation", "idiom lost in translation between languages",
        "localize the app for Japanese users", "localize strings for a global release",
        "speech bubble showing foreign language text", "speech recognition translating on the fly",
        "translate the document into Spanish", "translate button in the browser toolbar",
        "vernacular slang used by local speakers", "vernacular expressions in native speech",
    ],
    reg_en=[
        "globe with speech bubbles in different languages",
        "translate button converting text to another language",
        "language selector dropdown in app settings",
        "multilingual interface supporting ten languages",
        "language learning app showing vocabulary cards",
        "speech bubble with foreign script characters",
        "language icon for a localization settings screen",
        "international flag representing a language choice",
        "language detection switching to native tongue",
        "translation app converting spoken words in real time",
    ],
    conv_en=[
        "I need a language icon for my translation app",
        "add a language symbol to the localization settings",
        "show a language selector for the app onboarding",
        "use the language icon for the multilingual feature",
    ],
    typo_en=[
        "translate the documnet into French",
        "localise the app for Japanees users",
        "langauge selector in the settings menu",
        "speech recogniton in a foreign languge",
    ],
    bnd_en=[
        "keyboard typing letters on a layout",
        "chat bubble conversation message icon",
        "book open pages of written text",
        "microphone recording spoken words",
        "flag country identifier national symbol",
        "font letter A typography text formatting",
    ],
    valid_en=["language translation icon", "multilingual language symbol", "language selector icon"],
    test_en=["translate language icon", "language localization symbol", "language app settings"],
)

# 449
process_icon("memo",
    st_en=["cv", "file", "idea", "note", "notepad", "page", "paper"],
    pst_en=[
        "cv attached as a memo for HR review", "cv template formatted as a memo document",
        "file saved as a memo in the folder", "file icon representing a short memo",
        "idea scribbled on a memo pad", "idea captured in a quick memo",
        "note left on the fridge for the family", "sticky note reminder memo on the desk",
        "notepad memo pages torn off and handed over", "notepad filled with handwritten memos",
        "page of a memo with bullet points", "one-page memo circulated to the team",
        "paper memo printed and posted on the board", "paper note folded and slipped under the door",
    ],
    reg_en=[
        "short memo document with lined pages",
        "sticky note memo jotted down quickly",
        "office memo printed and distributed to staff",
        "memo icon for a notes and reminders app",
        "handwritten memo with key points listed",
        "inter-office memo sent between departments",
        "memo page with a folded corner",
        "quick memo captured on a phone",
        "memo template for a corporate briefing",
        "notebook memo pad icon for productivity app",
    ],
    conv_en=[
        "I need a memo icon for my notes app",
        "add a memo symbol to the document section",
        "show a memo for the quick note feature",
        "use the memo icon for the internal message board",
    ],
    typo_en=[
        "quick mmo jotted on the notepad",
        "ofice memmo distributed to the team",
        "sicky note memoo on the fridge",
        "memo documnet saved in the folder",
    ],
    bnd_en=[
        "clipboard with a checklist attached",
        "notebook spiral-bound with many pages",
        "envelope sealed letter ready to mail",
        "calendar page with a date marked",
        "to-do list with checkboxes on paper",
        "document file with multiple pages stacked",
    ],
    valid_en=["memo note icon", "quick memo document", "memo notepad symbol"],
    test_en=["office memo icon", "memo note reminder", "memo document page"],
)

# 450
process_icon("saxophone",
    st_en=["brass", "instrument", "jazz", "music", "sax", "saxophone", "woodwind"],
    pst_en=[
        "brass instrument gleaming under stage lights", "brass section warming up in the pit",
        "wind instrument with keys and a bell", "instrument case for a tenor sax",
        "jazz club featuring live saxophone solos", "jazz standard played on a smoky stage",
        "music flowing from the saxophone bell", "music notation for a sax lead line",
        "sax solo blowing through the night", "alto sax squeaking a high note",
        "saxophone neck strap supporting the weight", "saxophone mouthpiece with a reed attached",
        "woodwind instrument fingering chart", "woodwind section in the marching band",
    ],
    reg_en=[
        "golden saxophone with a curved bell and keys",
        "jazz musician playing tenor saxophone on stage",
        "alto sax solo in a dimly lit jazz club",
        "saxophone reed vibrating against the mouthpiece",
        "soprano saxophone standing straight like a clarinet",
        "marching band member carrying a baritone sax",
        "saxophone icon for a music practice app",
        "smooth jazz melody played on a vintage sax",
        "saxophone strap hanging from the player's neck",
        "street musician playing saxophone in the subway",
    ],
    conv_en=[
        "I need a saxophone icon for my music app",
        "add a saxophone symbol to the jazz section",
        "show a saxophone for the woodwind instrument list",
        "use the saxophone icon for the jazz club feature",
    ],
    typo_en=[
        "golden saxaphone with curved bell",
        "jazz saxophoen solo on the stage",
        "alto saaxophone in the jazz club",
        "woodwing saxophone reed and mouthpiece",
    ],
    bnd_en=[
        "trumpet brass instrument with valves",
        "clarinet single-reed woodwind instrument",
        "flute silver transverse wind instrument",
        "trombone slide brass instrument in orchestra",
        "oboe double-reed woodwind in the symphony",
        "bassoon large double-reed woodwind instrument",
    ],
    valid_en=["saxophone jazz icon", "golden saxophone symbol", "saxophone music instrument"],
    test_en=["sax jazz musician", "saxophone woodwind icon", "saxophone music app"],
)

# 451
process_icon("syringe",
    st_en=["covid-19", "doctor", "immunizations", "medical", "medicine", "needle", "shot", "sick", "syringe", "vaccinate", "vaccine"],
    pst_en=[
        "covid-19 vaccine rolled out globally", "covid-19 booster shot at the clinic",
        "doctor preparing a syringe for injection", "doctor administering the flu shot",
        "childhood immunizations tracked in the app", "immunizations required before travel abroad",
        "medical syringe drawn up with medication", "medical procedure requiring an injection",
        "medicine injected directly into the bloodstream", "medicine measured in the syringe barrel",
        "needle inserted into the upper arm", "fine needle used for an allergy test",
        "flu shot scheduled for the autumn season", "shot given at the pharmacy walk-in clinic",
        "sick patient receiving an IV drip", "sick child getting a vaccination at the doctor",
        "syringe filled and ready for injection", "syringe with plunger pulled back",
        "vaccinate children against measles early", "vaccination campaign for the whole community",
        "vaccine stored in a cold chain fridge", "vaccine approved for public distribution",
    ],
    reg_en=[
        "glass syringe with a metal needle and plunger",
        "nurse drawing up a dose in a syringe",
        "vaccine syringe icon for an immunization app",
        "flu shot appointment reminder notification",
        "COVID-19 vaccine injection into the upper arm",
        "syringe and vial medication preparation",
        "insulin syringe for diabetic self-injection",
        "blood draw syringe used in a lab test",
        "vaccination record updated with a new shot",
        "syringe icon for a healthcare or clinic app",
    ],
    conv_en=[
        "I need a syringe icon for my health app",
        "add a syringe symbol to the vaccination section",
        "show a syringe for the immunization tracker",
        "use the syringe icon for the medical procedure log",
    ],
    typo_en=[
        "vacine syringe prepared for injection",
        "flu shto administered at the clinic",
        "syrange filled with the medication",
        "neddle inserted into the upper arm",
    ],
    bnd_en=[
        "pill tablet medication capsule shape",
        "stethoscope doctor listening to heartbeat",
        "bandage adhesive strip on a small wound",
        "thermometer reading a fever temperature",
        "test tube blood sample vial in a rack",
        "IV drip bag hanging on a hospital stand",
    ],
    valid_en=["syringe vaccine icon", "medical syringe symbol", "injection needle icon"],
    test_en=["syringe shot clinic", "vaccine syringe health app", "needle injection symbol"],
)

print("\nDone! All 11 icons processed.")
