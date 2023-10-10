import pandas as pd
import json
from pypinyin import pinyin, lazy_pinyin, Style
import re

xlsx_file = pd.ExcelFile('臺灣華語文能力基準詞語表_111-11-14.xlsx')

sheet_names = xlsx_file.sheet_names
df = pd.read_excel(xlsx_file, sheet_names[0])
selected_col = ["詞語", "書面字頻(每百萬字)"]

df = df[selected_col]
# print(df.head())

bopomofo_dict = json.loads(open("bopomofo_dict_with_frequency.json", "r").read())

def bopomofo_to_keystroke(bopomofo:str) -> str:
    map = {
        "ㄅ": "1", "ㄆ": "q", "ㄇ": "a",
        "ㄈ": "z", "ㄉ": "2", "ㄊ": "w",
        "ㄋ": "s", "ㄌ": "x", "ㄍ": "e",
        "ㄎ": "d", "ㄏ": "c", "ㄐ": "r",
        "ㄑ": "f", "ㄒ": "v", "ㄓ": "5",
        "ㄔ": "t", "ㄕ": "g", "ㄖ": "b",
        "ㄗ": "y", "ㄘ": "h", "ㄙ": "n",
        "ㄚ": "8", "ㄛ": "i", "ㄜ": "k",
        "ㄝ": ",", "ㄞ": "9", "ㄟ": "o",
        "ㄠ": "l", "ㄡ": ".", "ㄢ": "0",
        "ㄣ": "p", "ㄤ": ";", "ㄥ": "/",
        "ㄦ": "-", "ㄧ": "u", "ㄨ": "j",
        "ㄩ": "m", "ˊ": "6", "ˇ": "3",
        "ˋ": "4",  "˙": "7",
    }

    keystroke = ""
    for word in bopomofo:
        keystroke += map[word]
    return keystroke

def sort_dict_by_value(my_dict: dict) -> dict:
    for key in my_dict:
        # Sort, considering None as a very low value
        my_dict[key] = sorted(my_dict[key].items(), key=lambda x: x[1] if x[1] is not None else float('-inf'), reverse=True)
    return my_dict


for i, (index, row) in enumerate(df.iterrows()):
    word = row["詞語"]
    frequency = row["書面字頻(每百萬字)"]
    
    word = re.sub(r"\d", "", word)
    word = re.sub(r"\(\w\)", "", word)
    words = word.split("/")
    for word in words:
        BOPOMOFO_result = ""
        for pin in pinyin(word, style=Style.BOPOMOFO):
            BOPOMOFO_result += pin[0]
        # print(BOPOMOFO_result)
        keystoke = bopomofo_to_keystroke(BOPOMOFO_result)

        if keystoke in bopomofo_dict:
            bopomofo_dict[keystoke][word] = frequency
        else:
            bopomofo_dict[keystoke] = {word: frequency}
        print(keystoke, bopomofo_dict[keystoke])

bopomofo_dict = sort_dict_by_value(bopomofo_dict)

# json.dump(bopomofo_dict, open("bopomofo_dict_with_frequency.json", "w", encoding="utf-8"))
# print(bopomofo_dict[:10])