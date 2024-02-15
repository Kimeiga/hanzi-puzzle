from collections import defaultdict
from collections import deque
import json
import re

entries = {}

unencoded_components = {
    "{1}":  "⿹⿺㇉一灬",
    "{2}":  "⿱⺈𫩏",
    "{3}":  "⿱⺈⿵冂人",
    "{4}":  "⿱⺌冖",
    "{5}":  "⿸⿰丨コ𠄠",
    "{6}":  "⿰丨亖",
    "{7}":  "⿻一申⿰㇀丶",
    "{8}":  "⿻⿱㇒一乚",
    "{9}":  "⿱⿰㇒㇖丨",
    "{10}":  "⿻⿻㇈丿丶",
    "{11}":  "⿰⿱丶㇀⿱㇒丶",
    "{12}":  "⿱⺊⿷己三",
    "{13}":  "⿸⿰丿⿱⺊⺂七",
    "{14}":  "ユ儿",
    "{15}":  "⿻𱍸㇒",
    "{16}":  "⿲⿺𠄌⺀⿺𠄌⺀㇂",
    "{17}":  "良",
    "{18}":  "良",
    "{19}":  "⿻日乂",
    "{20}":  "丸",
    "{21}":  "⿰⺼又",
    "{22}":  "⿺㇉一",
    "{23}":  "⿹⿺㇉一丨",
    "{24}":  "⿰丨く",
    "{25}":  "⿱一⿰𠄌⿺乀丿",
    "{26}":  "⿱亠⿲刀丫⿸⿱丿𠄌㇏",
    "{27}":  "⿱𠃋𠃋",
    "{28}":  "⿻弋一",
    "{29}":  "⿻弋𢆶",
    "{30}":  "⿻𠃋㇇",
    "{31}":  "⿴囗⿻𰀪丶",
    "{32}":  "⿱⿻𠮛⿰丨丨冖",
    "{33}":  "弓",
    "{34}":  "⿹勹丿",
    "{35}":  "⿻几𠄠",
    "{36}":  "",
    "{37}":  "⿱⺊冖",
    "{38}":  "⿱𰀉冖",
    "{39}":  "匕",
    "{40}":  "亞",
    "{41}":  "⿻𦉫𠄠",
    "{42}":  "彐",
    "{43}":  "⺕",
    "{44}":  "⿱十冖",
    "{45}":  "⿱⿰一丨㇀",
    "{46}":  "⿻日乚",
    "{47}":  "⊖鳥灬",
    "{48}":  "㐄",
    "{49}":  "⿰丨丿",
    "{50}":  "コ",
    "{51}":  "⿺㇉⿻三丨",
    "{52}":  "𢎘",
    "{53}":  "⿴⿱丿𢎘丶",
    "{54}":  "丿⿹⿺㇉⿱コ一",
    "{55}":  "⿸广⿻コ⿰丨丨",
    "{56}":  "⿳𠂉卌一",
    "{57}":  "⿺𠂇丨",
    "{58}":  "𠂎",
    "{59}":  "⿹勹灬",
    "{60}":  "？",
    "{61}":  "戕",
    "{62}":  "⿻丅⿱艹二",
    "{63}":  "舟",
    "{64}":  "？",
    "{65}":  "？",
    "{66}":  "？",
    "{67}":  "⿴⿰丨丨𠄠",
    "{68}":  "⿻土⿻丷口",
    "{69}":  "？",
    "{70}":  "业",
    "{71}":  "𠀉",
    "{72}":  "𠀉",
    "{73}":  "⿴𠀃三",
    "{74}":  "？",
    "{75}":  "？",
    "{76}":  "⿰丨三",
    "{77}":  "？",
    "{78}":  "⿱⿻口⿰丨丨一",
    "{79}":  "亞",  # "⿱⿰⿳㇑㇐㇞⿳㇞㇐㇑㇐",
    "{80}":  "⿱冖八",
    "{81}":  "？",
    "{82}":  "⿱𦘒一",
    "{83}":  "⿳亠丷冖",
    "{84}":  "⿰丿乛",
    "{85}":  "⿰丿⿱丶乛",
    "{86}":  "⿲丶丶丶",
    "{87}":  "⿳亠口冖",
    "{88}":  "⿵𠆢一",
    "{89}":  "？",
    "{90}":  "？",
    "{91}":  "⿱⿱⿽⿺⿰丨㇕㇐㇐㇑㇗",
    "{92}":  "？",
    "{93}":  "⿻昌乚",
    "{94}":  "共",
    "{95}":  "⿻尸一",
    "{96}":  "？",
    "{97}":  "⿺⿻㇂丿丶",
    "{98}":  "⿻一曲",
    "{99}":  "⿻𦉫𠄠",
    "{100}":  "⿱㇇乀",
    "{101}":  "？",
    "{102}":  "？",
    "{103}":  "？",
    "{104}":  "？",
    "{105}":  "？",
    "{106}":  "？",
    "{107}":  "？",
    "{108}":  "𭁟",
    "{109}":  "⿻⿱㇒一丿",
    "{110}":  "冂",
    "{111}":  "？",
    "{112}":  "⿵⿰⿰丿丨𠃍一",
    "{113}":  "⿵冂八",
    "{114}":  "⿱土八",
    "{115}":  "⿻𰀪⺀",
    "{116}":  "？",
    "{117}":  "⿺𠃊⺊",
    "{118}":  "？",
    "{119}":  "⿻己⿱工工",
    "{120}":  "匚",
    "{121}":  "⿱⺈罒",
}

radical_substitutions = {
    "牜": "牛",
    "𤣩": "玉",
    "𥫗": "竹",
    "艹": "艸",
    "月": "肉",
    "糹": "糸",
    "訁": "言",
    "釒": "金",
    "飠": "食",
    "⻠": "食",
    "忄": "心",
    "犭": "犬",
    "⺝": "月",
    "讠": "言",
    "亻": "人",
    "氵": "水",
    "扌": "手",
    "⻐": "金",
    "⻗": "雨",
}


def replace_components(match):
    key = match.group(0)
    return unencoded_components.get(key, key)


def replace_radicals(text):
    for key, value in radical_substitutions.items():
        text = text.replace(key, value)
    return text


with open('ids.txt', 'r', encoding='utf-8-sig') as file:
    lines = file.read().split('\n')

    for line_number, line in enumerate(lines):
        if line.startswith('#') or not line:
            continue

        parts = line.split("\t")

        # Substitute unencoded components
        parts[2] = re.sub(
            r'\{(\d+)\}', lambda m: replace_components(m), parts[2])

        # Substitute radicals after replacing unencoded components
        # parts[2] = replace_radicals(parts[2])

        pattern = r'\^(.*?)\$'
        matches = re.findall(pattern, parts[2])

        characters_between = ''.join(
            # c for match in matches for c in match if c not in '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〾↔↷') if matches else None
            c for match in matches for c in match if c not in '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〾↔↷⊖') if matches else None

        if characters_between:
            entries[parts[1]] = characters_between

final_entries = {}

with open('char_min.json', 'r', encoding='utf-8') as file:
    char2entry = json.load(file)

stop_set = set(["亻", "丶", "一", "丨", "丿", "乀",
               "二", "丷", "亠", "冖", "丁", "冂", "人"])


def decompose(value, depth=0):
    if len(value) == 1:
        return value
    if '⊖' in value:
        return value.replace('⊖', '')

    ret = ""

    for char in value:
        if char in entries and char not in entries[char] and all(c in char2entry for c in entries[char]) and all(c not in stop_set for c in entries[char]):
            ret += decompose(entries[char], depth=1)
        else:
            ret += char

        # if char in entries and char not in entries[char]:
        #     ret += decompose(entries[char], depth=1)
        # else:
        #     ret += value

    return ret


def bfs_decompose(char):
    cur_list = entries[char]
    nxt_list = ""

    while True:
        stop_search = False
        for c in cur_list:
            if c not in entries or c in entries[c] or "？" in entries[c] or c not in char2entry:
                stop_search = True
                break
            nxt_list += entries[c]

        if stop_search:
            return cur_list

        cur_list = nxt_list
        nxt_list = ""


all_components = defaultdict(set)

with open('character_strokes.json', 'r', encoding='utf-8') as file:
    char2strokes = json.load(file)


# figure out the heuristic for when to stop decomposing
for key, value in entries.items():

    # print(key)
    # if key == "㠶":
    # if key == "𩁨":
    #     print(value)
    if "？" in value:
        continue

    # temporarily just use the regular stuff to be easy

    # full_decomposition = decompose(value)
    full_decomposition = value

    for char in full_decomposition:
        if char not in char2strokes:
            # print(char)
            all_components[0].add(char)
        else:
            all_components[char2strokes[char]].add(char)

    final_entries[key] = full_decomposition


with open('ids.json', 'w', encoding='utf-8') as file:
    json.dump(final_entries, file, ensure_ascii=False, indent=4)

with open('ids_min.json', 'w', encoding='utf-8') as file:
    json.dump(final_entries, file, ensure_ascii=False, separators=(',', ':'))

print(len(all_components))

# Convert all sets to lists for JSON compatibility
all_components_list = defaultdict(
    list, {k: list(v) for k, v in all_components.items()})

# Now you can serialize all_components_list to JSON
with open('all_components.json', 'w', encoding='utf-8') as file:
    json.dump(all_components_list, file,
              ensure_ascii=False, separators=(',', ':'))
