import json


def map_characters_to_strokes(file_path='Unihan_IRGSources.txt'):
    entries = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if 'kTotalStrokes' in line:
                parts = line.strip().split('\t')
                if len(parts) > 2:
                    # Extract code point (e.g., "U+3400") and convert to character
                    code_point = parts[0]
                    char = chr(int(code_point[2:], 16))
                    # Extract total strokes
                    total_strokes = parts[2]
                    print(char)
                    print(code_point)
                    entries[char] = int(total_strokes.split(' ')[-1])

    return entries


entries = map_characters_to_strokes()

# Output to a minified JSON file
with open('character_strokes.json', 'w', encoding='utf-8') as json_file:
    json.dump(entries, json_file, ensure_ascii=False, separators=(',', ':'))

print("Mapping completed and saved to character_strokes.json.")
