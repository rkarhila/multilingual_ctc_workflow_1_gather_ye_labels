#!/bin/bash

for l in *_*; do
    if [ -f $l/all_sentences.txt  ]; then
	python3 scripts/yet_another_transcription_cleaner.py $l/all_sentences.txt $l/all_prompts.txt $l/all_utterances.txt;
    fi;
done
