import json


if __name__ == "__main__":
    PLAIN_TEXT_DATASET_PATH = ".\\Plain_Text_Datasets\\"
    KEY_STROKE_DATASET_PATH = ".\\Key_Stroke_Datasets\\"
    TRAIN_DATASET_PATH = ".\\Train_Datasets\\"
    TEST_DATASET_PATH = ".\\Test_Datasets\\"
    FILE_NAME = "data_process_job.json"

    job_list = []

    # Create Cleaned Dataset from existing plain text dataset
    mode = "clean"
    src_files = ["Chinese_news.txt", "Chinese_WebCrawlData_cc100.txt", "Chinese_gossip.txt"]
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


    # Create KeyStroke Dataset from existing plain text dataset
    mode = "convert"
    src_files = ["Chinese_news-ch.txt", "Chinese_WebCrawlData_cc100-ch.txt"]
    convert_types = ["bopomofo", "cangjie", "pinyin"]
    skip_convert = True

    for src_file in src_files:
        for convert_type in convert_types:
            dataset_name = None
            if src_file.find("cc100") > 0:
                dataset_name = "cc100"
            elif src_file.find("news") > 0:
                dataset_name = "news"
            else:
                raise ValueError("Invalid file name: " + src_file)

            job_list.append({
                "mode": mode,
                "description": f"Convert {src_file} to {convert_type}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": KEY_STROKE_DATASET_PATH + f"{convert_type}-{dataset_name}-0.txt",
                "convert_type": convert_type,
                "status": "done" if skip_convert else None
                })

    mode = "convert"
    src_files = ["English.txt"]
    convert_types = ["english"]
    for src_file in src_files:
        for convert_type in convert_types:
            job_list.append({
                "mode": mode,
                "description": f"Convert {src_file} to {convert_type}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": KEY_STROKE_DATASET_PATH + f"{convert_type}-0.txt",
                "convert_type": convert_type,
                "status": "done" if skip_convert else None
                })


    # Split Dataset into Train and Test Dataset
    mode = "split"
    src_files = ["bopomofo-cc100-0.txt", "cangjie-cc100-0.txt", "pinyin-cc100-0.txt", "english-0.txt"]
    train_test_split_ratio = 0.5
    skip_split = True

    for src_file in src_files:
        train_file_name = src_file.replace("-0.txt", "-0-train.txt")
        test_file_name = src_file.replace("-0.txt", "-0-test.txt")

        job_list.append({
            "mode": mode,
            "description": f"Split {src_file} with {train_test_split_ratio} into {train_file_name} and {test_file_name} datasets.",
            "input_file_path": KEY_STROKE_DATASET_PATH + src_file, 
            "train_file_path": TRAIN_DATASET_PATH + train_file_name,
            "test_file_path": TEST_DATASET_PATH + test_file_name,
            "train_test_split_ratio": train_test_split_ratio,
            "status": "done" if skip_split else None
            })



    # Create Error Dataset from existing keystroke dataset
    mode = "gen_error"
    src_files = ["bopomofo-cc100-0-test.txt", "cangjie-cc100-0-test.txt", "pinyin-cc100-0-test.txt", "english-0-test.txt"]
    error_rates = [0.1, 0.01]
    error_types = ["random"]
    skip_gen_error = True

    # job_list = []
    for src_file in src_files:
        for error_type in error_types:
            for error_rate in error_rates:
                error_rate_name = str(error_rate).replace(".", "_")
                output_file_name = src_file.replace("-0-", f"-{error_rate_name}-")
                job_list.append({
                    "mode": mode,
                    "description": f"Generate {error_type} error for {dataset_name} with error rate {error_rate}",
                    "input_file_path": TEST_DATASET_PATH + src_file, 
                    "output_file_path": TEST_DATASET_PATH + output_file_name,
                    "error_type": error_type,
                    "error_rate": error_rate,
                    "status": "done" if skip_gen_error else None
                    })
                


    with open(FILE_NAME, "w") as f:
        json.dump(job_list, f, indent=4)
