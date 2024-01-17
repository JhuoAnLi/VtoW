import os

from MyLib.KeyStrokeConverter import KeyStrokeConverter
from MyLib.TypoGenerater import TypoGenerater


if __name__ == '__main__':
    PLAIN_TEXT_DATASET_PATH = ".\\Dataset\\Plain_Text_Datasets\\"
    TARGET_DATASET_PATH = ".\\Dataset\\Key_Stroke_Datasets\\"

    files = ["Chinese_cleaned.txt"]
    convert_types = ["bopomofo"] #, "pinyin"]
    error_rates = [0, 0.001, 0.003, 0.01 ,0.05, 0.1]

    
    for file in files:
        with open(PLAIN_TEXT_DATASET_PATH + file, "r", encoding="utf-8") as file:
            lines = file.readlines()

            for convert_type in convert_types:
                for error_rate in error_rates:
                    filename = "{}-{}.txt".format(convert_type, str(error_rate).replace(".", "_"))

                    if os.path.exists(TARGET_DATASET_PATH + filename) == False:
                        try:
                            data = ""
                            for line in lines:
                                data += TypoGenerater.generate(KeyStrokeConverter.convert(line.strip(), convert_type), error_rate) + "\n"
                            
                            translation_table = str.maketrans({str(i): "" for i in range(10)})

                            

                            with open(TARGET_DATASET_PATH + filename, "w", encoding="utf-8") as file2:
                                    file2.write(data)
                            print("Dataset with keystroke type: {} error rate: {}, created successfully: ".format(convert_type, error_rate) + filename)
                        except Exception as e:
                            print("Error: " + str(e))
                    else:
                        print("File already exists: " + filename)