import os
from MyLib.KeyStrokeConverter import KeyStrokeConverter
from MyLib.TypoGenerater import TypoGenerater
from joblib import Parallel, delayed
from tqdm import tqdm

def process_file(file_path, convert_type, error_rate):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            data = ""
            for line in lines:
                data += TypoGenerater.generate(KeyStrokeConverter.convert(line.strip(), convert_type), error_rate) + "\n"

            filename = "{}-cc100-{}.txt".format(convert_type, str(error_rate).replace(".", "_"))
            with open(TARGET_DATASET_PATH + filename, "w", encoding="utf-8") as file2:
                file2.write(data)
                
            print("Dataset with keystroke type: {} error rate: {}, created successfully: {}".format(
                convert_type, error_rate, filename))
    except Exception as e:
        print("Error: " + str(e))

if __name__ == '__main__':
    PLAIN_TEXT_DATASET_PATH = ".\\Dataset\\Plain_Text_Datasets\\"
    TARGET_DATASET_PATH = ".\\Dataset\\Key_Stroke_Datasets\\"

    files = ["Chinese_WebCrawlData_cc100.txt"]
    convert_types = ["pinyin"]
    error_rates = [0, 0.001, 0.003, 0.01, 0.05, 0.1]

    def process_wrapper(file, convert_type, error_rate):
        process_file(os.path.join(PLAIN_TEXT_DATASET_PATH, file), convert_type, error_rate)

    # Wrap the Parallel call with tqdm to display the progress bar
    Parallel(n_jobs=-1)(
        delayed(process_wrapper)(file, convert_type, error_rate)
        for file in tqdm(files, desc="Processing files")
        for convert_type in tqdm(convert_types, desc="Processing conversion types", leave=False)
        for error_rate in tqdm(error_rates, desc="Processing error rates", leave=False)
    )
