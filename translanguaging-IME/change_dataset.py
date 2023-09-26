import random
import string
from CangjieKeyMap import CangjieKeyMap

with open("VtoW\\translanguaging-IME\\datasets\\englishwords.txt", "r") as file:
    word_list = [line.strip() for line in file]

with open(
    "VtoW\\translanguaging-IME\\datasets\\chinese_news_cangjie_mix.txt",
    "r",
    encoding="utf-8",
) as input_file, open(
    "VtoW\\translanguaging-IME\\datasets\\most15_newdataset.txt",
    "w",  # Use "a" for append mode
) as output_file:
    for line in input_file:
        line = line.strip()  # Remove trailing newline and spaces
        parts = line.split("\t")  # Split the line into English and Chinese parts
        english_text = parts[0]
        chinese_text = parts[1]
        chinese_text = " ".join(chinese_text)

        selected_word = random.choice(word_list)
        if len(chinese_text) <= 15:
            random_int = random.randint(0, 14)
            chinese_text_list = list(chinese_text)
            r = " " + selected_word + " "
            chinese_text_list.insert(random_int, r)
        if len(chinese_text) > 15:
            random_int = random.randint(0, len(chinese_text) - 1)
            chinese_text_list = list(chinese_text)
            r = " " + selected_word + " "
            chinese_text_list.insert(random_int, r)
        # english_text_list = english_text.split()
        # # print(english_text_list)
        # english_text_list.insert(random_int, selected_word)
        # english_text = " ".join(english_text_list)
        # # print(random_int)
        chinese_text = "".join(chinese_text_list)
        output_file.write(chinese_text + "\n")
