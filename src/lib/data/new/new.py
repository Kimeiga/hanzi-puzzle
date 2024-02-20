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

cedict = {}

with open('cedict_ts.u8', 'r', encoding='utf-8') as file:
    for line_num, line in enumerate(file, 1):
        if line.startswith("#") or not line.strip():
            continue

        match = re.match(r'^(\S+)\s+(\S+)\s+(\[[^]]+\])\s+(\/.*\/)$', line)
        if match:
            traditional, simplified, pronunciation, definitions = match.groups()

            cedict[simplified] = {'p': pronunciation[1:-1]}

            # Prepare the definitions list, removing empty entries
            definition_list = [definition.strip() for definition in definitions.split(
                '/') if definition.strip()]

            obj = {'w': simplified,
                   'p': pronunciation[1:-1], 'd': definition_list}

            for char in simplified:
                # Filter out unwanted characters
                if char in ['ˋ', '，', '·', 'π', '、'] or ord(char) < 128 or char in ['ㄅ', 'ㄧ', 'ㄤ']:
                    continue

                if char == simplified:
                    char2wordContainingChar[char]['c'] = obj
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

    # if all(word['w'] != char for word in wordList['w']):
    #     print(char)

    if 'c' not in wordList:
        print(char)

with open("subtlex.json", "r", encoding='utf-8') as file:
    subtlex_data = json.load(file)

dictionary_char = {}

with open("../dictionary_char_2024-01-18.jsonl", "r", encoding='utf-8') as file:
    for line in file:
        entry = json.loads(line)
        dictionary_char[entry['char']] = entry

# for char in


dictionary_word = {}
with open("dictionary_word_2024-01-18.jsonl", "r", encoding='utf-8') as file:
    for line in file:
        entry = json.loads(line)
        dictionary_word[entry['simp']] = entry

final_entries = defaultdict(lambda: defaultdict(list))
print('starting')

notInCedict = {
    "拗陷": "ào​xiàn",
    "斐济岛": "Fěi​jì​Dǎo",
    "颖上县": "Yǐng​shàng​xiàn"
}


def convert_numerical_pinyin_to_tone_marks(pinyin_with_number):
    tone_marks = {
        'a': ['ā', 'á', 'ǎ', 'à'],
        'e': ['ē', 'é', 'ě', 'è'],
        'i': ['ī', 'í', 'ǐ', 'ì'],
        'o': ['ō', 'ó', 'ǒ', 'ò'],
        'u': ['ū', 'ú', 'ǔ', 'ù'],
        'ü': ['ǖ', 'ǘ', 'ǚ', 'ǜ']
    }

    # Extract the tone number and remove it from the syllable
    tone_number = int(pinyin_with_number[-1])
    pinyin = pinyin_with_number[:-1]

    # Handle the fifth tone (neutral tone) directly
    if tone_number == 5:
        return pinyin  # Return the pinyin without any tone mark

    adjusted_tone_number = tone_number - 1  # Adjust for array indexing

    # Find the main vowel to apply the tone mark to
    for vowel in tone_marks:
        if vowel in pinyin:
            # Replace the vowel with its toned counterpart
            return pinyin.replace(vowel, tone_marks[vowel][adjusted_tone_number])
    # Return original if no match (shouldn't happen in proper pinyin)
    return pinyin_with_number


for char in subtlex_data[:3000]:
    if char in ["𠈌",
                "傢",
                "碁",
                "濙",
                "堃",
                "皙",
                "阢",
                "榘",
                "鱆"]:
        print(char)

    longest = 0
    longest_char = ""

    # if char in dictionary_char:
    #     if 'statistics' not in dictionary_char[char]:
    #         print("statistics not in dictionary_char ", char)

    #     if 'topWords' not in dictionary_char[char]['statistics']:
    #         print("topWords not in dictionary_char ", char)

    #     if dictionary_char[char]['statistics']['topWords'] == []:
    #         print("topWords is empty in dictionary_char ", char)

    #     if len(dictionary_char[char]['statistics']['topWords']) == 1:
    #         print("topWords is length 1 in dictionary_char ", char)
    #         print(dictionary_char[char]['statistics']['topWords'])

    #     if len(dictionary_char[char]['statistics']['topWords']) > longest:
    #         longest = len(dictionary_char[char]['statistics']['topWords'])
    #         longest_char = char

    # else:
    #     print("not in dictionary_char ", char)

    # final_entries[char] = char2wordContainingChar[char]
    top_words = dictionary_char[char]['statistics']['topWords']

    for index, word in enumerate(top_words):

        if word['word'] in cedict:
            top_words[index]['p'] = ''.join(
                map(convert_numerical_pinyin_to_tone_marks, [c for c in cedict[word['word']]['p'].split(' ') if c.isalnum()]))
        else:
            objs = [item for item in dictionary_word[word['word']]
                    ['items'] if item['source'] == 'cedict']

            # print(objs)

            if len(objs) > 0:
                if len(objs) == 1:
                    top_words[index]['p'] = objs[0]['pinyin']
                else:
                    print(word['word'], ' more than one cedict entry')
            else:
                top_words[index]['p'] = notInCedict[word['word']]

            if len(objs) > 1:
                print(word['word'])
            if len(objs) == 0:
                print(word['word'])

            # print(word['word'])

    final_entries[char]['w'] = [w for w in dictionary_char[char]
                                ['statistics']['topWords'] if w['word'] != char]
    final_entries[char]['c'] = next(
        (w for w in dictionary_char[char]['statistics']['topWords'] if w['word'] == char), None)
    final_entries[char]['i'] = ids_data[char]
    final_entries[char]['s'] = [char2strokes.get(
        char, 0) for char in ids_data[char]]

print(longest)
print(longest_char)

with open('char2wordContainingChar.json', 'w', encoding='utf-8') as file:
    json.dump(final_entries, file, ensure_ascii=False, indent=4)
with open('char2wordContainingChar_min.json', 'w', encoding='utf-8') as file:
    json.dump(final_entries, file,
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
