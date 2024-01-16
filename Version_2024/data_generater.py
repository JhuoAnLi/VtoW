import os

from MyLib.KeyStrokeConverter import KeyStrokeConverter
from MyLib.TypoGenerater import TypoGenerater


if __name__ == '__main__':
    PLAIN_TEXT_DATASET_PATH = ".\\Dataset\\Plain_Text_Datasets\\"
    TARGET_DATASET_PATH = ".\\Dataset\\Key_Stroke_Datasets\\"

    files = ["English.txt"]
    convert_types = ["english"]#, "cangjie", "bopomofo", "pinyin"]
    error_rates = [0, 0.001, 0.003, 0.01 ,0.05, 0.1]

    
    for file in files:
        with open(PLAIN_TEXT_DATASET_PATH + file, "r", encoding="utf-8") as file:
            lines = file.readlines()

                

            for convert_type in convert_types:
                for error_rate in error_rates:
                    filename = "{}-{}.txt".format(convert_type, str(error_rate).replace(".", "_"))

                    if os.path.exists(TARGET_DATASET_PATH + filename) == False:
                        with open(TARGET_DATASET_PATH + filename, "w", encoding="utf-8") as file2:
                            for line in lines:
                                file2.write(TypoGenerater.generate(KeyStrokeConverter.convert(line.strip(), convert_type), error_rate) + "\n")


    # input_string = "你好嗎"
    # convert_type = "pinyin"
    # print(KeyStrokeConverter.convert(input_string, convert_type))
    # print(TypoGenerater.generate(input_string, 0.2))