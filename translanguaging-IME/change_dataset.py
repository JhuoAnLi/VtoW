import random
import string
from CangjieKeyMap.CangjieKeyMap import CangjieKeyMap
a = 1
with open("translanguaging-IME\datasets\englishwords.txt", "r") as file:
    word_list = [line.strip() for line in file]

with open(
    "translanguaging-IME\datasets\chinese_news_cangjie_mix.txt",
    "r",
    encoding="utf-8",
) as input_file, open(
    "translanguaging-IME\datasets\most15_newdataset.txt",
    "w",  # Use "a" for append mode
) as output_file:
    for line in input_file:
        line = line.strip()
        parts = line.split("\t")
        english_text = parts[0]
        chinese_text = parts[1]
        chinese_text = "".join(chinese_text)
        chinese_text_list = list(chinese_text)
        english_text_list = english_text.split()

        # if a != 10 and a < 10:
        #     print(chinese_text_list[1], english_text_list[1])
        # a += 1
        if len(chinese_text) <= 15:
            selected_word = random.choice(word_list)
            random_int = random.randint(0, 14)
            r = " " + selected_word + " "
            chinese_text_list.insert(random_int, r)
            # english_text_list.insert(random_int, selected_word)
        if len(chinese_text) > 15:
            selected_word = random.choice(word_list)
            random_int = random.randint(0, len(chinese_text) - 1)
            r = " " + selected_word + " "
            chinese_text_list.insert(random_int, r)
            # english_text_list.insert(random_int, selected_word)

        english_text = " ".join(english_text_list)
        chinese_text = "".join(chinese_text_list)
        output_file.write(chinese_text + "\n")

CHINESE_NEWS_TXT_PATH = "translanguaging-IME\datasets\test.txt"
CHINESE_NEWS_CANGJIE_MIX_PATH = "translanguaging-IME\datasets\chinese_mix_english.txt"

cangjie_key_map = CangjieKeyMap()

with open(CHINESE_NEWS_TXT_PATH, "r", encoding="utf-8") as news_file:
    with open(CHINESE_NEWS_CANGJIE_MIX_PATH, "w", encoding="utf-8") as news_mix_file:
        for line in news_file:
            line = line.strip()
            cangjie_line = cangjie_key_map.convert_to_cangjie_key(line)
            news_mix_file.write(cangjie_line + "\t" + line + "\n")
