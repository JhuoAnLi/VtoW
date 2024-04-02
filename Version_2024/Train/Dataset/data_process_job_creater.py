import json

# Create V2 Dataset

if __name__ == "__main__":
    PLAIN_TEXT_DATASET_PATH = ".\\Plain_Text_Datasets\\"
    KEY_STROKE_DATASET_PATH = ".\\Key_Stroke_Datasets\\"
    TRAIN_DATASET_PATH = ".\\Train_Datasets\\"
    TEST_DATASET_PATH = ".\\Test_Datasets\\"
    FILE_NAME = "data_process_job.json"

    job_list = []

    # Create Cleaned Dataset from existing plain text dataset
    mode = "clean"
    src_files = ["Chinese_WebCrawlData_cc100.txt"]
    languages = ["chinese"]
    skip_clean = True

    for src_file in src_files:
        for language in languages:
            dataset_name = None
            if src_file.find("cc100") > 0:
                dataset_name = "cc100"
            elif src_file.find("news") > 0:
                dataset_name = "news"
            elif src_file.find("gossip") > 0:
                dataset_name = "gossip"
            else:
                raise ValueError("Invalid file name: " + src_file)

            job_list.append({
                "mode": mode,
                "description": f"Clean {src_file} to {language}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": PLAIN_TEXT_DATASET_PATH + f"{src_file.replace('.txt', '-ch.txt')}",
                "language": language,
                "status": "done" if skip_clean else None
                })

    # Split Dataset into words
    mode = "split_word"
    src_files = ["Chinese_WebCrawlData_cc100-ch.txt"]
    min_split_word_len = 1
    max_split_word_len = 3
    languages = ["ch"]
    skip_split_word = False

    output_file_name_list = []
    for src_file in src_files:
        for language in languages:
            dataset_name = None
            if src_file.find("cc100") > 0:
                dataset_name = "cc100"
            elif src_file.find("news") > 0:
                dataset_name = "news"
            else:
                raise ValueError("Invalid file name: " + src_file)

            output_file_name = f"wlen{min_split_word_len}-{max_split_word_len}_{dataset_name}.txt"
            output_file_name_list.append(output_file_name)
            job_list.append({
                "mode": mode,
                "description": f"Split {src_file} into words with length {min_split_word_len}-{max_split_word_len}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": PLAIN_TEXT_DATASET_PATH + output_file_name,
                "min_split_word_len": min_split_word_len,
                "max_split_word_len": max_split_word_len,
                "language": language,
                "status": "done" if skip_split_word else None
                })

    mode = "split_word"
    src_files = ["English.txt"]

    languages = ["en"]
    skeip_split_word = False

    for src_file in src_files:
        for language in languages:
            if src_file.find("English") < 0:
                raise ValueError("Invalid file name: " + src_file)


            output_file_name = f"wlen{min_split_word_len}-{max_split_word_len}_English.txt"
            output_file_name_list.append(output_file_name)
            job_list.append({
                "mode": mode,
                "description": f"Split {src_file} into words with length {min_split_word_len}-{max_split_word_len}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": PLAIN_TEXT_DATASET_PATH + output_file_name,
                "min_split_word_len": min_split_word_len,
                "max_split_word_len": max_split_word_len,
                "language": language,
                "status": "done" if skip_split_word else None
                })


    # Create KeyStroke Dataset from existing plain text dataset
    mode = "convert"
    src_files = ["wlen1-3_cc100.txt"]
    convert_types = ["bopomofo", "cangjie", "pinyin"]
    skip_convert = False

    convert_files = []
    for src_file in src_files:
        for convert_type in convert_types:

            output_file_name = f"0_{convert_type}_{src_file}"
            convert_files.append(output_file_name)
            job_list.append({
                "mode": mode,
                "description": f"Convert {src_file} to {convert_type}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": KEY_STROKE_DATASET_PATH + output_file_name,
                "convert_type": convert_type,
                "status": "done" if skip_convert else None
                })

    mode = "convert"
    src_files = ["wlen1-3_English.txt"]  # todo: fix this
    convert_types = ["english"]
    for src_file in src_files:
        for convert_type in convert_types:

            output_file_name = f"0_{convert_type}_{src_file}"
            convert_files.append(output_file_name)
            job_list.append({
                "mode": mode,
                "description": f"Convert {src_file} to {convert_type}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": KEY_STROKE_DATASET_PATH + output_file_name,
                "convert_type": convert_type,
                "status": "done" if skip_convert else None
                })


    # Create Error Dataset from existing keystroke dataset
    mode = "gen_error"
    src_files = convert_files
    error_rates = [0.1, 0.01]
    error_types = ["random"]
    skip_gen_error = False

    with_error_files = []
    for src_file in src_files:
        for error_type in error_types:
            for error_rate in error_rates:
                error_rate_name = str(error_rate).replace(".", "-")
                error_type_name = "r" if error_type == "random" else "8a" if error_type == "8adjacent" else error_type

                src_file_name = src_file.split("_")[1:]
                output_file_name = f"{error_type_name}{error_rate_name}_{'_'.join(src_file_name)}"
                with_error_files.append(output_file_name)
                job_list.append({
                    "mode": mode,
                    "description": f"Generate '{error_type}' error for {src_file} with error rate {error_rate}",
                    "input_file_path": KEY_STROKE_DATASET_PATH + src_file, 
                    "output_file_path": KEY_STROKE_DATASET_PATH + output_file_name,
                    "error_type": error_type,
                    "error_rate": error_rate,
                    "status": "done" if skip_gen_error else None
                    })
                
    # Split Dataset into Train and Test Dataset
    mode = "split"
    src_files = with_error_files + convert_files
    train_test_split_ratio = 0.5
    skip_split = False

    for src_file in src_files:
        train_file_name = src_file.replace(".txt", "_train.txt")
        test_file_name = src_file.replace(".txt", "_test.txt")

        job_list.append({
            "mode": mode,
            "description": f"Split {src_file} with {train_test_split_ratio} into {train_file_name} and {test_file_name} datasets.",
            "input_file_path": KEY_STROKE_DATASET_PATH + src_file,
            "train_file_path": TRAIN_DATASET_PATH + train_file_name,
            "test_file_path": TEST_DATASET_PATH + test_file_name,
            "train_test_split_ratio": train_test_split_ratio,
            "status": "done" if skip_split else None
            })
        

    with open(FILE_NAME, "w") as f:
        json.dump(job_list, f, indent=4)
