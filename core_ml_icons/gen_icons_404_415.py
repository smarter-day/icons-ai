#!/usr/bin/env python3
"""Generate English training data for icons 404-415."""
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

# 404 — seat (e764)
process_icon("seat",
    st_en=["chair", "furniture", "movie", "seat", "table", "theater"],
    pst_en=[
        "comfortable chair reserved for the guest", "chair icon for a seating arrangement app",
        "furniture in a living room or office", "furniture store icon with a seat",
        "movie seat reservation in a cinema app", "assigned movie seat number on a ticket",
        "reserve a seat before the show starts", "seat icon next to a reservation form",
        "seat at the dining table for two", "table and seat setup at the restaurant",
        "theater seat with a fold-down cushion", "assigned theater seat in row G",
    ],
    reg_en=[
        "fold-down theater seat with padded armrests",
        "reserve a seat for the concert in advance",
        "seating icon for a ticketing or booking app",
        "single seat viewed from the front with a backrest",
        "choose your seat on a flight booking screen",
        "venue seat map icon for an event app",
        "cushioned seat in a cinema row",
        "seat assignment printed on the boarding pass",
        "restaurant table seat booking confirmation",
        "empty seat waiting to be claimed before the show",
    ],
    conv_en=[
        "I need a seat icon for my theater booking app",
        "add a seat symbol to the reservation section",
        "show a seat for the venue seating map feature",
        "use the seat icon for the cinema ticket selector",
    ],
    typo_en=[
        "saet reserved for the guest",
        "seeat number on the ticket",
        "seta in the front row",
        "seay at the theater",
    ],
    bnd_en=[
        "three-seat sofa against the living room wall",
        "comfortable couch with throw pillows",
        "wooden park bench along a garden path",
        "outdoor bench with a metal frame",
        "bar stool with a round padded seat",
        "tall kitchen stool at a breakfast counter",
    ],
    valid_en=[
        "theater seat with padded armrests",
        "seat reservation icon in a booking app",
        "assigned seat in a cinema row",
    ],
    test_en=[
        "reserve a seat for the concert",
        "seat selector in a ticketing app",
        "seat icon for a venue map",
    ],
)

# 405 — shorts (e6d9)
process_icon("shorts",
    st_en=["boxers", "drawers", "pants", "shorts", "summer", "swimsuit", "trunks", "underwear"],
    pst_en=[
        "boxer shorts in a laundry pile", "elastic waistband boxers on a hanger",
        "dresser drawers holding folded shorts", "pull out the drawers to find your shorts",
        "casual pants cut short at the thigh", "athletic pants shortened to shorts length",
        "pair of shorts for a summer outing", "denim shorts with cuffed hems",
        "summer shorts on a beach day", "bright summer shorts in a tropical print",
        "swimsuit trunks for the pool", "board shorts worn as a swimsuit at the beach",
        "swim trunks for the outdoor pool", "board trunks with a drawstring waist",
        "cotton underwear boxer shorts", "loose underwear shorts in a cotton blend",
    ],
    reg_en=[
        "knee-length shorts with two side pockets",
        "wear shorts on a warm summer afternoon",
        "clothing icon for a casual or summer fashion app",
        "athletic shorts with a drawstring elastic waist",
        "pack a pair of shorts for the beach vacation",
        "summer apparel icon in a wardrobe tracker",
        "light cotton shorts folded on a shelf",
        "pull on shorts for a morning jog in the park",
        "bottoms category icon in an activewear app",
        "denim cutoff shorts with a frayed hem",
    ],
    conv_en=[
        "I need a shorts icon for my wardrobe tracker app",
        "add a shorts symbol to the summer clothing section",
        "show shorts for the activewear category",
        "use the shorts icon for the beach outfit feature",
    ],
    typo_en=[
        "shoorts for a summer day",
        "shrots folded in a drawer",
        "horts for the gym session",
        "shortts with a drawstring waist",
    ],
    bnd_en=[
        "slim fit trousers with a front crease",
        "navy blue dress pants for a business look",
        "floral summer skirt above the knee",
        "A-line skirt in a solid neutral color",
        "one-piece swimsuit with adjustable straps",
        "bikini top and bottom set for the beach",
    ],
    valid_en=[
        "knee-length shorts with side pockets",
        "shorts icon for a summer clothing app",
        "athletic shorts with a drawstring",
    ],
    test_en=[
        "denim shorts for a casual day",
        "shorts for a beach vacation",
        "shorts in a wardrobe tracker app",
    ],
)

# 406 — speaker (f8df)
process_icon("speaker",
    st_en=["audio", "device", "music", "sound", "subwoofer", "transducer", "tweeter"],
    pst_en=[
        "audio output from a bookshelf speaker", "audio device plugged into the stereo system",
        "smart speaker device on the kitchen counter", "wireless audio device for music playback",
        "music coming from the living room speaker", "play music through a bluetooth speaker",
        "full sound from a floor-standing speaker", "crisp sound coming from the tweeter cone",
        "deep bass from the subwoofer speaker", "subwoofer producing low-frequency rumble",
        "transducer converting electrical signal to sound", "audio transducer in a portable speaker",
        "tweeter producing high-frequency notes", "small tweeter dome on top of the speaker",
    ],
    reg_en=[
        "rectangular speaker with a fabric grille front",
        "connect a bluetooth speaker for outdoor music",
        "audio output icon in a sound settings menu",
        "tall floor-standing speaker in a home theater",
        "adjust the treble and bass on the speaker",
        "music playback icon for a smart home app",
        "compact portable speaker with a wrist strap",
        "pair the speaker with the phone via bluetooth",
        "sound system icon for an entertainment app",
        "bookshelf speaker with a woven cone driver",
    ],
    conv_en=[
        "I need a speaker icon for my music player app",
        "add a speaker symbol to the audio output section",
        "show a speaker for the sound settings feature",
        "use the speaker icon for the home audio category",
    ],
    typo_en=[
        "spekaer connected to the amp",
        "speeaker on the bookshelf",
        "speakre playing music outdoors",
        "speaekr volume turned up",
    ],
    bnd_en=[
        "over-ear headphones on a studio desk",
        "wireless earbuds in a charging case",
        "studio condenser microphone on a boom arm",
        "handheld microphone at a music venue",
        "vintage radio with a dial and speaker grille",
        "portable AM FM radio for camping trips",
    ],
    valid_en=[
        "bookshelf speaker with fabric grille",
        "speaker icon for an audio app",
        "bluetooth speaker for music playback",
    ],
    test_en=[
        "speaker connected to the stereo",
        "portable speaker for outdoor music",
        "audio speaker icon in settings",
    ],
)

# 407 — thermometer (f491)
process_icon("thermometer",
    st_en=["covid-19", "mercury", "status", "temperature"],
    pst_en=[
        "covid-19 temperature check at the entrance", "fever screening during covid-19 with a thermometer",
        "mercury rising in the glass thermometer", "old mercury thermometer reading 38 degrees",
        "status indicator showing current temperature", "system status with a thermometer icon",
        "body temperature measured with a thermometer", "outdoor temperature shown in a weather app",
    ],
    reg_en=[
        "glass thermometer with a red mercury column",
        "check body temperature with a digital thermometer",
        "health icon for a fever or symptom tracker",
        "digital thermometer displaying a high temperature",
        "measure the oven temperature before baking",
        "weather icon showing the current outdoor temperature",
        "clinical thermometer with degree markings on the side",
        "log daily temperature in a health monitoring app",
        "medical icon representing fever or illness",
        "thermometer icon rising to indicate high heat",
    ],
    conv_en=[
        "I need a thermometer icon for my fever tracker app",
        "add a thermometer symbol to the health status section",
        "show a thermometer for the temperature monitoring feature",
        "use the thermometer icon for the weather display",
    ],
    typo_en=[
        "thermometre showing a fever",
        "thermomater reading 39 degrees",
        "therometer reading high",
        "thermomter outside temperature",
    ],
    bnd_en=[
        "stethoscope worn around a doctor's neck",
        "doctor listening with a stethoscope",
        "plastic syringe with a metal needle tip",
        "medical syringe prepared for an injection",
        "red first aid kit box with a white cross",
        "medical kit with bandages and antiseptic",
    ],
    valid_en=[
        "thermometer showing body temperature",
        "thermometer icon for a health app",
        "digital thermometer reading a fever",
    ],
    test_en=[
        "glass thermometer with red mercury",
        "temperature check with a thermometer",
        "thermometer in a weather or health app",
    ],
)

# 408 — trombone (e782)
process_icon("trombone",
    st_en=["band", "brass", "horn", "orchestra", "trombone"],
    pst_en=[
        "trombone player in the high school marching band", "brass band featuring trombones and trumpets",
        "brass trombone with a wide bell and slide", "brass instrument section in a jazz ensemble",
        "deep horn sound from the trombone slide", "horn instrument icon for a music reference app",
        "trombone section in a full symphony orchestra", "orchestra warm-up with trombones and tubas",
        "play the trombone in a jazz big band", "extend the trombone slide for a lower note",
    ],
    reg_en=[
        "long trombone with a sliding tube and wide bell",
        "play the trombone in a jazz or classical ensemble",
        "brass instrument icon for a music or band app",
        "trombone player pushing the slide outward",
        "practice trombone scales before the rehearsal",
        "wind instrument icon in a music education app",
        "trombone bell pointing forward with a silver finish",
        "jazzy trombone solo during a big band performance",
        "orchestral instrument icon for a classical music app",
        "trombone silhouette with a curved mouthpiece",
    ],
    conv_en=[
        "I need a trombone icon for my music app",
        "add a trombone symbol to the brass instruments section",
        "show a trombone for the jazz band feature",
        "use the trombone icon for the orchestra category",
    ],
    typo_en=[
        "tromobne slide extended",
        "tromboen in the jazz band",
        "trombnoe playing a low note",
        "trombonne with a slide",
    ],
    bnd_en=[
        "gold trumpet with three valves and a wide bell",
        "trumpet fanfare at a ceremony",
        "large tuba with a wide upward-facing bell",
        "brass tuba player in a marching band",
        "curved saxophone with a wide flared bell",
        "jazz saxophonist playing a smooth solo",
    ],
    valid_en=[
        "trombone with a sliding tube and wide bell",
        "trombone icon for a music app",
        "jazz trombone brass instrument",
    ],
    test_en=[
        "trombone slide extended for a low note",
        "trombone in a jazz big band",
        "trombone instrument icon",
    ],
)

# 409 — umbrella (f0e9)
process_icon("umbrella",
    st_en=["protection", "rain", "storm", "wet"],
    pst_en=[
        "umbrella for protection from the rain", "sun protection umbrella on the beach",
        "rain umbrella opened on a rainy day", "carry a rain umbrella just in case",
        "storm umbrella blown inside out in the wind", "stormy weather icon with an umbrella",
        "stay dry and avoid getting wet with an umbrella", "wet streets require an umbrella",
    ],
    reg_en=[
        "open umbrella with a curved wooden handle",
        "open your umbrella before stepping into the rain",
        "weather icon for a rain or forecast app",
        "dome-shaped canopy of a brightly colored umbrella",
        "compact travel umbrella folded into a sleeve",
        "rainy day icon in a calendar or weather widget",
        "umbrella with raindrops falling around it",
        "share an umbrella with a friend in the rain",
        "outdoor event icon with protection from the weather",
        "striped umbrella tilted against the wind",
    ],
    conv_en=[
        "I need an umbrella icon for my weather app",
        "add an umbrella symbol to the rain forecast section",
        "show an umbrella for the bad weather reminder",
        "use the umbrella icon for the storm alert feature",
    ],
    typo_en=[
        "unbrella opened in the rain",
        "umbrelal in the storm",
        "umbrela for rainy days",
        "umrella blown inside out",
    ],
    bnd_en=[
        "yellow raincoat with a hood pulled up",
        "waterproof rain jacket for stormy weather",
        "dark storm cloud with rain falling below",
        "weather icon showing heavy rain showers",
        "beach parasol with colorful stripes in the sand",
        "patio umbrella over a garden table and chairs",
    ],
    valid_en=[
        "open umbrella in the rain",
        "umbrella icon for a weather app",
        "rain umbrella with a curved handle",
    ],
    test_en=[
        "umbrella opened on a rainy day",
        "weather umbrella icon",
        "stay dry with an umbrella in the storm",
    ],
)

# 410 — volleyball (f45f)
process_icon("volleyball",
    st_en=["ball", "beach", "game", "olympics", "sport", "volleyball"],
    pst_en=[
        "volleyball ball with panel seams", "round ball spiked over the net",
        "beach volleyball game on the sand", "beach volleyball court set up by the ocean",
        "game of volleyball in the school gym", "outdoor game of volleyball with friends",
        "olympics volleyball match at the stadium", "beach volleyball in the summer olympics",
        "team sport played with a net and ball", "sport icon for a volleyball club app",
        "volleyball serve from behind the back line", "volleyball spike at the net",
    ],
    reg_en=[
        "round volleyball with colored panel seams",
        "serve the volleyball over the net to start the rally",
        "sports icon for a volleyball club or court app",
        "white volleyball with blue and yellow panels",
        "beach volleyball tournament on a sunny weekend",
        "team sport icon for a fitness or activity app",
        "volleyball bouncing off the forearms in a bump pass",
        "join a recreational volleyball league this season",
        "ball sport icon for an outdoor activity tracker",
        "volleyball floating above the net at a beach court",
    ],
    conv_en=[
        "I need a volleyball icon for my sports app",
        "add a volleyball symbol to the team sports section",
        "show a volleyball for the beach sports feature",
        "use the volleyball icon for the outdoor activities category",
    ],
    typo_en=[
        "voleyball game at the beach",
        "volleball spike at the net",
        "volleybal serve from the back line",
        "volleybll on the sand court",
    ],
    bnd_en=[
        "orange basketball with black seam lines",
        "basketball going through a hoop and net",
        "black and white soccer ball on a grass field",
        "soccer ball kicked into a goal net",
        "fuzzy yellow tennis ball on a clay court",
        "tennis ball bouncing on the baseline",
    ],
    valid_en=[
        "volleyball with colored panel seams",
        "volleyball icon for a sports app",
        "beach volleyball game",
    ],
    test_en=[
        "volleyball spiked over the net",
        "volleyball tournament on the beach",
        "volleyball sport icon",
    ],
)

# 411 — volume (f6a8)
process_icon("volume",
    st_en=["audio", "control", "medium", "music", "sound", "speaker"],
    pst_en=[
        "audio volume control on a media player", "audio level adjusted with a volume slider",
        "control the volume from the notification bar", "volume control knob on a stereo",
        "medium volume for background listening", "set to medium volume during the meeting",
        "music volume turned up for the workout", "lower the music volume at night",
        "sound volume raised during a movie scene", "decrease the sound volume in a quiet room",
        "speaker volume icon in the phone status bar", "speaker volume slider in audio settings",
    ],
    reg_en=[
        "speaker icon with sound waves indicating volume",
        "adjust the volume with the slider in settings",
        "audio control icon in a media or music app",
        "volume icon with three curved sound wave arcs",
        "turn up the volume during a workout playlist",
        "system sound icon in phone or computer settings",
        "speaker symbol with a single arc for low volume",
        "tap the volume icon to mute or unmute audio",
        "media player icon for controlling audio output",
        "volume level bars rising with increasing sound",
    ],
    conv_en=[
        "I need a volume icon for my media player app",
        "add a volume symbol to the audio controls section",
        "show a volume icon for the sound settings feature",
        "use the volume icon for the media playback screen",
    ],
    typo_en=[
        "voulme turned up for the movie",
        "volmue setting in the app",
        "volumee on the media player",
        "vlume slider in settings",
    ],
    bnd_en=[
        "mute icon with a crossed-out speaker",
        "speaker with an X through it for muted audio",
        "equalizer bars adjusting audio frequency levels",
        "music equalizer with sliders for bass and treble",
        "bookshelf speaker with a fabric cone driver",
        "portable bluetooth speaker on a desk",
    ],
    valid_en=[
        "volume icon with sound wave arcs",
        "audio volume control symbol",
        "speaker volume in settings",
    ],
    test_en=[
        "turn up the volume in a music app",
        "volume slider in phone settings",
        "volume icon for a media player",
    ],
)

# 412 — watch (f2e1)
process_icon("watch",
    st_en=["alert", "clock", "time", "watch", "wristwatch"],
    pst_en=[
        "watch alert vibrating on the wrist", "alert notification on a smartwatch screen",
        "analog clock face on a wristwatch", "clock icon for a time tracking feature",
        "check the time on your wrist watch", "time icon in a schedule or calendar app",
        "classic wristwatch with leather strap", "smartwatch displaying the current time",
        "luxury wristwatch with a sapphire crystal", "wristwatch on a wooden display stand",
    ],
    reg_en=[
        "round wristwatch with an analog dial face",
        "glance at the watch to check the time",
        "time icon for a schedule or clock app",
        "smartwatch with a digital screen on the wrist",
        "set a reminder on the wristwatch for the meeting",
        "wearable device icon in a health or fitness app",
        "watch with a metal bracelet and hour markers",
        "track workout time and heart rate on the watch",
        "time management icon in a productivity app",
        "vintage watch with Roman numeral hour markers",
    ],
    conv_en=[
        "I need a watch icon for my time tracking app",
        "add a watch symbol to the schedule section",
        "show a watch for the time management feature",
        "use the watch icon for the wearable device screen",
    ],
    typo_en=[
        "wtach strapped to the wrist",
        "watcch on the wrist",
        "wathc vibrating with an alert",
        "atch on a leather strap",
    ],
    bnd_en=[
        "round wall clock with hour and minute hands",
        "analog alarm clock on a bedside table",
        "countdown timer ticking down to zero",
        "kitchen timer set for 20 minutes",
        "stopwatch used to time a sprint",
        "sports stopwatch with a lap button",
    ],
    valid_en=[
        "analog wristwatch with a round dial",
        "watch icon for a time tracking app",
        "smartwatch on the wrist",
    ],
    test_en=[
        "glance at the watch to check time",
        "wristwatch for a schedule app",
        "watch icon in a productivity app",
    ],
)

# 413 — water (f773)
process_icon("water",
    st_en=["lake", "liquid", "ocean", "sea", "swim", "wet"],
    pst_en=[
        "calm lake reflecting the surrounding mountains", "kayaking on a still lake in the morning",
        "liquid water droplet icon for a hydration app", "clean liquid water in a glass",
        "ocean waves rolling onto the beach", "swim in the ocean on a summer day",
        "sea view from a cliffside restaurant", "open sea navigation on a sailing chart",
        "swim in the water on a hot afternoon", "swim training tracked in a fitness app",
        "wet surface warning icon on a floor", "wet weather icon for a rain forecast",
    ],
    reg_en=[
        "blue water drop with a pointed top",
        "stay hydrated by drinking water throughout the day",
        "hydration icon for a water intake tracker app",
        "rippling water surface in a calm pool",
        "pour a glass of water from the tap",
        "nature or environment icon representing water",
        "single water droplet falling into a still surface",
        "swimming in cool water on a hot summer day",
        "water resource icon for a conservation or eco app",
        "ocean water icon on a weather or travel app",
    ],
    conv_en=[
        "I need a water icon for my hydration tracker app",
        "add a water symbol to the health and fitness section",
        "show water for the swimming activity feature",
        "use the water icon for the ocean or lake category",
    ],
    typo_en=[
        "wter staying hydrated all day",
        "watre in a glass on the table",
        "wateer filling the pool slowly",
        "waetr drop icon in the app",
    ],
    bnd_en=[
        "ice cube floating in a cold glass of water",
        "snowflake symbol for frozen water or cold weather",
        "orange campfire flame burning on logs",
        "flame icon for heat or fire indicator",
        "large ocean wave curling before it breaks",
        "surfing wave icon for a beach or surf app",
    ],
    valid_en=[
        "blue water droplet icon",
        "water icon for a hydration app",
        "flowing water symbol",
    ],
    test_en=[
        "water drop for a hydration tracker",
        "swim in the ocean water",
        "water icon in a fitness app",
    ],
)

# 414 — wind (f72e)
process_icon("wind",
    st_en=["air", "blow", "breeze", "fall", "seasonal", "weather"],
    pst_en=[
        "fresh air breeze indicated by wind lines", "air flow icon for a ventilation or fan app",
        "wind blow bending the tree branches", "blow of wind scattering autumn leaves",
        "light breeze icon on a weather forecast", "ocean breeze on a summer afternoon",
        "fall wind scattering colorful leaves", "autumn fall wind stripping the leaves off",
        "seasonal wind icon in a nature app", "seasonal weather feature for winter winds",
        "weather wind indicator in a forecast app", "strong weather wind advisory issued",
    ],
    reg_en=[
        "curved lines suggesting wind blowing sideways",
        "wind speed forecast displayed in a weather app",
        "weather icon representing wind or breezy conditions",
        "sweeping wind lines curving across the screen",
        "adjust activities based on the wind forecast",
        "climate icon in a nature or outdoor planning app",
        "strong wind bending a tree branch to one side",
        "wind advisory warning for a coastal region",
        "air quality and wind icon in an environment app",
        "gentle breeze lines floating across a clear sky",
    ],
    conv_en=[
        "I need a wind icon for my weather app",
        "add a wind symbol to the weather forecast section",
        "show wind for the outdoor conditions feature",
        "use the wind icon for the sailing or kite activity screen",
    ],
    typo_en=[
        "wnid advisory for the coast",
        "widn blowing through the trees",
        "winnd forecast for tomorrow",
        "wond blowing at 30 km per hour",
    ],
    bnd_en=[
        "funnel-shaped tornado spinning across the field",
        "tornado warning in a storm alert app",
        "dark storm cloud with lightning and heavy rain",
        "severe storm warning icon in a weather forecast",
        "desk fan spinning on a hot summer day",
        "ceiling fan icon for a smart home control app",
    ],
    valid_en=[
        "wind lines blowing sideways",
        "wind icon for a weather app",
        "breezy wind symbol",
    ],
    test_en=[
        "wind forecast in a weather app",
        "wind blowing autumn leaves",
        "wind icon for outdoor activities",
    ],
)

# 415 — wireless (e7df)
process_icon("wireless",
    st_en=["connection", "hotspot", "internet", "network", "nfc",
           "rss", "scan", "signal", "wifi", "wireless", "www"],
    pst_en=[
        "wireless connection established on the device", "stable connection icon in network settings",
        "mobile hotspot sharing internet over wifi", "enable hotspot to share the connection",
        "internet signal coming from the router", "internet access via a wireless network",
        "wireless network icon in the phone status bar", "connect to the available network",
        "nfc wireless tap to pay at the register", "nfc chip for contactless wireless transfer",
        "rss feed delivered wirelessly to the reader", "rss wireless update icon in a news app",
        "scan for available wireless networks", "scan a qr code wirelessly on the phone",
        "strong wireless signal in the corner icon", "weak signal bars on a wireless connection",
        "wifi signal icon connecting to the router", "wifi bars in the phone status bar",
        "wireless connection to a smart home device", "wireless charging pad for the smartphone",
        "www access through a wireless network", "browse the www on a wireless connection",
    ],
    reg_en=[
        "fan-shaped wifi signal icon with curved arcs",
        "connect to a wireless network in the settings",
        "connectivity icon for a network or internet app",
        "signal bars growing from a central bottom point",
        "scan for wifi networks in the area",
        "wireless indicator in a smart home control app",
        "wireless icon showing four signal strength bars",
        "enable wireless to connect to the internet",
        "network status icon in a mobile device settings menu",
        "wireless signal radiating from a central tower",
    ],
    conv_en=[
        "I need a wireless icon for my network settings app",
        "add a wireless symbol to the connectivity section",
        "show a wireless icon for the wifi status feature",
        "use the wireless icon for the internet connection screen",
    ],
    typo_en=[
        "wireles signal in the settings bar",
        "wirelss connection to the router",
        "wirelese network available nearby",
        "wirelesd connection for the device",
    ],
    bnd_en=[
        "bluetooth symbol connecting two devices",
        "short-range bluetooth icon in device settings",
        "ethernet cable plugged into a network port",
        "wired internet connection via an ethernet cable",
        "cellular signal bars showing mobile strength",
        "4G LTE signal icon in the phone status bar",
    ],
    valid_en=[
        "wireless wifi signal icon",
        "wireless connection for a network app",
        "wifi signal bars in settings",
    ],
    test_en=[
        "connect to wireless network",
        "wireless icon in phone settings",
        "wifi wireless signal symbol",
    ],
)
