import os

from tqdm import tqdm

if __name__ == "__main__":
    SRC_DATASET_PATH = ".\\Train_Datasets\\"
    TARGET_DATASET_PATH = ".\\Train_Datasets\\"

    target_languages = ["bopomofo", "cangjie", "pinyin", "english"]
    error_rates = [0]


    data_file_names = ["bopomofo-cc100-0-train.txt", "cangjie-cc100-0-train.txt", "pinyin-cc100-0-train.txt", "english-0-train.txt"]

    for file in os.listdir(TARGET_DATASET_PATH):
        if not file.endswith("-train.txt"):
            os.remove(TARGET_DATASET_PATH + file)
        elif file.find("-len") > 0:
            os.remove(TARGET_DATASET_PATH + file)
    
    for target_language in target_languages:
        for error_rate in error_rates:
            TARGET_LANGUAGE = target_language
            ERROR_RATE = error_rate
            CUT_SIZE = 3

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
                    new_lines = [line + "\t1" if TARGET_LANGUAGE in file_name else line + "\t0" for line in lines]
                
                with open(os.path.join(TARGET_DATASET_PATH, target_file_name), "a", encoding="utf-8") as file:
                    for line in new_lines:
                        file.write(line + "\n")
