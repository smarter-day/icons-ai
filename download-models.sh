#!/bin/zsh

source .venv/bin/activate
python -m nltk.downloader wordnet
python -m nltk.downloader stopwords
