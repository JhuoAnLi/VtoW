import os

from joblib import Parallel, delayed
from tqdm import tqdm

if __name__ == "__main__":
    SRC_DATASET_PATH = os.path.join(os.path.dirname(__file__) , ".\\Key_Stroke_Datasets\\")
    TARGET_DATASET_PATH = os.path.join(os.path.dirname(__file__) , ".\\Train_Datasets\\")
    CUT_SIZE = 20
    TARGET_LANGUAGE = "bopomofo"
    ERROR_RATE = 0

    data_file_names = ["bopomofo-news-0.txt", "cangjie-news-0.txt", "pinyin-news-0.txt", "english-0.txt"]

    target_file_name = "{}-{}.txt".format(TARGET_LANGUAGE, str(ERROR_RATE).replace(".", "_"))


    if os.path.exists(TARGET_DATASET_PATH + target_file_name):
       print("Removing old file: " + target_file_name)
       os.remove(TARGET_DATASET_PATH + target_file_name)

    for file_name in tqdm(data_file_names, desc="Processing files"):
        with open(SRC_DATASET_PATH + file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            lines = [line.replace("<ctrl>", "") for line in lines]  # remove the <ctrl> in the line
            lines = [line.replace("\n", "") for line in lines] # remove the \n in the line
            joined_lines = "".join(lines)
            new_lines = [joined_lines[i:i + CUT_SIZE] for i in range(0, len(joined_lines), CUT_SIZE)]
            new_lines = [line + "\t1" if TARGET_LANGUAGE in file_name else line + "\t0" for line in new_lines]
        
        with open(TARGET_DATASET_PATH + target_file_name, "a", encoding="utf-8") as file:
            for line in new_lines:
                file.write(line + "\n")
