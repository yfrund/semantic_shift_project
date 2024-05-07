import numpy as np
from save_to_file import ri_to_csv

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

    with open('tokens_test.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
        rand_matrix = random_matrix(len(data), 10)

        embeddings = embed(data, rand_matrix, 3, 'both', ['apple', 'sit'])
        ri_to_csv(embeddings, 'random_indexing_test.csv')





if __name__ == '__main__':
    main()

#TODO: add support for word forms (eg apple + apples) - pass as sublist of forms? eg terms = [['apple', 'apples'], 'try']
#TODO: save random matrix and embeddings to make reusable with other terms