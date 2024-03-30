

if __name__ == "__main__":
    SRC_DATASET_PATH = ".\\Plain_Text_Datasets\\"
    TARGET_DATASET_PATH = ".\\Plain_Text_Datasets\\"

    # cut Chinse text in to 3 words
    cut_word_sizes = [3]
    src_file_names = ["Chinese_WebCrawlData_cc100-ch"]

    for src_file_name in src_file_names:
        for cut_word_size in cut_word_sizes:
            src_file_path = SRC_DATASET_PATH + src_file_name + ".txt"
            target_file_path = TARGET_DATASET_PATH + src_file_name + f"-w{cut_word_size}.txt"

            with open(src_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = [line.replace("\n", "") for line in lines]
                joined_lines = "".join(lines)
            new_lines = [joined_lines[i:i + cut_word_size] for i in range(0, len(joined_lines), cut_word_size)]

            with open(target_file_path, "w", encoding="utf-8") as file:
                for line in new_lines:
                    file.write(line + "\n")

    # cut English text in to 1 words
    cut_word_sizes = [1]
    src_file_names = ["English.txt"]
    MAX_WORD_SIZE = 20

    for src_file_name in src_file_names:
        for cut_word_size in cut_word_sizes:
            src_file_path = SRC_DATASET_PATH + src_file_name
            target_file_path = TARGET_DATASET_PATH + src_file_name.replace(".txt", f"-w{cut_word_size}.txt")

            with open(src_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = [line.replace("\n", "") for line in lines]
                joined_lines = "".join(lines)
                words = joined_lines.split(" ")
                temp = ""
                new_lines = []
                for word in words:
                    if len(temp)+len(word) < MAX_WORD_SIZE:
                        temp += word + " "
                    else:
                        new_lines.append(temp)
                        temp = word + " "

            with open(target_file_path, "w", encoding="utf-8") as file:
                for line in new_lines:
                    file.write(line + "\n")

