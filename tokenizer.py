from spacy.lang.en import English, stop_words
from string import punctuation




def tokenize(out, stopwords, tokenizer, *raw):
    for file in raw:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            with open(out, 'w', encoding='utf-8') as out:
                for line in lines:
                    tokens = tokenizer(line)
                    for token in tokens:
                        if token.text not in stopwords and token.text.strip().translate(str.maketrans('', '', punctuation)) != '':
                            out.write(token.text.strip())
                            out.write('\n')


def main():
    nlp = English()
    tokenizer = nlp.tokenizer
    stopwords = stop_words.STOP_WORDS

    tokenize('tokens_test.txt', stopwords, tokenizer, 'pg5200.txt')

if __name__ == '__main__':
    main()