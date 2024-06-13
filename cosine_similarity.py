from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import sys

def similarity(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]

def interpret_similarity(similarity):
    if similarity > 0.85:
        return 'Very similar (likely minimal or no semantic shift)'
    elif similarity > 0.6:
        return 'Moderately similar (possible slight semantic shift)'
    elif similarity > 0.4:
        return 'Somewhat similar (likely moderate semantic shift)'
    else:
        return 'Not similar (likely significant semantic shift)'

def read_vectors(file_path):
    df = pd.read_csv(file_path, index_col=0)
    terms = df.index.tolist()
    vectors = df.values
    return df.columns.tolist(), {term: vectors[i] for i, term in enumerate(terms)}

def align_vectors(vector1, vector2, context_words1, context_words2):
    '''cosine_similarity assumes vectors of the same size, so need to align them'''
    combined_context_words = list(set(context_words1 + context_words2))
    aligned_vector1 = np.zeros(len(combined_context_words))
    aligned_vector2 = np.zeros(len(combined_context_words))
    context_word_to_index = {word: idx for idx, word in enumerate(combined_context_words)}
    #map original values to context words, otherwise filled with 0
    for word, value in zip(context_words1, vector1):
        aligned_vector1[context_word_to_index[word]] = value
    for word, value in zip(context_words2, vector2):
        aligned_vector2[context_word_to_index[word]] = value
    return aligned_vector1, aligned_vector2

# def compute_similarity(vectors1, vectors2):
#     similarities = cosine_similarity(vectors1, vectors2)
#     return similarities


def main(file1, file2, output_file):
    context_words1, vectors1 = read_vectors(file1)
    context_words2, vectors2 = read_vectors(file2)

    with open(output_file, 'w') as f:
        f.write('Term,Similarity,Interpretation\n') #header
        for term, vector1 in vectors1.items():
            if term in vectors2:
                vector2 = vectors2[term]
                aligned_vector1, aligned_vector2 = align_vectors(vector1, vector2, context_words1, context_words2)
                similarity_score = similarity(aligned_vector1, aligned_vector2)
                interpretation = interpret_similarity(similarity_score)
                f.write(f'{term},{similarity_score},{interpretation}\n') #save


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print(f'Usage: {sys.argv[0]} <file1> <file2> <output_file>')
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]

    main(file1, file2, output_file)
