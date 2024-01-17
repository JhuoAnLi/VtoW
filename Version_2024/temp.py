import os
import json

from MyLib.KeyStrokeConverter import KeyStrokeConverter
from MyLib.TypoGenerater import TypoGenerater
from MyLib.LanguageCleaner import LanguageCleaner

if __name__ == '__main__':
    PLAIN_TEXT_DATASET_PATH = ".\\Dataset\\Plain_Text_Datasets\\"
    TARGET_DATASET_PATH = ".\\Dataset\\Key_Stroke_Datasets\\"

    files = ["Chinese.txt"]

    
    for file in files:
        with open(PLAIN_TEXT_DATASET_PATH + file, "r", encoding="utf-8") as file:
            json_file = json.load(file)
            lines = [line["內容"] for line in json_file]

            lines = [LanguageCleaner.cleanChinese(line) for line in lines]

            with open(PLAIN_TEXT_DATASET_PATH + "Chinese_cleaned.txt", "w", encoding="utf-8") as file2:
                file2.write("\n".join(lines))
