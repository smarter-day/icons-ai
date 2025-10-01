#!/bin/zsh

source .venv/bin/activate

BASE_LANGUAGE="en"
SECONDARY_LANGUAGES="ru"

echo '----------------------------------------------------------------------------------'
echo ' STEP 1: PREPARE MODELS'
echo '----------------------------------------------------------------------------------'
python3 prepare_models.py --languages $BASE_LANGUAGE,$SECONDARY_LANGUAGES

echo '----------------------------------------------------------------------------------'
echo ' STEP 2: CLEANING ICONS DATA'
echo '----------------------------------------------------------------------------------'
python3 strip_icons.py

echo '----------------------------------------------------------------------------------'
echo ' STEP 3: GENERATE SYNONYMS'
echo '----------------------------------------------------------------------------------'
python generate_synonims.py

echo '----------------------------------------------------------------------------------'
echo ' STEP 4: TRANSLATE ICONS TAGS AND SAVE TRANSLATIONS IN CACHE'
echo '----------------------------------------------------------------------------------'
python3 translate_keywords.py --languages $SECONDARY_LANGUAGES

echo '----------------------------------------------------------------------------------'
echo ' STEP 5: TRANSLATE STRIPPED ICONS FILES'
echo '----------------------------------------------------------------------------------'
python translate_icons.py --languages $SECONDARY_LANGUAGES

echo '----------------------------------------------------------------------------------'
echo ' STEP 6: BUILD EMBEDDINGS'
echo '----------------------------------------------------------------------------------'
python 02_create_icons_embeddings.py --languages $BASE_LANGUAGE,$SECONDARY_LANGUAGES

echo '----------------------------------------------------------------------------------'
echo ' Now you can check how it works: python3 03_search_icons.py ru                    '
echo '----------------------------------------------------------------------------------'
