from collections import defaultdict
import numpy as np
from save_to_file import save_to_csv

def pmi_score(data, window, direction, terms, out):
    occurrences = {term: defaultdict(int) for term in terms}
    prob_terms = {}
    prob_context = {}
    with open(data, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        length = len(lines)

        for term in terms:
            prob_terms[term] = lines.count(term+'\n')/length
        for i, line in enumerate(lines):
            line = line.lower().strip()
            if line in terms:
                if direction == 'right':
                    context = lines[i + 1:i + window + 1]
                    for c in context:
                        occurrences[line][c.strip()] += 1
                        prob_context[c.strip()] = lines.count(c)/length
                elif direction == 'left':
                    context = lines[i - window:i]
                    for c in context:
                        occurrences[line][c.strip()] += 1
                        prob_context[c.strip()] = lines.count(c) / length
                elif direction == 'both':
                    context = lines[i - window:i] + lines[i + 1:i + window + 1]
                    for c in context:
                        occurrences[line][c.strip()] += 1
                        prob_context[c.strip()] = lines.count(c) / length

    for term in occurrences:

        for word in occurrences[term]:
            prob = occurrences[term][word]/length
            prob = prob / (prob_terms[term]*prob_context[word])
            prob = np.log(prob)

            occurrences[term][word] = prob

    save_to_csv(occurrences, out)

def main():
    pmi_score('tokens_test.txt', 3, 'both', ['apple', 'cloud'], 'pmi_test.csv')

if __name__ == '__main__':
    main()