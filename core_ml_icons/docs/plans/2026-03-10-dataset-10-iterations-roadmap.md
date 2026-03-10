# Dataset Improvement Roadmap: Next 10 Iterations

## Purpose

This roadmap defines the next 10 dataset iterations for improving icon retrieval by
task-title text in English and Russian.

The target remains practical search quality:

- a user writes a task title, short intent, or short natural query
- the model suggests the icon the user would expect from that task text

This roadmap follows the current editorial rules:

- no automatic expression generation
- no automatic machine translation as final content
- `en` and `ru` stay synchronized
- phrases are task-first, not icon-description-first

## Current Baseline

Status as of 2026-03-10:

- `711` icons in the main dataset
- semantic coverage summary:
  - `236` grouped
  - `54` pair-risk
  - `421` isolated
- documentation and audit flow already exist
- `navigation-location` has already gone through a full task-first rewrite pass

## Progress Snapshot

Completed in the current cycle:

- `Iteration 1`: `warehouse-logistics`
- `Iteration 2`: `payments-shopping`
- `Iteration 3`: `tools-settings`
- `Iteration 4`: `networking-wireless`
- `Iteration 5`: `comments-messages`
- `Iteration 6`: `pair-risk` mini-batches
  - `axe` / `knife-kitchen`
  - `crab` / `fish`
  - `baseball` / `baseball-bat`
- `Iteration 7`: first low-coverage grouped batch
  - `euro-sign`
  - `hryvnia-sign`
  - `lira-sign`
  - `rupiah-sign`
  - `ruble-sign`
  - `rupee-sign`
- `Iteration 8`: targeted `ru` parity pass on already touched icons

Still open:

- `Iteration 9`: `valid/test` quality pass
  - completed batches:
    - `navigation-location`
    - `comments-messages`
    - `tools-settings`
    - `networking-wireless`
    - `payments-shopping`
  - remaining batches:
    - none
- `Iteration 10`: checkpoint review and merged rebuild

## Iteration Format

Each iteration should produce:

1. one concrete dataset improvement pass
2. a short audit after the edits
3. a decision on whether the same group needs another pass or can be frozen for now

Completion rule for each iteration:

- no `en/ru` count mismatch in touched icons
- no duplicate rows in touched files
- no exact shared texts inside the touched semantic group
- new phrases read like task titles, user intents, or short search requests

## Iteration 1

### Focus
`warehouse-logistics`

### Why now
This group still likely contains broad retrieval words such as `inventory`, `archive`,
`shipping`, `warehouse`, `box`, `storage`, `склад`, `коробка`.

### Work
- audit the group
- remove or rewrite designer-like and generic phrases
- replace broad short terms with task-like queries
- separate `box`, `boxes`, `archive`, `warehouse`, `truck`, `shipping`-style intents
- add missing `en/ru` task-like pairs where the group becomes too thin after cleanup

### Expected result
- less confusion between storage, delivery, archive, and package-related icons
- better task-title retrieval for shipping and inventory tasks

## Iteration 2

### Focus
`payments-shopping`

### Why now
Part of this group was already cleaned for exact duplicates, but it still needs a full
task-first rewrite pass.

### Work
- rewrite overly abstract commerce words into user-intent phrases
- separate payment, checkout, receipt, coupon, premium, investment, cash, grocery intents
- ensure short phrases still reflect what a user would type as a task

### Expected result
- fewer collisions between money, shopping, checkout, and deal-related icons
- better icon choice for spending and purchase tasks

## Iteration 3

### Focus
`tools-settings`

### Why now
This group usually causes broad overlap on words like `tool`, `settings`, `fix`,
`repair`, `configure`.

### Work
- rewrite generic maintenance words into task-like actions
- separate configuration from repair and hardware tools
- distinguish `gear`, `wrench`, `toolbox`, `hammer`, `screwdriver`, `screwdriver-wrench`

### Expected result
- cleaner separation between settings, repair, construction, and utility tasks

## Iteration 4

### Focus
`networking-wireless`

### Why now
This is a frequent user-intent area and likely contains short overlapping terms such as
`wifi`, `router`, `wireless`, `network`, `signal`, `nfc`.

### Work
- keep valid core keywords where they are genuinely expected by users
- rewrite overly broad network phrases into concrete intents
- separate internet access, local networking, pairing, and tap-to-connect intents

### Expected result
- better retrieval for connectivity tasks without collapsing all network icons together

## Iteration 5

### Focus
`comments-messages` and adjacent communication icons

### Why now
This is a high-frequency product area where users often write short titles such as
`reply to message`, `leave a comment`, `send message`.

### Work
- separate comment, message, chat, reply, and notification-style intents
- reduce shared language between speech-bubble families
- add more task-title phrasing and fewer generic nouns

### Expected result
- more stable distinction between commenting and messaging intents

## Iteration 6

### Focus
Remaining high-value `pair-risk` icons

### Why now
After the biggest groups, the next quality jump comes from local pairs and triplets.

### Work
- select the strongest `pair-risk` items from `docs/icon-semantic-coverage.json`
- cluster them into small work batches
- rewrite or enrich them with task-like phrases
- promote stable pairs into semantic groups where useful

### Expected result
- `pair-risk` count should drop materially from the current `54`
- fewer edge-case confusions in close icon pairs

## Iteration 7

### Focus
Low-coverage icons below the practical target

### Why now
Some icons still have weak train coverage even after structural cleanup.

### Work
- collect the weakest icons by train volume
- add manual `en/ru` task-like phrases
- avoid adding broad nouns just to inflate counts
- prioritize icons that are both low-coverage and semantically close to neighbors

### Expected result
- reduced failure rate on underrepresented icons
- fewer classes that are only learnable from tiny phrase sets

## Iteration 8

### Focus
Russian parity pass

### Why now
The dataset should improve as a bilingual system, not only in English.

### Work
- audit all icons still missing full `ru` coverage
- bring weak `ru` files closer to the quality and shape of `en`
- rewrite literal or awkward Russian phrases into natural task-title language
- keep intent parity without forcing literal translation

### Expected result
- stronger Russian retrieval quality
- fewer cases where `ru` lags behind `en` in usefulness or naturalness

## Iteration 9

### Focus
`valid` and `test` quality pass

### Why now
Training data is not enough on its own. Evaluation must reflect real task-title inputs.

### Work
- expand `valid/test` for the most conflict-prone groups
- replace synthetic-looking evaluation rows with realistic short tasks
- ensure no split leakage in touched icons
- keep `en/ru` validation and test sets synchronized by intent

### Expected result
- more trustworthy validation signals
- less risk of overestimating model quality

## Iteration 10

### Focus
Freeze candidate set and run a full checkpoint review

### Why now
After nine focused passes, the dataset needs a checkpoint before the next expansion wave.

### Work
- run a full audit over the repository
- summarize what changed across the previous iterations
- identify the next three most harmful groups or risk clusters
- rebuild merged datasets for `en` and `ru`
- prepare a concise review document with findings and next priorities

### Expected result
- a stable checkpoint for discussion
- clear evidence of what improved and what still blocks acceptable quality

## Practical Success Metrics

By the end of these 10 iterations, the expected direction is:

- fewer broad shared terms inside conflict groups
- more task-like phrasing across the dataset
- lower `pair-risk` pressure
- stronger `ru` parity
- better validation quality

The roadmap is successful if, after these iterations:

- conflict groups contain mostly differentiating task-like phrases
- weak icons no longer rely on generic one-word labels
- bilingual sync remains intact
- evaluation sets better reflect real task-title search

## Discussion Questions For Review

After each 2-3 iterations, review:

1. Are we improving retrieval quality or only making the dataset cleaner on paper?
2. Which groups still produce phrases that sound like design metadata rather than task text?
3. Are users more likely to search by short noun phrases, by actions, or by task titles in our product?
4. Do we need more product-context phrasing for certain categories?
5. Which icons still cannot be justified by realistic task-title inputs?
