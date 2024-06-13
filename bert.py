import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
from collections import defaultdict
from save_to_file import bert_to_csv

def get_word_embeddings(corpus, word, model, tokenizer):
    word_embeddings = []
    contexts = []
    for sentence in corpus:
        inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
        outputs = model(**inputs)
        last_hidden_state = outputs.last_hidden_state.squeeze(0)
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze(0))
        for i, token in enumerate(tokens):
            if token == word:
                word_embedding = last_hidden_state[i].detach().numpy()
                word_embeddings.append(word_embedding)
                contexts.append(sentence)
    return np.array(word_embeddings), contexts

def perform_clustering(embeddings, max_clusters):
    try:
        n_samples = embeddings.shape[0]
        n_clusters = min(n_samples - 1, max_clusters)
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(embeddings)
        return kmeans.labels_, kmeans.cluster_centers_
    except Exception as e:
        print('Error performing clustering:', e)
        return None, None



def plot_clusters(embeddings, labels, title='Clusters'):
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=labels)
    plt.title(title)
    plt.show()

def compare_clusters(centers1, centers2, threshold=0.5):
    centers1 = np.atleast_2d(centers1)
    centers2 = np.atleast_2d(centers2)

    distances = cdist(centers1, centers2, 'cosine')

    match_count = np.sum(distances < threshold)
    return match_count

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        corpus = file.readlines()
    return [line.strip() for line in corpus if line.strip()]

def analyze_clusters(labels, contexts):
    cluster_contexts = defaultdict(list)
    for label, context in zip(labels, contexts):
        cluster_contexts[label].append(context)
    return cluster_contexts

def main(corpus_paths, terms, max_clusters=10, threshold=0.5, output=None):
    corpora = [load_corpus(path) for path in corpus_paths]

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    cluster_analysis = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for term in terms:
        embeddings_list = []
        contexts_list = []
        for corpus in corpora:
            embeddings, contexts = get_word_embeddings(corpus, term, model, tokenizer)
            embeddings_list.append(embeddings)
            contexts_list.append(contexts)

        # print(embeddings_list)
        cluster_labels = []
        cluster_centers = []
        for i, embeddings in enumerate(embeddings_list):
            if len(embeddings) >= 2:
                # optimal_clusters = find_optimal_clusters(embeddings, max_clusters)
                labels, centers = perform_clustering(embeddings, max_clusters)
                if labels is not None and centers is not None:
                    cluster_labels.append(labels)
                    cluster_centers.append(centers)
                    plot_clusters(embeddings, labels, title=f'Clusters for "{term}" in Corpus {i + 1}')
                else:
                    print(f'Clustering failed for "{term}" in Corpus {i + 1}.')
                    continue
            else:
                print(f'Not enough samples for "{term}" in Corpus {i+1} to form clusters.')
                return

        if len(cluster_centers) == len(corpora):
            for i in range(len(corpora)):
                for j in range(i + 1, len(corpora)):
                    matches = compare_clusters(cluster_centers[i], cluster_centers[j], threshold)
                    print(f'Number of matching clusters for "{term}" between Corpus {i+1} and Corpus {j+1}: {matches}')

            for i, (labels, contexts) in enumerate(zip(cluster_labels, contexts_list)):
                cluster_contexts = analyze_clusters(labels, contexts)
                for cluster, contexts in cluster_contexts.items():
                    cluster_analysis[f'Corpus {i + 1}'][term][cluster].extend(contexts)
                    print(f'Analysis of clusters for "{term}" in Corpus {i + 1}:')
                    for context in contexts:
                        print(f'  Cluster {cluster} contexts:')
                        print(f'    {context}')
    if output:
        bert_to_csv(cluster_analysis, output)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Compare semantic clusters across multiple corpora.')
    parser.add_argument('--input', type=str, nargs='+', required=True, help='Paths to the corpus files.')
    parser.add_argument('--terms', type=str, nargs='+', required=True, help='Terms to analyze in the corpora.')
    parser.add_argument('--max_clusters', type=int, default=10, help='Maximum number of clusters for finding the optimal number.')
    parser.add_argument('--threshold', type=float, default=0.5, help='Threshold for cluster comparison.')
    parser.add_argument('--output', help='Path to save output')

    args = parser.parse_args()

    main(args.input, args.terms, args.max_clusters, args.threshold, args.output)
