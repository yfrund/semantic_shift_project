import argparse
from collections import defaultdict
import numpy as np
from save_to_file import save_to_csv
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', nargs='+', help='Tokenized corpora')
    parser.add_argument('--window', '-w', type=int, help='Window size - number of tokens on each side')
    parser.add_argument('--direction', '-d', type=str, help='Window direction: left, right or both.')
    parser.add_argument('--terms', '-t', nargs='+', help='Terms of interest.')
    parser.add_argument('--output', '-o', help='Path to the output file.')
    args = parser.parse_args()

    return args

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

    save_to_csv(occurrences, f'{out}_{os.path.basename(data).split(".")[0]}.csv')

def main():
    args = parse_args()

    for corpus in args.input:
        pmi_score(corpus, args.window, args.direction, args.terms, args.output)

if __name__ == '__main__':
    main()