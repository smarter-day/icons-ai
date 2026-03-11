#!/usr/bin/env python3
"""Batch task-001: Add task-style phrases to 20 lowest-coverage icons.

Icons: tablet, tank-water, vest-patches, wheelchair, window,
       capsules, cupcake, moped, scrubber, stairs,
       table-rows, tape, truck-moving, users, watch-smart,
       bin, cucumber, microchip, mushroom, paste
"""

import csv
from pathlib import Path

icons_dir = Path("icons")


def read_texts(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [r["text"].strip() for r in csv.DictReader(f)]


def append_csv(path, rows):
    with path.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)


def expand(icon, new_en, new_ru):
    assert len(new_en) == len(new_ru), f"{icon}: EN={len(new_en)} RU={len(new_ru)} mismatch"
    en_path = icons_dir / icon / "train_en.csv"
    ru_path = icons_dir / icon / "train_ru.csv"
    existing_en = set(read_texts(en_path))
    existing_ru = set(read_texts(ru_path))
    add_en = [(t, icon) for t in new_en if t not in existing_en]
    add_ru = [(t, icon) for t in new_ru if t not in existing_ru]
    append_csv(en_path, add_en)
    append_csv(ru_path, add_ru)
    total_en = len(existing_en) + len(add_en)
    total_ru = len(existing_ru) + len(add_ru)
    print(f"  {icon}: +{len(add_en)} EN  +{len(add_ru)} RU  (total EN={total_en} RU={total_ru})")


# ── tablet ───────────────────────────────────────────────────────────────────
expand("tablet",
    new_en=[
        # keywords
        "tablet",
        "iPad",
        "e-reader",
        "android tablet",
        # direct tasks
        "charge the tablet before the trip",
        "download the app on the tablet",
        "update the tablet software tonight",
        "buy a new tablet for the kids",
        "set up parental controls on the tablet",
        "replace the cracked tablet screen",
        "connect the tablet to the bluetooth speaker",
        "back up the tablet to the cloud",
        "install a screen protector on the tablet",
        "reset the tablet to factory settings",
        # contextual
        "tablet needs charging before the flight",
        "bring the tablet for the road trip",
        "tablet for watching movies on the plane",
        "load the kids tablet with games before vacation",
        "tablet case from Amazon arriving Friday",
        "new tablet for mom's birthday gift",
        "trade in old tablet at the electronics store",
        "tablet for reading books at the beach",
        # short informal
        "charge tablet",
        "tablet update",
        "fix tablet",
        "get tablet case",
        "tablet - kids",
        # conversational
        "the tablet battery dies so fast lately",
        "need to get a bigger tablet for drawing",
        "the kids broke the tablet screen again",
        "should I get an iPad or Android tablet",
        "tablet is running out of storage",
        # typos
        "tabet needs charging",
        "donwload app on tabelt",
        "updaet the talblet tonight",
        "conect tablet to speakr",
    ],
    new_ru=[
        # keywords
        "планшет",
        "айпад",
        "электронная книга",
        "андроид планшет",
        # direct tasks
        "зарядить планшет перед поездкой",
        "скачать приложение на планшет",
        "обновить планшет сегодня вечером",
        "купить новый планшет для детей",
        "настроить родительский контроль на планшете",
        "заменить разбитый экран планшета",
        "подключить планшет к bluetooth колонке",
        "сделать резервную копию планшета",
        "наклеить защитное стекло на планшет",
        "сбросить планшет до заводских настроек",
        # contextual
        "зарядить планшет перед полётом",
        "взять планшет в дорогу",
        "планшет для просмотра фильмов в самолёте",
        "загрузить игры на детский планшет перед каникулами",
        "чехол для планшета придёт в пятницу",
        "новый планшет маме на день рождения",
        "сдать старый планшет в магазин электроники",
        "планшет для чтения на пляже",
        # short informal
        "зарядить планшет",
        "обновить планшет",
        "починить планшет",
        "купить чехол для планшета",
        "планшет - дети",
        # conversational
        "планшет стал быстро разряжаться",
        "нужен планшет побольше для рисования",
        "дети снова разбили экран планшета",
        "взять айпад или андроид планшет",
        "на планшете заканчивается память",
        # typos
        "планшет нуждатся в зарядке",
        "скачтаь приложение на планшет",
        "обновтиь планшет сеогдня",
        "подклчить планшет к колноке",
    ],
)

# ── tank-water ───────────────────────────────────────────────────────────────
expand("tank-water",
    new_en=[
        # keywords
        "water tank",
        "cistern",
        "rainwater tank",
        "water storage",
        # direct tasks
        "check the water tank level",
        "clean the water tank this weekend",
        "refill the water tank before summer",
        "install a rainwater collection tank",
        "drain and flush the water tank",
        "replace the water tank valve",
        "insulate the water tank for winter",
        "test the water tank for leaks",
        "order a new water tank online",
        "schedule water tank maintenance",
        # contextual
        "water tank inspection due next month",
        "tank filter needs replacing before rain season",
        "water tank delivery arriving Tuesday",
        "rainwater tank for the garden irrigation",
        "water tank for the cabin off-grid",
        "hot water tank warranty expires soon",
        "tank level low after the dry spell",
        "water tank for the camping trip",
        # short informal
        "check tank",
        "tank level",
        "flush tank",
        "tank maintenance",
        "water tank - order",
        # conversational
        "the water tank is almost empty",
        "need to get the tank cleaned before winter",
        "water tank has been making weird noises",
        "should we upgrade to a bigger water tank",
        "the old water tank is starting to rust",
        # typos
        "watre tank level check",
        "clena the water tnk",
        "rainwter tank instal",
        "watter tank maintennce",
    ],
    new_ru=[
        # keywords
        "бак для воды",
        "цистерна",
        "бак дождевой воды",
        "водохранилище",
        # direct tasks
        "проверить уровень воды в баке",
        "почистить бак для воды в выходные",
        "наполнить бак перед летом",
        "установить бак для сбора дождевой воды",
        "слить и промыть бак для воды",
        "заменить клапан на баке для воды",
        "утеплить бак для воды на зиму",
        "проверить бак на протечки",
        "заказать новый бак для воды",
        "запланировать обслуживание бака",
        # contextual
        "осмотр бака для воды в следующем месяце",
        "фильтр бака нужно заменить до сезона дождей",
        "доставка бака для воды во вторник",
        "бак дождевой воды для полива огорода",
        "бак для воды в дачный домик",
        "гарантия на бойлер скоро истекает",
        "уровень бака низкий после засухи",
        "бак с водой для похода",
        # short informal
        "проверить бак",
        "уровень бака",
        "промыть бак",
        "обслуживание бака",
        "бак - заказать",
        # conversational
        "бак для воды почти пуст",
        "надо почистить бак до зимы",
        "бак для воды издаёт странные звуки",
        "может стоит поставить бак побольше",
        "старый бак начал ржаветь",
        # typos
        "првоерить уровень бака",
        "поистить бак для вды",
        "бка дождевой воды установить",
        "обслжуивание бака для воды",
    ],
)

# ── vest-patches ─────────────────────────────────────────────────────────────
expand("vest-patches",
    new_en=[
        # keywords
        "vest",
        "patches",
        "denim vest",
        "biker vest",
        # direct tasks
        "sew new patches on the vest",
        "iron on the band patches tonight",
        "order custom patches for the vest",
        "buy a denim vest at the thrift store",
        "pick up embroidered patches from the shop",
        "stitch the loose patch back onto the vest",
        "design a custom patch for the club",
        "wash the vest before adding patches",
        "remove the old patch from the jacket",
        "get the biker vest from the closet",
        # contextual
        "patches for the vest arriving this week",
        "finish the vest before the festival",
        "vest patches project for the weekend",
        "new patches from the concert merch table",
        "denim vest ready for the motorcycle rally",
        "patch collection for the road trip jacket",
        "sewing kit for the vest patches tonight",
        "vintage patches for the vest from eBay",
        # short informal
        "sew patches",
        "iron on patch",
        "vest project",
        "order patches",
        "fix vest patch",
        # conversational
        "need more patches for the back of the vest",
        "the patch is coming off the vest again",
        "found a cool patch at the flea market",
        "the vest is almost covered in patches now",
        "looking for a good place to buy patches online",
        # typos
        "swe patches on the vset",
        "irno on the patcch tonight",
        "ordr custom patchs",
        "deinm vest from thrift stroe",
    ],
    new_ru=[
        # keywords
        "жилет",
        "нашивки",
        "джинсовый жилет",
        "байкерский жилет",
        # direct tasks
        "пришить новые нашивки на жилет",
        "наклеить нашивки утюгом сегодня вечером",
        "заказать нашивки для жилета",
        "купить джинсовый жилет в секонде",
        "забрать вышитые нашивки из мастерской",
        "пришить отвалившуюся нашивку на жилет",
        "нарисовать дизайн нашивки для клуба",
        "постирать жилет перед тем как пришивать",
        "снять старую нашивку с куртки",
        "достать байкерский жилет из шкафа",
        # contextual
        "нашивки для жилета придут на этой неделе",
        "доделать жилет до фестиваля",
        "проект с нашивками на выходные",
        "новые нашивки с мерча после концерта",
        "джинсовый жилет к мотослёту",
        "коллекция нашивок для дорожной куртки",
        "набор для шитья для нашивок на вечер",
        "винтажные нашивки для жилета с eBay",
        # short informal
        "пришить нашивки",
        "наклеить нашивку",
        "проект жилет",
        "заказать нашивки",
        "починить нашивку",
        # conversational
        "нужно больше нашивок на спину жилета",
        "нашивка снова отваливается от жилета",
        "нашёл крутую нашивку на блошином рынке",
        "жилет уже почти весь в нашивках",
        "ищу где купить нашивки в интернете",
        # typos
        "пришть нашивки на жлет",
        "наклитеь нашивку утюогм",
        "зкаазать нашивки для жилтеа",
        "джинсовй жилет из секнода",
    ],
)

# ── wheelchair ───────────────────────────────────────────────────────────────
expand("wheelchair",
    new_en=[
        # keywords
        "wheelchair",
        "mobility aid",
        "accessible",
        "disability",
        # direct tasks
        "book wheelchair assistance at the airport",
        "charge the electric wheelchair overnight",
        "fix the wheelchair brake",
        "order replacement wheelchair tires",
        "schedule wheelchair maintenance appointment",
        "check wheelchair accessible route to the venue",
        "fold the wheelchair and put it in the car",
        "adjust the wheelchair footrests",
        "clean and oil the wheelchair wheels",
        "return the rental wheelchair after the trip",
        # contextual
        "wheelchair repair before the vacation",
        "accessible parking spot at the mall",
        "wheelchair ramp installation next week",
        "wheelchair battery low before the outing",
        "wheelchair cushion replacement due soon",
        "accessible hotel room for the conference",
        "wheelchair for grandma's hospital visit",
        "portable wheelchair ramp for the van",
        # short informal
        "charge wheelchair",
        "fix wheelchair",
        "book wheelchair",
        "wheelchair tires",
        "wheelchair ramp",
        # conversational
        "the wheelchair tire keeps going flat",
        "need to find a wheelchair accessible restaurant",
        "wheelchair battery doesn't last all day anymore",
        "should get the wheelchair serviced soon",
        "looking for a lighter travel wheelchair",
        # typos
        "chrage the weelchair tonight",
        "wheechair repair scheduld",
        "accesible route to venu",
        "wehlchair tires replacment",
    ],
    new_ru=[
        # keywords
        "инвалидная коляска",
        "средство передвижения",
        "доступная среда",
        "инвалидность",
        # direct tasks
        "заказать коляску в аэропорту",
        "зарядить электрическую коляску на ночь",
        "починить тормоз на коляске",
        "заказать запасные шины для коляски",
        "записаться на обслуживание коляски",
        "проверить доступный маршрут до места",
        "сложить коляску и положить в машину",
        "отрегулировать подножки коляски",
        "почистить и смазать колёса коляски",
        "вернуть прокатную коляску после поездки",
        # contextual
        "ремонт коляски перед отпуском",
        "парковка для инвалидов в торговом центре",
        "установка пандуса на следующей неделе",
        "аккумулятор коляски садится перед прогулкой",
        "пора заменить подушку коляски",
        "доступный номер в отеле для конференции",
        "коляска для бабушки на приём в больницу",
        "переносной пандус для фургона",
        # short informal
        "зарядить коляску",
        "починить коляску",
        "заказать коляску",
        "шины для коляски",
        "пандус для коляски",
        # conversational
        "шина на коляске снова спустила",
        "нужно найти ресторан с доступом для колясок",
        "аккумулятор коляски не держит весь день",
        "пора отвезти коляску на обслуживание",
        "ищу более лёгкую дорожную коляску",
        # typos
        "заярдить коляску сегодян",
        "ремнот коляски запланриован",
        "достуный маршрут до места",
        "шниы для коялски замена",
    ],
)

# ── window ───────────────────────────────────────────────────────────────────
expand("window",
    new_en=[
        # keywords
        "window",
        "app window",
        "browser window",
        "desktop window",
        # direct tasks
        "open a new browser window",
        "close the extra window",
        "resize the window to half screen",
        "move the window to the second monitor",
        "split the screen into two windows",
        "maximize the app window",
        "minimize all windows on the desktop",
        "arrange windows side by side",
        "pin the window on top",
        "restore the closed window",
        # contextual
        "too many windows open on the desktop",
        "browser window for the meeting notes",
        "open a separate window for the video call",
        "window layout for the coding session",
        "second window for the reference docs",
        "window snapping on the new monitor setup",
        "fullscreen window for the presentation",
        "private browsing window for the search",
        # short informal
        "new window",
        "close window",
        "resize window",
        "split windows",
        "window - second monitor",
        # conversational
        "I have way too many windows open right now",
        "the window keeps popping up in the wrong spot",
        "need to arrange my windows better",
        "the app window froze and won't close",
        "can't find the window I was working in",
        # typos
        "opne new browsr window",
        "clsoe the exrta window",
        "reszie window to half screeen",
        "minimze all widnows",
    ],
    new_ru=[
        # keywords
        "окно",
        "окно приложения",
        "окно браузера",
        "окно рабочего стола",
        # direct tasks
        "открыть новое окно браузера",
        "закрыть лишнее окно",
        "изменить размер окна на половину экрана",
        "переместить окно на второй монитор",
        "разделить экран на два окна",
        "развернуть окно приложения",
        "свернуть все окна на рабочем столе",
        "расположить окна рядом друг с другом",
        "закрепить окно поверх остальных",
        "восстановить закрытое окно",
        # contextual
        "слишком много окон открыто на рабочем столе",
        "окно браузера для заметок со встречи",
        "открыть отдельное окно для видеозвонка",
        "расположение окон для сессии кодинга",
        "второе окно для справочных документов",
        "привязка окон на новом мониторе",
        "полноэкранное окно для презентации",
        "приватное окно для поиска",
        # short informal
        "новое окно",
        "закрыть окно",
        "размер окна",
        "разделить окна",
        "окно - второй монитор",
        # conversational
        "слишком много окон открыто",
        "окно всё время появляется не там",
        "нужно нормально расположить окна",
        "окно приложения зависло и не закрывается",
        "не могу найти нужное окно",
        # typos
        "откырть ноовое окно браузера",
        "закрыьт лишнее окон",
        "размре окна на половнуи экрана",
        "свренуть все окна",
    ],
)

# ── capsules ─────────────────────────────────────────────────────────────────
expand("capsules",
    new_en=[
        # keywords
        "capsules",
        "medication",
        "supplements",
        "vitamins",
        # direct tasks
        "take the capsules before bed",
        "refill the capsule prescription at the pharmacy",
        "order vitamin capsules online",
        "buy fish oil capsules at the drugstore",
        "sort the capsules into the weekly pill organizer",
        "pick up the capsules from the pharmacy",
        "check if the capsules expired",
        "take two capsules with breakfast",
        "ask the doctor about the new capsules",
        "switch from tablets to capsules",
        # contextual
        "capsules running low need to reorder",
        "vitamin capsules for the morning routine",
        "capsule refill before the trip",
        "probiotic capsules after the antibiotics course",
        "capsules for the 30-day supplement plan",
        "evening capsules with dinner tonight",
        "allergy capsules before pollen season",
        "melatonin capsules for the jet lag",
        # short informal
        "take capsules",
        "refill capsules",
        "order vitamins",
        "capsules - pharmacy",
        "morning capsules",
        # conversational
        "almost out of capsules need to reorder",
        "forgot to take the capsules this morning",
        "the new capsules are easier to swallow",
        "need to set a reminder for the capsules",
        "pharmacy is out of my capsules again",
        # typos
        "tke capsulse before bed",
        "refil capsle prescription",
        "vitiamn capsules orderd",
        "capusles running low",
    ],
    new_ru=[
        # keywords
        "капсулы",
        "лекарства",
        "добавки",
        "витамины",
        # direct tasks
        "выпить капсулы перед сном",
        "продлить рецепт на капсулы в аптеке",
        "заказать витамины в капсулах онлайн",
        "купить капсулы рыбьего жира в аптеке",
        "разложить капсулы в органайзер на неделю",
        "забрать капсулы из аптеки",
        "проверить срок годности капсул",
        "выпить две капсулы за завтраком",
        "спросить врача про новые капсулы",
        "перейти с таблеток на капсулы",
        # contextual
        "капсулы заканчиваются надо заказать",
        "витамины в капсулах для утреннего приёма",
        "пополнить запас капсул перед поездкой",
        "пробиотики в капсулах после курса антибиотиков",
        "капсулы на 30-дневный курс добавок",
        "вечерние капсулы с ужином сегодня",
        "капсулы от аллергии до сезона пыльцы",
        "капсулы мелатонина от джетлага",
        # short informal
        "выпить капсулы",
        "пополнить капсулы",
        "заказать витамины",
        "капсулы - аптека",
        "утренние капсулы",
        # conversational
        "капсулы почти закончились надо заказать",
        "забыл выпить капсулы утром",
        "новые капсулы легче глотать",
        "нужно поставить напоминание о капсулах",
        "в аптеке опять нет моих капсул",
        # typos
        "выпть капусулы перед сном",
        "продлтиь рецпет на капсулы",
        "витмины в каспулах заказать",
        "каспулы заканчиавются",
    ],
)

# ── cupcake ──────────────────────────────────────────────────────────────────
expand("cupcake",
    new_en=[
        # keywords
        "cupcake",
        "muffin",
        "frosting",
        "bakery treat",
        # direct tasks
        "bake cupcakes for the party",
        "order cupcakes from the bakery",
        "frost the cupcakes tonight",
        "buy cupcake liners at the store",
        "make chocolate cupcakes for the bake sale",
        "decorate the cupcakes with sprinkles",
        "bring cupcakes to the office tomorrow",
        "try the new cupcake recipe this weekend",
        "pick up cupcakes for the birthday",
        "pack cupcakes for the school event",
        # contextual
        "cupcakes for the kids birthday party Saturday",
        "vanilla cupcakes for the bridal shower",
        "gluten free cupcakes for the potluck",
        "cupcake ingredients from the grocery store",
        "cupcake order from the bakery by Friday",
        "red velvet cupcakes for Valentine's Day",
        "mini cupcakes for the baby shower",
        "cupcake decorating supplies for the weekend",
        # short informal
        "bake cupcakes",
        "order cupcakes",
        "cupcake recipe",
        "cupcakes - party",
        "frost cupcakes",
        # conversational
        "need to bake cupcakes before the party",
        "the cupcakes turned out great last time",
        "should I make cupcakes or a regular cake",
        "forgot to order the cupcakes for Saturday",
        "cupcakes are way easier than a full cake",
        # typos
        "bkae cupckes for the party",
        "ordr cupcakes from bakrey",
        "forst the cupckaes tonight",
        "buy cupacke liners",
    ],
    new_ru=[
        # keywords
        "кекс",
        "маффин",
        "глазурь",
        "выпечка",
        # direct tasks
        "испечь кексы на вечеринку",
        "заказать кексы в пекарне",
        "украсить кексы глазурью сегодня вечером",
        "купить формочки для кексов",
        "приготовить шоколадные кексы на продажу",
        "украсить кексы посыпкой",
        "принести кексы в офис завтра",
        "попробовать новый рецепт кексов в выходные",
        "забрать кексы ко дню рождения",
        "упаковать кексы на школьный праздник",
        # contextual
        "кексы на день рождения ребёнка в субботу",
        "ванильные кексы на девичник",
        "безглютеновые кексы на общий стол",
        "ингредиенты для кексов из магазина",
        "заказ кексов из пекарни к пятнице",
        "красные бархатные кексы на День Валентина",
        "мини-кексы на baby shower",
        "материалы для украшения кексов на выходные",
        # short informal
        "испечь кексы",
        "заказать кексы",
        "рецепт кексов",
        "кексы - вечеринка",
        "украсить кексы",
        # conversational
        "нужно испечь кексы до вечеринки",
        "кексы в прошлый раз отлично получились",
        "сделать кексы или обычный торт",
        "забыла заказать кексы на субботу",
        "кексы гораздо проще чем целый торт",
        # typos
        "испчеь кексы на вечрениук",
        "зкаазть кексы из пекрани",
        "укарсить кексы глазруью",
        "куптиь формочки дял кексов",
    ],
)

# ── moped ────────────────────────────────────────────────────────────────────
expand("moped",
    new_en=[
        # keywords
        "moped",
        "scooter",
        "vespa",
        "motor scooter",
        # direct tasks
        "ride the moped to work today",
        "charge the electric moped overnight",
        "get the moped serviced this week",
        "renew the moped insurance",
        "buy a helmet for the moped",
        "park the moped near the entrance",
        "fill up the moped with gas",
        "register the new moped at the DMV",
        "change the moped oil this weekend",
        "lock the moped before going inside",
        # contextual
        "moped service appointment Thursday morning",
        "moped insurance renewal due next month",
        "new moped battery arriving this week",
        "moped commute instead of driving tomorrow",
        "scooter ride to the farmers market Saturday",
        "moped cover for the rainy season",
        "vespa rental for the vacation in Italy",
        "moped parking pass for the campus",
        # short informal
        "charge moped",
        "moped service",
        "lock moped",
        "moped gas",
        "ride scooter",
        # conversational
        "the moped won't start this morning",
        "need to get the scooter fixed soon",
        "moped is cheaper than driving to work",
        "thinking about getting an electric moped",
        "the moped mirror is cracked need a new one",
        # typos
        "chrage the mopd tonight",
        "moepd service appoinment",
        "rdie the scootr to work",
        "mopde insurance renweal",
    ],
    new_ru=[
        # keywords
        "мопед",
        "скутер",
        "веспа",
        "моторолер",
        # direct tasks
        "поехать на мопеде на работу",
        "зарядить электрический мопед на ночь",
        "отвезти мопед на техобслуживание",
        "продлить страховку на мопед",
        "купить шлем для мопеда",
        "припарковать мопед у входа",
        "заправить мопед бензином",
        "зарегистрировать новый мопед в ГАИ",
        "поменять масло в мопеде в выходные",
        "закрыть мопед на замок",
        # contextual
        "техобслуживание мопеда в четверг утром",
        "страховка мопеда истекает в следующем месяце",
        "новый аккумулятор для мопеда на этой неделе",
        "поехать на мопеде вместо машины завтра",
        "поездка на скутере на рынок в субботу",
        "чехол для мопеда на сезон дождей",
        "аренда веспы на отпуск в Италии",
        "парковочный пропуск для мопеда",
        # short informal
        "зарядить мопед",
        "сервис мопеда",
        "запереть мопед",
        "заправить мопед",
        "поехать на скутере",
        # conversational
        "мопед не заводится сегодня утром",
        "надо починить скутер побыстрее",
        "на мопеде дешевле ездить на работу",
        "думаю купить электрический мопед",
        "зеркало на мопеде треснуло нужно новое",
        # typos
        "заярдить мопде на ночь",
        "моепд на техобслуивание",
        "поехтаь на скутре на работу",
        "страховка мопдеа продлить",
    ],
)

# ── scrubber ─────────────────────────────────────────────────────────────────
expand("scrubber",
    new_en=[
        # keywords
        "scrubber",
        "seek bar",
        "playhead",
        "timeline position",
        # direct tasks
        "drag the scrubber to the right moment",
        "seek to the two minute mark in the podcast",
        "jump to the chorus using the scrubber",
        "rewind the video with the scrubber",
        "skip ahead in the track with the seek bar",
        "set the playback position to the beginning",
        "scrub back to find that quote",
        "move the playhead to the next chapter",
        "fast forward using the timeline scrubber",
        "tap the scrubber to skip the intro",
        # contextual
        "scrubber position for the podcast timestamp",
        "find the right moment with the seek bar",
        "playhead at the start of the second act",
        "scrubber for the video editing timeline",
        "seek bar to jump to the highlight",
        "timeline scrubber in the music player",
        "playback position for the audiobook chapter",
        "scrubber position saved for later",
        # short informal
        "seek video",
        "scrub audio",
        "drag playhead",
        "rewind scrubber",
        "skip with scrubber",
        # conversational
        "need to rewind to where I left off",
        "drag the scrubber back to that part",
        "the scrubber keeps jumping to the wrong spot",
        "can't find the right moment with the seek bar",
        "scrubber is too small to drag accurately",
        # typos
        "scruber dragged to rewidn",
        "sek bar jump to timestmap",
        "playhad at the begining",
        "timelien scrubber positon",
    ],
    new_ru=[
        # keywords
        "ползунок",
        "полоса перемотки",
        "плейхед",
        "позиция на шкале",
        # direct tasks
        "перетащить ползунок к нужному моменту",
        "перемотать к второй минуте подкаста",
        "перейти к припеву с помощью ползунка",
        "перемотать видео назад ползунком",
        "пропустить вперёд по полосе перемотки",
        "установить позицию воспроизведения на начало",
        "отмотать назад чтобы найти цитату",
        "переместить плейхед к следующей главе",
        "перемотать вперёд ползунком на шкале",
        "нажать на ползунок чтобы пропустить вступление",
        # contextual
        "позиция ползунка для метки подкаста",
        "найти нужный момент с помощью ползунка",
        "плейхед на начале второго акта",
        "ползунок для монтажа видео",
        "полоса перемотки к лучшему моменту",
        "ползунок в музыкальном плеере",
        "позиция воспроизведения для главы аудиокниги",
        "сохранить позицию ползунка на потом",
        # short informal
        "перемотать видео",
        "перемотка аудио",
        "двигать плейхед",
        "назад ползунком",
        "пропустить ползунком",
        # conversational
        "нужно вернуться к тому месту где остановился",
        "перетащить ползунок обратно к тому моменту",
        "ползунок постоянно перескакивает не туда",
        "не могу найти нужный момент ползунком",
        "ползунок слишком маленький неудобно тянуть",
        # typos
        "позлунок перетащить к нчалу",
        "перемотаьт видео ползнуком",
        "плейхде на начале главы",
        "ползунок прыгает не туад",
    ],
)

# ── stairs ───────────────────────────────────────────────────────────────────
expand("stairs",
    new_en=[
        # keywords
        "stairs",
        "steps",
        "staircase",
        "stairwell",
        # direct tasks
        "take the stairs instead of the elevator",
        "climb the stairs for exercise today",
        "fix the broken stair railing",
        "install a baby gate at the top of the stairs",
        "replace the carpet on the stairs",
        "paint the stair risers white",
        "add non-slip strips to the stairs",
        "vacuum the stairs this afternoon",
        "check the stairwell lights",
        "repair the cracked step on the front porch",
        # contextual
        "stairs count toward daily step goal",
        "stair railing repair quote this week",
        "new carpet for the stairs arriving Friday",
        "stairs exercise routine in the morning",
        "stairwell cleaning on the schedule",
        "baby gate for the stairs before the visit",
        "stairs lighting upgrade for safety",
        "step repair before the home inspection",
        # short informal
        "fix stairs",
        "clean stairs",
        "stairs exercise",
        "stair railing",
        "paint stairs",
        # conversational
        "the stairs creak every time I go up",
        "need to fix that loose step soon",
        "taking the stairs more to stay active",
        "the stair carpet is getting worn out",
        "stairs are too dark at night need better lights",
        # typos
        "tak the staris today",
        "fix the stiar railing",
        "clmib stairs for exerscise",
        "repiar the cracked stp",
    ],
    new_ru=[
        # keywords
        "лестница",
        "ступеньки",
        "лестничный пролёт",
        "лестничная клетка",
        # direct tasks
        "ходить по лестнице вместо лифта",
        "подняться по лестнице для зарядки",
        "починить перила на лестнице",
        "установить ворота безопасности наверху лестницы",
        "заменить ковёр на лестнице",
        "покрасить подступенки в белый",
        "наклеить противоскользящие полоски на ступеньки",
        "пропылесосить лестницу после обеда",
        "проверить свет на лестничной клетке",
        "отремонтировать треснувшую ступеньку на крыльце",
        # contextual
        "ходьба по лестнице идёт в зачёт шагов",
        "смета на ремонт перил на этой неделе",
        "новый ковёр для лестницы в пятницу",
        "зарядка на лестнице утром",
        "уборка лестничной клетки по расписанию",
        "ворота на лестницу до приезда гостей с ребёнком",
        "улучшить освещение лестницы для безопасности",
        "ремонт ступеньки до осмотра дома",
        # short informal
        "починить лестницу",
        "убрать лестницу",
        "зарядка на лестнице",
        "перила лестницы",
        "покрасить лестницу",
        # conversational
        "лестница скрипит каждый раз когда поднимаюсь",
        "надо починить шатающуюся ступеньку",
        "стараюсь чаще ходить по лестнице",
        "ковёр на лестнице уже протёрся",
        "на лестнице темно ночью нужен свет",
        # typos
        "ходтиь по лесницте вместо лифта",
        "почниить перила на лесницте",
        "поднтяься по лестнце утром",
        "ремнот треснвушей ступеньки",
    ],
)

# ── table-rows ───────────────────────────────────────────────────────────────
expand("table-rows",
    new_en=[
        # keywords
        "table rows",
        "spreadsheet rows",
        "data rows",
        "row layout",
        # direct tasks
        "add a new row to the spreadsheet",
        "delete the empty rows in the table",
        "sort the rows by date",
        "merge the duplicate rows",
        "format the header row bold",
        "freeze the top row in the spreadsheet",
        "hide the extra rows from the view",
        "copy the row to the other sheet",
        "insert a row above the total",
        "resize the row height in the table",
        # contextual
        "row formatting for the monthly report",
        "clean up empty rows before sharing the file",
        "table rows for the inventory spreadsheet",
        "row grouping for the budget template",
        "color code the rows by status",
        "data rows imported from the CSV file",
        "header row style for the project tracker",
        "alternating row colors for readability",
        # short informal
        "add row",
        "sort rows",
        "delete rows",
        "format rows",
        "freeze row",
        # conversational
        "there are too many empty rows in this spreadsheet",
        "need to sort these rows by priority",
        "the row data got messed up after the import",
        "can't figure out how to freeze the top row",
        "rows are all jumbled need to reorganize",
        # typos
        "ad a new row to teh table",
        "delte empty rowss",
        "srot rows by daet",
        "freez the top rwow",
    ],
    new_ru=[
        # keywords
        "строки таблицы",
        "строки электронной таблицы",
        "строки данных",
        "строковый формат",
        # direct tasks
        "добавить новую строку в таблицу",
        "удалить пустые строки в таблице",
        "отсортировать строки по дате",
        "объединить дублирующиеся строки",
        "выделить строку заголовка жирным",
        "закрепить верхнюю строку в таблице",
        "скрыть лишние строки",
        "скопировать строку на другой лист",
        "вставить строку над итогом",
        "изменить высоту строки в таблице",
        # contextual
        "форматирование строк для ежемесячного отчёта",
        "убрать пустые строки перед отправкой файла",
        "строки таблицы для инвентарной ведомости",
        "группировка строк для шаблона бюджета",
        "цветовая маркировка строк по статусу",
        "строки данных импортированы из CSV",
        "стиль заголовка для трекера проекта",
        "чередование цветов строк для читаемости",
        # short informal
        "добавить строку",
        "сортировать строки",
        "удалить строки",
        "формат строк",
        "закрепить строку",
        # conversational
        "слишком много пустых строк в таблице",
        "нужно отсортировать строки по приоритету",
        "данные в строках сбились после импорта",
        "не могу закрепить верхнюю строку",
        "строки перемешались надо перестроить",
        # typos
        "добвить новую стрку в таблицу",
        "удлаить пустые сторки",
        "сортирвоать строки по дтае",
        "закрпеить вернюю строку",
    ],
)

# ── tape ─────────────────────────────────────────────────────────────────────
expand("tape",
    new_en=[
        # keywords
        "tape",
        "adhesive tape",
        "duct tape",
        "packing tape",
        # direct tasks
        "buy tape at the store",
        "tape the box shut for shipping",
        "grab the tape from the drawer",
        "wrap the gift with tape",
        "seal the envelope with tape",
        "fix the torn page with tape",
        "tape the poster to the wall",
        "pack the boxes with packing tape",
        "use duct tape to fix the leak temporarily",
        "tape the wires to the baseboard",
        # contextual
        "tape for packing boxes this weekend",
        "washi tape for the scrapbook project",
        "masking tape before painting the room",
        "tape dispenser for the office desk",
        "clear tape for wrapping presents tonight",
        "duct tape roll for the camping gear",
        "tape for the moving day supplies list",
        "medical tape for the first aid kit",
        # short informal
        "buy tape",
        "grab tape",
        "tape - office",
        "packing tape",
        "tape the box",
        # conversational
        "we're out of tape again",
        "need tape to seal these boxes",
        "where did I put the tape dispenser",
        "the tape keeps peeling off the wall",
        "should I use duct tape or packing tape",
        # typos
        "tpae the box for shippng",
        "buy tpae at the stor",
        "grba the taep from drawr",
        "fix the torn pge with taep",
    ],
    new_ru=[
        # keywords
        "скотч",
        "клейкая лента",
        "изолента",
        "упаковочный скотч",
        # direct tasks
        "купить скотч в магазине",
        "заклеить коробку скотчем для отправки",
        "взять скотч из ящика",
        "обернуть подарок с помощью скотча",
        "заклеить конверт скотчем",
        "починить порванную страницу скотчем",
        "приклеить плакат на стену скотчем",
        "запаковать коробки упаковочным скотчем",
        "заклеить протечку изолентой временно",
        "приклеить провода скотчем к плинтусу",
        # contextual
        "скотч для упаковки коробок в выходные",
        "декоративный скотч для скрапбука",
        "малярный скотч перед покраской комнаты",
        "диспенсер для скотча на рабочий стол",
        "прозрачный скотч для упаковки подарков вечером",
        "рулон изоленты в походное снаряжение",
        "скотч в список покупок для переезда",
        "медицинский пластырь в аптечку",
        # short informal
        "купить скотч",
        "взять скотч",
        "скотч - офис",
        "упаковочный скотч",
        "заклеить коробку",
        # conversational
        "скотч снова закончился",
        "нужен скотч заклеить эти коробки",
        "куда я положил диспенсер для скотча",
        "скотч постоянно отклеивается от стены",
        "использовать изоленту или упаковочный скотч",
        # typos
        "заклетиь коробку скочтем",
        "кпуить скотч в магзаине",
        "взтяь стокч из ящкиа",
        "починтиь страниуц скотечм",
    ],
)

# ── truck-moving ─────────────────────────────────────────────────────────────
expand("truck-moving",
    new_en=[
        # keywords
        "moving truck",
        "U-Haul",
        "box truck",
        "moving van",
        # direct tasks
        "rent a moving truck for Saturday",
        "return the rental truck by noon",
        "load the furniture into the moving truck",
        "reserve a U-Haul for the move",
        "drive the moving truck to the new place",
        "unload the moving truck at the new apartment",
        "fill up the moving truck with gas before returning",
        "get the moving truck insurance",
        "pick up the rental truck in the morning",
        "check the moving truck for scratches before driving",
        # contextual
        "moving truck reservation for next Friday",
        "U-Haul pickup at 8am Saturday morning",
        "moving truck big enough for the whole apartment",
        "truck rental for the cross town move",
        "friends helping load the moving truck at ten",
        "moving truck parked on the street overnight",
        "return the moving truck after unloading Sunday",
        "gas receipt for the moving truck rental",
        # short informal
        "rent truck",
        "load truck",
        "U-Haul Saturday",
        "return truck",
        "moving truck gas",
        # conversational
        "need to book the moving truck soon",
        "the moving truck is huge should be enough",
        "forgot to reserve the rental truck",
        "how much does a moving truck cost for one day",
        "the moving truck barely fit in the driveway",
        # typos
        "rnet a moving trcuk Saturday",
        "retrun the rentl truck",
        "load furnituer into the trcuk",
        "reserv a U-Haul for movign",
    ],
    new_ru=[
        # keywords
        "грузовик для переезда",
        "газель",
        "фургон",
        "грузовая машина",
        # direct tasks
        "арендовать грузовик на субботу",
        "вернуть арендованный грузовик до обеда",
        "загрузить мебель в грузовик",
        "забронировать газель на переезд",
        "перегнать грузовик на новое место",
        "разгрузить грузовик у новой квартиры",
        "заправить грузовик перед возвратом",
        "оформить страховку на грузовик",
        "забрать арендованный грузовик утром",
        "осмотреть грузовик на царапины перед поездкой",
        # contextual
        "бронирование грузовика на следующую пятницу",
        "забрать газель в 8 утра в субботу",
        "грузовик достаточно большой для всей квартиры",
        "аренда грузовика для переезда по городу",
        "друзья помогают грузить в десять утра",
        "грузовик припаркован на улице на ночь",
        "вернуть грузовик после разгрузки в воскресенье",
        "чек за бензин для арендованного грузовика",
        # short informal
        "арендовать грузовик",
        "загрузить грузовик",
        "газель на субботу",
        "вернуть грузовик",
        "бензин для грузовика",
        # conversational
        "нужно побыстрее забронировать грузовик",
        "грузовик огромный должно хватить",
        "забыл забронировать грузовик",
        "сколько стоит грузовик на один день",
        "грузовик еле поместился на подъездной дорожке",
        # typos
        "арнедовать грзуовик на субботу",
        "верунть арнедованный грузвоик",
        "загурзить мебль в грузовки",
        "забронриовать газль на переезд",
    ],
)

# ── users ────────────────────────────────────────────────────────────────────
expand("users",
    new_en=[
        # keywords
        "users",
        "team members",
        "group",
        "accounts",
        # direct tasks
        "invite new users to the team",
        "review the user list in the admin panel",
        "remove inactive users from the account",
        "set user permissions for the project",
        "add a user to the shared workspace",
        "export the user list to a spreadsheet",
        "reset the user password",
        "create new user accounts for the interns",
        "assign users to the project group",
        "update user roles in the system",
        # contextual
        "new user onboarding before Monday",
        "user access audit for the quarterly review",
        "team member accounts for the new project",
        "user permissions cleanup this week",
        "shared workspace users need updating",
        "deactivate users who left the company",
        "user invites sent before the meeting",
        "admin panel user management session",
        # short informal
        "add users",
        "remove users",
        "user list",
        "user permissions",
        "team members",
        # conversational
        "there are too many inactive users in the system",
        "need to add the new hires to the team",
        "someone forgot to remove the old users",
        "the user list is getting really long",
        "which users have admin access right now",
        # typos
        "invte new usres to the team",
        "reveiw user lsit",
        "remvoe inactive uesrs",
        "add uesr to workspce",
    ],
    new_ru=[
        # keywords
        "пользователи",
        "участники команды",
        "группа",
        "учётные записи",
        # direct tasks
        "пригласить новых пользователей в команду",
        "проверить список пользователей в панели админа",
        "удалить неактивных пользователей из аккаунта",
        "настроить права пользователей для проекта",
        "добавить пользователя в общее рабочее пространство",
        "экспортировать список пользователей в таблицу",
        "сбросить пароль пользователя",
        "создать учётные записи для стажёров",
        "назначить пользователей в группу проекта",
        "обновить роли пользователей в системе",
        # contextual
        "онбординг нового пользователя до понедельника",
        "аудит доступа пользователей к квартальному обзору",
        "аккаунты участников для нового проекта",
        "чистка прав пользователей на этой неделе",
        "пользователи общего пространства нуждаются в обновлении",
        "деактивировать пользователей которые ушли",
        "приглашения пользователей до встречи",
        "сессия управления пользователями в админке",
        # short informal
        "добавить пользователей",
        "удалить пользователей",
        "список пользователей",
        "права пользователей",
        "участники команды",
        # conversational
        "слишком много неактивных пользователей в системе",
        "нужно добавить новичков в команду",
        "кто-то забыл удалить старых пользователей",
        "список пользователей стал очень длинным",
        "у кого сейчас админский доступ",
        # typos
        "приглсаить новых ползователей",
        "проврить списко пользовтаелей",
        "удалтиь неактвиных пользовтелей",
        "добваить пользоватля в рабочее простанрство",
    ],
)

# ── watch-smart ──────────────────────────────────────────────────────────────
expand("watch-smart",
    new_en=[
        # keywords
        "smartwatch",
        "Apple Watch",
        "wearable",
        "smart wristwatch",
        # direct tasks
        "charge the smartwatch tonight",
        "pair the smartwatch with the phone",
        "install a new watch face",
        "update the smartwatch firmware",
        "set up notifications on the smartwatch",
        "replace the smartwatch band",
        "calibrate the smartwatch heart rate sensor",
        "sync the smartwatch with the fitness app",
        "enable the always-on display",
        "turn off smartwatch bedtime mode",
        # contextual
        "smartwatch charging cable for the trip",
        "new watch band arriving this week",
        "smartwatch repair appointment on Wednesday",
        "Apple Watch trade-in before the upgrade",
        "smartwatch setup for the new phone",
        "fitness goals on the smartwatch this month",
        "smartwatch silent mode for the meeting",
        "waterproof smartwatch for the swim",
        # short informal
        "charge watch",
        "watch update",
        "new watch face",
        "sync watch",
        "watch band",
        # conversational
        "the smartwatch battery barely lasts a day",
        "need to update the watch it's been lagging",
        "the watch band broke need a replacement",
        "thinking about getting the new Apple Watch",
        "smartwatch notifications are really useful",
        # typos
        "chrage the smarwatch tonight",
        "pari the smartwtach with phone",
        "instal new watch fce",
        "updtae smartwach firmware",
    ],
    new_ru=[
        # keywords
        "умные часы",
        "Apple Watch",
        "носимое устройство",
        "смарт-часы",
        # direct tasks
        "зарядить умные часы на ночь",
        "подключить часы к телефону",
        "установить новый циферблат",
        "обновить прошивку часов",
        "настроить уведомления на умных часах",
        "заменить ремешок на часах",
        "откалибровать датчик пульса",
        "синхронизировать часы с фитнес-приложением",
        "включить постоянный экран",
        "отключить ночной режим на часах",
        # contextual
        "зарядка для часов в поездку",
        "новый ремешок придёт на этой неделе",
        "ремонт умных часов в среду",
        "сдать Apple Watch перед обновлением",
        "настроить часы для нового телефона",
        "фитнес-цели на часах в этом месяце",
        "беззвучный режим часов на встречу",
        "водонепроницаемые часы для плавания",
        # short informal
        "зарядить часы",
        "обновить часы",
        "новый циферблат",
        "синхронизировать часы",
        "ремешок для часов",
        # conversational
        "часы еле живут до конца дня",
        "нужно обновить часы тормозят",
        "ремешок на часах порвался нужен новый",
        "думаю купить новые Apple Watch",
        "уведомления на часах реально удобные",
        # typos
        "заярдить умнеы часы на ночь",
        "подлкючить часы к теелфону",
        "установтиь новый ицферблат",
        "обновтиь прошвику часов",
    ],
)

# ── bin ──────────────────────────────────────────────────────────────────────
expand("bin",
    new_en=[
        # keywords
        "recycling bin",
        "recycle",
        "waste bin",
        "recycling container",
        # direct tasks
        "take the recycling bin out to the curb",
        "sort the bottles into the recycling bin",
        "clean the recycling bin this weekend",
        "bring the bin back from the curb",
        "rinse the cans before putting them in the bin",
        "check what goes in the recycling bin",
        "replace the broken recycling bin lid",
        "label the recycling bins for guests",
        "empty the office recycling bin",
        "order a new recycling bin from the city",
        # contextual
        "recycling bin pickup day is Tuesday",
        "bin needs cleaning before garbage day",
        "recycling bin overflowing before pickup",
        "new bin from the council arriving soon",
        "sort recycling before taking the bin out",
        "bin lid blown off in the storm",
        "extra recycling bin for the holiday packaging",
        "bin placement rules from the HOA",
        # short informal
        "take bin out",
        "sort recycling",
        "clean bin",
        "bin day",
        "empty bin",
        # conversational
        "the recycling bin is overflowing again",
        "forgot to take the bin out last night",
        "which bin does cardboard go in",
        "the bin smells terrible need to wash it",
        "neighbors keep using our recycling bin",
        # typos
        "tke the bin ot to the curb",
        "srot the bottels into the bin",
        "clena the recyling bin",
        "emtpy the ofice bin",
    ],
    new_ru=[
        # keywords
        "контейнер для переработки",
        "переработка",
        "мусорный бак",
        "контейнер для раздельного сбора",
        # direct tasks
        "вынести контейнер к дороге",
        "рассортировать бутылки по контейнерам",
        "помыть контейнер для переработки в выходные",
        "занести контейнер обратно с улицы",
        "ополоснуть банки перед тем как бросить в бак",
        "проверить что можно выбрасывать в контейнер",
        "заменить сломанную крышку на контейнере",
        "подписать контейнеры для гостей",
        "опустошить офисный контейнер для переработки",
        "заказать новый контейнер у управляющей компании",
        # contextual
        "день вывоза мусора во вторник",
        "бак надо помыть до дня вывоза",
        "контейнер переполнен до вывоза",
        "новый бак от управляющей компании скоро",
        "рассортировать перед тем как выносить",
        "крышку бака сдуло ветром",
        "дополнительный бак для праздничной упаковки",
        "правила расстановки баков от ТСЖ",
        # short informal
        "вынести бак",
        "рассортировать мусор",
        "помыть бак",
        "день вывоза",
        "опустошить бак",
        # conversational
        "контейнер опять переполнен",
        "забыл вынести бак вчера вечером",
        "в какой бак выбрасывать картон",
        "бак ужасно пахнет надо помыть",
        "соседи опять пользуются нашим контейнером",
        # typos
        "выенсти контейнре к дрооге",
        "рассортриовать бутлыки по бакам",
        "помтыь контейнер для перрабтоки",
        "опустшоить офисный кноетйнер",
    ],
)

# ── cucumber ─────────────────────────────────────────────────────────────────
expand("cucumber",
    new_en=[
        # keywords
        "cucumber",
        "pickle",
        "gherkin",
        "cuke",
        # direct tasks
        "buy cucumbers at the store",
        "slice cucumbers for the salad",
        "make pickled cucumbers this weekend",
        "add cucumbers to the grocery list",
        "grow cucumbers in the garden this summer",
        "peel the cucumber for the sandwich",
        "chop cucumbers for the veggie tray",
        "pickle the cucumbers with dill and garlic",
        "bring cucumbers for the picnic",
        "wash the cucumbers before slicing",
        # contextual
        "cucumbers for the Greek salad tonight",
        "cucumber seedlings for the spring garden",
        "pickled cucumbers ready by next week",
        "cucumber and cream cheese sandwiches for tea",
        "cucumbers from the farmers market Saturday",
        "cucumber water for the party",
        "fresh cucumbers for the cold soup",
        "cucumber face mask ingredients",
        # short informal
        "buy cucumbers",
        "slice cucumbers",
        "pickle cucumbers",
        "cucumbers - salad",
        "grow cucumbers",
        # conversational
        "we're out of cucumbers for the salad",
        "the garden cucumbers are finally ready",
        "need cucumbers for the tzatziki sauce",
        "cucumbers were on sale at the market today",
        "forgot to buy cucumbers for the sandwiches",
        # typos
        "buy cucumbrs at the stroe",
        "slcie cucumers for salda",
        "pickel cucumbers with dil",
        "cucmbers for the gorcery list",
    ],
    new_ru=[
        # keywords
        "огурец",
        "солёный огурец",
        "корнишон",
        "огурчик",
        # direct tasks
        "купить огурцы в магазине",
        "нарезать огурцы в салат",
        "засолить огурцы в выходные",
        "добавить огурцы в список покупок",
        "посадить огурцы на даче этим летом",
        "почистить огурец для бутерброда",
        "порезать огурцы для овощной тарелки",
        "замариновать огурцы с укропом и чесноком",
        "взять огурцы на пикник",
        "помыть огурцы перед нарезкой",
        # contextual
        "огурцы для греческого салата на ужин",
        "рассада огурцов на весну",
        "солёные огурцы будут готовы к следующей неделе",
        "бутерброды с огурцом и сливочным сыром",
        "огурцы с фермерского рынка в субботу",
        "огуречная вода для вечеринки",
        "свежие огурцы для холодного супа",
        "огурцы для маски для лица",
        # short informal
        "купить огурцы",
        "нарезать огурцы",
        "засолить огурцы",
        "огурцы - салат",
        "посадить огурцы",
        # conversational
        "огурцы для салата закончились",
        "огурцы на даче наконец-то созрели",
        "нужны огурцы для соуса цацики",
        "огурцы были по скидке на рынке",
        "забыл купить огурцы для бутербродов",
        # typos
        "кпуить огруцы в магзаине",
        "нрезать огурцы в слаат",
        "засолтиь огуцры с укропом",
        "огрцуы в спиоск покупок",
    ],
)

# ── microchip ────────────────────────────────────────────────────────────────
expand("microchip",
    new_en=[
        # keywords
        "microchip",
        "processor",
        "CPU",
        "semiconductor",
        # direct tasks
        "upgrade the CPU in the desktop",
        "replace the old processor this weekend",
        "check the CPU temperature under load",
        "order a new microchip for the project",
        "install the processor in the motherboard",
        "apply thermal paste on the CPU",
        "benchmark the new processor",
        "research which CPU to buy for the build",
        "return the defective microchip",
        "compare processors for the new laptop",
        # contextual
        "CPU upgrade before the gaming season",
        "new processor arriving Thursday",
        "microchip for the Raspberry Pi project",
        "CPU cooler needed for the new processor",
        "chip shortage affecting the order",
        "processor benchmark results for the review",
        "thermal paste application before installing CPU",
        "microchip soldering for the electronics class",
        # short informal
        "upgrade CPU",
        "check chip temp",
        "order processor",
        "CPU benchmark",
        "new chip",
        # conversational
        "the CPU is overheating need better cooling",
        "thinking about upgrading to a faster processor",
        "the new chip is way faster than the old one",
        "chip prices are finally coming down",
        "need to figure out which processor fits the board",
        # typos
        "upgarde the CPU in the desktpo",
        "chekc the processer temperature",
        "instal the processer on motherbaord",
        "benchamrk the new CPU",
    ],
    new_ru=[
        # keywords
        "микрочип",
        "процессор",
        "ЦПУ",
        "полупроводник",
        # direct tasks
        "обновить процессор в десктопе",
        "заменить старый процессор в выходные",
        "проверить температуру процессора под нагрузкой",
        "заказать новый чип для проекта",
        "установить процессор в материнскую плату",
        "нанести термопасту на процессор",
        "провести бенчмарк нового процессора",
        "выбрать какой процессор купить для сборки",
        "вернуть бракованный микрочип",
        "сравнить процессоры для нового ноутбука",
        # contextual
        "апгрейд процессора до игрового сезона",
        "новый процессор придёт в четверг",
        "микрочип для проекта на Raspberry Pi",
        "кулер для нового процессора",
        "дефицит чипов задерживает заказ",
        "результаты бенчмарка процессора для обзора",
        "нанесение термопасты перед установкой",
        "пайка микрочипов на уроке электроники",
        # short informal
        "обновить процессор",
        "проверить температуру чипа",
        "заказать процессор",
        "бенчмарк ЦПУ",
        "новый чип",
        # conversational
        "процессор перегревается нужно охлаждение",
        "думаю обновиться на более быстрый процессор",
        "новый чип намного быстрее старого",
        "цены на чипы наконец-то снижаются",
        "нужно понять какой процессор подходит к плате",
        # typos
        "обноивть процесор в десктпое",
        "прворить температуру процесосра",
        "устанвоить процессор в мтаеринскую пулат",
        "бенмчарк ноовго процесосра",
    ],
)

# ── mushroom ─────────────────────────────────────────────────────────────────
expand("mushroom",
    new_en=[
        # keywords
        "mushroom",
        "mushrooms",
        "shiitake",
        "chanterelle",
        # direct tasks
        "buy mushrooms at the grocery store",
        "cook mushrooms for dinner tonight",
        "slice the mushrooms for the pizza",
        "forage for mushrooms in the forest",
        "add mushrooms to the stir fry",
        "grow mushrooms at home with a kit",
        "clean the mushrooms before cooking",
        "dry the mushrooms for storage",
        "marinate the mushrooms for the grill",
        "pick up shiitake mushrooms from the market",
        # contextual
        "mushrooms for the pasta sauce tonight",
        "mushroom risotto for Sunday dinner",
        "foraging trip for wild mushrooms this weekend",
        "mushroom growing kit arriving tomorrow",
        "chanterelles from the farmers market Saturday",
        "cream of mushroom soup for the cold day",
        "mushrooms as a meat substitute for the recipe",
        "stuffed mushrooms for the appetizer platter",
        # short informal
        "buy mushrooms",
        "cook mushrooms",
        "slice mushrooms",
        "mushrooms - dinner",
        "forage mushrooms",
        # conversational
        "we need mushrooms for the recipe tonight",
        "the mushrooms at the market looked amazing",
        "should I use shiitake or button mushrooms",
        "the mushroom kit is finally growing",
        "forgot to add mushrooms to the grocery list",
        # typos
        "buy mushroms at the stor",
        "slcie mushrooms for the piza",
        "cook mushroooms for dinne",
        "forag for mushroms in the forst",
    ],
    new_ru=[
        # keywords
        "грибы",
        "шампиньоны",
        "шиитаке",
        "лисички",
        # direct tasks
        "купить грибы в магазине",
        "приготовить грибы на ужин",
        "нарезать грибы для пиццы",
        "пойти за грибами в лес",
        "добавить грибы в жаркое",
        "вырастить грибы дома из набора",
        "почистить грибы перед готовкой",
        "засушить грибы для хранения",
        "замариновать грибы для шашлыка",
        "купить шиитаке на рынке",
        # contextual
        "грибы для пасты сегодня вечером",
        "грибное ризотто на воскресный ужин",
        "поход за грибами в выходные",
        "набор для выращивания грибов придёт завтра",
        "лисички с фермерского рынка в субботу",
        "грибной суп-крем на холодный день",
        "грибы как замена мясу в рецепте",
        "фаршированные грибы на закуску",
        # short informal
        "купить грибы",
        "приготовить грибы",
        "нарезать грибы",
        "грибы - ужин",
        "за грибами",
        # conversational
        "нужны грибы для рецепта сегодня",
        "грибы на рынке выглядели отлично",
        "шиитаке или шампиньоны для блюда",
        "набор для грибов наконец-то начал расти",
        "забыл добавить грибы в список покупок",
        # typos
        "куптиь грибы в магзиане",
        "нарзеать грибы для пицыц",
        "пригтовить грибы на жуин",
        "пойит за грибмаи в лес",
    ],
)

# ── paste ────────────────────────────────────────────────────────────────────
expand("paste",
    new_en=[
        # keywords
        "paste",
        "clipboard",
        "Ctrl+V",
        "paste text",
        # direct tasks
        "paste the text into the document",
        "paste the link into the chat",
        "paste the address from the clipboard",
        "paste the code snippet into the editor",
        "paste the image into the presentation",
        "paste the phone number into the form",
        "paste the tracking number into the notes",
        "paste the password from the manager",
        "paste the copied data into the spreadsheet",
        "paste the URL into the browser",
        # contextual
        "paste the meeting link before the call",
        "clipboard content for the email draft",
        "paste formatting from the template",
        "paste values only without formatting",
        "paste the reference number for the order",
        "clipboard history for the copied items",
        "paste special in the spreadsheet",
        "paste the recipe into the notes app",
        # short informal
        "paste link",
        "paste text",
        "paste code",
        "paste address",
        "clipboard paste",
        # conversational
        "I copied it but can't paste it anywhere",
        "need to paste the link before I forget",
        "the paste shortcut isn't working",
        "paste keeps adding weird formatting",
        "clipboard cleared before I could paste",
        # typos
        "pste the text into docment",
        "passte the link into caht",
        "pase the code snippt",
        "patse the URL into browsr",
    ],
    new_ru=[
        # keywords
        "вставить",
        "буфер обмена",
        "Ctrl+V",
        "вставка текста",
        # direct tasks
        "вставить текст в документ",
        "вставить ссылку в чат",
        "вставить адрес из буфера обмена",
        "вставить код в редактор",
        "вставить картинку в презентацию",
        "вставить номер телефона в форму",
        "вставить трек-номер в заметки",
        "вставить пароль из менеджера паролей",
        "вставить скопированные данные в таблицу",
        "вставить URL в браузер",
        # contextual
        "вставить ссылку на встречу до звонка",
        "содержимое буфера для черновика письма",
        "вставить форматирование из шаблона",
        "вставить только значения без форматирования",
        "вставить номер заказа",
        "история буфера обмена для скопированного",
        "специальная вставка в таблице",
        "вставить рецепт в приложение заметок",
        # short informal
        "вставить ссылку",
        "вставить текст",
        "вставить код",
        "вставить адрес",
        "вставка из буфера",
        # conversational
        "скопировал но не могу вставить",
        "нужно вставить ссылку пока не забыл",
        "горячая клавиша вставки не работает",
        "при вставке добавляется странное форматирование",
        "буфер очистился раньше чем вставил",
        # typos
        "встваить текст в докумнет",
        "вставтиь ссылку в чта",
        "вствить код в рдеактор",
        "встаивть URL в барузер",
    ],
)

print("\nBatch 001 complete. Run merge and audit next.")
