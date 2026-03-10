# RU Gap Closure Plan

## Summary

Next cycle focuses on closing missing `ru` coverage instead of more broad cleanup.
At the checkpoint, `ru` covered only `582` of `711` icons, so the most direct quality gain is to expand bilingual coverage for high-value icons first.

Priority order:
1. Close missing `ru` for `grouped` icons.
2. Close missing `ru` for `unknown` icons.
3. Take a selective `isolated` batch instead of trying to close all isolated gaps at once.

## Key Changes

### Batch 1: High-value grouped missing_ru

Goal: close all `34` missing-ru icons with `grouped` status.

First-wave examples:
- `badge-sheriff`
- `bolt-lightning`
- `book-bible`
- `book-medical`
- `book-quran`
- `books-medical`
- `burger-cheese`
- `capsules`
- `car-bolt`
- `car-key`
- `champagne-glass`
- `copyright`
- `drone-front`
- `glass`
- `mug`
- `music`
- `pencil`
- `podcast`
- `saxophone`
- `speaker`

For each icon:
- create `train_ru.csv`, `valid_ru.csv`, `test_ru.csv` if they do not exist
- if `ru` is partial, complete the full set
- keep `ru` task-like, natural, and aligned by intent with `en`
- keep split counts equal between `en` and `ru`

### Batch 2: Unknown missing_ru

Goal: close the small technical tail before moving to isolated icons.

Approach:
- verify why these icons are not represented cleanly in coverage status
- close missing `ru` sets with the same manual task-first approach
- if coverage mapping is incomplete, update the source of truth after the `ru` sets are done

### Batch 3: Selective isolated missing_ru

Goal: take a useful subset instead of closing all isolated gaps at once.

Entry criteria:
- the icon is common in product tasks
- the icon is low-coverage and still lacks `ru`
- the icon belongs to a broad-term cluster that will need cleanup later

Initial shortlist:
- `address-book`
- `apple-whole`
- `avocado`
- `banana`
- `bandage`
- `bitcoin-sign`
- `blueberries`
- `bottle-baby`
- `broccoli`

## Editorial Rules

- no automatic generation
- no machine translation as the final text
- every `ru` row must read like a task title, intent, or short user query
- do not copy editor-like or icon-description-first wording into `ru`
- preserve intent parity with `en`, not literal wording
- before closing each batch, ensure `valid/test` do not repeat `train`

## Exit Criteria

The cycle is done when:
- all `34` grouped `missing_ru` icons are fully closed
- all `unknown` `missing_ru` icons are either closed or classified into an explicit coverage status
- the selected isolated batch is also fully closed
- merged `ru` dataset is rebuilt
- audit shows no:
  - `missing_files`
  - `count_mismatches`
  - `duplicate_rows`
  - `split_overlap`

## Test Plan

After each batch:
- run `python3 scripts/audit_icon_dataset.py --json`
- check touched icons for:
  - `train_ru/valid_ru/test_ru` presence
  - equal split counts between `en` and `ru`
  - no duplicate rows
  - no overlap between `train` and `valid/test`
- if the batch touches grouped icons, also check for new shared exact texts inside the semantic group

After the full cycle:
- rebuild the merged `ru` dataset
- compare the number of merged `ru` icon folders before and after
- update the checkpoint summary with:
  - how many missing `ru` icons were closed
  - which groups are now fully bilingual
  - which isolated gaps still remain

## Assumptions

- this cycle does not include another broad shared-term cleanup
- grouped missing-ru icons matter more than isolated ones
- every new `ru` icon must mirror `en` split counts
- if `en` has weak or awkward text, rewrite the intent naturally in `ru` instead of copying it literally
