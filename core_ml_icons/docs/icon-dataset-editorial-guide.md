# Icon Dataset Editorial Guide

## Purpose

This repository stores bilingual icon-search datasets for Core ML text classification.
The target is practical quality on real user queries while keeping English and Russian
datasets synchronized.

The primary target is task-title search: a user writes a task name or a short task-like
intent, and the model should suggest the icon that best matches that task text.
Because of that, dataset phrases should primarily sound like what a user would type as
the title of a task, event, reminder, or action.

## Non-Negotiable Rules

1. No automatic expression generation.
   Every new expression must be written or deliberately edited by a human.
2. No automatic machine translation as final dataset content.
   Translation tools may be used only as a rough draft, but every Russian phrase must be
   manually reviewed and rewritten when needed.
3. English and Russian must stay in sync.
   Any new `train_en.csv` row must have a corresponding `train_ru.csv` row with the same
   label and the same intent. The same rule applies to `valid` and `test`.
4. Every phrase must be meaningful.
   A phrase must sound natural, carry a clear intent, and help the classifier pick the
   correct icon instead of vaguely describing a broad topic.
5. Prefer task-like phrasing over icon description.
   The default question is not "how do we describe this icon?" but "what task text would
   make the user expect this icon?" Visual descriptions are secondary support material,
   not the core of the dataset.

## What Good Phrases Look Like

Each icon should contain a mix of phrase types in both languages:

- Task titles and task-like intents: `pay rent` / `оплатить аренду`
- Short user requests: `find my location` / `найти мое местоположение`
- Near synonyms that a user might still type: `wireless network` / `беспроводная сеть`
- Product or UI contexts that still read like real intent: `share current location` / `поделиться геопозицией`
- Direct icon names when users genuinely search that way: `wifi` / `вайфай`
- Visual descriptions only as a small secondary layer: `map with a marker` / `карта с отметкой`
- Realistic noisy input: mild typos or conversational phrasing that a user might actually type

## Task-First Principle

When adding a phrase, assume the user is naming a task and expects a matching icon.

- Good framing: `track package`, `book a flight`, `show current location`
- Weak framing: `icon with a box`, `crosshair icon`, `picture of a map pin`

If a phrase sounds like metadata for a designer rather than text from a real task, it is
usually the wrong primary training example.

## What Must Not Be Added

- Overly broad words without context such as `travel`, `music`, `tool`, `holiday`, `food`, `building`
- Mechanical template rewrites with one-word substitution
- Phrases that sound machine-generated or unnatural
- Literal Russian translations that do not sound like real Russian
- Phrases that fit several neighboring icons equally well

## Translation Rules

- Translate intent, not individual words
- Preserve the same phrase style across languages
- Keep common UI terms in their natural product form when needed: `wifi`, `bluetooth`, `NFC`, `QR code`
- Prefer natural Russian phrasing over literal calques

## Disambiguation Rule

For confusing icon families, add phrases that separate neighboring classes instead of
repeating shared category terms.

The canonical conflict map lives in `docs/icon-semantic-groups.yml`.
The full status map for all icons lives in `docs/icon-semantic-coverage.json`.
Before extending an icon, check whether it belongs to a semantic group and compare the
new phrase against the neighboring icons in that same group.

Examples:

- `map-pin`: `drop a pin` / `поставить пин на карте`
- `location-dot`: `current location marker` / `маркер текущего местоположения`
- `map`: `city map` / `карта города`
- `map-location`: `map with a marker` / `карта с отметкой`

## Recommended Per-Icon Mix

- 30-40% task titles and task-like intents
- 20-30% short queries
- 20-30% product or UI phrases that still read like user intent
- 10-15% visual or semantic descriptions
- 10-15% realistic noisy input

## Author Checklist

Before adding a new `en/ru` pair, confirm:

1. Both phrases sound natural
2. Both phrases are meaningful on their own
3. The pair sounds like something a user could type as a task title, task intent, or short query
4. The pair is not a near-duplicate of an existing row
5. The pair does not collide with neighboring labels
6. The Russian phrase preserves the same intent even if it is not literal
7. If the phrase is visual, it is justified as secondary support rather than the main pattern

If any answer is no, the pair must be rewritten or rejected.

## Working Process

1. Audit the icon folder before editing
2. Check `docs/icon-semantic-groups.yml` for the icon's conflict group
3. Fix split leakage first
4. Add new English and Russian rows together
5. Re-run dataset audit
6. Only then merge datasets for model training

## Current Priorities

1. Eliminate duplicate texts across `train/valid/test`
2. Complete missing Russian files for icons that only have English
3. Raise low-coverage icons to the minimum target volume
4. Strengthen known conflict groups with differentiating phrases
5. Expand `valid` and `test` to more reliable sizes
