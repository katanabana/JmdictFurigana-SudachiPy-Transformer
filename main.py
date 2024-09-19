import os
import json
import sys
from collections import defaultdict

from wanakana import to_katakana


def main():
    # Retrieve initial_directory and transformed_directory from command-line arguments
    initial_directory, transformed_filename = sys.argv[1:3]
    encoding = 'utf-8-sig'  # Specify UTF-8 encoding with BOM (Byte Order Mark)

    transformed_dictionary = defaultdict(lambda: defaultdict(list))
    # Iterate through files in initial_directory
    for filename in os.listdir(initial_directory):
        # Construct paths for initial and transformed files
        initial_path = os.path.join(initial_directory, filename)

        print(f'transforming "{initial_path}"')

        # Load initial JSON dictionary file
        with open(initial_path, encoding=encoding) as initial_file:
            initial_dictionary = json.load(initial_file)

        # Process each item in the initial dictionary
        for item in initial_dictionary:
            parts = []

            # Process furigana parts in each item
            for part in item['furigana']:
                reading = part.get('rt', part['ruby'])  # Use 'rt' if available, else 'ruby'
                part = [part['ruby'], to_katakana(reading)]  # Transform part reading to katakana
                parts.append(part)

            reading = to_katakana(item['reading'])
            # Choose parts with the maximum length for the same reading
            if len(transformed_dictionary[item['text']][reading]) < len(parts):
                transformed_dictionary[item['text']][reading] = parts

    # Write transformed dictionary to a new JSON file
    with open(transformed_filename, 'w+', encoding=encoding) as transformed_file:
        json.dump(transformed_dictionary, transformed_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
