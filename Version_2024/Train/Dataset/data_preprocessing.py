import os

from joblib import Parallel, delayed
from tqdm import tqdm

if __name__ == "__main__":
    SRC_DATASET_PATH = ".\\Key_Stroke_Datasets\\"
    TARGET_DATASET_PATH = ".\\Train_Datasets\\"

    cut_sizes = [20, 5, 3]
    target_languages = ["bopomofo", "cangjie", "pinyin", "english"]
    error_rates = [0]


    data_file_names = ["bopomofo-cc100-0.txt", "cangjie-cc100-0.txt", "pinyin-cc100-0.txt", "english-0.txt"]

    for target_language in target_languages:
        for error_rate in error_rates:
            for cut_size in cut_sizes:

                CUT_SIZE = cut_size
                TARGET_LANGUAGE = target_language
                ERROR_RATE = error_rate

                target_file_name = "{}-{}-len{}.txt".format(TARGET_LANGUAGE, str(ERROR_RATE).replace(".", "_"), CUT_SIZE)

                if os.path.exists(TARGET_DATASET_PATH + target_file_name):
                    if "y" == input("File already exists. Do you want to overwrite it? (y/n)"):
                        print("Removing old file: " + target_file_name)
                        os.remove(TARGET_DATASET_PATH + target_file_name)
                    else:
                        print("File not overwritten. Exiting...")
                        exit()

                for file_name in tqdm(data_file_names, desc="Processing files"):
                    with open(SRC_DATASET_PATH + file_name, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        lines = [line.replace("\n", "") for line in lines] # remove the \n in the line
                        joined_lines = "".join(lines)
                        new_lines = [joined_lines[i:i + CUT_SIZE] for i in range(0, len(joined_lines), CUT_SIZE)]
                        new_lines = [line + "\t1" if TARGET_LANGUAGE in file_name else line + "\t0" for line in new_lines]
                    
                    with open(TARGET_DATASET_PATH + target_file_name, "a", encoding="utf-8") as file:
                        for line in new_lines:
                            file.write(line + "\n")
