import argparse

from spacy.lang.en import English, stop_words
from string import punctuation
import nltk
from nltk.stem import WordNetLemmatizer

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help='Tokenized corpora')
    parser.add_argument('--tokens', '-t', help='Path to save tokenized text')
    parser.add_argument('--output', '-o', help='Path to the output file')
    args = parser.parse_args()

    return args
def tokenize(raw, stopwords, tokenizer, out_file):

    with open(raw, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        with open(out_file, 'w', encoding='utf-8') as out:
            for line in lines:
                tokens = tokenizer(line)
                for token in tokens:
                    if token.text not in stopwords and token.text.strip().translate(str.maketrans('', '', punctuation)) != '':
                        out.write(token.text.strip().lower())
                        out.write('\n')

def lemmatize(input, output):

    lemmatizer = WordNetLemmatizer()
    with open(input, 'r', encoding='utf-8') as infile, open(output, 'w', encoding='utf-8') as outfile:
        for line in infile:
            word = line.strip()
            if word:
                lemmatized_word = lemmatizer.lemmatize(word)
                outfile.write(lemmatized_word + '\n')


def main():
    nltk.download('wordnet')
    nlp = English()
    tokenizer = nlp.tokenizer
    stopwords = stop_words.STOP_WORDS


    # tokenize('tokens_test.txt', stopwords, tokenizer, 'pg5200.txt')

    args = parse_args()

    tokenize(args.input, stopwords, tokenizer, args.tokens)
    lemmatize(args.tokens, args.output)


if __name__ == '__main__':
    main()