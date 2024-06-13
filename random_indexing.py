import argparse
import os
import numpy as np
from save_to_file import ri_to_csv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', nargs='+', help='Tokenized corpora')
    parser.add_argument('--window', '-w', type=int, help='Window size - number of tokens on each side')
    parser.add_argument('--direction', '-d', type=str, help='Window direction: left, right or both.')
    parser.add_argument('--terms', '-t', nargs='+', help='Terms of interest.')
    parser.add_argument('--output', '-o', help='Path to the output file.')
    args = parser.parse_args()

    return args

def random_matrix(vocab_size, dims):
    matrix = set()

    while len(matrix) != vocab_size:
        vector = tuple(np.random.choice([-1,0,1], size=dims, p=[0.2,0.6,0.2]))
        matrix.add(vector)

    return list(matrix)

def word_to_random_index(word, data):
    data = np.array(data)
    return np.flatnonzero(data==word)

def embed(data, random_matrix, window, direction, terms):
    embeddings = {}

    for term in terms:
        # print(term)
        indices = word_to_random_index(term+'\n', data)

        temp = []
        for index in indices:

            if direction == 'right':
                emb = np.sum(random_matrix[index+1:index+window+1], axis=0)
                temp.append(emb)

            elif direction == 'left':
                emb = np.sum(random_matrix[index-window:index], axis=0)
                temp.append(emb)

            elif direction == 'both':
                emb = np.sum(random_matrix[index-window:index]+random_matrix[index+1:index+window+1], axis=0)
                temp.append(emb)

        temp = np.sum(temp, axis=0)
        embeddings[term] = temp

    return embeddings



def main():

    args = parse_args()

    for corpus in args.input:
        with open(corpus, 'r', encoding='utf-8') as f:
            data = f.readlines()
            rand_matrix = random_matrix(len(data), 10)

            embeddings = embed(data, rand_matrix, args.window, args.direction, args.terms)
            ri_to_csv(embeddings, f'{args.output}_{os.path.basename(args.corpus).split(".")[0]}.csv')


if __name__ == '__main__':
    main()

