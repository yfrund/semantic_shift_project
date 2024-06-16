import os
import argparse

def merge_txt_files(folder_path, output_file):
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')

def main():
    parser = argparse.ArgumentParser(description="Merge content of all text files in a folder.")
    parser.add_argument("--input", "-i", help="Path to the folder containing the text files.")
    parser.add_argument("--output", "-o", help="Path to the output file.")
    args = parser.parse_args()

    merge_txt_files(args.input, args.output)

if __name__ == "__main__":
    main()
