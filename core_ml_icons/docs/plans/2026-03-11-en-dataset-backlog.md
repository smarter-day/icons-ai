# План следующего цикла по английскому датасету

## Summary

Английский датасет находится в чистом техническом состоянии, но всё ещё ограничен по качеству обучения:

- `711` иконок
- `29,753` train-строки
- `2,133` valid-строки
- `2,110` test-строк
- `0` missing files
- `0` count mismatches
- `0` duplicate rows
- `0` split overlap

Главные ограничения теперь не structural, а semantic:

- среднее покрытие `41.85` train-фразы на иконку
- медиана `41`
- `331` иконка имеют меньше `40` train-фраз
- `482` иконки имеют меньше `45`
- `12.14%` train-строк однословные
- `15.39%` train-строк состоят из `1-2` слов
- `349` train-текстов размечены минимум на `3` разных иконки

Следующий цикл должен быть сосредоточен на четырёх вещах:

1. low-coverage tail
2. broad shared terms
3. конфликтные пары и микрогруппы
4. стабилизация `test_en`

## Priority 1: Low-Coverage Tail

### Цель

Поднять иконки с самым слабым `train_en` до usable floor, не плодя шаблонный мусор.

### Batch 1: все иконки `<30`

Всего: `32` иконки.

- `litecoin-sign` — `20`
- `jar-wheat` — `23`
- `kazoo` — `25`
- `baht-sign` — `26`
- `bitcoin-sign` — `26`
- `bluetooth` — `26`
- `hand-holding` — `26`
- `hose-reel` — `26`
- `jar` — `26`
- `cent-sign` — `27`
- `hand-pointer` — `27`
- `value-absolute` — `27`
- `dagger` — `28`
- `elevator` — `28`
- `gif` — `28`
- `gingerbread-man` — `28`
- `gun` — `28`
- `hockey-sticks` — `28`
- `hospital-user` — `28`
- `sterling-sign` — `28`
- `won-sign` — `28`
- `baby` — `29`
- `engine` — `29`
- `euro-sign` — `29`
- `hands-bubbles` — `29`
- `hands-holding` — `29`
- `hard-drive` — `29`
- `hospitals` — `29`
- `jug-detergent` — `29`
- `note-medical` — `29`
- `peso-sign` — `29`
- `toilet-portable` — `29`

### Work Rules

- добавлять только ручные, task-first, meaning-bearing фразы
- не расширять класс механическими синонимами
- не добавлять broad nouns без различающего контекста
- для уже конфликтных иконок добавлять distinct intents, а не просто объём

### Минимальный target

- сначала довести все иконки `<30` до `45-50` train-фраз
- затем переоценить ambiguity и решить, кому нужен добор до `55-60`

## Priority 2: Broad Shared Terms

### Цель

Снизить label noise от общих train-текстов, которые размечены на много классов сразу.

### Первая волна

- `fruit`
- `covid-19`
- `water`
- `sound`
- `health`
- `car`
- `breakfast`
- `sport`
- `movie`

### Work Rules

- не просто удалять общий термин
- заменять его на более task-like и различающий intent
- работать group-by-group, а не глобально по одному слову
- после каждого batch проверять shared exact texts внутри затронутой группы

## Priority 3: Conflict Pairs And Micro-Groups

### Цель

Развести самые близкие по смыслу иконки, где train-сигналы всё ещё пересекаются слишком сильно.

### Первая волна

- `bread-loaf` / `bread-slice`
- `book` / `books`
- `lock-open` / `unlock`
- `user` / `user-large`
- `book-medical` / `books-medical`
- `building` / `buildings`
- `cheese` / `cheese-swiss`
- `alarm-clock` / `clock`
- `balloon` / `balloons`
- `campfire` / `fire`
- `champagne-glass` / `champagne-glasses`
- `cookie` / `cookie-bite`
- `sun` / `sun-cloud`
- `sushi` / `sushi-roll`
- `vial` / `vials`

### Work Rules

- `rewrite-first`, а не blind expansion
- для каждой пары выделять разные intent bands
- короткие фразы сохранять только там, где они действительно помогают поиску
- после правок проверять количество shared exact texts между парой

## Priority 4: Evaluation Stabilization

### Цель

Убрать шумную оценку там, где `test_en` уже просел до `1-2` примеров.

### Иконки с неполным `test_en`

- `hockey-stick` — `2`
- `loveseat` — `2`
- `meter` — `2`
- `music-note` — `2`
- `oil-well` — `2`
- `pan-frying` — `2`
- `person-walking` — `2`
- `peso-sign` — `2`
- `plate-utensils` — `1`
- `police-box` — `2`
- `terminal` — `2`
- `timer` — `2`
- `toggle-on` — `2`
- `trailer` — `2`
- `trash-can` — `2`
- `truck-pickup` — `2`
- `truck-ramp` — `2`
- `vest-patches` — `2`
- `video` — `2`
- `walkie-talkie` — `2`
- `washing-machine` — `2`
- `watch-smart` — `2`

### Minimal Target

- вернуть все эти иконки к `3` test-примерам
- все новые `test` строки должны быть task-like
- никаких пересечений с `train`

## Recommended Order

1. закрыть весь batch иконок `<30`
2. пройти broad-term группы `fruit`, `car`, `health`, `movie`
3. развести top conflict pairs
4. восстановить `test_en` у неполных иконок
5. перейти к следующему low-coverage слою `<40`

## Test Plan

После каждого batch:

- запускать `python3 scripts/audit_icon_dataset.py --json`
- проверять touched icons на:
  - `count_mismatches`
  - `duplicate_rows`
  - `split_overlap`
- отдельно проверять shared exact texts внутри затронутых групп и пар

После low-coverage batch:

- сравнивать train-counts до/после
- проверять, что новые строки не внесли новые broad shared terms

После evaluation batch:

- убедиться, что `test_en` снова стабилен по размеру
- проверить отсутствие leakage между `train` и `test`

## Assumptions

- Следующий цикл по английскому датасету должен быть `rewrite + selective enrichment`, а не очередной structural cleanup.
- Главная цель датасета остаётся прежней: поиск нужной иконки по названию задачи или короткому пользовательскому intent.
- Любое расширение train должно быть ручным и осмысленным; автогенерация не используется.
