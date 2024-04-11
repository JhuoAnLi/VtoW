import json
import os

from tqdm import tqdm

from DataProcessLib.LanguageCleaner import LanguageCleaner
from DataProcessLib.KeyStrokeConverter import KeyStrokeConverter
from DataProcessLib.TypoGenerater import TypoGenerater


def split_train_test_file(input_file_path, train_file_path, test_file_path, train_test_split_size):
    with open(input_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        split_index = int(len(lines) * train_test_split_size)
        train_lines = lines[:split_index]
        test_lines = lines[split_index:]
    
    with open(train_file_path, "w", encoding="utf-8") as file:
        for line in train_lines:
            file.write(line)

    with open(test_file_path, "w", encoding="utf-8") as file:
        for line in test_lines:
            file.write(line)

def split_by_word(input_file_path, output_file_path, min_split_word_len, max_split_word_len, language="en"):
    with open(input_file_path, "r", encoding="utf-8") as file_in:
        lines = file_in.readlines()
        output_lines = []
        if language == "en":
            input_string = "".join(lines)
            words = [word for line in input_string.split('\n') for word in line.split(' ')]
            i = 0
            with tqdm(total=len(words)) as pbar:
                while i < len(words):
                    output_lines.append(' '.join(words[i:i+1]))
                    output_lines.append(' '.join(words[i+1:i+3]))
                    output_lines.append(' '.join(words[i+3:i+6]))
                    pbar.update(6)
                    i += 6
        elif language == "ch":
            joined_lines = "".join(lines).replace("\n", "")
            words = [word for word in joined_lines]
            i = 0
            with tqdm(total=len(words)) as pbar:
                while i < len(words):
                    output_lines.append(''.join(words[i:i+1]))
                    output_lines.append(''.join(words[i+1:i+3]))
                    output_lines.append(''.join(words[i+3:i+6]))
                    pbar.update(6)
                    i += 6
        else:
            raise ValueError("Invalid language: " + language)
    
    with open(output_file_path, "w", encoding="utf-8") as file_out:
        file_out.write("\n".join(output_lines))

def cut_keystroke_by(input_file_path, output_file_path, cut_out_len):
    with open(input_file_path, "r", encoding="utf-8") as file_in:
        keystroke_lines = file_in.readlines()
        keystroke_lines = [line.replace("\n", "") for line in keystroke_lines if line.strip() != ""]
        joined_keystroke_lines = "".join(keystroke_lines)
        out_keystrokes = [joined_keystroke_lines[i:i+cut_out_len] for i in range(0, len(joined_keystroke_lines), cut_out_len)]
    with open(output_file_path, "w", encoding="utf-8") as file_out:
        file_out.write("\n".join(out_keystrokes))

if __name__ == "__main__":
    NUM_PROCESSES = 4
    PROCESS_JOB_FILE = "data_process_job.json"

    KEY_STROKE_DATASET_PATH = ".\\Key_Stroke_Datasets\\"
    TRAIN_DATASET_PATH = ".\\Train_Datasets\\"
    TEST_DATASET_PATH = ".\\Test_Datasets\\"

    job_list = json.load(open(PROCESS_JOB_FILE, "r"))

    # clear all files in the dataset folders
    if len(os.listdir(KEY_STROKE_DATASET_PATH)) > 0:
        if input("Do you want to remove all files in Key_Stroke_Datasets? (y/n)") == "y":
            print("Removing all files in Key_Stroke_Datasets")
            for file_name in os.listdir(KEY_STROKE_DATASET_PATH):
                os.remove(os.path.join(KEY_STROKE_DATASET_PATH, file_name))

    if len(os.listdir(TRAIN_DATASET_PATH)) > 0:
        if input("Do you want to remove all files in Train_Datasets? (y/n)") == "y":
            print("Removing all files in Train_Datasets")
            for file_name in os.listdir(TRAIN_DATASET_PATH):
                os.remove(os.path.join(TRAIN_DATASET_PATH, file_name))

    if len(os.listdir(TEST_DATASET_PATH)) > 0:
        if input("Do you want to remove all files in Test_Datasets? (y/n)") == "y":
            print("Removing all files in Test_Datasets")
            for file_name in os.listdir(TEST_DATASET_PATH):
                os.remove(os.path.join(TEST_DATASET_PATH, file_name))

    unfinished_jobs = []
    for job in job_list:
        if job.get("status") != "done" or job.get("status") is None:
            try: 
                if job["mode"] == "clean":
                    LanguageCleaner.clean_file_parallel(job["input_file_path"], job["output_file_path"], job["language"], num_processes=NUM_PROCESSES)
                elif job["mode"] == "convert":
                    KeyStrokeConverter.convert_file_parallel(job["input_file_path"], job["output_file_path"], job["convert_type"], num_processes=NUM_PROCESSES)
                elif job["mode"] == "gen_error":
                    TypoGenerater.generate_file_parallel(job["input_file_path"], job["output_file_path"], job["error_type"], job["error_rate"], num_processes=NUM_PROCESSES)
                elif job["mode"] == "split":
                    split_train_test_file(job["input_file_path"], job["train_file_path"], job["test_file_path"], job["train_test_split_ratio"])
                elif job["mode"] == "split_word":
                    split_by_word(job["input_file_path"], job["output_file_path"], job["min_split_word_len"], job["max_split_word_len"], job["language"])
                elif job["mode"] == "cut_keystroke":
                    cut_keystroke_by(job["input_file_path"], job["output_file_path"], job["cut_out_len"])
                else:
                    raise ValueError("Invalid mode: " + job["mode"])
                
                print(f"Success: In {job['mode']}, {job['description']}")
                job["status"] = "done"
            except Exception as e:
                print(f"Error: In {job['mode']}, {job['description']}")
                print("Error: " + str(e))
                unfinished_jobs.append(job)
                job["status"] = "error"
                continue


    if len(unfinished_jobs) > 0:
        print("----- Unfinished jobs -----")
        for job in unfinished_jobs:
            print(job)

    with open(PROCESS_JOB_FILE, "w") as f:
        json.dump(job_list, f, indent=4)