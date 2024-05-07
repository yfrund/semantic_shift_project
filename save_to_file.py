import csv

def save_to_csv(occurrences, out):
    all_words = set(word for term in occurrences.values() for word in term.keys())

    with open(out, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row with all unique words
        header = ['Term'] + list(all_words)
        writer.writerow(header)

        # Write each term and its corresponding word frequencies
        for term, words in occurrences.items():
            row = [term] + [words.get(word, 0) for word in all_words]
            writer.writerow(row)

def ri_to_csv(embeddings, out):

    with open(out, 'w', newline='') as f:
        writer = csv.writer(f)
        for key, value in embeddings.items():
            writer.writerow([key, value])