#!/usr/bin/env python3
"""Generate English training data for icons 452-464."""
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

# 452
process_icon("address-book",
    st_en=["contact", "directory", "employee", "index", "portfolio", "rolodex", "username"],
    pst_en=[
        "contact saved in the address book", "contact list synced across devices",
        "company directory with all staff entries", "directory of suppliers organized by name",
        "employee record stored in the address book", "employee contact shared with the team",
        "index of clients sorted alphabetically", "address index tab for quick navigation",
        "portfolio of contacts built over years", "business portfolio contact list exported",
        "old rolodex card flipped to find a number", "rolodex replaced by a digital address book",
        "username and email saved in the contact book", "username linked to a phone entry",
    ],
    reg_en=[
        "address book with tabbed alphabetical sections",
        "contact list stored in a digital address book",
        "phone and email entries organized in one place",
        "address book icon for a contacts app",
        "company directory listing all employees",
        "rolodex-style address book with flip cards",
        "address book synced to phone and laptop",
        "business card collection in an address book",
        "address book updated after a job change",
        "personal address book with birthdays and notes",
    ],
    conv_en=[
        "I need an address book icon for my contacts app",
        "add an address book symbol to the directory section",
        "show an address book for the contact management screen",
        "use the address book icon for the employee directory",
    ],
    typo_en=[
        "adress book with alphabetical tabs",
        "contcat list in the address book",
        "rolodxe card flipped to find a number",
        "employe directory in the address book",
    ],
    bnd_en=[
        "envelope sealed letter ready to send",
        "phone receiver handset calling icon",
        "calendar with events and dates scheduled",
        "card business name and title on cardstock",
        "bookmark saved page in a document",
        "folder file container organizing documents",
    ],
    valid_en=["address book contacts icon", "contact directory symbol", "address book app icon"],
    test_en=["address book employee list", "rolodex address book", "contact address book icon"],
)

# 453
process_icon("bitcoin-sign",
    st_en=["currency"],
    pst_en=[
        "digital currency stored in a crypto wallet", "currency exchange rate for bitcoin",
    ],
    reg_en=[
        "Bitcoin symbol with a strikethrough B",
        "cryptocurrency icon for a finance app",
        "Bitcoin sign representing digital currency",
        "BTC symbol shown on an exchange dashboard",
        "Bitcoin logo used in a crypto wallet app",
        "digital coin icon for a blockchain app",
        "Bitcoin sign marking the price of crypto",
        "crypto currency Bitcoin badge on a chart",
        "Bitcoin sign next to a dollar amount",
        "decentralized currency symbol for Web3 apps",
    ],
    conv_en=[
        "I need a Bitcoin sign icon for my crypto app",
        "add a Bitcoin symbol to the currency section",
        "show a Bitcoin sign for the crypto wallet feature",
        "use the Bitcoin icon for the price tracker",
    ],
    typo_en=[
        "bitocin sign in the crypto wallet",
        "bitconi symbol on the exchange rate",
        "btcoin currency icon for finance app",
        "bicoin sign marking the price",
    ],
    bnd_en=[
        "dollar sign currency symbol for USD",
        "euro sign currency symbol for EUR",
        "coin gold disc currency icon",
        "bank building financial institution icon",
        "credit card payment method icon",
        "ethereum ETH logo blockchain currency",
    ],
    valid_en=["Bitcoin sign icon", "BTC currency symbol", "Bitcoin crypto icon"],
    test_en=["Bitcoin sign finance app", "BTC symbol icon", "bitcoin currency sign"],
)

# 454
process_icon("book-bible",
    st_en=["book", "catholicism", "christianity", "god", "holy"],
    pst_en=[
        "book of scriptures read at the pulpit", "prayer book opened on the church pew",
        "catholicism practices guided by the Bible", "Catholic mass with Bible readings",
        "christianity centered on the holy scripture", "christianity symbol for a faith app",
        "word of god preached every Sunday morning", "god-given scripture quoted in a sermon",
        "holy bible placed on the altar", "holy text revered by the congregation",
    ],
    reg_en=[
        "leather-bound Bible with gold lettering",
        "holy Bible open to a scripture passage",
        "church Bible on the lectern for Sunday service",
        "Bible icon for a faith or devotional app",
        "scripture reading marked with a ribbon bookmark",
        "Old and New Testament in one Bible cover",
        "Bible study group with highlighted passages",
        "Bible verse displayed on a morning reminder",
        "family Bible passed down through generations",
        "pocket New Testament carried for daily reading",
    ],
    conv_en=[
        "I need a Bible icon for my devotional app",
        "add a Bible symbol to the scripture section",
        "show a Bible for the daily verse feature",
        "use the Bible icon for the faith community page",
    ],
    typo_en=[
        "leather-bound bibile on the altar",
        "holy scriputre read at the pulpit",
        "christinity guided by the holy bible",
        "bible vrese displayed every morning",
    ],
    bnd_en=[
        "book open pages of general reading material",
        "scroll ancient rolled parchment document",
        "cross Christian symbol two perpendicular lines",
        "church building with a steeple and cross",
        "prayer hands pressed together in worship",
        "quran Muslim holy text on a stand",
    ],
    valid_en=["Bible holy book icon", "scripture Bible symbol", "Bible faith app icon"],
    test_en=["Bible christianity icon", "holy bible book", "Bible devotional symbol"],
)

# 455
process_icon("book-medical",
    st_en=["diary", "documentation", "health", "history", "journal", "library", "read", "record", "research"],
    pst_en=[
        "medical diary tracking daily symptoms", "diary of patient observations logged daily",
        "clinical documentation filed after each visit", "documentation requirements for hospital records",
        "health log maintained by the primary care doctor", "health history reviewed before surgery",
        "patient history recorded in the medical chart", "history of medications listed in the file",
        "medical journal with peer-reviewed articles", "research journal published quarterly",
        "hospital library stocked with medical references", "library of clinical guidelines for staff",
        "read the patient chart before the consultation", "read the research paper on drug interactions",
        "health record updated after the appointment", "record of vaccinations in the patient file",
        "medical research notes compiled in a notebook", "research data published in the journal",
    ],
    reg_en=[
        "medical book with a red cross on the cover",
        "patient health record kept in a medical book",
        "clinical reference book on a doctor's desk",
        "medical journal documenting patient history",
        "health log icon for an electronic records app",
        "medical textbook used in nursing school",
        "diagnostic manual referenced during consultation",
        "medical record book with tabbed sections",
        "research notebook filled with clinical findings",
        "medical book icon for a healthcare platform",
    ],
    conv_en=[
        "I need a medical book icon for my health app",
        "add a medical book symbol to the records section",
        "show a medical journal for the patient history screen",
        "use the medical book icon for the clinical notes feature",
    ],
    typo_en=[
        "medical diray tracking patient symptoms",
        "clincial documentation filed after visit",
        "helath history reviewed before operation",
        "patinet record updated after appointment",
    ],
    bnd_en=[
        "clipboard with a patient checklist attached",
        "stethoscope doctor listening to heartbeat",
        "pill bottle prescription medication container",
        "heart rate monitor ECG waveform icon",
        "folder patient file stored in a cabinet",
        "notebook plain journal without medical cross",
    ],
    valid_en=["medical book icon", "health record book symbol", "medical journal icon"],
    test_en=["medical book patient history", "health record book icon", "medical reference book"],
)

# 456
process_icon("bowling-ball",
    st_en=["alley", "candlepin", "gutter", "lane", "strike", "tenpin"],
    pst_en=[
        "bowling alley busy on a Friday night", "alley lanes waxed for the tournament",
        "candlepin bowling in New England style", "candlepin ball smaller than tenpin",
        "ball rolled into the gutter on frame one", "gutter ball ending a perfect run",
        "lane one reserved for the league team", "bowling lane with arrows as guide marks",
        "strike knocked all ten pins at once", "strike celebration with a fist pump",
        "tenpin setup waiting for the first ball", "tenpin bowling scored at the sports center",
    ],
    reg_en=[
        "heavy black bowling ball with three finger holes",
        "bowling ball rolling down the polished lane",
        "bowling ball knocking down all ten pins",
        "colorful bowling ball selected from the rack",
        "bowling ball icon for a sports scoring app",
        "strike frame marked with an X on the scorecard",
        "bowling alley with rows of lanes and pins",
        "league night bowling with a personalized ball",
        "bowling ball spinning toward the head pin",
        "bowling ball returned by the ball return machine",
    ],
    conv_en=[
        "I need a bowling ball icon for my sports app",
        "add a bowling ball symbol to the game tracker",
        "show a bowling ball for the alley booking feature",
        "use the bowling ball icon for the score section",
    ],
    typo_en=[
        "bowling bll rolling down the lane",
        "strike with a heavy bowlign ball",
        "guttter ball on the first frame",
        "tenpni pins set up at the end",
    ],
    bnd_en=[
        "billiard pool ball with a number on it",
        "basketball orange sphere with black seams",
        "soccer ball round black and white panels",
        "tennis ball yellow fuzzy sphere for court play",
        "pin single bowling pin white with red stripe",
        "golf ball dimpled white sphere on a tee",
    ],
    valid_en=["bowling ball sport icon", "bowling ball lane symbol", "bowling ball strike icon"],
    test_en=["bowling ball alley icon", "strike bowling ball", "bowling ball tenpin sport"],
)

# 457
process_icon("car-key",
    st_en=["auto", "automobile", "car", "key", "lock", "rental", "sedan", "transportation", "travel", "vehicle"],
    pst_en=[
        "auto repair shop handing over the keys", "auto key programmed at the dealership",
        "automobile key fob with remote buttons", "automobile ignition key on the ring",
        "car key placed on the counter at check-in", "car key scratched trying to unlock the door",
        "key cut at the locksmith for a spare", "key handed to the valet at the hotel",
        "lock disengaged by the car key fob", "lock opened remotely from the pocket",
        "rental car key picked up at the desk", "rental agreement signed before getting the key",
        "sedan key fob with push-to-start button", "sedan door unlocked by the proximity key",
        "transportation key for a fleet vehicle", "transportation company tracking all keys",
        "travel car hire key collected at the airport", "travel preparation includes car rental key",
        "vehicle key stored on a hook in the hallway", "vehicle ignition key inserted to start",
    ],
    reg_en=[
        "car key with a fob and unlock button",
        "ignition key inserted into the car starter",
        "key fob unlocking the car from a distance",
        "rental car key handed over at the counter",
        "spare car key cut at the locksmith",
        "valet handing back the car key after parking",
        "car key icon for a vehicle management app",
        "smart key proximity sensor unlocking the door",
        "car key on a ring with a brand logo tag",
        "lost car key emergency roadside assistance call",
    ],
    conv_en=[
        "I need a car key icon for my vehicle app",
        "add a car key symbol to the rental section",
        "show a car key for the fleet management screen",
        "use the car key icon for the valet booking feature",
    ],
    typo_en=[
        "car kye handed over at the rental desk",
        "ignition ky inserted to start the engine",
        "car keyfob unlockign the door remotely",
        "rentla car key picked up at the airport",
    ],
    bnd_en=[
        "house key door key on a plain ring",
        "padlock closed security icon",
        "key safe wall-mounted box with a code",
        "gear shift stick in a manual car",
        "steering wheel car interior control",
        "car silhouette without any key symbol",
    ],
    valid_en=["car key icon", "vehicle key fob symbol", "car key rental icon"],
    test_en=["car key ignition icon", "rental car key symbol", "car key fob icon"],
)

# 458
process_icon("corn",
    st_en=["cob", "corn", "ear", "fall", "grain", "kernel", "maize", "popcorn"],
    pst_en=[
        "corn cob grilled at the summer barbecue", "cob of corn boiled and buttered",
        "fresh corn harvested from the stalk", "corn on the cob at the county fair",
        "ear of corn pulled back to reveal kernels", "ear detached from the stalk at harvest",
        "fall harvest corn displayed as decoration", "fall cornucopia with corn and gourds",
        "grain corn dried and stored in the silo", "grain crop field stretching to the horizon",
        "golden kernel popped on a hot pan", "kernel by kernel corn removed from the cob",
        "maize cultivated by indigenous farmers", "maize flour ground for tortillas",
        "popcorn kernels exploding in the microwave", "buttered popcorn in a bag at the movie theater",
    ],
    reg_en=[
        "yellow corn cob with rows of golden kernels",
        "corn on the cob with a green husk pulled back",
        "field corn growing tall in the summer heat",
        "corn icon for a recipe or harvest app",
        "buttered corn cob at a summer cookout",
        "dried corn hanging in the barn for fall",
        "corn maze attraction at the pumpkin patch",
        "popcorn made from dried corn kernels",
        "maize crop harvested with a combine",
        "sweet corn boiled and served at the picnic",
    ],
    conv_en=[
        "I need a corn icon for my recipe app",
        "add a corn symbol to the vegetable section",
        "show a corn cob for the harvest tracker",
        "use the corn icon for the fall produce page",
    ],
    typo_en=[
        "yellow crn cob buttered at the cookout",
        "popcron kernels popped in the microwave",
        "corn kerenel removed from the cob",
        "mazie crop harvested in the fall",
    ],
    bnd_en=[
        "wheat stalk grain crop in a golden field",
        "carrot orange root vegetable with leafy top",
        "sunflower tall yellow head with seeds",
        "pumpkin round orange gourd for fall",
        "banana yellow curved fruit with peel",
        "pineapple tropical fruit with spiky crown",
    ],
    valid_en=["corn cob icon", "corn vegetable symbol", "corn on the cob harvest"],
    test_en=["corn grain crop icon", "maize corn symbol", "corn cob fall icon"],
)

# 459
process_icon("drone-front",
    st_en=["aerial", "surveillance", "uav", "unmanned", "vehicle"],
    pst_en=[
        "aerial photography from a drone overhead", "aerial drone survey of the construction site",
        "surveillance drone monitoring the border", "surveillance footage captured by the drone",
        "uav flying autonomously over the farmland", "uav deployed for search and rescue",
        "unmanned aircraft controlled from the ground", "unmanned drone carrying a delivery package",
        "vehicle with four rotors hovering in place", "aerial vehicle captured on radar",
    ],
    reg_en=[
        "quadcopter drone viewed from the front",
        "drone with four rotors hovering at eye level",
        "delivery drone flying above the neighborhood",
        "drone front view with camera mounted below",
        "UAV icon for a drone management app",
        "surveillance drone patrolling a wide area",
        "racing drone lined up at the starting gate",
        "agricultural drone spraying crops from above",
        "drone pilot launching a flight from the field",
        "drone front-facing icon for a flight app",
    ],
    conv_en=[
        "I need a drone icon for my flight app",
        "add a drone symbol to the UAV section",
        "show a drone for the aerial survey feature",
        "use the drone icon for the delivery tracker",
    ],
    typo_en=[
        "quadcpter drone hovering in place",
        "surviellance drone monitoring the area",
        "droen front camera mounted below",
        "uav flyng autonomously over the field",
    ],
    bnd_en=[
        "helicopter rotor aircraft flying sideways",
        "airplane commercial jet in flight",
        "satellite dish receiving signals from orbit",
        "camera on a tripod for photography",
        "robot arm automated industrial machine",
        "remote control handheld transmitter device",
    ],
    valid_en=["drone front view icon", "UAV drone symbol", "drone aerial icon"],
    test_en=["drone quadcopter icon", "drone surveillance symbol", "drone delivery icon"],
)

# 460
process_icon("lamp-desk",
    st_en=["bright", "furniture", "light"],
    pst_en=[
        "bright beam from the desk lamp hitting the page", "bright lamp illuminating the late-night study",
        "furniture piece completing the home office setup", "furniture store lamp section",
        "desk light switched on for the evening session", "reading light adjusted over the notebook",
    ],
    reg_en=[
        "adjustable desk lamp with a curved neck",
        "lamp illuminating a workspace at night",
        "desk lamp switched on for late-night studying",
        "architect lamp with a spring-balanced arm",
        "LED desk lamp saving energy in the office",
        "desk lamp icon for a productivity or office app",
        "bedside lamp on a nightstand for reading",
        "clamp-on lamp attached to a shelf above the desk",
        "lamp casting a warm yellow circle on the desk",
        "home office desk with a lamp and laptop",
    ],
    conv_en=[
        "I need a desk lamp icon for my workspace app",
        "add a lamp symbol to the office setup section",
        "show a desk lamp for the lighting control feature",
        "use the lamp icon for the study mode screen",
    ],
    typo_en=[
        "adujstable desk lmap on the table",
        "dessk lamp switched on for studying",
        "lamp iluminatig the workspace at night",
        "LED desklamp saving energy",
    ],
    bnd_en=[
        "ceiling light overhead panel fixture",
        "floor lamp tall standing light in the corner",
        "candle flame flickering on a holder",
        "lightbulb glowing incandescent idea icon",
        "flashlight handheld torch beam icon",
        "lantern camping portable light source",
    ],
    valid_en=["desk lamp icon", "lamp light workspace", "desk lamp study symbol"],
    test_en=["lamp desk office icon", "desk lamp light symbol", "lamp furniture icon"],
)

# 461
process_icon("trademark",
    st_en=["copyright", "mark", "register", "symbol", "tm", "trademark"],
    pst_en=[
        "copyright notice printed at the bottom of the page", "copyright law protecting creative works",
        "brand mark registered with the trademark office", "mark identifying the owner of the brand",
        "register a trademark before launching the product", "registered trademark symbol after the brand name",
        "legal symbol appended to a brand name", "symbol denoting intellectual property ownership",
        "tm symbol placed next to a new product name", "tm superscript after an unregistered brand",
        "trademark application filed with the government", "trademark protects the brand identity",
    ],
    reg_en=[
        "TM superscript symbol after a brand name",
        "trademark symbol indicating unregistered brand",
        "registered trademark R circle on a logo",
        "intellectual property mark on a product label",
        "trademark icon for a legal or brand management app",
        "brand name followed by the trademark symbol",
        "trademark filing to protect a company name",
        "copyright and trademark symbols on a document",
        "trademark symbol printed on packaging",
        "legal mark showing ownership of a brand",
    ],
    conv_en=[
        "I need a trademark icon for my brand app",
        "add a trademark symbol to the legal section",
        "show a TM mark for the brand registration feature",
        "use the trademark icon for the intellectual property page",
    ],
    typo_en=[
        "trademaerk symbol after the brand name",
        "TM superscirpt on the product label",
        "copyirght and trademark on the document",
        "regsiter the trademarrk before launch",
    ],
    bnd_en=[
        "registered R circle symbol different from TM",
        "copyright C circle symbol for creative works",
        "patent document protecting an invention",
        "legal scales of justice icon",
        "shield badge protection symbol",
        "stamp approval seal on a document",
    ],
    valid_en=["trademark TM symbol", "brand trademark icon", "trademark legal mark"],
    test_en=["trademark symbol icon", "TM mark brand", "trademark registration symbol"],
)

# 462
process_icon("transmission",
    st_en=["car", "clutch", "drivetrain", "gear", "gearbox", "manual", "shifter", "transmission"],
    pst_en=[
        "car transmission rebuilt by the mechanic", "car gearbox serviced at the shop",
        "clutch pedal pressed before shifting gears", "worn clutch slipping during acceleration",
        "drivetrain sending power to all four wheels", "drivetrain diagram for a mechanics course",
        "gear engaged smoothly at highway speed", "gear worn down after years of use",
        "gearbox oil changed at the service interval", "gearbox housing opened for inspection",
        "manual transmission preferred by driving enthusiasts", "manual gearshift in a sports car",
        "gear shifter knob wrapped in leather", "shifter moved into drive position",
        "transmission fluid checked on the dipstick", "automatic transmission shifting at the right RPM",
    ],
    reg_en=[
        "car gearbox with multiple gear positions",
        "manual transmission shift pattern on the knob",
        "automatic transmission cross-section diagram",
        "transmission fluid service reminder icon",
        "drivetrain diagram showing gearbox and axle",
        "gear shifter inside the center console",
        "transmission icon for a car service app",
        "clutch and gearbox replaced after high mileage",
        "sports car six-speed manual transmission",
        "transmission warning light on the dashboard",
    ],
    conv_en=[
        "I need a transmission icon for my car service app",
        "add a gearbox symbol to the drivetrain section",
        "show a transmission for the vehicle diagnostics screen",
        "use the transmission icon for the manual shift feature",
    ],
    typo_en=[
        "manual transmision shifted into second gear",
        "clutch pedal presses before gear change",
        "gearbox servied at the mechanic shop",
        "drivertain sending power to the wheels",
    ],
    bnd_en=[
        "steering wheel car interior driver control",
        "engine block motor under the hood",
        "brake pedal foot control stopping the car",
        "speedometer gauge showing current speed",
        "wrench mechanic tool for repairs",
        "car dashboard with instrument cluster",
    ],
    valid_en=["transmission gearbox icon", "car transmission symbol", "manual gearbox icon"],
    test_en=["transmission car service", "gearbox drivetrain icon", "transmission shift symbol"],
)

# 463
process_icon("user",
    st_en=["adult", "bust", "default", "employee", "gender-neutral", "person", "profile", "silhouette", "username"],
    pst_en=[
        "adult user account created on the platform", "adult profile verified with an ID",
        "bust silhouette as a default avatar", "bust icon representing an anonymous user",
        "default avatar shown before uploading a photo", "default user icon in a new account",
        "employee profile listed in the directory", "employee record with contact details",
        "gender-neutral icon suitable for any user", "gender-neutral profile in an inclusive app",
        "person icon tapped to open the profile", "person walking as a generic user icon",
        "profile page showing name and bio", "user profile updated with a new photo",
        "silhouette placeholder before a photo is added", "silhouette figure in a user list",
        "username displayed below the avatar icon", "username searched in the directory",
    ],
    reg_en=[
        "simple silhouette of a person as a user icon",
        "generic human figure representing any account",
        "user avatar placeholder in a profile card",
        "default person icon shown before photo upload",
        "user icon tapped to open account settings",
        "profile silhouette in a login or signup form",
        "user symbol in a navigation menu bar",
        "single person icon representing one account",
        "user icon for an employee directory app",
        "gender-neutral person icon for an inclusive platform",
    ],
    conv_en=[
        "I need a user icon for my profile screen",
        "add a user symbol to the account section",
        "show a person icon for the login feature",
        "use the user icon for the employee directory",
    ],
    typo_en=[
        "defualt user silhouette before photo upload",
        "persone icon tapped for account settings",
        "proflie page showing username and bio",
        "employe user record in the directory",
    ],
    bnd_en=[
        "group of people multiple users icon",
        "user with a gear settings badge overlay",
        "user with a check verified account badge",
        "user plus add a new account icon",
        "avatar photo uploaded profile picture",
        "contact person in an address book entry",
    ],
    valid_en=["user profile icon", "person silhouette symbol", "user account icon"],
    test_en=["default user icon", "user profile silhouette", "person user symbol"],
)

# 464
process_icon("user-police",
    st_en=["cop", "officer", "patrol", "police", "trooper"],
    pst_en=[
        "cop directing traffic at the intersection", "cop on duty patrolling the neighborhood",
        "police officer responding to an emergency call", "officer in uniform at the precinct",
        "patrol unit driving through the area", "patrol officer checking the perimeter",
        "police department badge icon for a safety app", "police scanner picking up the call",
        "state trooper pulling over a speeding vehicle", "trooper stationed at the highway checkpoint",
    ],
    reg_en=[
        "police officer silhouette with a badge and cap",
        "cop in uniform represented as a user icon",
        "law enforcement officer avatar in a safety app",
        "police icon for an emergency contact screen",
        "officer on patrol shown as a person symbol",
        "police user icon for a first responder app",
        "security officer profile in a building management app",
        "police trooper with a hat brim and badge",
        "cop icon used in a neighborhood watch feature",
        "law enforcement user symbol for a dispatch app",
    ],
    conv_en=[
        "I need a police officer icon for my safety app",
        "add a cop symbol to the emergency contact section",
        "show a police user for the patrol tracking feature",
        "use the officer icon for the first responder page",
    ],
    typo_en=[
        "plice officer responding to the emergency",
        "cop durecting traffic at the corner",
        "trooper patoling the highway checkpoint",
        "officre in uniform at the precinct",
    ],
    bnd_en=[
        "firefighter helmet and gear silhouette",
        "doctor person in a medical coat icon",
        "security guard badge shield symbol",
        "soldier military person in uniform",
        "judge person with a gavel in court",
        "construction worker with a hard hat",
    ],
    valid_en=["police officer icon", "cop user symbol", "law enforcement icon"],
    test_en=["police user icon", "officer patrol symbol", "user police badge icon"],
)

print("\nDone! All 13 icons processed.")
