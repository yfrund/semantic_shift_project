from collections import defaultdict
from save_to_file import save_to_csv
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', nargs='+', help='Tokenized corpora')
    parser.add_argument('--window', '-w', type=int, help='Window size - number of tokens on each side')
    parser.add_argument('--direction', '-d', type=str, help='Window direction: left, right or both.')
    parser.add_argument('--terms', '-t', nargs='+', help='Terms of interest.')
    parser.add_argument('--rate', '-r', type=int, help='Occurrence rate for normalized frequency.')
    parser.add_argument('--output', '-o', help='Path to the output file.')
    args = parser.parse_args()

    return args
def normalize(occurences,length, rate):
    for term in occurences:
        for context_word in occurences[term]:
            freq = occurences[term][context_word]/length*rate
            occurences[term][context_word] = freq


def frequency(data, window, direction, terms, rate, out):
    occurrences = {term: defaultdict(int) for term in terms}
    with open(data, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        length = len(lines)
        for i, line in enumerate(lines):
            line = line.lower().strip()
            if line in terms:
                if direction == 'right':
                    context = lines[i+1:i+window+1]
                    for c in context:
                        occurrences[line][c.strip()] +=1
                elif direction == 'left':
                    context = lines[i-window:i]
                    for c in context:
                        occurrences[line][c.strip()] +=1
                elif direction == 'both':
                    context = lines[i-window:i]+lines[i+1:i+window+1]
                    for c in context:
                        occurrences[line][c.strip()] +=1
    normalize(occurrences, length, rate)
    print(occurrences)
    save_to_csv(occurrences, f'{out}_{os.path.basename(data).split(".")[0]}.csv')

def main():
    args = parse_args()
    for corpus in args.input:
        frequency(corpus, args.window, args.direction, args.terms, args.rate, args.output)

if __name__ == '__main__':
    main()
    # frequency('data/corpus_2001_2005.txt.lemmas', 3, 'both', ['veto', 'impeachment', 'subpoena'], 100, 'test.csv')