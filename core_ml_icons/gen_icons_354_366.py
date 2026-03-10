#!/usr/bin/env python3
"""Generate English training data for icons 354-366."""
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

# 354 — panties (e6d4)
process_icon("panties",
    st_en=["bikini", "swim", "two-piece", "underclothes", "underclothing", "underwear"],
    pst_en=[
        "bikini bottom hanging on a hook", "floral bikini for a beach vacation",
        "swim briefs for the pool", "swim season clothing at the store",
        "two-piece swimwear set for summer", "matching two-piece for the beach",
        "comfortable underclothes for everyday wear", "pack underclothes for a weekend trip",
        "underclothing section in a clothing app", "basic underclothing folded in a drawer",
        "cotton underwear in a laundry pile", "buy underwear in a clothing store",
    ],
    reg_en=[
        "women's underwear neatly folded in a drawer",
        "clothing icon for a lingerie or apparel category",
        "fashion app icon representing intimate wear",
        "lace-trimmed underwear on a white background",
        "add panties to the wardrobe or laundry checklist",
        "intimate apparel category in an e-commerce store",
        "soft cotton underwear with an elastic waistband",
        "swimwear bottom for the beach and pool",
        "clothing icon for a fashion shopping app",
        "bikini briefs laid flat for a product photo",
    ],
    conv_en=[
        "I need a panties icon for my wardrobe tracker app",
        "add a panties symbol to the clothing category",
        "show panties for the intimate apparel section",
        "use the panties icon for the fashion shopping feature",
    ],
    typo_en=[
        "panites in the laundry basket",
        "panteis folded in a drawer",
        "pantis in the underwear drawer",
        "pandies with a lace trim",
    ],
    bnd_en=[
        "sports bra with a racerback design",
        "lace bra hanging on a clothing rack",
        "denim shorts with a frayed hem",
        "athletic shorts for running and workouts",
        "pair of ankle socks in a dresser drawer",
        "colorful patterned socks on a wooden floor",
    ],
    valid_en=[
        "women's underwear icon",
        "panties in a clothing app",
        "intimate apparel symbol",
    ],
    test_en=[
        "bikini briefs for a wardrobe tracker",
        "cotton underwear folded in a drawer",
        "panties icon in a fashion app",
    ],
)

# 355 — pants (e6d5)
process_icon("pants",
    st_en=["jeans", "legs", "pants", "pockets", "slacks"],
    pst_en=[
        "blue jeans with a worn denim look", "pair of jeans hanging on a hook",
        "pants covering both legs from waist to ankle", "wide-leg pants for a relaxed fit",
        "dress pants pressed and ready for work", "fold your pants before putting them away",
        "cargo pants with deep side pockets", "pockets sewn into the front of the pants",
        "tailored slacks for a business casual look", "light gray slacks paired with a blazer",
    ],
    reg_en=[
        "pair of trousers folded neatly in half",
        "wardrobe icon for a clothing tracker app",
        "fashion app icon representing bottom clothing",
        "dark navy dress pants with a belt loop",
        "packing pants for a business trip",
        "bottoms category in an online clothing store",
        "wide-leg pants hanging on a clothing rack",
        "ironing pants before an important meeting",
        "apparel icon for a laundry or wardrobe app",
        "slim fit pants with front creases and cuffs",
    ],
    conv_en=[
        "I need a pants icon for my outfit planner app",
        "add a pants symbol to the wardrobe section",
        "show pants for the clothing category",
        "use the pants icon for the laundry tracker feature",
    ],
    typo_en=[
        "paants with deep pockets",
        "pnats folded in the drawer",
        "pats hanging on the rack",
        "pabts for a casual day",
    ],
    bnd_en=[
        "denim shorts cut above the knee",
        "athletic shorts with a drawstring waist",
        "pleated skirt flaring out at the waist",
        "knee-length skirt in a floral print",
        "jogger sweatpants with an elastic ankle cuff",
        "track pants with a stripe down the side",
    ],
    valid_en=[
        "trousers folded neatly in half",
        "pants icon for a wardrobe app",
        "pair of dress pants",
    ],
    test_en=[
        "jeans hanging on a clothing rack",
        "pants for an outfit tracker",
        "slacks pressed for a business meeting",
    ],
)

# 356 — peanut (e430)
process_icon("peanut",
    st_en=["goober", "legume", "nut", "shell"],
    pst_en=[
        "goober candy peanut at the movie theater", "southern slang goober pea snack",
        "peanut is a legume not a true tree nut", "legume crop grown underground in the soil",
        "roasted nut in a snack mix", "nut allergy warning on the food label",
        "peanut in its outer bumpy shell", "cracking the shell to get to the nut inside",
    ],
    reg_en=[
        "whole peanut in its tan beige shell",
        "roasted peanuts in a bowl as a snack",
        "food icon for a nut or allergy tracker",
        "two peanuts inside a bumpy oval shell",
        "spreading peanut butter on a slice of bread",
        "allergy warning icon in a food labeling app",
        "handful of peanuts at a baseball stadium",
        "pale brown legume shell with ridged seams",
        "ingredient icon for a recipe app",
        "peanuts roasting in a bag at a street fair",
    ],
    conv_en=[
        "I need a peanut icon for my allergy tracking app",
        "add a peanut symbol to the snacks category",
        "show a peanut for the nut allergy warning section",
        "use the peanut icon for the healthy snacks feature",
    ],
    typo_en=[
        "paenut in a shell",
        "penut roasted in a bag",
        "peanut buttr spread on toast",
        "peantu allergy warning",
    ],
    bnd_en=[
        "whole almond with a smooth brown skin",
        "sliced almonds scattered on a baking tray",
        "walnut with a wrinkled kernel inside a hard shell",
        "cracked walnut half on a wooden surface",
        "green pistachio with a cracked shell",
        "bowl of salted pistachio nuts",
    ],
    valid_en=[
        "peanut in its bumpy shell",
        "roasted peanuts as a snack",
        "peanut icon for a food app",
    ],
    test_en=[
        "peanut shell cracked open",
        "handful of peanuts at a game",
        "peanut allergy symbol",
    ],
)

# 357 — pencil (f303)
process_icon("pencil",
    st_en=["design", "draw", "edit", "lead", "maintenance", "modify", "pencil", "update", "write"],
    pst_en=[
        "design a layout with a pencil sketch", "rough pencil design on graph paper",
        "draw a quick sketch with a pencil", "draw freehand lines on the canvas",
        "edit a text field by tapping the pencil", "edit mode activated with a pencil icon",
        "sharp lead tip of a number two pencil", "lead pencil smudging on a rough paper",
        "maintenance mode icon for app settings", "schedule maintenance using the pencil button",
        "modify an entry by clicking the pencil", "modify existing data in the form",
        "yellow pencil with a pink eraser", "pencil icon to indicate editable content",
        "update a record by tapping the pencil", "update your profile with the edit pencil",
        "write notes by hand with a pencil", "write in a sketchbook with a sharpened pencil",
    ],
    reg_en=[
        "yellow wooden pencil with a sharp tip",
        "tap the pencil icon to enter edit mode",
        "edit button in a content management system",
        "pencil with a pink eraser on the end",
        "drawing a freehand sketch on paper",
        "design tool icon for a creative app",
        "hexagonal pencil barrel with a painted yellow finish",
        "pencil icon next to an editable text field",
        "note-taking app with a pencil symbol",
        "sharpened pencil leaving a graphite line on paper",
    ],
    conv_en=[
        "I need a pencil icon for my notes editing app",
        "add a pencil symbol to the edit button",
        "show a pencil for the drawing canvas section",
        "use the pencil icon for the modify profile feature",
    ],
    typo_en=[
        "pencial for drawing",
        "pencl sketch on paper",
        "pencli icon for editing",
        "penci drawing on paper",
    ],
    bnd_en=[
        "fountain pen with a nib writing in ink",
        "ballpoint pen clicking on a desk",
        "thick marker drawing a bold line on paper",
        "highlighter marker cap removed and ready to use",
        "wooden ruler with centimeter markings",
        "metal straight edge ruler on a drafting table",
    ],
    valid_en=[
        "yellow pencil with a sharp tip",
        "pencil icon for editing a document",
        "pencil symbol to draw or write",
    ],
    test_en=[
        "tap pencil to enter edit mode",
        "hand-drawn sketch with a pencil",
        "pencil icon in a note-taking app",
    ],
)

# 358 — person (f183)
process_icon("person",
    st_en=["man", "person standing", "stand", "standing", "woman"],
    pst_en=[
        "silhouette of a man standing upright", "man icon in a user profile",
        "person standing with arms at their sides", "person standing in a queue at the store",
        "stand straight for a posture reminder", "stand up from the desk for a break",
        "standing figure used as a person icon", "standing position tracked in a fitness app",
        "silhouette of a woman in an app icon", "woman standing in a user profile photo",
    ],
    reg_en=[
        "simple silhouette of a person standing upright",
        "user account icon for a profile screen",
        "generic person icon for a contact in an address book",
        "stick figure of a person with a round head",
        "tap the person icon to view your profile",
        "avatar placeholder in a social media app",
        "lone human figure standing facing forward",
        "person icon next to a username field",
        "default user icon when no photo is uploaded",
        "tall standing figure representing an individual",
    ],
    conv_en=[
        "I need a person icon for my user profile screen",
        "add a person symbol to the account settings",
        "show a person for the attendees list section",
        "use the person icon for the contact placeholder",
    ],
    typo_en=[
        "peron standing in line",
        "persom looking forward",
        "preson standing upright",
        "perosn icon for profile",
    ],
    bnd_en=[
        "person icon inside a circle badge",
        "circular avatar with a head and shoulders outline",
        "two people standing side by side as a group",
        "three person silhouettes representing a team",
        "person running with arms and legs extended",
        "jogging figure icon for a fitness tracker",
    ],
    valid_en=[
        "person standing silhouette icon",
        "user profile person symbol",
        "person icon for a contact list",
    ],
    test_en=[
        "standing person figure",
        "generic person icon in an app",
        "person symbol for a user account",
    ],
)

# 359 — phone (f095)
process_icon("phone",
    st_en=["call", "earphone", "number", "phone", "receiver", "support",
           "talking", "telephone", "voice"],
    pst_en=[
        "make a phone call to a friend", "incoming call notification on the screen",
        "earphone connected to the phone", "built-in earphone for hands-free calls",
        "dial a phone number on the keypad", "save the number in your contacts",
        "desk phone sitting on the office table", "pick up the phone to answer the call",
        "classic phone receiver off the hook", "lift the receiver to make a call",
        "call customer support for assistance", "support hotline phone number on the website",
        "talking on the phone for an hour", "talking hands-free while driving",
        "old rotary telephone on a wooden desk", "telephone handset icon for making calls",
        "voice call over the internet", "leave a voice message after the beep",
    ],
    reg_en=[
        "old-fashioned telephone handset silhouette",
        "tap to call a contact from the address book",
        "customer service phone icon on a help page",
        "curved phone receiver with a coiled cord",
        "phone call icon on a mobile contact screen",
        "helpline icon for a support center app",
        "rotary dial telephone on a vintage desk",
        "answer or decline a call with the phone button",
        "phone symbol next to a business contact number",
        "classic handset with earpiece and mouthpiece",
    ],
    conv_en=[
        "I need a phone icon for my call log feature",
        "add a phone symbol to the contact details screen",
        "show a phone for the support and help section",
        "use the phone icon for the emergency contact feature",
    ],
    typo_en=[
        "phoen call from a friend",
        "phnoe ringing on the desk",
        "phome call notification",
        "pohne receiver off the hook",
    ],
    bnd_en=[
        "smartphone screen with app icons on it",
        "hand holding a modern touchscreen mobile phone",
        "voicemail cassette icon for a missed message",
        "microphone wave icon for a voicemail recording",
        "video camera icon for a video call",
        "two faces in a split screen for a video call",
    ],
    valid_en=[
        "old telephone handset icon",
        "phone icon for calling a contact",
        "classic phone receiver symbol",
    ],
    test_en=[
        "phone call icon in a contacts app",
        "telephone receiver silhouette",
        "dial phone number on screen",
    ],
)

# 360 — pickleball (e435)
process_icon("pickleball",
    st_en=["paddle", "pickleball", "wiffle"],
    pst_en=[
        "pickleball paddle on the court", "lightweight paddle used in pickleball",
        "pickleball game on an outdoor court", "popular pickleball club for seniors",
        "wiffle ball used in a pickleball game", "wiffle ball with small holes for airflow",
    ],
    reg_en=[
        "pickleball paddle and a perforated plastic ball",
        "playing pickleball with friends on a sunny afternoon",
        "sports icon for a pickleball club or court booking app",
        "solid paddle with a short handle and wide flat face",
        "weekly pickleball league game at the recreation center",
        "activity icon in a sports scheduling app",
        "small plastic ball with holes next to a flat paddle",
        "beginner pickleball class at the local gym",
        "recreational sport icon for a wellness tracker",
        "paddle raised and ready to hit the incoming pickleball",
    ],
    conv_en=[
        "I need a pickleball icon for my sports tracker app",
        "add a pickleball symbol to the outdoor sports section",
        "show a pickleball for the court booking feature",
        "use the pickleball icon for the recreational activity list",
    ],
    typo_en=[
        "pickelball paddle in the bag",
        "picklball court reservation",
        "picklebll on the outdoor court",
        "picklbeal game at the park",
    ],
    bnd_en=[
        "tennis racket with a wide string head",
        "fuzzy yellow tennis ball on a clay court",
        "badminton shuttlecock with feather fins",
        "badminton racket in an overhead smash position",
        "table tennis paddle with a rubber surface",
        "white ping pong ball bouncing off the table",
    ],
    valid_en=[
        "pickleball paddle and ball",
        "playing pickleball on a court",
        "pickleball sport icon",
    ],
    test_en=[
        "pickleball paddle ready to hit",
        "pickleball game at the rec center",
        "pickleball sports app icon",
    ],
)

# 361 — podcast (f2ce)
process_icon("podcast",
    st_en=["audio", "broadcast", "music", "sound"],
    pst_en=[
        "audio waves from a podcast episode", "audio content streamed on demand",
        "broadcast your podcast to thousands of listeners", "live broadcast from a home studio",
        "music and podcast app combined", "music podcast reviewing new album releases",
        "sound waves radiating from a microphone", "clear sound quality for a podcast recording",
    ],
    reg_en=[
        "microphone with signal waves radiating outward",
        "subscribe to a podcast for weekly episodes",
        "podcast icon for an audio content platform",
        "circular waves pulsing from a broadcast tower",
        "record and publish a podcast episode",
        "audio app icon for a podcast aggregator",
        "signal waves emanating from a standing microphone",
        "listen to a podcast during the morning commute",
        "media symbol for podcast hosting services",
        "podcast logo with signal arcs stacked above a dot",
    ],
    conv_en=[
        "I need a podcast icon for my audio streaming app",
        "add a podcast symbol to the listen section",
        "show a podcast for the broadcast media feature",
        "use the podcast icon for the episode player",
    ],
    typo_en=[
        "podcats episode about productivity",
        "podacst recording in a home studio",
        "podcst available for download",
        "pocast about technology news",
    ],
    bnd_en=[
        "studio condenser microphone on a boom arm",
        "handheld dynamic microphone for live performances",
        "classic boxy radio with a dial and antenna",
        "portable AM FM radio with a telescopic antenna",
        "over-ear headphones on a studio mixing desk",
        "wireless earbuds in a charging case",
    ],
    valid_en=[
        "podcast broadcast signal waves",
        "podcast icon for an audio app",
        "subscribe to a podcast feed",
    ],
    test_en=[
        "podcast signal arc icon",
        "podcast episode player",
        "audio podcast broadcast symbol",
    ],
)

# 362 — potato (e440)
process_icon("potato",
    st_en=["potato", "spud", "tater", "tuber"],
    pst_en=[
        "baked potato with sour cream topping", "potato icon for a recipe app",
        "boiling spuds for mashed potatoes", "spud growing underground in the garden",
        "crispy tater tots with ketchup", "tater salad at a summer barbecue",
        "starchy tuber grown in the soil", "root tuber harvested in autumn",
    ],
    reg_en=[
        "lumpy brown potato with rough bumpy skin",
        "baking a potato in the oven for dinner",
        "vegetable icon for a grocery or recipe app",
        "whole russet potato with small eyes on the skin",
        "mashing potatoes with butter and cream",
        "ingredient icon for a comfort food recipe",
        "potato slice showing white starchy flesh inside",
        "french fries made from freshly cut potatoes",
        "root vegetable icon in a farm or harvest app",
        "pile of potatoes in a wooden crate at the market",
    ],
    conv_en=[
        "I need a potato icon for my recipe tracker app",
        "add a potato symbol to the vegetable category",
        "show a potato for the side dishes section",
        "use the potato icon for the grocery shopping list",
    ],
    typo_en=[
        "potatoe baked in the oven",
        "potatp in a stew",
        "ptato chips in a bag",
        "potaot with butter and sour cream",
    ],
    bnd_en=[
        "long orange carrot with feathery green top",
        "carrot sticks cut for a snack plate",
        "round yellow onion with dry papery skin",
        "sliced onion rings on a wooden board",
        "orange sweet potato with tapered ends",
        "roasted sweet potato in a baking dish",
    ],
    valid_en=[
        "brown potato with rough skin",
        "baked potato for a recipe app",
        "potato vegetable icon",
    ],
    test_en=[
        "whole potato ready for baking",
        "potato in a grocery app",
        "mashed potato ingredient",
    ],
)

# 363 — print (f02f)
process_icon("print",
    st_en=["business", "computer", "copy", "document", "office", "paper", "printer"],
    pst_en=[
        "print a business card on demand", "business document sent to the printer",
        "send a file from the computer to the printer", "computer print job queue",
        "print two copies of the receipt", "copy of the invoice printed for records",
        "print a document from the cloud", "document ready to print in PDF format",
        "office printer running out of toner", "office print station on the second floor",
        "paper coming out of the printer tray", "load paper into the printer drawer",
        "wireless printer connected to the network", "printer icon in the share sheet",
    ],
    reg_en=[
        "desktop printer with a paper tray open",
        "tap print to send the document to the printer",
        "printer icon in a document sharing menu",
        "laser printer on an office desk",
        "print a boarding pass at the airport kiosk",
        "print button in a web browser or PDF viewer",
        "inkjet printer spraying dots onto a white page",
        "print a recipe to hang on the kitchen wall",
        "print dialog box in a desktop application",
        "printer with a document emerging from the top",
    ],
    conv_en=[
        "I need a print icon for my document viewer app",
        "add a print symbol to the file sharing menu",
        "show a printer for the export and print section",
        "use the print icon for the receipt output feature",
    ],
    typo_en=[
        "prnit the document now",
        "pritn ready in the queue",
        "prnt the boarding pass",
        "pint the document to the office printer",
    ],
    bnd_en=[
        "flatbed scanner with a glass lid for documents",
        "scan a document with a handheld scanner",
        "fax machine sending a document over phone lines",
        "old fax machine with a paper feeder on top",
        "photocopier machine producing duplicate documents",
        "large office copier with a touch screen panel",
    ],
    valid_en=[
        "printer icon for printing documents",
        "desktop printer with paper tray",
        "print button in a document app",
    ],
    test_en=[
        "send document to the printer",
        "printer icon in a PDF viewer",
        "print a file from the app",
    ],
)

# 364 — radiation (f7b9)
process_icon("radiation",
    st_en=["danger", "dangerous", "deadly", "hazard", "nuclear", "radioactive", "warning"],
    pst_en=[
        "danger zone marked with a radiation symbol", "danger warning sign outside a nuclear plant",
        "dangerous levels of radiation detected", "dangerous radioactive material in a sealed container",
        "deadly dose of radiation exposure", "deadly radioactive fallout after an explosion",
        "hazard symbol on a nuclear waste barrel", "radiation hazard sign on the door",
        "nuclear reactor with a radiation warning", "nuclear waste storage facility",
        "radioactive isotope with a short half-life", "radioactive material stored in a lead container",
        "warning label on a radiation source", "warning sign for ionizing radiation in a lab",
    ],
    reg_en=[
        "trefoil radiation symbol with three black arcs",
        "radiation warning sign on a nuclear facility door",
        "hazard icon for a safety or compliance app",
        "three-bladed fan shape inside a yellow circle",
        "alert for radiation exposure in a health app",
        "nuclear safety icon for a risk management dashboard",
        "classic black radiation trefoil on yellow background",
        "radiation level detector alert in a monitoring app",
        "ionizing radiation warning in a laboratory setting",
        "biohazard-style warning icon for nuclear material",
    ],
    conv_en=[
        "I need a radiation icon for my safety warning app",
        "add a radiation symbol to the hazard alerts section",
        "show radiation for the nuclear safety indicator",
        "use the radiation icon for the danger zone warning",
    ],
    typo_en=[
        "radaition warning sign",
        "radition hazard symbol",
        "radioation warning level",
        "radiaton sign on the wall",
    ],
    bnd_en=[
        "biohazard symbol with three interlocking circles",
        "biohazard warning on a medical waste container",
        "skull and crossbones on a poison label",
        "toxic danger skull symbol on a chemical bottle",
        "flammable warning sign with a fire triangle",
        "explosive hazard diamond on a transport vehicle",
    ],
    valid_en=[
        "radiation trefoil warning symbol",
        "radiation hazard sign on a door",
        "nuclear radiation warning icon",
    ],
    test_en=[
        "radiation warning sign",
        "radioactive hazard symbol",
        "radiation danger icon in a safety app",
    ],
)

# 365 — router (f8da)
process_icon("router",
    st_en=["bandwidth", "connection", "dsl", "ethernet", "internet", "modem",
           "switch", "wifi", "wireless", "www"],
    pst_en=[
        "router limiting bandwidth for guest users", "bandwidth usage graph on the network dashboard",
        "stable internet connection through a home router", "connection status indicator on the router",
        "dsl modem router combo for broadband", "dsl internet service at home",
        "ethernet cable plugged into the back of the router", "ethernet port on the router for wired devices",
        "internet router providing WiFi at home", "internet connection icon in network settings",
        "modem router combo from the ISP", "restart the modem to fix the connection",
        "network switch connecting multiple devices", "managed switch in a small office network",
        "wifi signal coming from the router", "wifi router broadcasting on two frequencies",
        "wireless router broadcasting a signal", "wireless connection to the home network",
        "www traffic routed through the internet gateway", "www access provided by the ISP router",
    ],
    reg_en=[
        "boxy router with blinking LED lights and antennas",
        "restart the router to fix a slow connection",
        "network icon in a home or office IT dashboard",
        "dual-band router with two antennas sticking up",
        "connect all devices to the home WiFi router",
        "IT infrastructure icon for a network management app",
        "router sitting next to a modem under the TV stand",
        "configure the router settings in the browser",
        "network hardware icon for a connectivity app",
        "router with port lights flashing as data flows",
    ],
    conv_en=[
        "I need a router icon for my network monitor app",
        "add a router symbol to the internet settings screen",
        "show a router for the WiFi configuration section",
        "use the router icon for the network devices feature",
    ],
    typo_en=[
        "routre blinking on the shelf",
        "routerr keeps disconnecting",
        "rotuer reset needed",
        "routr not connecting",
    ],
    bnd_en=[
        "cable modem with coaxial port and ethernet",
        "DSL modem with a blinking activity light",
        "wifi signal bars radiating from a center point",
        "wireless signal icon with three curved arcs",
        "network switch with many ethernet ports on the back",
        "rack-mounted network switch in a server room",
    ],
    valid_en=[
        "wifi router with antennas at home",
        "router icon for network settings",
        "internet router device",
    ],
    test_en=[
        "home router blinking LED lights",
        "router in a network monitor app",
        "configure router settings",
    ],
)

# 366 — rss (f09e)
process_icon("rss",
    st_en=["blog", "feed", "journal", "news", "writing"],
    pst_en=[
        "subscribe to a blog via RSS feed", "blog updates delivered through an rss reader",
        "RSS feed from a news website", "follow a feed for the latest updates",
        "online journal with an rss subscription option", "daily journal posts available as rss feed",
        "news aggregator collecting rss feeds", "latest news articles in an rss reader",
        "writing published as an rss feed", "follow the author's writing through rss",
    ],
    reg_en=[
        "three curved arcs above a filled dot in the corner",
        "subscribe to a website using the RSS icon",
        "RSS feed aggregator icon in a news reader app",
        "orange square with white WiFi-like signal arcs",
        "add an RSS feed to your podcast or blog reader",
        "content distribution symbol for web publishing",
        "signal wave icon used to represent syndicated content",
        "click the RSS icon to get automatic content updates",
        "web syndication icon for a content management platform",
        "stacked arcs growing wider from a bottom-left origin",
    ],
    conv_en=[
        "I need an RSS icon for my news reader app",
        "add an RSS symbol to the feed subscription button",
        "show RSS for the subscribe to updates section",
        "use the RSS icon for the content syndication feature",
    ],
    typo_en=[
        "rss fede subscription link",
        "rrs news feed from the blog",
        "rss blgo update notification",
        "rss newss aggregator",
    ],
    bnd_en=[
        "bookmark ribbon folded at the top of a page",
        "star bookmark saving a webpage for later",
        "share icon with a dot and two branching arrows",
        "share sheet icon in a mobile browser",
        "chain link icon representing a hyperlink",
        "URL link icon for copying and sharing",
    ],
    valid_en=[
        "RSS feed icon with signal arcs",
        "subscribe to content via RSS",
        "RSS symbol for a news reader",
    ],
    test_en=[
        "RSS feed aggregator icon",
        "orange RSS subscribe button",
        "RSS symbol on a blog",
    ],
)
