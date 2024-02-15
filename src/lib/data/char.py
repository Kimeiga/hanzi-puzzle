# for this game, we will be trying to learn simplified chinese, since it will be the most useful in our daily life
# among the options of simplified, traditional, and japanese

# so we will use the simplified version of everything as the key

import json


def create_char_json():

    entries = {}

    with open('dictionary_char_2024-01-18.jsonl', 'r') as file:
        for line in file:
            entry = json.loads(line)

            # only add character if it has top words information
            if "statistics" in entry and len(entry.get('statistics', {}).get('topWords', [])) > 0 and 'tradVariants' not in entry:
                entries[entry['char']] = {k: v for k,
                                          v in entry.items() if k != '_id'}

    print(len(entries))

    # add ids information
    with open('character_strokes.json', 'r', encoding='utf-8') as file:
        char2strokes = json.load(file)

    # add ids information

    with open('ids.json', 'r', encoding='utf-8') as file:
        ids_data = json.load(file)

    for char, value in entries.items():
        if char in ids_data:
            value['ids'] = ids_data[char]
            value['ids_strokes'] = [char2strokes.get(
                char, 0) for char in value['ids']]
        else:
            print(char)

    with open('char.json', 'w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)

    with open('char_min.json', 'w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False, separators=(',', ':'))


def create_char_json_japanese():

    entries = {}

    with open('kanjidic2-en-3.5.0.json', 'r') as file:
        kanjidic = json.load(file)['characters']

    for kanji in kanjidic:
        if len(kanji['readingMeaning'].get('groups', [])) > 0 and kanji['misc']['jlptLevel'] != None and kanji['misc']['frequency'] != None:
            entries[kanji['literal']] = kanji

    # add ids information
    with open('character_strokes.json', 'r', encoding='utf-8') as file:
        char2strokes = json.load(file)

    with open('ids.json', 'r', encoding='utf-8') as file:
        ids_data = json.load(file)

    for char, value in entries.items():
        if char in ids_data:
            value['ids'] = ids_data[char]
            value['ids_strokes'] = [char2strokes.get(
                char, 0) for char in value['ids']]
        else:
            print(char)

    print(len(entries))

    with open('char.json', 'w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)

    with open('char_min.json', 'w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False, separators=(',', ':'))


def rest():

    with open("ids.json", 'r', encoding='utf-8') as file:
        ids_data = json.load(file)

    with open('char_min.json', 'r', encoding='utf-8') as file:
        entries = json.load(file)
        print(len(entries))

        print(type(entries))

        print(len(list(filter(lambda e: len(
            e.get('statistics', {}).get('topWords', [])) > 0, entries.values()))))

        print(len(list(filter(lambda e: len(
            e.get('statistics', {}).get('topWords', [])) > 0 and 'simpVariants' not in e, entries.values()))))


create_char_json()


def japanese_test():

    with open('kanjidic2-en-3.5.0.json', 'r') as file:
        kanjidic = json.load(file)['characters']

    s1 = set()
    s2 = set()
    s3 = set()
    s4 = set()

    print(len(kanjidic))

    for kanji in kanjidic:

        if kanji['misc']['frequency'] != None:
            print(kanji['misc']['frequency'])

        if 'readingMeaning' in kanji and len(kanji['readingMeaning'].get('groups', [])) > 0:
            s1.add(kanji['literal'])

            if kanji['misc']['frequency'] != None:
                s2.add(kanji['literal'])
            if kanji['misc']['grade'] != None:
                s3.add(kanji['literal'])
            if kanji['misc']['jlptLevel'] != None:
                s4.add(kanji['literal'])

    print(len(s1))
    print(len(s2))
    print(len(s3))
    print(len(s4))
