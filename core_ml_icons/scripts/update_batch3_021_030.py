"""
Batch 3 (icons 021-030): Add second phrase per search term for each icon.
Icons: bat, bath, battery-bolt, bed-bunk, bell-ring, bell-school, bells, bench-tree, bicycle, billboard
"""

import json
import csv
from pathlib import Path

base = Path("/Users/idjugostran/Projects/icons-ai/core_ml_icons")


def append_rows(filepath, rows, label):
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        for text in rows:
            w.writerow([text, label])


def count_data_rows(filepath):
    """Count data rows (excluding header) in a CSV file."""
    with open(filepath, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1


def update_icon(icon, new_pst_en, new_pst_ru):
    icon_dir = base / "icons" / icon

    # Load existing log
    with open(icon_dir / "icon_log.json", "r", encoding="utf-8") as f:
        log = json.load(f)

    # Sanity check: one new phrase per search term
    n_terms = len(log["categories"]["search_terms"]["en"])
    assert len(new_pst_en) == n_terms, (
        f"{icon}: expected {n_terms} EN phrases, got {len(new_pst_en)}"
    )
    assert len(new_pst_ru) == n_terms, (
        f"{icon}: expected {n_terms} RU phrases, got {len(new_pst_ru)}"
    )

    # Append new rows to train CSVs
    append_rows(icon_dir / "train_en.csv", new_pst_en, icon)
    append_rows(icon_dir / "train_ru.csv", new_pst_ru, icon)

    # Update icon_log.json
    log["categories"]["phrase_per_search_term"]["en"].extend(new_pst_en)
    log["categories"]["phrase_per_search_term"]["ru"].extend(new_pst_ru)

    # Update row counts
    log["rows"]["train_en"] = count_data_rows(icon_dir / "train_en.csv")

    with open(icon_dir / "icon_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"Updated {icon}: +{len(new_pst_en)} EN rows, +{len(new_pst_ru)} RU rows  "
          f"(train_en now {log['rows']['train_en']} rows)")


# ─── 021: bat ────────────────────────────────────────────────────────────────
# Search terms: animal, batman, bruce wayne, flying, gotham, halloween, mammal, vampire, wings
update_icon(
    icon="bat",
    new_pst_en=[
        "rescue the injured animal",           # animal
        "batman movie marathon tonight",        # batman
        "dress up as bruce wayne",              # bruce wayne
        "see bats flying overhead",             # flying
        "gotham inspired halloween setup",      # gotham
        "carve pumpkins for halloween",         # halloween
        "learn about nocturnal mammals",        # mammal
        "vampire costume for the party",        # vampire
        "bat wings craft project",              # wings
    ],
    new_pst_ru=[
        "спасти раненое животное",
        "марафон фильмов о Бэтмене сегодня",
        "нарядиться Брюсом Уэйном",
        "увидеть летучих мышей в полёте",
        "хэллоуинское оформление в стиле Готэма",
        "вырезать тыквы к хэллоуину",
        "узнать о ночных млекопитающих",
        "костюм вампира для вечеринки",
        "поделка с крыльями летучей мыши",
    ],
)

# ─── 022: bath ───────────────────────────────────────────────────────────────
# Search terms: bath, bathtub, clean, shower, tub, wash
update_icon(
    icon="bath",
    new_pst_en=[
        "relax in a warm bath tonight",         # bath
        "scrub and rinse the bathtub",          # bathtub
        "get everything clean before guests",   # clean
        "quick shower before the meeting",      # shower
        "fill the tub for the baby",            # tub
        "wash hands before dinner",             # wash
    ],
    new_pst_ru=[
        "расслабиться в тёплой ванне вечером",
        "отдраить и ополоснуть ванну",
        "навести чистоту перед приходом гостей",
        "быстрый душ перед встречей",
        "наполнить ванну для малыша",
        "помыть руки перед ужином",
    ],
)

# ─── 023: battery-bolt ───────────────────────────────────────────────────────
# Search terms: charge, power, status
update_icon(
    icon="battery-bolt",
    new_pst_en=[
        "plug in the tablet to charge",         # charge
        "save power before the flight",         # power
        "battery status in the settings menu",  # status
    ],
    new_pst_ru=[
        "подключить планшет к зарядке",
        "экономить энергию перед полётом",
        "статус батареи в меню настроек",
    ],
)

# ─── 024: bed-bunk ───────────────────────────────────────────────────────────
# Search terms: lodging, mattress, rest, siblings, sleep, sleepover, travel
update_icon(
    icon="bed-bunk",
    new_pst_en=[
        "find affordable lodging nearby",       # lodging
        "flip the mattress this weekend",       # mattress
        "rest before the big game",             # rest
        "siblings take turns on the top bunk",  # siblings
        "set a consistent sleep schedule",      # sleep
        "plan the sleepover menu and games",    # sleepover
        "hostel bunk beds for the road trip",   # travel
    ],
    new_pst_ru=[
        "найти доступное жильё поблизости",
        "перевернуть матрас в эти выходные",
        "отдохнуть перед важным матчем",
        "братья и сёстры по очереди спят наверху",
        "установить стабильный режим сна",
        "спланировать меню и игры для ночёвки",
        "двухъярусные кровати в хостеле для поездки",
    ],
)

# ─── 025: bell-ring ──────────────────────────────────────────────────────────
# Search terms: Ringing Bell, alarm, alert, chime, notification, reminder, request
update_icon(
    icon="bell-ring",
    new_pst_en=[
        "hear the bell ringing downstairs",     # Ringing Bell
        "alarm goes off at 6am",                # alarm
        "get an alert when order ships",        # alert
        "gentle chime at the hour",             # chime
        "check app notifications now",          # notification
        "reminder to call the dentist",         # reminder
        "ring the bell at the front desk",      # request
    ],
    new_pst_ru=[
        "услышать звонящий колокол внизу",
        "будильник срабатывает в 6 утра",
        "получить оповещение об отправке заказа",
        "мягкий перезвон в начале часа",
        "проверить уведомления приложения",
        "напомнить позвонить стоматологу",
        "позвонить в звонок на стойке регистрации",
    ],
)

# ─── 026: bell-school ────────────────────────────────────────────────────────
# Search terms: alert, chime, class, notification, reminder
update_icon(
    icon="bell-school",
    new_pst_en=[
        "send an alert to all students",        # alert
        "afternoon chime signals lunch break",  # chime
        "get to class on time today",           # class
        "turn on school app notifications",     # notification
        "set a reminder for the exam",          # reminder
    ],
    new_pst_ru=[
        "разослать оповещение всем ученикам",
        "дневной перезвон сигнализирует об обеде",
        "прийти на урок вовремя сегодня",
        "включить уведомления школьного приложения",
        "поставить напоминание об экзамене",
    ],
)

# ─── 027: bells ──────────────────────────────────────────────────────────────
# Search terms: alert, christmas, holiday, notification, reminder, request, xmas
update_icon(
    icon="bells",
    new_pst_en=[
        "ring the bells to get attention",      # alert
        "hang christmas bells on the wreath",   # christmas
        "pick up holiday bells from the store", # holiday
        "enable bells notification sound",      # notification
        "set a bells reminder for the party",   # reminder
        "ring bells at the ceremony",           # request
        "decorate the tree with xmas bells",    # xmas
    ],
    new_pst_ru=[
        "позвонить в колокольчики чтобы привлечь внимание",
        "повесить рождественские колокольчики на венок",
        "купить праздничные колокольчики в магазине",
        "включить звук уведомления с колокольчиком",
        "поставить напоминание с колокольчиком на вечеринку",
        "звонить в колокола на церемонии",
        "украсить ёлку рождественскими колокольчиками",
    ],
)

# ─── 028: bench-tree ─────────────────────────────────────────────────────────
# Search terms: bench, outside, park, picnic, tree
update_icon(
    icon="bench-tree",
    new_pst_en=[
        "paint the old garden bench",           # bench
        "eat lunch outside today",              # outside
        "meet at the park entrance",            # park
        "pack a picnic basket for Sunday",      # picnic
        "water the newly planted tree",         # tree
    ],
    new_pst_ru=[
        "покрасить старую садовую скамейку",
        "пообедать на улице сегодня",
        "встретиться у входа в парк",
        "собрать корзину для пикника в воскресенье",
        "полить только что посаженное дерево",
    ],
)

# ─── 029: bicycle ────────────────────────────────────────────────────────────
# Search terms: bicycle, bike, gears, pedal, transportation, vehicle
update_icon(
    icon="bicycle",
    new_pst_en=[
        "lock the bicycle at the station",      # bicycle
        "plan a long bike tour this summer",    # bike
        "adjust the gears before the ride",     # gears
        "teach the kids to pedal",              # pedal
        "cycling is the fastest transportation downtown",  # transportation
        "insure the vehicle before spring",     # vehicle
    ],
    new_pst_ru=[
        "пристегнуть велосипед на станции",
        "спланировать длительный велотур этим летом",
        "отрегулировать передачи перед поездкой",
        "научить детей крутить педали",
        "велосипед — самый быстрый транспорт в центре",
        "застраховать транспортное средство до весны",
    ],
)

# ─── 030: billboard ──────────────────────────────────────────────────────────
# Search terms: advertising, promotion, sign, signboard, slogan poster
update_icon(
    icon="billboard",
    new_pst_en=[
        "review the advertising budget",        # advertising
        "launch the spring promotion",          # promotion
        "hang the sign above the entrance",     # sign
        "replace the faded signboard outside",  # signboard
        "brainstorm a catchy slogan for the poster",  # slogan poster
    ],
    new_pst_ru=[
        "проверить рекламный бюджет",
        "запустить весеннюю акцию",
        "повесить знак над входом",
        "заменить выцветшую вывеску снаружи",
        "придумать запоминающийся слоган для плаката",
    ],
)

print("\nAll 10 icons updated successfully.")
