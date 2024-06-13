
import argparse
import gensim
from gensim.models import Word2Vec
import cosine_similarity
from save_to_file import w2v_to_csv


def read_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        corpus = file.readlines()
    tokenized_corpus = [gensim.utils.simple_preprocess(line) for line in corpus]
    return tokenized_corpus


def get_embedding(model, term):
    return model.wv[term]


def main(corpora_paths, terms, output):
    corpora = [read_corpus(path) for path in corpora_paths]

    models = [Word2Vec(sentences=corpus, vector_size=300, window=5, min_count=1, sg=1) for corpus in corpora]

    for term in terms:
        print(f'Comparing embeddings for term: "{term}"')

        embeddings = []
        for model in models:
            if term in model.wv:
                embeddings.append(get_embedding(model, term))
            else:
                print(f'Warning: Term "{term}" not found in one of the corpora.')
                embeddings.append(None)

        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                if embeddings[i] is not None and embeddings[j] is not None:
                    similarity = cosine_similarity.similarity([embeddings[i]], [embeddings[j]])[0][0]
                    print(f'Cosine similarity between "{term}" in corpus {i + 1} and corpus {j + 1}: {similarity:.4f}')
                    print(cosine_similarity.interpret_similarity(similarity))
                    w2v_to_csv(term, similarity, cosine_similarity.interpret_similarity(similarity), output)
                else:
                    print(
                        f'Cannot calculate similarity for "{term}" between corpus {i + 1} and corpus {j + 1} due to missing embedding.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare word embeddings to detect semantic shifts')
    parser.add_argument('--input', '-i', type=str, nargs='+', help='Paths to the corpus files')
    parser.add_argument('--terms', '-t', type=str, nargs='+', help='The terms to compare between the corpora')
    parser.add_argument('--output', '-o', help='Path to save output')

    args = parser.parse_args()
    main(args.input, args.terms, args.output)
