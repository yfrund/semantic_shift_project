import os
import re
import xml.etree.ElementTree as ET

def extract_text_by_period(start_year, end_year, corpus_root):
    extracted_text = []
    #match different naming conventions
    year_patterns = [
        re.compile(r'__(\d{4})'),
        re.compile(r'__\w+-(\d{4})'),
        re.compile(r'__\w+-\w+-(\d{4})')
    ]


    for root, _, files in os.walk(corpus_root):
        for file in files:
            file_year = None
            for pattern in year_patterns:
                match = pattern.search(file)
                if match:
                    file_year = int(match.group(1))
                    # print(file_year)
                    break
            if file_year and start_year <= file_year <= end_year:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:

                    with open(file_path, 'r', encoding='ISO-8859-1') as f:
                        content = f.read()

                extracted_text.append(extract_text_from_xml(content))

    return extracted_text

def extract_text_from_xml(content):
    try:
        root = ET.fromstring(content)

        return ' '.join(root.itertext())
    except ET.ParseError:
        return ''

def main():
    period1 = [2001, 2005]
    period2 = [2008, 2012]
    corpus_root = 'europarl'

    period1_text = extract_text_by_period(*period1, corpus_root)
    period2_text = extract_text_by_period(*period2, corpus_root)

    period1_combined_text = ' '.join(period1_text)
    period2_combined_text = ' '.join(period2_text)


    output_file1 = f'corpus_{period1[0]}_{period1[1]}.txt'
    output_file2 = f'corpus_{period2[0]}_{period2[1]}.txt'
    with open(output_file1, 'w', encoding='utf-8') as f:
        f.write(period1_combined_text)

    with open(output_file2, 'w', encoding='utf-8') as f:
        f.write(period2_combined_text)

    print(f'Extraction complete')

if __name__=='__main__':
    main()