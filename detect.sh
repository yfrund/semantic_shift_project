#!/bin/bash

TOKENIZER_SCRIPT='tokenizer.py'
NORMALIZED_FREQ_SCRIPT='normalized_frequency.py'
PMI_SCRIPT='pmi.py'
RANDOM_INDEXING_SCRIPT='random_indexing.py'
WORD2VEC_SCRIPT='word2vec.py'
BERT_SCRIPT='bert.py'
COSINE_SIMILARITY_SCRIPT='cosine_similarity.py'
OUTPUT_DIR='output'
DATA='data'

mkdir -p $OUTPUT_DIR


CORPUS_R1='corpus_2001_2005.txt'
CORPUS_R2='corpus_2008_2012.txt'


echo 'Running tokenization and lemmatization'

python3 $TOKENIZER_SCRIPT --input $DATA/$CORPUS_R1 --tokens $DATA/$CORPUS_R1.tokens --output $DATA/$CORPUS_R1.lemmas
python3 $TOKENIZER_SCRIPT --input $DATA/$CORPUS_R2 --tokens $DATA/$CORPUS_R2.tokens --output $DATA/$CORPUS_R2.lemmas


CORPUS_TL1="$DATA/$CORPUS_R1.lemmas"
CORPUS_TL2="$DATA/$CORPUS_R2.lemmas"

WINDOW=3
DIRECTION='both'
TERMS=('surveillance' 'bailout' 'transparency' 'lobbying' 'precedent' 'subpoena' 'impeachment' 'asylum' 'veto' 'constitution')
RATE=1000
MAX_CLUSTERS=10
THRESHOLD=0.5

echo 'Running normalized_frequency...'
python3 $NORMALIZED_FREQ_SCRIPT --input $CORPUS_TL1 $CORPUS_TL2 --window $WINDOW --direction $DIRECTION --terms "${TERMS[@]}" --rate $RATE --output $OUTPUT_DIR/normalized_frequency.csv


echo 'Running PMI...'
python3 $PMI_SCRIPT --input $CORPUS_TL1 $CORPUS_TL2 --window $WINDOW --direction $DIRECTION --terms "${TERMS[@]}" --output $OUTPUT_DIR/pmi.csv


echo 'Running random_indexing...'
python3 $RANDOM_INDEXING_SCRIPT --input $CORPUS_TL1 $CORPUS_TL2 --window $WINDOW --direction $DIRECTION --terms "${TERMS[@]}" --output $OUTPUT_DIR/random_indexing.csv


echo 'Running word2vec...'
#to train models:
#python3 $WORD2VEC_SCRIPT --input $DATA/$CORPUS_R1 $DATA/$CORPUS_R2 --terms "${TERMS[@]}" --window $WINDOW --output $OUTPUT_DIR/word2vec.csv --model_save_dir $OUTPUT_DIR

#to work with pre-trained models
python3 $WORD2VEC_SCRIPT --models $OUTPUT_DIR/word2vec_models/model_${CORPUS_R1}.bin $OUTPUT_DIR/word2vec_models/model_${CORPUS_R2}.bin --terms "${TERMS[@]}" --window $WINDOW --output $OUTPUT_DIR/word2vec.csv --model_save_dir $OUTPUT_DIR


echo 'Running BERT...'
python3 $BERT_SCRIPT --input $DATA/$CORPUS_R1 $DATA/$CORPUS_R2 --terms "${TERMS[@]}" --max_clusters $MAX_CLUSTERS --threshold $THRESHOLD --output $OUTPUT_DIR/bert.csv

#echo 'Running cosine similarity analysis...'
CORPUS_R1_CSV="${CORPUS_R1%.txt}.csv"
CORPUS_R2_CSV="${CORPUS_R2%.txt}.csv"
#
python3 $COSINE_SIMILARITY_SCRIPT $OUTPUT_DIR/normalized_frequency.csv_${CORPUS_R1_CSV} $OUTPUT_DIR/normalized_frequency.csv_${CORPUS_R2_CSV} $OUTPUT_DIR/normalized_frequency_similarity.csv
python3 $COSINE_SIMILARITY_SCRIPT $OUTPUT_DIR/pmi.csv_${CORPUS_R1_CSV} $OUTPUT_DIR/pmi.csv_${CORPUS_R2_CSV} $OUTPUT_DIR/pmi_similarity.csv
#python3 $COSINE_SIMILARITY_SCRIPT $OUTPUT_DIR/random_indexing.csv_${CORPUS_R1_CSV} $OUTPUT_DIR/random_indexing.csv_${CORPUS_R2_CSV} $OUTPUT_DIR/random_indexing_similarity.csv

echo 'All similarities calculated and saved in $OUTPUT_DIR.'
