import pandas as pd
import json
import re
from pypinyin import pinyin, Style


if __name__ == "__main__":

    xlsx_file = pd.ExcelFile('.\\datasets\\臺灣華語文能力基準漢字表_111-09-20.xlsx')

    sheet_names = xlsx_file.sheet_names
    df = pd.read_excel(xlsx_file, sheet_names[0])
    selected_col = ["漢字", "書面字頻（每百萬字）"]

    df = df[selected_col]
    # print(df.head())

    src_dict = json.loads(open("pinyin_dict.json", "r", encoding="utf-8").read())

    for i, (index, row) in enumerate(df.iterrows()):
        word = row["漢字"]
        frequency = row["書面字頻（每百萬字）"]
        
        word = re.sub(r"\d", "", word)
        word = re.sub(r"\(\w\)", "", word)
        words = word.split("/")
        for word in words:
            keystoke = pinyin(word, style=Style.NORMAL)[0][0]
            print(keystoke, word, frequency)
            if keystoke in src_dict:
                for w, f in src_dict[keystoke]:
                    if w == word:
                        src_dict[keystoke].remove([w, f])
                        src_dict[keystoke].append([w, frequency])
                        break
            else:
                src_dict[keystoke] = [[word, frequency]]
            print(keystoke, src_dict[keystoke])

    for keystoke in src_dict:
        src_dict[keystoke] = sorted(src_dict[keystoke], key=lambda x: x[1], reverse=True)
    json.dump(src_dict, open("pinyin_dict_with_frequency.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)