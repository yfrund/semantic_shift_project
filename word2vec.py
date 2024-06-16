import argparse

from gensim.models import Word2Vec
from save_to_file import w2v_to_csv
import os
import nltk
from nltk.corpus import stopwords
from cosine_similarity import similarity, interpret_similarity

def read_corpus(file_path, stopwords):
    tokenized_corpus = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            tokens = nltk.word_tokenize(line.lower())
            tokens = [token for token in tokens if token.isalpha() and token not in stopwords]
            tokenized_corpus.append(tokens)
    return tokenized_corpus

def train_word2vec_model(tokenized_corpus, model_save_path, window):
    model = Word2Vec(sentences=tokenized_corpus, vector_size=300, window=window, min_count=5, sg=1)
    save_model(model, model_save_path)
    return model

def save_model(model, model_path):
    model.save(model_path)
    print(f'Model saved to {model_path}')


def get_embedding(model, term):
    if term in model.wv:
        return model.wv[term]
    else:
        return None

def main(model_paths, input_corpora, terms, output, window, model_save_dir):

    os.makedirs(model_save_dir, exist_ok=True)

    stopwords_en = set(stopwords.words('english'))

    models = []
    if model_paths:
        #load models if --model_path is passed
        for path in model_paths:
            model = Word2Vec.load(path)
            models.append(model)
    elif input_corpora:
        #train models if --input is passed
        for corpus in input_corpora:
            print(f'Tokenizing {os.path.basename(corpus)}')
            tokenized_corpus = read_corpus(corpus, stopwords_en)

            model_save_path = os.path.join(model_save_dir, f'model_{os.path.basename(corpus)}.bin')
            print(f'Training model_{os.path.basename(corpus)}.bin')
            models.append(train_word2vec_model(tokenized_corpus, model_save_path, window))
    else:
        print('Error: Either --models or --input must be provided.')
        return


    for term in terms:
        embeddings = []
        print(f'Comparing embeddings for "{term}"')

        for model in models:
            try:
                embedding = get_embedding(model, term)

                embeddings.append(embedding)

            except KeyError:
                print(f'Embedding not found')

        if all(item is not None for item in embeddings):
            # print(f'embeddings: {embeddings}')
            sim = similarity(embeddings[0], embeddings[1])
            # print(sim)
            interpretation = interpret_similarity(sim)

            w2v_to_csv(term, sim, interpretation, output)
        else:
            w2v_to_csv(term, 'Could not compute similarity', 'Term did not occur in one of the corpora', output)




if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Compare word embeddings to detect semantic shifts')
    parser.add_argument('--input', '-i', nargs='+', help='Paths to corpora for training Word2Vec models')
    parser.add_argument('--models', '-m', type=str, nargs='+', help='Paths to the pretrained Word2Vec model files')
    parser.add_argument('--terms', '-t', type=str, nargs='+', help='The terms to compare between the models')
    parser.add_argument('--window', '-w', type=int, help='Window size - number of tokens on each side')
    parser.add_argument('--output', '-o', help='Path to save output')
    parser.add_argument('--model_save_dir', '-msd', help='Directory to save the trained models')

    args = parser.parse_args()

    main(args.models, args.input, args.terms, args.output, args.window, args.model_save_dir)