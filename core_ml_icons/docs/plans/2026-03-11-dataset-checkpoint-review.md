# Dataset Checkpoint Review

## Scope

This checkpoint closes the 10-iteration roadmap cycle after:

- task-first rewrites for the main conflict groups in `train`
- targeted pair-risk cleanup
- first low-coverage enrichment batch
- Russian parity cleanup on touched icons
- `valid/test` rewrites for the highest-risk evaluation groups

## Technical State

Full audit status on 2026-03-11:

- `711` total icon folders
- `0` missing files inside audited bilingual sets
- `0` count mismatches
- `0` duplicate rows
- `0` split overlap

Merged datasets rebuilt:

- `en`: `711` icon folders
  - `train_en.csv`: `29753` rows
  - `valid_en.csv`: `2133` rows
  - `test_en.csv`: `2110` rows
- `ru`: `582` icon folders
  - `train_ru.csv`: `24293` rows
  - `valid_ru.csv`: `1746` rows
  - `test_ru.csv`: `1723` rows

## Completed Batches

Main train rewrites completed in this cycle:

- `warehouse-logistics`
- `payments-shopping`
- `tools-settings`
- `networking-wireless`
- `comments-messages`
- `navigation-location`

Pair-risk mini-batches completed:

- `axe` / `knife-kitchen`
- `crab` / `fish`
- `baseball` / `baseball-bat`

Low-coverage grouped batch completed:

- `euro-sign`
- `hryvnia-sign`
- `lira-sign`
- `rupiah-sign`
- `ruble-sign`
- `rupee-sign`

`valid/test` quality pass completed for:

- `navigation-location`
- `comments-messages`
- `tools-settings`
- `networking-wireless`
- `payments-shopping`

## Remaining Blockers

### 1. Missing Russian coverage

The largest remaining problem is still bilingual incompleteness:

- `129` icons still do not have full `ru` coverage

Examples:

- `address-book`
- `apple-whole`
- `avocado`
- `badge-sheriff`
- `banana`
- `bandage`
- `bitcoin-sign`
- `blueberries`
- `bolt-lightning`
- `book-bible`

This is the main blocker for a truly bilingual retrieval model.

### 2. Low-coverage tail

Structural quality is clean, but many icons are still below the practical train target.

Examples from the low-coverage tail:

- `baby`: `29 / 29`
- `ant`: `39 / 39`
- `apartment`: `41 / 41`
- `airplay`: `44 / 44`
- `badge-dollar`: `47 / 47`
- `abacus`: `54 / 54`

This no longer looks like a hygiene problem. It is now a coverage problem.

### 3. Shared broad terms across labels

The next accuracy ceiling is set by remaining broad train terms reused across many labels.

Top remaining `en` conflicts:

- `covid-19`
- `fruit`
- `breakfast`
- `car`
- `health`

Top remaining `ru` conflicts:

- `авто`
- `десерт`
- `питомец`
- `поездка`
- `рождество`

These are the strongest candidates for the next semantic cleanup cycle.

## Recommended Next Cycle

Priority order for the next cycle:

1. Close the biggest `ru` coverage gaps for high-value icons.
2. Run targeted cleanup on the remaining broad shared terms.
3. Continue low-coverage enrichment, starting with grouped and pair-risk icons.

## Shortlist: Next 3 Most Harmful Problems

1. `129` icons still missing full `ru`.
2. The long low-coverage tail below practical train volume.
3. Broad shared terms still reused across many labels in food, health, transport, and holiday clusters.
