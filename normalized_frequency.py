from collections import defaultdict
from save_to_file import save_to_csv

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
    save_to_csv(occurrences, out)

def main():
    frequency('tokens_test.txt', 3, 'both', ['apple', 'cloud', 'stream', 'lamp'], 10000, 'occurrences_test.csv')

if __name__ == '__main__':
    main()