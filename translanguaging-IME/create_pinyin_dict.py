from pypinyin import pinyin, Style
import json

if __name__ == "__main__":
    my_dict = {}
    with open(".\\Cangie-Bopomofo\\my-frequent.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = lines[:131]
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) > 0]
        for line in lines:
            for word in line:
                keysrokes = pinyin(word, style=Style.NORMAL)
                if my_dict.get(keysrokes[0][0]) is None:
                    my_dict[keysrokes[0][0]] = [[word, 0]]
                else:
                    my_dict[keysrokes[0][0]].append([word, 0])

    with open(".\\pinyin_dict.json", "w", encoding="utf-8") as file:
        json.dump(my_dict, file, ensure_ascii=False, indent=4)
