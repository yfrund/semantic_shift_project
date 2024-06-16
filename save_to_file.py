import csv

def save_to_csv(occurrences, out):
    all_words = set(word for term in occurrences.values() for word in term.keys())

    with open(out, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        header = ['Term'] + list(all_words)
        writer.writerow(header)


        for term, words in occurrences.items():
            row = [term] + [words.get(word, 0) for word in all_words] #vectors for the same term will be the same length
            writer.writerow(row)

def ri_to_csv(embeddings, out):

    with open(out, 'w', newline='') as f:
        writer = csv.writer(f)
        for key, value in embeddings.items():
            writer.writerow([key, value])

def w2v_to_csv(term, similarity, interpretation, out):

    with open(out, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([term, similarity, interpretation])

def bert_to_csv(cluster_analysis, out):

    with open(out, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Corpus', 'Term', 'Cluster', 'Contexts'])
        for corpus_id, term_analysis in cluster_analysis.items():
            for term, clusters in term_analysis.items():
                for cluster_id, contexts in clusters.items():
                    for context in contexts:
                        writer.writerow([corpus_id, term, cluster_id, context])
