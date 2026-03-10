#!/usr/bin/env python3
"""Generate English training data for icons 465-475."""
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

# 465
process_icon("badge-sheriff",
    st_en=["cowboy", "justice", "law", "western"],
    pst_en=[
        "cowboy sheriff pinning a badge on his vest", "cowboy hat and star badge in the old west",
        "justice served by the county sheriff", "justice symbol on a star-shaped badge",
        "law enforcement badge worn by the sheriff", "law and order in a western town",
        "western sheriff keeping the peace in town", "western film hero with a shiny star badge",
    ],
    reg_en=[
        "gold star-shaped sheriff badge pinned to a vest",
        "western sheriff badge with a star cutout",
        "county sheriff badge engraved with a name",
        "old west lawman wearing a tin star badge",
        "sheriff badge icon for a western-themed app",
        "deputy sheriff badge smaller than the sheriff's star",
        "badge of authority pinned on a cowboy sheriff",
        "sheriff star badge on a leather holster belt",
        "law enforcement badge for a security game app",
        "sheriff badge symbol for a roles and ranks feature",
    ],
    conv_en=[
        "I need a sheriff badge icon for my game app",
        "add a badge-sheriff symbol to the law section",
        "show a sheriff star for the western role feature",
        "use the badge-sheriff icon for the officer rank",
    ],
    typo_en=[
        "gold sehriff badge pinned to the vest",
        "western sherif star badge of authority",
        "sherrif badge in the old west town",
        "cownboy law badge for the deputy",
    ],
    bnd_en=[
        "police officer badge round shield design",
        "medal award ribbon hanging from a pin",
        "star gold five-point star shape symbol",
        "crown royalty symbol with jewels",
        "seal official wax impression on a document",
        "ribbon award rosette with a center disc",
    ],
    valid_en=["sheriff badge star icon", "western sheriff badge symbol", "badge-sheriff icon"],
    test_en=["sheriff star badge law", "cowboy sheriff badge icon", "badge-sheriff western"],
)

# 466
process_icon("book-quran",
    st_en=["book", "islam", "muslim", "religion"],
    pst_en=[
        "holy book opened to a verse for recitation", "sacred book passed down through generations",
        "islam guided by the teachings of the Quran", "islam scripture recited during prayer",
        "muslim community reading the Quran together", "muslim prayer book on the shelf",
        "religion centered on the holy Quran", "religion class studying Quranic verses",
    ],
    reg_en=[
        "green Quran with Arabic calligraphy on the cover",
        "Quran opened on a wooden stand for recitation",
        "Muslim holy scripture bound in leather",
        "Quran icon for a faith or prayer app",
        "Quran verse displayed in Arabic script",
        "Quran placed on a stand at the mosque",
        "Islamic holy book revered by the community",
        "Quran memorized by students at the madrasa",
        "Quran recited during the evening prayer",
        "Quran gifted to a new Muslim convert",
    ],
    conv_en=[
        "I need a Quran icon for my Islamic app",
        "add a Quran symbol to the religion section",
        "show a Quran for the daily verse feature",
        "use the Quran icon for the prayer guide page",
    ],
    typo_en=[
        "holy quran opened for recitaiton",
        "muslm community reading the quran",
        "isalm scripture recited at prayer",
        "relgion class studying Quranic verse",
    ],
    bnd_en=[
        "Bible Christian holy scripture on a lectern",
        "Torah Jewish scroll rolled with handles",
        "book open pages of general reading",
        "scroll ancient parchment rolled document",
        "mosque building with dome and minaret",
        "crescent moon and star Islamic symbol",
    ],
    valid_en=["Quran holy book icon", "Islamic Quran symbol", "book-quran faith icon"],
    test_en=["Quran book islam icon", "muslim holy book symbol", "Quran prayer app icon"],
)

# 467
process_icon("books-medical",
    st_en=["diary", "documentation", "health", "journal", "library", "read", "records", "research"],
    pst_en=[
        "medical diary tracking patient observations daily", "diary entry logged after each clinical visit",
        "clinical documentation stored in a records system", "documentation standards for hospital procedures",
        "health reference books on the doctor's shelf", "health library available to all hospital staff",
        "peer-reviewed journal on surgical techniques", "medical journal subscription for professionals",
        "hospital library stocked with clinical references", "digital library of medical textbooks",
        "read the protocol before performing the procedure", "read the drug interaction manual carefully",
        "patient records archived in multiple volumes", "records pulled for a legal medical review",
        "research notes compiled across several volumes", "multi-volume research collection in the lab",
    ],
    reg_en=[
        "stack of medical books with a red cross on the spine",
        "multiple health reference volumes on a shelf",
        "medical library with rows of clinical textbooks",
        "doctor's bookshelf of diagnostic and treatment guides",
        "medical books icon for a healthcare education app",
        "nursing textbooks stacked beside the workstation",
        "collection of medical journals in a teaching hospital",
        "medical research library with indexed volumes",
        "books-medical icon for a clinical resource platform",
        "set of medical books covering anatomy and pharmacology",
    ],
    conv_en=[
        "I need a medical books icon for my health platform",
        "add a books-medical symbol to the library section",
        "show medical books for the clinical reference feature",
        "use the books-medical icon for the research archive",
    ],
    typo_en=[
        "stack of medicla books on the shelf",
        "helath library with clinical textboks",
        "medical journla subscription for staff",
        "clincial docuemntation in multiple volumes",
    ],
    bnd_en=[
        "single medical book with a cross on cover",
        "clipboard with patient checklist attached",
        "folder file organizer for medical records",
        "notebook plain journal without medical cross",
        "library building with books and columns",
        "graduation cap academic achievement icon",
    ],
    valid_en=["medical books icon", "health library books symbol", "books-medical reference"],
    test_en=["medical books stack icon", "clinical books symbol", "books-medical library icon"],
)

# 468
process_icon("bottle-baby",
    st_en=["baby", "bottle", "formula", "infant", "nurse", "nursing"],
    pst_en=[
        "baby fed with a bottle before bedtime", "baby bottle warmed in a bowl of water",
        "bottle sterilized in the microwave before use", "glass bottle with a silicone nipple",
        "formula prepared and poured into the bottle", "powdered formula measured for a feed",
        "infant drinking from a held bottle", "infant hunger cue responded to with a bottle",
        "nurse handing a bottle to the new parent", "nurse teaching bottle-feeding technique",
        "nursing parent switching between breast and bottle", "nursing schedule tracked in a baby app",
    ],
    reg_en=[
        "baby bottle with measurement marks on the side",
        "plastic baby bottle with a silicone teat",
        "bottle of infant formula ready to feed",
        "baby bottle icon for a parenting or infant app",
        "warming a baby bottle under warm running water",
        "sterilized baby bottle in the drying rack",
        "formula-filled bottle for a newborn feeding",
        "dad holding a bottle for the baby at night",
        "bottle with a slow-flow nipple for a newborn",
        "baby bottle symbol in a feeding schedule app",
    ],
    conv_en=[
        "I need a baby bottle icon for my parenting app",
        "add a bottle symbol to the feeding tracker",
        "show a baby bottle for the infant schedule screen",
        "use the bottle-baby icon for the formula section",
    ],
    typo_en=[
        "baaby bottle warmed before feeding",
        "infnat bottle with silicone nipple",
        "fomrula poured into the baby bottle",
        "nurssing schedule tracked in the app",
    ],
    bnd_en=[
        "pacifier soother rubber nipple for calming",
        "sippy cup toddler transition drinking cup",
        "milk carton school lunch dairy container",
        "breast pump electric double-pump device",
        "baby food jar with pureed fruit inside",
        "water bottle reusable adult drink container",
    ],
    valid_en=["baby bottle icon", "infant bottle symbol", "bottle-baby feeding icon"],
    test_en=["baby bottle formula icon", "infant feeding bottle", "bottle-baby parenting app"],
)

# 469
process_icon("bowl-hot",
    st_en=["bisque", "bouillon", "bowl", "broth", "chicken", "chowder", "gazpacho", "ramen", "stew"],
    pst_en=[
        "lobster bisque served in a warm bowl", "creamy bisque with a swirl of cream",
        "bouillon cube dissolved in hot water", "chicken bouillon for a quick broth base",
        "bowl of steaming soup on the table", "ceramic bowl with a lid keeping it hot",
        "warm broth sipped on a cold evening", "broth ladled from the pot into a bowl",
        "chicken soup remedy for a winter cold", "chicken noodle soup in a deep bowl",
        "clam chowder served in a bread bowl", "thick New England chowder with cream",
        "cold gazpacho poured into a chilled bowl", "gazpacho blended from fresh tomatoes",
        "ramen bowl topped with a soft-boiled egg", "steaming ramen delivered to the table",
        "beef stew simmered for three hours", "hearty stew with vegetables and dumplings",
    ],
    reg_en=[
        "steaming bowl of hot soup with vapor rising",
        "ceramic bowl filled with ramen and toppings",
        "hot soup bowl icon for a food delivery app",
        "bowl of broth with noodles and vegetables",
        "chicken soup in a large white bowl",
        "stew ladled into a bowl at dinnertime",
        "hot bowl of chowder on a wooden table",
        "steam curling from a freshly served bowl",
        "bowl of soup emoji for a comfort food app",
        "instant noodle bowl heated in the microwave",
    ],
    conv_en=[
        "I need a hot bowl icon for my food app",
        "add a soup bowl symbol to the menu section",
        "show a steaming bowl for the hot meals feature",
        "use the bowl-hot icon for the ramen category",
    ],
    typo_en=[
        "steamig bowl of ramen with soft-boiled egg",
        "chickne soup in a large cerarmic bowl",
        "hot boowl of stew on the dinner table",
        "ramne bowl topped with nori and egg",
    ],
    bnd_en=[
        "plate flat dish with food served on it",
        "mug handle cup for hot coffee or tea",
        "pot large cooking vessel on the stove",
        "salad bowl cold greens and vegetables",
        "cup and saucer for a warm beverage",
        "ladle long-handled spoon for serving soup",
    ],
    valid_en=["hot bowl soup icon", "steaming bowl symbol", "bowl-hot ramen icon"],
    test_en=["hot bowl food app", "soup bowl steaming icon", "bowl-hot stew symbol"],
)

# 470
process_icon("bra",
    st_en=["bikini", "bra", "brassiere", "swim"],
    pst_en=[
        "bikini top worn at the beach", "bikini set for a summer vacation",
        "bra fitting appointment at the lingerie store", "bra size measured for the right support",
        "brassiere with underwire for extra support", "brassiere laundered with delicate care",
        "swim top with built-in bra lining", "swimwear category in a fashion app",
    ],
    reg_en=[
        "bra with two cups and adjustable straps",
        "lingerie bra icon for a clothing or fashion app",
        "sports bra worn during a workout session",
        "underwire bra providing shape and support",
        "bra hanging on a drying rack after washing",
        "swimwear bra top for beachwear",
        "bra size guide in an apparel shopping app",
        "strapless bra worn under an evening dress",
        "bra icon for a women's clothing category",
        "padded bra for everyday comfortable wear",
    ],
    conv_en=[
        "I need a bra icon for my fashion app",
        "add a bra symbol to the lingerie section",
        "show a bra for the women's clothing category",
        "use the bra icon for the swimwear section",
    ],
    typo_en=[
        "sports bra wron during the workout",
        "bra fittign appointment at the store",
        "brasseire with underwire for support",
        "swimear bra top for beach season",
    ],
    bnd_en=[
        "underwear briefs folded in a drawer",
        "swimsuit one-piece full-body swim garment",
        "tank top sleeveless shirt worn casually",
        "shirt clothing top worn as outerwear",
        "bikini bottom paired with a swim top",
        "dress full garment for formal occasions",
    ],
    valid_en=["bra lingerie icon", "brassiere fashion symbol", "bra clothing icon"],
    test_en=["bra swimwear icon", "bra fashion app symbol", "bra lingerie category"],
)

# 471
process_icon("copyright",
    st_en=["brand", "copyright", "mark", "register", "trademark"],
    pst_en=[
        "brand identity protected by copyright law", "brand name filed for legal protection",
        "copyright notice printed at the bottom of the page", "copyright infringement case filed in court",
        "mark indicating protected intellectual property", "watermark applied to prevent unauthorized use",
        "register a copyright before publishing the work", "registered mark on a published design",
        "trademark and copyright protecting the brand", "trademark attorney filing the copyright claim",
    ],
    reg_en=[
        "copyright symbol C inside a circle",
        "copyright notice on a website footer",
        "all rights reserved copyright statement",
        "copyright year printed on a published book",
        "copyright icon for a legal or content management app",
        "creative work protected by copyright",
        "copyright infringement warning on digital content",
        "copyright symbol placed beside the author name",
        "copyright registration submitted to the office",
        "copyright badge showing ownership of original content",
    ],
    conv_en=[
        "I need a copyright icon for my content app",
        "add a copyright symbol to the legal section",
        "show a copyright mark for the publishing feature",
        "use the copyright icon for the rights management page",
    ],
    typo_en=[
        "copyrigt symbol on the website footer",
        "all rigths reserved copywright notice",
        "copyirght year printed in the book",
        "registerred copyright filed with the office",
    ],
    bnd_en=[
        "trademark TM superscript brand symbol",
        "registered R circle mark on a logo",
        "patent document protecting an invention",
        "creative commons license share-alike icon",
        "legal scales of justice court symbol",
        "fingerprint unique ownership identifier",
    ],
    valid_en=["copyright symbol icon", "copyright C circle mark", "copyright legal icon"],
    test_en=["copyright notice symbol", "copyright mark icon", "copyright legal app"],
)

# 472
process_icon("glass",
    st_en=["alcohol", "beverage", "drink", "glass", "milk", "water"],
    pst_en=[
        "alcohol poured into a tall clear glass", "a glass of alcohol set on the bar counter",
        "cold beverage in a frosted glass", "beverage glass filled to the brim",
        "drink of water from a tall glass", "drink poured into a glass at the restaurant",
        "glass filled with ice and lemonade", "empty glass left on the counter",
        "glass of cold milk with a cookie", "milk poured into a glass for a child",
        "water glass refilled by the server", "glass of water placed beside the plate",
    ],
    reg_en=[
        "tall clear drinking glass on a table",
        "glass filled with cold water and ice",
        "glass of milk beside a plate of cookies",
        "empty glass turned upside down on a shelf",
        "drinking glass icon for a hydration app",
        "glass of water reminder for daily intake",
        "frosted glass of juice on a summer day",
        "glass half full on the breakfast table",
        "glass of water in a minimalist icon style",
        "beverage glass used in a restaurant menu app",
    ],
    conv_en=[
        "I need a glass icon for my hydration app",
        "add a glass symbol to the drink section",
        "show a drinking glass for the water tracker",
        "use the glass icon for the beverage menu",
    ],
    typo_en=[
        "tall cleer drinking glass on the table",
        "gllass of cold water with ice cubes",
        "bevrage glass filled to the rim",
        "glas of milk beside the cookie plate",
    ],
    bnd_en=[
        "wine glass with a stem and bowl",
        "mug with a handle for hot drinks",
        "bottle water bottle with a cap",
        "cup small handle-less vessel for espresso",
        "can soda tin cylindrical drink container",
        "pitcher large jug for pouring drinks",
    ],
    valid_en=["drinking glass icon", "glass of water symbol", "glass beverage icon"],
    test_en=["glass drink icon", "water glass symbol", "glass milk icon"],
)

# 473
process_icon("lungs",
    st_en=["air", "breath", "covid-19", "exhalation", "inhalation", "lungs", "organ", "respiration", "respiratory"],
    pst_en=[
        "fresh air filling the lungs on a morning run", "air quality sensor measuring lung health",
        "deep breath taken before diving underwater", "breath held during a meditation exercise",
        "covid-19 affecting the respiratory system", "covid-19 lung scan showing inflammation",
        "exhalation releasing carbon dioxide slowly", "full exhalation emptying the lungs",
        "deep inhalation expanding the chest cavity", "inhalation of fresh mountain air",
        "lungs diagram labeled for anatomy class", "healthy lungs shown in a medical illustration",
        "vital organ keeping the body oxygenated", "organ transplant waiting list for lungs",
        "respiration rate monitored by a fitness band", "respiration tracked during sleep stages",
        "respiratory infection treated with antibiotics", "respiratory system affected by asthma",
    ],
    reg_en=[
        "pair of lungs illustrated for an anatomy app",
        "healthy lungs glowing pink in a medical diagram",
        "lung capacity measured with a spirometer",
        "lungs icon for a respiratory health app",
        "breathing exercise with lungs expanding fully",
        "lungs scan showing clear airways",
        "pulmonary system diagram with bronchi labeled",
        "COVID-19 effect on lung tissue illustrated",
        "asthma inhaler supporting lung function",
        "lungs symbol for a fitness breathing tracker",
    ],
    conv_en=[
        "I need a lungs icon for my health app",
        "add a lungs symbol to the respiratory section",
        "show lungs for the breathing exercise feature",
        "use the lungs icon for the pulmonary health page",
    ],
    typo_en=[
        "healthy lunsg shown in the anatomy diagram",
        "repsiratory infection affecting the lungs",
        "deep breeth expanding the lung capacity",
        "covid-19 inflamation in the lung tissue",
    ],
    bnd_en=[
        "heart organ beating in the chest cavity",
        "kidney bean-shaped organ filtering blood",
        "brain organ in the skull for cognition",
        "stomach digestive organ for food processing",
        "liver large organ for detoxification",
        "nose breathing airway entry point icon",
    ],
    valid_en=["lungs organ icon", "respiratory lungs symbol", "lungs health icon"],
    test_en=["lungs anatomy icon", "breathing lungs symbol", "lungs respiratory app"],
)

# 474
process_icon("mosque",
    st_en=["building", "islam", "landmark", "mosque", "muslim", "religion"],
    pst_en=[
        "building with a dome and minaret silhouette", "religious building recognized worldwide",
        "islam practiced in the mosque daily", "islamic worship inside the mosque",
        "famous landmark mosque visited by tourists", "landmark mosque in the city skyline",
        "mosque crowded during Friday prayer", "mosque icon for a prayer time app",
        "muslim community gathering at the mosque", "muslim worshipper removing shoes at the door",
        "religion centered on prayer at the mosque", "religion and community meeting place",
    ],
    reg_en=[
        "mosque with a large dome and tall minarets",
        "islamic mosque silhouette at sunset",
        "mosque icon for a prayer time or Quran app",
        "Friday prayer congregation at the mosque",
        "ornate mosque facade with geometric patterns",
        "minaret tower of a mosque used for the call to prayer",
        "mosque visited by Muslim pilgrims",
        "local mosque serving the community",
        "historic mosque landmark in a travel app",
        "mosque symbol for an Islamic cultural app",
    ],
    conv_en=[
        "I need a mosque icon for my prayer app",
        "add a mosque symbol to the Islamic section",
        "show a mosque for the prayer time feature",
        "use the mosque icon for the Muslim community page",
    ],
    typo_en=[
        "mosque with a large doem and minarets",
        "islmaic mosque silouhette at sunset",
        "mosqe icon for the prayer time app",
        "musim community gathering at the mosuqe",
    ],
    bnd_en=[
        "church Christian building with a steeple",
        "temple Hindu or Buddhist religious building",
        "synagogue Jewish place of worship",
        "cathedral large Gothic Christian church",
        "crescent moon and star Islamic symbol",
        "prayer beads rosary for counting prayers",
    ],
    valid_en=["mosque building icon", "islamic mosque symbol", "mosque prayer app icon"],
    test_en=["mosque landmark icon", "muslim mosque symbol", "mosque religion icon"],
)

# 475
process_icon("volcano",
    st_en=["caldera", "eruption", "lava", "magma", "mountain", "smoke", "volcano"],
    pst_en=[
        "caldera formed after the eruption collapsed", "caldera lake inside an extinct volcano",
        "volcanic eruption sending ash into the sky", "eruption warning issued by seismologists",
        "lava flowing down the slope at night", "red lava stream hardening into rock",
        "magma chamber pressurizing beneath the surface", "magma rising toward the surface",
        "volcanic mountain visible from the coast", "mountain peak glowing with lava",
        "smoke column rising from the crater", "thick smoke billowing from the volcano",
        "volcano erupting with fire and ash clouds", "volcano icon for a natural disaster app",
    ],
    reg_en=[
        "volcano erupting with lava and ash plume",
        "mountain with a glowing red crater at the top",
        "active volcano on a tropical island",
        "volcano icon for a geology or science app",
        "lava flow from a Hawaiian shield volcano",
        "volcano hazard map showing danger zones",
        "erupting volcano for a weather or disaster app",
        "caldera of a supervolcano from aerial view",
        "volcanic smoke column visible for miles",
        "volcano silhouette at dusk with glowing lava",
    ],
    conv_en=[
        "I need a volcano icon for my science app",
        "add a volcano symbol to the natural disaster section",
        "show a volcano for the geology feature",
        "use the volcano icon for the eruption alert page",
    ],
    typo_en=[
        "volocano erupting with lava and ash",
        "volcanic erruption warning issued",
        "lava flowng down the mountain slope",
        "volcanoe caldera visible from above",
    ],
    bnd_en=[
        "mountain peak snowy summit without lava",
        "fire flame burning orange without a crater",
        "island tropical land mass in the ocean",
        "earthquake crack splitting the ground",
        "geyser hot spring shooting water upward",
        "campfire logs burning in a ring of stones",
    ],
    valid_en=["volcano eruption icon", "volcanic mountain symbol", "volcano lava icon"],
    test_en=["volcano science app icon", "erupting volcano symbol", "volcano lava mountain"],
)

print("\nDone! All 11 icons processed.")
