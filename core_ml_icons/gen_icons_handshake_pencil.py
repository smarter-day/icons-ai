from pathlib import Path
import csv, json

base = Path("icons")

def write_csv(fp, rows):
    with open(fp, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(["text", "label"])
        for r in rows:
            w.writerow(r)

def save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru,
              conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru,
              valid_en, valid_ru, test_en, test_ru):
    icon_dir = base / icon
    icon_dir.mkdir(parents=True, exist_ok=True)

    train_en = [(t, icon) for t in st_en + pst_en + reg_en + conv_en + typo_en + bnd_en]
    train_ru = [(t, icon) for t in st_ru + pst_ru + reg_ru + conv_ru + typo_ru + bnd_ru]

    write_csv(icon_dir / "train_en.csv", train_en)
    write_csv(icon_dir / "train_ru.csv", train_ru)
    write_csv(icon_dir / "valid_en.csv", [(t, icon) for t in valid_en])
    write_csv(icon_dir / "valid_ru.csv", [(t, icon) for t in valid_ru])
    write_csv(icon_dir / "test_en.csv",  [(t, icon) for t in test_en])
    write_csv(icon_dir / "test_ru.csv",  [(t, icon) for t in test_ru])

    icon_log = {
        "icon": icon,
        "rows": {"train_en": len(train_en), "valid_en": 3, "test_en": 3},
        "categories": {
            "search_terms":           {"en": st_en,    "ru": st_ru},
            "phrase_per_search_term": {"en": pst_en,   "ru": pst_ru},
            "regular":                {"en": reg_en,   "ru": reg_ru},
            "conversational":         {"en": conv_en,  "ru": conv_ru},
            "typo":                   {"en": typo_en,  "ru": typo_ru},
            "boundary":               {"en": bnd_en,   "ru": bnd_ru},
            "valid":                  {"en": valid_en, "ru": valid_ru},
            "test":                   {"en": test_en,  "ru": test_ru},
        }
    }
    with open(icon_dir / "icon_log.json", "w", encoding="utf-8") as f:
        json.dump(icon_log, f, ensure_ascii=False, indent=2)

    print(f"{icon}: {len(train_en)} train rows ({len(st_en)} st + {len(pst_en)} pst + 24)")

# ── 1. handshake ──────────────────────────────────────────────────────────────
icon = "handshake"
st_en = ["agreement", "greeting", "meeting", "partnership"]
st_ru = ["соглашение", "приветствие", "встреча", "партнёрство"]
pst_en = [
    "formal business agreement signed",
    "reaching an agreement between parties",
    "friendly greeting handshake",
    "greeting someone with a handshake",
    "first meeting introduction handshake",
    "scheduled meeting with a new client",
    "strategic business partnership",
    "long-term partnership between companies",
]
pst_ru = [
    "официальное деловое соглашение подписано",
    "достижение договорённости между сторонами",
    "дружеское рукопожатие при приветствии",
    "поприветствовать жестом рукопожатия",
    "рукопожатие при первой встрече",
    "встреча с новым клиентом",
    "стратегическое деловое партнёрство",
    "долгосрочное партнёрство между компаниями",
]
reg_en = [
    "two hands clasped together in a handshake",
    "deal closed with a handshake",
    "business handshake after contract signing",
    "professional introduction between colleagues",
    "confirm partnership with a handshake symbol",
    "alliance or collaboration icon",
    "joint venture agreement",
    "welcoming a new team member",
    "community cooperation and mutual support",
    "sealing a deal with a handshake",
]
reg_ru = [
    "два сцепленных кулака в рукопожатии",
    "сделка закрыта рукопожатием",
    "деловое рукопожатие после подписания контракта",
    "профессиональное знакомство между коллегами",
    "подтвердить партнёрство иконкой рукопожатия",
    "значок союза или сотрудничества",
    "соглашение о совместном предприятии",
    "приветствие нового члена команды",
    "общественное сотрудничество и взаимная поддержка",
    "скрепить сделку рукопожатием",
]
conv_en = [
    "I need a handshake icon for the partnership screen",
    "add a handshake symbol to the deals section",
    "show a handshake for the agreement confirmation",
    "use the handshake icon for the collaboration feature",
]
conv_ru = [
    "нужна иконка рукопожатия для экрана партнёрства",
    "добавить символ рукопожатия в раздел сделок",
    "показать рукопожатие для подтверждения соглашения",
    "использовать иконку рукопожатия для функции совместной работы",
]
typo_en = [
    "handsahke agreement",
    "handshakke meeting",
    "partnerhsip deal",
    "agremeent handshake",
]
typo_ru = [
    "рукапожатие соглашение",
    "партнёрствo встреча",
    "соглашенее рукопожатие",
    "встрeча партнёрство",
]
bnd_en = [
    "waving hand to say hello or goodbye",
    "hand wave gesture as a friendly hello",
    "raised fist symbol of solidarity",
    "thumbs up approval reaction",
    "people holding hands walking together",
    "clapping hands applause celebration",
]
bnd_ru = [
    "машущая рукой жест приветствия или прощания",
    "жест помахать рукой как дружеское привет",
    "поднятый кулак как символ солидарности",
    "большой палец вверх одобрение реакция",
    "люди держатся за руки идут вместе",
    "аплодирующие руки овация праздник",
]
valid_en = ["two people shaking hands", "business deal handshake", "partnership agreement icon"]
valid_ru = ["два человека жмут руки", "деловое рукопожатие", "иконка партнёрского соглашения"]
test_en  = ["handshake symbol for agreements", "clasped hands business meeting", "collaboration deal icon"]
test_ru  = ["символ рукопожатия для соглашений", "сцепленные руки деловая встреча", "иконка совместной сделки"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 2. language ───────────────────────────────────────────────────────────────
icon = "language"
st_en = ["dialect", "idiom", "localize", "speech", "translate", "vernacular"]
st_ru = ["диалект", "идиома", "локализация", "речь", "перевод", "просторечие"]
pst_en = [
    "regional dialect spoken in the south",
    "linguistic dialect variation",
    "common English idiom explained",
    "idiom meaning lost in translation",
    "localize the app for Japanese users",
    "localize date formats and currency",
    "text-to-speech feature",
    "freedom of speech in public",
    "translate the page to Spanish",
    "automatic translate button",
    "vernacular slang used in conversation",
    "everyday vernacular language",
]
pst_ru = [
    "региональный диалект на юге страны",
    "лингвистическое диалектное разнообразие",
    "распространённая английская идиома объяснена",
    "смысл идиомы теряется при переводе",
    "локализовать приложение для японских пользователей",
    "локализация форматов дат и валюты",
    "функция преобразования текста в речь",
    "свобода слова на публике",
    "перевести страницу на испанский",
    "кнопка автоматического перевода",
    "просторечный жаргон в разговоре",
    "повседневный разговорный язык",
]
reg_en = [
    "globe with speech bubble representing language",
    "app language selector screen",
    "switch interface language to French",
    "multi-language support for international users",
    "localization settings for different regions",
    "translator tool for foreign text",
    "language learning flashcard app",
    "bilingual dictionary lookup",
    "native language detection",
    "spoken language preference setting",
]
reg_ru = [
    "глобус с речевым пузырём — иконка языка",
    "экран выбора языка приложения",
    "переключить язык интерфейса на французский",
    "поддержка нескольких языков для международных пользователей",
    "настройки локализации для разных регионов",
    "инструмент-переводчик для иностранного текста",
    "приложение для изучения языка с карточками",
    "поиск в двуязычном словаре",
    "определение родного языка",
    "настройка предпочтительного разговорного языка",
]
conv_en = [
    "I need a language icon for the settings screen",
    "add a translate symbol to the content viewer",
    "show a language selector for international users",
    "use the language icon for the localization menu",
]
conv_ru = [
    "нужна иконка языка для экрана настроек",
    "добавить символ перевода в просмотрщик контента",
    "показать выбор языка для международных пользователей",
    "использовать иконку языка для меню локализации",
]
typo_en = [
    "langauge settings",
    "tranlsate text",
    "localise app",
    "speach recognition",
]
typo_ru = [
    "настройки языкa",
    "перевод текст",
    "локализацяи приложения",
    "распознавние речи",
]
bnd_en = [
    "speech bubble for comments and chat messages",
    "globe showing the entire world map",
    "microphone for voice input recording",
    "keyboard for typing text input",
    "chat conversation bubble with text",
    "book open for reading content",
]
bnd_ru = [
    "речевой пузырь для комментариев и сообщений чата",
    "глобус отображающий карту всего мира",
    "микрофон для записи голосового ввода",
    "клавиатура для ввода текста",
    "пузырь диалога чата с текстом",
    "открытая книга для чтения контента",
]
valid_en = ["language selection setting", "translate button for foreign text", "app localization icon"]
valid_ru = ["настройка выбора языка", "кнопка перевода иностранного текста", "иконка локализации приложения"]
test_en  = ["language icon for multilingual app", "speech and translation symbol", "locale switcher icon"]
test_ru  = ["иконка языка для мультиязычного приложения", "символ речи и перевода", "иконка переключателя языка"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 3. lemon ──────────────────────────────────────────────────────────────────
icon = "lemon"
st_en = ["citrus", "fruit", "lemon", "lemonade", "lime", "tart"]
st_ru = ["цитрус", "фрукт", "лимон", "лимонад", "лайм", "кислый"]
pst_en = [
    "citrus fruit full of vitamin C",
    "fresh citrus juice for breakfast",
    "tropical fruit salad bowl",
    "fruit basket with various fruits",
    "fresh lemon slice for garnish",
    "squeeze a lemon for salad dressing",
    "homemade lemonade recipe",
    "cold lemonade on a hot summer day",
    "lime wedge in a cocktail glass",
    "lime juice for guacamole",
    "tart flavor in the dessert",
    "tart lemon curd on toast",
]
pst_ru = [
    "цитрусовый фрукт богатый витамином C",
    "свежий цитрусовый сок на завтрак",
    "тропический фруктовый салат в миске",
    "корзина с разными фруктами",
    "долька лимона для украшения",
    "выжать лимон для заправки салата",
    "домашний рецепт лимонада",
    "холодный лимонад в жаркий летний день",
    "долька лайма в бокале коктейля",
    "сок лайма для гуакамоле",
    "кислый вкус в десерте",
    "кислый лимонный курд на тосте",
]
reg_en = [
    "bright yellow oval citrus fruit",
    "lemon wedge cut in half showing pulp",
    "add lemon to the cooking ingredients list",
    "vitamin C source for immune support",
    "lemon zest for baking recipes",
    "squeeze fresh lemon juice into water",
    "lemon-flavored food or drink item",
    "summer drink with lemon slices",
    "sour citrus fruit for cooking",
    "lemon emoji for fresh or sour content",
]
reg_ru = [
    "ярко-жёлтый овальный цитрусовый фрукт",
    "долька лимона разрезанная пополам с мякотью",
    "добавить лимон в список кулинарных ингредиентов",
    "источник витамина C для иммунитета",
    "лимонная цедра для рецептов выпечки",
    "выжать свежий лимонный сок в воду",
    "еда или напиток со вкусом лимона",
    "летний напиток с дольками лимона",
    "кислый цитрус для приготовления еды",
    "эмодзи лимона для свежего или кислого контента",
]
conv_en = [
    "I need a lemon icon for my recipe app",
    "add a citrus fruit symbol to the beverage section",
    "show a lemon for the flavoring ingredient",
    "use the lemon icon for the sour taste category",
]
conv_ru = [
    "нужна иконка лимона для приложения с рецептами",
    "добавить символ цитруса в раздел напитков",
    "показать лимон для раздела ингредиентов-ароматизаторов",
    "использовать иконку лимона для категории кислого вкуса",
]
typo_en = [
    "lemmon slice",
    "citurs fruit",
    "lemoande drink",
    "limon juice",
]
typo_ru = [
    "ломтик лемона",
    "цитрусовы фрукт",
    "напиток лимонад",
    "сок лимоа",
]
bnd_en = [
    "orange citrus fruit with segments",
    "green lime cut in half on a cutting board",
    "grapefruit halved showing pink flesh",
    "tangerine small orange citrus fruit",
    "apple round red or green fruit",
    "pineapple tropical spiky yellow fruit",
]
bnd_ru = [
    "апельсин цитрус с дольками",
    "зелёный лайм разрезанный пополам на доске",
    "грейпфрут разрезан пополам розовая мякоть",
    "мандарин маленький оранжевый цитрус",
    "яблоко круглый красный или зелёный фрукт",
    "ананас тропический с шипами жёлтый фрукт",
]
valid_en = ["yellow citrus lemon fruit", "fresh lemon slice", "lemon icon for recipes"]
valid_ru = ["жёлтый цитрусовый лимон", "свежая долька лимона", "иконка лимона для рецептов"]
test_en  = ["lemon fruit icon", "sour citrus ingredient", "lemonade symbol"]
test_ru  = ["иконка фрукта лимон", "кислый цитрусовый ингредиент", "символ лимонада"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 4. link ───────────────────────────────────────────────────────────────────
icon = "link"
st_en = ["attach", "attachment", "chain", "connect", "link"]
st_ru = ["прикрепить", "вложение", "цепочка", "соединить", "ссылка"]
pst_en = [
    "attach file to an email message",
    "attach document before sending",
    "email attachment paperclip",
    "open attachment from received message",
    "chain of connected items",
    "metal chain link symbol",
    "connect two accounts together",
    "connect the data sources",
    "share a link to the article",
    "copy the link to clipboard",
]
pst_ru = [
    "прикрепить файл к письму",
    "прикрепить документ перед отправкой",
    "вложение в электронном письме скрепка",
    "открыть вложение из полученного сообщения",
    "цепочка связанных элементов",
    "металлическое звено цепи символ",
    "связать два аккаунта вместе",
    "соединить источники данных",
    "поделиться ссылкой на статью",
    "скопировать ссылку в буфер обмена",
]
reg_en = [
    "chain link icon representing a hyperlink",
    "copy and paste a URL link",
    "share a web page link with friends",
    "clickable hyperlink in a document",
    "broken link indicating a dead page",
    "linked accounts across services",
    "embed a link inside text",
    "shorten a long link with a tool",
    "referral link for sharing rewards",
    "deep link into a specific app screen",
]
reg_ru = [
    "иконка цепного звена представляющая гиперссылку",
    "скопировать и вставить URL-ссылку",
    "поделиться ссылкой на веб-страницу с друзьями",
    "кликабельная гиперссылка в документе",
    "битая ссылка указывающая на недоступную страницу",
    "связанные аккаунты в сервисах",
    "вставить ссылку внутри текста",
    "сократить длинную ссылку с помощью инструмента",
    "реферальная ссылка для получения наград",
    "диплинк к конкретному экрану приложения",
]
conv_en = [
    "I need a link icon for the share button",
    "add a chain link symbol to the URL field",
    "show a link icon next to external references",
    "use the link icon for the connect accounts feature",
]
conv_ru = [
    "нужна иконка ссылки для кнопки поделиться",
    "добавить символ цепи к полю URL",
    "показать иконку ссылки рядом с внешними ссылками",
    "использовать иконку ссылки для функции связки аккаунтов",
]
typo_en = [
    "lnik to website",
    "attch file here",
    "conect two items",
    "hyperlik in text",
]
typo_ru = [
    "сылка на сайт",
    "прикрепит файл",
    "соеденить два элемента",
    "гиперсылка в тексте",
]
bnd_en = [
    "paperclip used to clip documents together",
    "anchor symbol for a fixed position on page",
    "bookmark saving a page for later reading",
    "pin marking a location on a map",
    "share arrow button sending content to others",
    "unlink broken chain indicating disconnection",
]
bnd_ru = [
    "скрепка для скрепления документов вместе",
    "якорь символ фиксированного положения на странице",
    "закладка сохранение страницы для чтения позже",
    "булавка отмечающая местоположение на карте",
    "кнопка поделиться стрелка отправки контента другим",
    "разорванная цепь означающая разъединение",
]
valid_en = ["hyperlink chain icon", "URL link to share", "connect items with a link"]
valid_ru = ["иконка цепи гиперссылки", "URL-ссылка для обмена", "соединить элементы ссылкой"]
test_en  = ["link icon for sharing", "web link chain symbol", "attach and connect icon"]
test_ru  = ["иконка ссылки для обмена", "символ цепи веб-ссылки", "иконка прикрепить и соединить"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 5. mango ──────────────────────────────────────────────────────────────────
icon = "mango"
st_en = ["fruit", "mango", "tropical"]
st_ru = ["фрукт", "манго", "тропический"]
pst_en = [
    "summer fruit bowl with berries",
    "exotic fruit for a smoothie",
    "ripe mango sliced for eating",
    "mango pulp in a recipe",
    "tropical destination vacation",
    "tropical juice blend drink",
]
pst_ru = [
    "летняя миска с фруктами и ягодами",
    "экзотический фрукт для смузи",
    "спелое манго нарезанное для еды",
    "мякоть манго в рецепте",
    "тропическое направление для отпуска",
    "тропический смешанный сок напиток",
]
reg_en = [
    "orange-yellow tropical mango fruit",
    "mango smoothie blended drink",
    "fresh sliced mango in a fruit salad",
    "sweet tropical flavor of mango",
    "mango chutney condiment for Indian food",
    "dried mango snack bag",
    "ripe mango for a tropical dessert",
    "mango sorbet frozen dessert",
    "tropical fruit emoji for summer vibes",
    "add mango to the grocery shopping list",
]
reg_ru = [
    "оранжево-жёлтое тропическое манго",
    "смузи из манго взбитый напиток",
    "свежее нарезанное манго в фруктовом салате",
    "сладкий тропический вкус манго",
    "чатни из манго приправа к индийской еде",
    "пакет сушёного манго закуска",
    "спелое манго для тропического десерта",
    "сорбет из манго замороженный десерт",
    "эмодзи тропического фрукта для летнего настроения",
    "добавить манго в список покупок",
]
conv_en = [
    "I need a mango icon for the tropical flavors section",
    "add a mango symbol to the smoothie builder",
    "show a mango for the exotic fruits category",
    "use the mango icon for the summer menu",
]
conv_ru = [
    "нужна иконка манго для раздела тропических вкусов",
    "добавить символ манго в конструктор смузи",
    "показать манго для категории экзотических фруктов",
    "использовать иконку манго для летнего меню",
]
typo_en = [
    "mago fruit",
    "tropicla fruit",
    "magno smoothie",
    "mnago juice",
]
typo_ru = [
    "фрукт манго",
    "трпический фрукт",
    "смузи из манго",
    "сок маго",
]
bnd_en = [
    "peach soft fuzzy orange stone fruit",
    "papaya tropical orange fruit with seeds",
    "pineapple tropical spiky yellow fruit",
    "banana yellow curved tropical fruit",
    "orange round citrus with segments",
    "coconut tropical round brown hairy fruit",
]
bnd_ru = [
    "персик мягкий пушистый оранжевый косточковый фрукт",
    "папайя тропический оранжевый фрукт с семенами",
    "ананас тропический с шипами жёлтый фрукт",
    "банан жёлтый изогнутый тропический фрукт",
    "апельсин круглый цитрус с дольками",
    "кокос тропический круглый коричневый волосатый фрукт",
]
valid_en = ["tropical mango fruit", "ripe mango icon", "mango for smoothie or juice"]
valid_ru = ["тропическое манго фрукт", "иконка спелого манго", "манго для смузи или сока"]
test_en  = ["mango icon tropical fruit", "sweet mango symbol", "exotic fruit mango"]
test_ru  = ["иконка манго тропический фрукт", "символ сладкого манго", "экзотический фрукт манго"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 6. music ──────────────────────────────────────────────────────────────────
icon = "music"
st_en = ["lyrics", "melody", "music", "musical note", "note", "sing", "sound"]
st_ru = ["текст песни", "мелодия", "музыка", "музыкальная нота", "нота", "петь", "звук"]
pst_en = [
    "song lyrics on screen",
    "display lyrics while playing a track",
    "catchy melody in the background",
    "compose a melody for the intro",
    "background music for the video",
    "play music in the gym",
    "musical note on a staff",
    "multiple musical notes in a sequence",
    "quarter note rest in sheet music",
    "sticky note reminder to practice",
    "sing along with the chorus",
    "karaoke sing mode",
    "ambient sound design",
    "natural sound of rain falling",
]
pst_ru = [
    "текст песни на экране",
    "отображать слова во время воспроизведения трека",
    "запоминающаяся мелодия на фоне",
    "сочинить мелодию для интро",
    "фоновая музыка для видео",
    "включить музыку в спортзале",
    "музыкальная нота на нотном стане",
    "несколько музыкальных нот подряд",
    "четвертная нота в нотах",
    "стикер-напоминание потренироваться",
    "петь вместе с припевом",
    "режим пения в стиле караоке",
    "дизайн звукового оформления",
    "естественный звук падающего дождя",
]
reg_en = [
    "double music note icon for audio content",
    "music player now playing screen",
    "add a song to the playlist",
    "streaming music from a service",
    "background music for a presentation",
    "musical score with notes on a staff",
    "compose music with a notation tool",
    "audio track waveform visualization",
    "music genre selection for radio",
    "instrumental music without lyrics",
]
reg_ru = [
    "иконка двойной музыкальной ноты для аудиоконтента",
    "экран воспроизведения музыкального плеера",
    "добавить песню в плейлист",
    "стриминг музыки из сервиса",
    "фоновая музыка для презентации",
    "музыкальная партитура с нотами на стане",
    "сочинять музыку с помощью инструмента нотации",
    "визуализация волновой формы аудиодорожки",
    "выбор жанра музыки для радио",
    "инструментальная музыка без слов",
]
conv_en = [
    "I need a music icon for the player screen",
    "add a musical note symbol to the audio section",
    "show a music note for the playlist feature",
    "use the music icon for the sound settings",
]
conv_ru = [
    "нужна иконка музыки для экрана плеера",
    "добавить символ музыкальной ноты в аудио раздел",
    "показать музыкальную ноту для функции плейлиста",
    "использовать иконку музыки для настроек звука",
]
typo_en = [
    "muisc player",
    "melodie playing",
    "lyircs display",
    "sounf music",
]
typo_ru = [
    "мзыкальный плеер",
    "мелодяи играет",
    "отображение тексат",
    "зувк музыки",
]
bnd_en = [
    "headphones worn over ears for listening",
    "speaker sound waves for audio output",
    "microphone for recording vocals",
    "radio broadcast with antenna waves",
    "waveform audio track editing",
    "record vinyl disc spinning on turntable",
]
bnd_ru = [
    "наушники надетые на уши для прослушивания",
    "динамик со звуковыми волнами для вывода аудио",
    "микрофон для записи вокала",
    "радио трансляция с антенными волнами",
    "редактирование аудиодорожки в виде волны",
    "виниловая пластинка вращающаяся на проигрывателе",
]
valid_en = ["music note icon for audio", "play music symbol", "musical sound icon"]
valid_ru = ["иконка музыкальной ноты для аудио", "символ воспроизведения музыки", "иконка музыкального звука"]
test_en  = ["music icon for player", "melody and song symbol", "audio music note"]
test_ru  = ["иконка музыки для плеера", "символ мелодии и песни", "аудио музыкальная нота"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 7. newspaper ──────────────────────────────────────────────────────────────
icon = "newspaper"
st_en = ["article", "editorial", "headline", "journal", "journalism", "news", "newsletter", "newspaper", "paper", "press"]
st_ru = ["статья", "передовица", "заголовок", "журнал", "журналистика", "новости", "рассылка", "газета", "бумага", "пресса"]
pst_en = [
    "feature article in a magazine",
    "long-form article for the web",
    "newspaper editorial opinion piece",
    "editorial board decision on policy",
    "front page headline breaking news",
    "bold headline announcing an election",
    "science journal research paper",
    "academic journal subscription",
    "citizen journalism blog post",
    "investigative journalism exposé",
    "daily news briefing",
    "breaking news alert notification",
    "company newsletter sent weekly",
    "subscribe to the email newsletter",
    "newspaper folded on a doorstep",
    "digital newspaper on a tablet",
    "office paper printer output",
    "paper document ready for review",
    "press conference announcement",
    "freedom of the press article",
]
pst_ru = [
    "журнальная статья-очерк",
    "длинная статья для веба",
    "передовая редакционная колонка мнение",
    "решение редколлегии по политике",
    "заголовок первой полосы экстренные новости",
    "жирный заголовок объявляющий о выборах",
    "научный журнал исследовательская статья",
    "подписка на академический журнал",
    "блог-пост гражданской журналистики",
    "журналистское расследование разоблачение",
    "ежедневный обзор новостей",
    "уведомление о срочных новостях",
    "еженедельная корпоративная рассылка",
    "подписаться на email-рассылку",
    "газета сложенная у порога",
    "цифровая газета на планшете",
    "офисная бумага выходящая из принтера",
    "бумажный документ готовый к проверке",
    "пресс-конференция объявление",
    "свобода прессы статья",
]
reg_en = [
    "folded newspaper with headlines visible",
    "daily newspaper delivery in the morning",
    "digital news feed on a smartphone",
    "breaking news banner at top of screen",
    "news aggregator app with articles",
    "sports section in the newspaper",
    "classified ads in a local paper",
    "newspaper archive from decades ago",
    "read the morning newspaper with coffee",
    "tabloid newspaper front page photo",
]
reg_ru = [
    "сложенная газета с видимыми заголовками",
    "утренняя доставка ежедневной газеты",
    "цифровая лента новостей на смартфоне",
    "баннер срочных новостей вверху экрана",
    "агрегатор новостей приложение со статьями",
    "спортивный раздел в газете",
    "объявления в местной газете",
    "архив газет за несколько десятилетий",
    "читать утреннюю газету за кофе",
    "первая страница таблоида с фотографией",
]
conv_en = [
    "I need a newspaper icon for the news feed",
    "add a news symbol to the articles section",
    "show a newspaper for the press releases",
    "use the newspaper icon for the media section",
]
conv_ru = [
    "нужна иконка газеты для ленты новостей",
    "добавить символ новостей в раздел статей",
    "показать газету для пресс-релизов",
    "использовать иконку газеты для медиа раздела",
]
typo_en = [
    "newpaper article",
    "headlien news",
    "jounalism report",
    "newletter update",
]
typo_ru = [
    "статя газеты",
    "заголовак новостей",
    "журналстика репортаж",
    "рассылка обновление",
]
bnd_en = [
    "book with pages open for reading",
    "document text file with lines of content",
    "magazine glossy cover with a photo",
    "blog post web page with text",
    "notification bell for alerts",
    "envelope email message unopened",
]
bnd_ru = [
    "книга с открытыми страницами для чтения",
    "текстовый документ с строками контента",
    "глянцевая обложка журнала с фотографией",
    "публикация в блоге веб-страница с текстом",
    "колокол уведомления для оповещений",
    "конверт непрочитанное электронное письмо",
]
valid_en = ["newspaper with headlines", "news article icon", "press and journalism symbol"]
valid_ru = ["газета с заголовками", "иконка новостной статьи", "символ прессы и журналистики"]
test_en  = ["newspaper icon for news feed", "daily paper headlines", "journalism news icon"]
test_ru  = ["иконка газеты для ленты новостей", "заголовки ежедневной газеты", "иконка журналистики новостей"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 8. nose ───────────────────────────────────────────────────────────────────
icon = "nose"
st_en = ["face", "nasal", "nostril", "smell", "sniff", "snout"]
st_ru = ["лицо", "носовой", "ноздря", "запах", "нюхать", "морда"]
pst_en = [
    "face recognition scan feature",
    "happy face emoji with big nose",
    "nasal congestion cold symptom",
    "nasal spray medication bottle",
    "nostril piercing jewelry",
    "clear nostril blocked nose",
    "detect a bad smell in the air",
    "pleasant smell of fresh flowers",
    "dog sniffing to find a scent",
    "sniff test for allergies",
    "pig snout cartoon character",
    "animal snout shape in a drawing",
]
pst_ru = [
    "функция сканирования распознавания лица",
    "эмодзи счастливого лица с большим носом",
    "заложенность носа симптом простуды",
    "флакон назального спрея лекарство",
    "пирсинг ноздри украшение",
    "прочистить заложенную ноздрю",
    "почувствовать неприятный запах в воздухе",
    "приятный аромат свежих цветов",
    "собака нюхает чтобы найти запах",
    "тест на нюх для аллергии",
    "пятачок свиньи мультяшный персонаж",
    "форма морды животного в рисунке",
]
reg_en = [
    "nose shape for a facial anatomy diagram",
    "scent detection or smell-related feature",
    "allergy symptom runny nose icon",
    "body part selector nose region",
    "nose job cosmetic surgery category",
    "aroma or fragrance symbol",
    "wine tasting nose for aroma assessment",
    "sniffing dog police tracking icon",
    "cartoon nose for an avatar creator",
    "nasal breathing exercise reminder",
]
reg_ru = [
    "форма носа для диаграммы анатомии лица",
    "обнаружение запаха или функция связанная с обонянием",
    "иконка симптома аллергии насморк",
    "выбор части тела область носа",
    "категория косметической хирургии ринопластика",
    "символ аромата или парфюма",
    "нос для оценки аромата при дегустации вина",
    "собака-ищейка полицейское отслеживание иконка",
    "мультяшный нос для создателя аватара",
    "напоминание о носовом дыхательном упражнении",
]
conv_en = [
    "I need a nose icon for the face anatomy screen",
    "add a smell symbol to the fragrance section",
    "show a nose for the allergy symptom tracker",
    "use the nose icon for the scent detection feature",
]
conv_ru = [
    "нужна иконка носа для экрана анатомии лица",
    "добавить символ запаха в раздел парфюма",
    "показать нос для трекера симптомов аллергии",
    "использовать иконку носа для функции обнаружения запаха",
]
typo_en = [
    "noze smell",
    "nasel spray",
    "sniif detect",
    "nostirl piercing",
]
typo_ru = [
    "нос запах",
    "назальны спрей",
    "нюхать обнаружить",
    "ноздря пирсинг",
]
bnd_en = [
    "mouth with lips for speaking or eating",
    "ear for listening or audio settings",
    "eye for vision or camera focus",
    "face emoji with full features smiling",
    "face with surgical mask covering nose and mouth",
    "finger pointing upward gesture",
]
bnd_ru = [
    "рот с губами для разговора или еды",
    "ухо для прослушивания или настроек аудио",
    "глаз для зрения или фокуса камеры",
    "эмодзи лица с улыбающимися чертами",
    "лицо в медицинской маске закрывающей нос и рот",
    "палец указывающий вверх жест",
]
valid_en = ["nose facial feature icon", "smell detection nose", "nasal anatomy symbol"]
valid_ru = ["иконка носа черты лица", "нос для обнаружения запаха", "символ назальной анатомии"]
test_en  = ["nose icon for face selector", "sniff and smell symbol", "nasal feature icon"]
test_ru  = ["иконка носа для выбора черт лица", "символ нюхать и запах", "иконка носового признака"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 9. note ───────────────────────────────────────────────────────────────────
icon = "note"
st_en = ["memo", "sticky note"]
st_ru = ["памятная записка", "стикер"]
pst_en = [
    "memo to colleagues about the meeting",
    "quick memo to self before forgetting",
    "sticky note on the fridge",
    "leave a sticky note as a reminder",
]
pst_ru = [
    "памятная записка коллегам о встрече",
    "быстрая записка себе чтобы не забыть",
    "стикер на холодильнике",
    "оставить стикер как напоминание",
]
reg_en = [
    "blank note for jotting down thoughts",
    "small note pinned to a bulletin board",
    "digital sticky note on the desktop",
    "leave a note for a coworker",
    "note with a quick to-do item",
    "reminder note stuck to a monitor",
    "empty note ready to write on",
    "personal note in a daily journal",
    "note-taking during a phone call",
    "sticky note color-coded for tasks",
]
reg_ru = [
    "чистая записка для записи мыслей",
    "маленькая записка приколотая к доске объявлений",
    "цифровой стикер на рабочем столе",
    "оставить записку коллеге",
    "записка с быстрым пунктом задачи",
    "напоминание приклеенное к монитору",
    "пустая записка готова для записи",
    "личная заметка в ежедневном журнале",
    "делать заметки во время телефонного звонка",
    "цветной стикер для задач",
]
conv_en = [
    "I need a note icon for the reminders screen",
    "add a sticky note symbol to the task list",
    "show a blank note for the memo feature",
    "use the note icon for quick annotations",
]
conv_ru = [
    "нужна иконка записки для экрана напоминаний",
    "добавить символ стикера в список задач",
    "показать чистую записку для функции памятки",
    "использовать иконку записки для быстрых аннотаций",
]
typo_en = [
    "stkcy note reminder",
    "emtpy note page",
    "quik memo write",
    "notte board",
]
typo_ru = [
    "стикрер напоминание",
    "пустая заметкa",
    "быстрая запискa",
    "доска заметко",
]
bnd_en = [
    "notebook with lined pages for journaling",
    "document text file with formatted content",
    "musical note for audio and sound",
    "clipboard with checklist for tasks",
    "sticky note with pin at top",
    "notepad spiral-bound for writing",
]
bnd_ru = [
    "блокнот с линованными страницами для журнала",
    "текстовый файл с форматированным контентом",
    "музыкальная нота для аудио и звука",
    "буфер обмена с контрольным списком для задач",
    "стикер с булавкой сверху",
    "спиральный блокнот для письма",
]
valid_en = ["blank sticky note for reminders", "quick note memo icon", "empty note to write on"]
valid_ru = ["чистый стикер для напоминаний", "иконка быстрой памятной записки", "пустая записка для написания"]
test_en  = ["note icon for memo feature", "sticky note reminder symbol", "blank note page icon"]
test_ru  = ["иконка записки для функции памятки", "символ стикера-напоминания", "иконка чистой страницы записки"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 10. page ──────────────────────────────────────────────────────────────────
icon = "page"
st_en = ["cv", "document", "empty", "file", "new", "pdf", "resume"]
st_ru = ["резюме", "документ", "пустой", "файл", "новый", "PDF", "резюме"]
pst_en = [
    "professional CV sent to hiring manager",
    "update the CV with recent experience",
    "sign a legal document",
    "document storage and retrieval",
    "blank empty canvas to start fresh",
    "empty template waiting to be filled",
    "open a local file from disk",
    "file manager folder navigation",
    "create a new document from scratch",
    "new page added to the project",
    "export to PDF format",
    "view PDF attachment in viewer",
    "upload a resume for the job application",
    "tailor the resume for the position",
]
pst_ru = [
    "профессиональное резюме отправлено менеджеру по найму",
    "обновить резюме с последним опытом",
    "подписать юридический документ",
    "хранение и поиск документов",
    "чистый пустой холст для нового начала",
    "пустой шаблон ожидающий заполнения",
    "открыть локальный файл с диска",
    "навигация по папкам файлового менеджера",
    "создать новый документ с нуля",
    "новая страница добавлена в проект",
    "экспортировать в формат PDF",
    "просмотреть вложение PDF в просмотрщике",
    "загрузить резюме для заявки на работу",
    "адаптировать резюме под должность",
]
reg_en = [
    "blank document page with folded corner",
    "single page of a text document",
    "resume page with name and experience",
    "PDF file icon for attachments",
    "new empty file ready to edit",
    "page break in a word processor",
    "contract page requiring a signature",
    "printable single-page flyer",
    "document preview before printing",
    "insert a new page into a report",
]
reg_ru = [
    "чистая страница документа с загнутым уголком",
    "одна страница текстового документа",
    "страница резюме с именем и опытом",
    "иконка PDF-файла для вложений",
    "новый пустой файл готов к редактированию",
    "разрыв страницы в текстовом редакторе",
    "страница контракта требующая подписи",
    "одностраничный флаер для печати",
    "предварительный просмотр документа перед печатью",
    "вставить новую страницу в отчёт",
]
conv_en = [
    "I need a page icon for the document viewer",
    "add a file symbol to the uploads section",
    "show a blank page for the new document button",
    "use the page icon for the resume builder",
]
conv_ru = [
    "нужна иконка страницы для просмотра документов",
    "добавить символ файла в раздел загрузок",
    "показать пустую страницу для кнопки нового документа",
    "использовать иконку страницы для конструктора резюме",
]
typo_en = [
    "documnet page",
    "pge layout",
    "emtpy file",
    "pdff export",
]
typo_ru = [
    "страниц документа",
    "макет страницe",
    "пустой файлл",
    "эксопрт pdf",
]
bnd_en = [
    "notebook multiple pages bound together",
    "folder containing multiple files",
    "clipboard holding a stack of papers",
    "book many pages bound in a cover",
    "paper stack of multiple sheets",
    "spreadsheet table with rows and columns",
]
bnd_ru = [
    "блокнот несколько страниц переплетённых вместе",
    "папка содержащая несколько файлов",
    "буфер обмена со стопкой бумаг",
    "книга много страниц переплетённых в обложку",
    "стопка бумаг из нескольких листов",
    "таблица с рядами и столбцами",
]
valid_en = ["blank document page icon", "single page file symbol", "PDF page icon"]
valid_ru = ["иконка чистой страницы документа", "символ файла одной страницы", "иконка страницы PDF"]
test_en  = ["page icon for document viewer", "empty file page symbol", "resume or CV page icon"]
test_ru  = ["иконка страницы для просмотра документов", "символ пустой страницы файла", "иконка страницы резюме"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 11. panties ───────────────────────────────────────────────────────────────
icon = "panties"
st_en = ["bikini", "swim", "two-piece", "underclothes", "underclothing", "underwear"]
st_ru = ["бикини", "купальный", "двойка купальник", "нижнее бельё", "нижняя одежда", "нижнее бельё"]
pst_en = [
    "bikini swimsuit for the beach",
    "string bikini summer style",
    "swim practice at the pool",
    "swim gear for open water",
    "two-piece swimsuit for summer",
    "two-piece outfit for a beach vacation",
    "underclothes drawer organization",
    "pack underclothes for the trip",
    "cotton underclothing comfort wear",
    "underclothing size guide",
    "women's underwear category",
    "pack underwear for a weekend trip",
]
pst_ru = [
    "купальник бикини для пляжа",
    "стринги-бикини летний стиль",
    "тренировка по плаванию в бассейне",
    "снаряжение для плавания на открытой воде",
    "купальник-двойка для лета",
    "наряд из двух частей для пляжного отдыха",
    "организация ящика с нижним бельём",
    "упаковать нижнее бельё для поездки",
    "хлопковое нижнее бельё для комфорта",
    "руководство по размерам нижней одежды",
    "категория женского нижнего белья",
    "упаковать нижнее бельё для поездки на выходные",
]
reg_en = [
    "women's underwear or panties clothing item",
    "laundry sorting by clothing type",
    "lingerie drawer icon for wardrobe app",
    "intimate apparel shopping category",
    "underwear size chart in a store",
    "pack underwear in a suitcase checklist",
    "swimwear bottom for the beach",
    "beach vacation packing list item",
    "clothing icon for the underwear category",
    "body-hugging underwear garment icon",
]
reg_ru = [
    "женское нижнее бельё или трусики предмет одежды",
    "сортировка белья по типу одежды",
    "иконка ящика с нижним бельём для приложения гардероба",
    "категория покупок нижнего белья",
    "таблица размеров нижнего белья в магазине",
    "список упаковки нижнего белья в чемодан",
    "нижняя часть купальника для пляжа",
    "пункт списка упаковки для пляжного отпуска",
    "иконка одежды для категории нижнего белья",
    "плотно облегающий предмет нижнего белья иконка",
]
conv_en = [
    "I need a panties icon for the laundry sorting feature",
    "add an underwear symbol to the clothing category",
    "show a panties icon for the lingerie section",
    "use the underwear icon for the packing checklist",
]
conv_ru = [
    "нужна иконка трусиков для функции сортировки белья",
    "добавить символ нижнего белья в категорию одежды",
    "показать иконку трусиков для раздела нижнего белья",
    "использовать иконку нижнего белья для контрольного списка упаковки",
]
typo_en = [
    "panteis underwear",
    "biikni swimsuit",
    "undrwear drawer",
    "lingerei category",
]
typo_ru = [
    "трусики нижнее белье",
    "купальни бикини",
    "ящик с нижниим бельём",
    "категория нижнего белтя",
]
bnd_en = [
    "pants trousers full-length leg garment",
    "bra top piece of lingerie set",
    "swimsuit one-piece for the pool",
    "shorts knee-length casual pants",
    "socks worn on feet under shoes",
    "skirt lower body garment for women",
]
bnd_ru = [
    "штаны брюки одежда полной длины для ног",
    "бюстгальтер верхняя часть комплекта нижнего белья",
    "цельный купальник для бассейна",
    "шорты повседневные штаны до колена",
    "носки надеваемые на ноги под обувь",
    "юбка одежда для нижней части тела",
]
valid_en = ["panties underwear clothing icon", "women's underwear symbol", "intimate apparel icon"]
valid_ru = ["иконка одежды трусики нижнее бельё", "символ женского нижнего белья", "иконка нижнего белья"]
test_en  = ["panties icon for clothing app", "underwear category symbol", "swimwear bottom icon"]
test_ru  = ["иконка трусиков для приложения одежды", "символ категории нижнего белья", "иконка низа купальника"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 12. pants ─────────────────────────────────────────────────────────────────
icon = "pants"
st_en = ["jeans", "legs", "pants", "pockets", "slacks"]
st_ru = ["джинсы", "ноги", "брюки", "карманы", "слаксы"]
pst_en = [
    "blue denim jeans casual outfit",
    "ripped jeans fashion trend",
    "cross your legs while sitting",
    "leg measurements for tailoring",
    "fold your pants neatly",
    "hang pants in the closet",
    "pants with deep side pockets",
    "check the pockets before washing",
    "dress slacks for office wear",
    "pressed slacks business attire",
]
pst_ru = [
    "синие джинсы из денима повседневный наряд",
    "рваные джинсы модный тренд",
    "скрестить ноги во время сидения",
    "замеры ног для портного",
    "аккуратно сложить брюки",
    "повесить брюки в шкафу",
    "брюки с глубокими боковыми карманами",
    "проверить карманы перед стиркой",
    "нарядные слаксы для офисной одежды",
    "отглаженные слаксы деловой наряд",
]
reg_en = [
    "pair of trousers clothing icon",
    "full-length pants for men or women",
    "wardrobe app pants category",
    "laundry pile with pants and shirts",
    "outfit builder pants selection",
    "cargo pants with many pockets",
    "dress pants for formal occasions",
    "yoga pants stretchy activewear",
    "pack a pair of pants for a trip",
    "iron pants before the interview",
]
reg_ru = [
    "иконка одежды пара брюк",
    "брюки полной длины для мужчин или женщин",
    "категория брюк в приложении гардероба",
    "куча белья брюки и рубашки",
    "конструктор образов выбор брюк",
    "карго-брюки с множеством карманов",
    "классические брюки для официальных мероприятий",
    "штаны для йоги эластичная спортивная одежда",
    "упаковать пару брюк для поездки",
    "погладить брюки перед собеседованием",
]
conv_en = [
    "I need a pants icon for the clothing selector",
    "add a trousers symbol to the wardrobe app",
    "show a pants icon for the outfit builder",
    "use the pants icon for the bottoms category",
]
conv_ru = [
    "нужна иконка брюк для выбора одежды",
    "добавить символ брюк в приложение гардероба",
    "показать иконку брюк для конструктора образов",
    "использовать иконку брюк для категории низа",
]
typo_en = [
    "pnats wardrobe",
    "jeens outfit",
    "trosers clothing",
    "slakcs dress code",
]
typo_ru = [
    "брюкки гардероб",
    "джинсы наряд",
    "брюкки одежда",
    "слаксы дресс-код",
]
bnd_en = [
    "shorts cropped pants above the knee",
    "skirt flowing lower body garment",
    "jeans specifically with rivets and denim texture",
    "leggings tight stretchy full-leg wear",
    "panties underwear intimate garment",
    "socks pulled up on the ankles",
]
bnd_ru = [
    "шорты укороченные брюки выше колена",
    "юбка струящаяся одежда для нижней части тела",
    "джинсы с заклёпками и текстурой денима",
    "леггинсы плотные эластичные на всю длину ног",
    "трусики нижнее бельё интимный предмет одежды",
    "носки подтянутые на лодыжках",
]
valid_en = ["pants trousers clothing icon", "full-length pants symbol", "wardrobe pants category"]
valid_ru = ["иконка одежды брюки", "символ брюк полной длины", "категория брюк гардероба"]
test_en  = ["pants icon for clothing app", "trousers wardrobe symbol", "jeans or slacks icon"]
test_ru  = ["иконка брюк для приложения одежды", "символ брюк гардероба", "иконка джинсов или слаксов"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── 13. pencil ────────────────────────────────────────────────────────────────
icon = "pencil"
st_en = ["design", "draw", "edit", "lead", "maintenance", "modify", "pencil", "update", "write"]
st_ru = ["дизайн", "рисовать", "редактировать", "грифель", "обслуживание", "изменить", "карандаш", "обновить", "писать"]
pst_en = [
    "graphic design tool set",
    "design the app interface layout",
    "draw a sketch on paper",
    "draw a diagram to explain the process",
    "edit the text in the document",
    "tap to edit this field",
    "lead pencil for writing notes",
    "wooden pencil with an eraser tip",
    "scheduled maintenance reminder",
    "log maintenance activity",
    "modify the settings configuration",
    "modify the user profile details",
    "classic yellow pencil icon",
    "sharpen a pencil before drawing",
    "update the record in the database",
    "update the app to the latest version",
    "handwrite a note with a pencil",
    "write the address on the envelope",
]
pst_ru = [
    "набор инструментов для графического дизайна",
    "разработать макет интерфейса приложения",
    "нарисовать эскиз на бумаге",
    "нарисовать схему для объяснения процесса",
    "отредактировать текст в документе",
    "нажмите чтобы изменить это поле",
    "карандаш с грифелем для записей",
    "деревянный карандаш с ластиком",
    "напоминание о плановом техобслуживании",
    "записать сервисные работы",
    "изменить конфигурацию настроек",
    "изменить данные профиля пользователя",
    "иконка классического жёлтого карандаша",
    "заточить карандаш перед рисованием",
    "обновить запись в базе данных",
    "обновить приложение до последней версии",
    "написать заметку от руки карандашом",
    "написать адрес на конверте",
]
reg_en = [
    "yellow wooden pencil with eraser on top",
    "pencil icon for editing or writing mode",
    "tap the pencil to edit your profile",
    "sketch tool in a drawing application",
    "hand-draw a signature with a pencil",
    "pencil underlining important text",
    "pencil and ruler design tools together",
    "fill out a form with a pencil",
    "architect drafting plans with a pencil",
    "crossword puzzle pencil and eraser",
]
reg_ru = [
    "жёлтый деревянный карандаш с ластиком сверху",
    "иконка карандаша для режима редактирования или письма",
    "нажмите на карандаш чтобы изменить профиль",
    "инструмент рисования в приложении для набросков",
    "нарисовать подпись от руки карандашом",
    "карандаш подчёркивающий важный текст",
    "карандаш и линейка инструменты дизайна вместе",
    "заполнить форму карандашом",
    "архитектор чертит планы карандашом",
    "карандаш и ластик для кроссворда",
]
conv_en = [
    "I need a pencil icon for the edit button",
    "add a pencil symbol to the write note feature",
    "show a pencil for the inline editing mode",
    "use the pencil icon for the modify action",
]
conv_ru = [
    "нужна иконка карандаша для кнопки редактирования",
    "добавить символ карандаша для функции написания заметки",
    "показать карандаш для режима встроенного редактирования",
    "использовать иконку карандаша для действия изменения",
]
typo_en = [
    "pencli draw",
    "eidt button",
    "wroite note",
    "pencl sketch",
]
typo_ru = [
    "карандш рисовать",
    "кнопка редактрования",
    "написать заметуку",
    "набросок карандашм",
]
bnd_en = [
    "pen ballpoint or fountain for writing",
    "paintbrush for applying color on canvas",
    "marker thick tip for highlighting",
    "eraser removing pencil marks",
    "ruler for measuring straight lines",
    "crayon wax coloring stick for kids",
]
bnd_ru = [
    "шариковая или перьевая ручка для письма",
    "кисть для нанесения краски на холст",
    "маркер толстый наконечник для выделения",
    "ластик стирающий следы карандаша",
    "линейка для измерения прямых линий",
    "восковой мелок для детского рисования",
]
valid_en = ["pencil icon for editing", "draw and write symbol", "pencil edit button icon"]
valid_ru = ["иконка карандаша для редактирования", "символ рисования и письма", "иконка кнопки редактирования карандашом"]
test_en  = ["pencil icon for write mode", "edit with pencil symbol", "drawing pencil icon"]
test_ru  = ["иконка карандаша для режима письма", "символ редактирования карандашом", "иконка карандаша для рисования"]
save_icon(icon, st_en, st_ru, pst_en, pst_ru, reg_en, reg_ru, conv_en, conv_ru, typo_en, typo_ru, bnd_en, bnd_ru, valid_en, valid_ru, test_en, test_ru)

# ── Update processed_icons.txt ────────────────────────────────────────────────
new_icons = [
    "handshake", "language", "lemon", "link", "mango",
    "music", "newspaper", "nose", "note", "page",
    "panties", "pants", "pencil",
]
with open("processed_icons.txt", "a", encoding="utf-8") as f:
    start = 516
    for i, name in enumerate(new_icons):
        f.write(f"{start + i:03d}. {name}\n")

print("\nDone. processed_icons.txt updated (516–528).")
