from collections import defaultdict
import json
import re

# Initialize defaultdict of defaultdicts of lists
char2wordContainingChar = defaultdict(lambda: defaultdict(list))
# add ids information
with open('../character_strokes.json', 'r', encoding='utf-8') as file:
    char2strokes = json.load(file)
with open('../ids.json', 'r', encoding='utf-8') as file:
    ids_data = json.load(file)

with open('cedict_ts.u8', 'r', encoding='utf-8') as file:
    for line in file:
        if line.startswith("#") or not line.strip():
            continue

        match = re.match(r'^(\S+)\s+(\S+)\s+(\[[^]]+\])\s+(\/.*\/)$', line)
        if match:
            traditional, simplified, pronunciation, definitions = match.groups()

            # Prepare the definitions list, removing empty entries
            definition_list = [definition.strip() for definition in definitions.split(
                '/') if definition.strip()]

            obj = {'w': simplified,
                   'p': pronunciation[1:-1], 'd': definition_list}

            for char in simplified:
                # Filter out unwanted characters
                if char in ['ˋ', '，', '·', 'π', '、'] or ord(char) < 128 or char in ['ㄅ', 'ㄧ', 'ㄤ']:
                    continue

                # Append the object to the list for this character
                char2wordContainingChar[char]['w'].append(obj)

                if char in ids_data:
                    char2wordContainingChar[char]['i'] = ids_data[char]
                    char2wordContainingChar[char]['s'] = [char2strokes.get(
                        char, 0) for char in ids_data[char]]
                else:
                    print(char)


for char, wordList in char2wordContainingChar.items():

    if all(word['w'] != char for word in wordList['w']):
        print(char)


with open('char2wordContainingChar.json', 'w', encoding='utf-8') as file:
    json.dump(char2wordContainingChar, file, ensure_ascii=False, indent=4)
with open('char2wordContainingChar_min.json', 'w', encoding='utf-8') as file:
    json.dump(char2wordContainingChar, file,
              ensure_ascii=False, separators=(',', ':'))

'''
todo:
𠈌
傢
碁
濙
堃
皙
阢
榘
鱆
'''
