import json

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


if __name__ == "__main__":
    NUM_PROCESSES = 4
    PROCESS_JOB_FILE = "data_process_job.json"

    job_list = json.load(open(PROCESS_JOB_FILE, "r"))

    unfinished_jobs = []
    for job in job_list:
        if job.get("status") != "done" or job.get("status") is None :
            try: 
                if job["mode"] == "clean":
                    LanguageCleaner.clean_file_parallel(job["input_file_path"], job["output_file_path"], job["language"], num_processes=NUM_PROCESSES)
                elif job["mode"] == "convert":
                    KeyStrokeConverter.convert_file_parallel(job["input_file_path"], job["output_file_path"], job["convert_type"], num_processes=NUM_PROCESSES)
                elif job["mode"] == "gen_error":
                    TypoGenerater.generate_file_parallel(job["input_file_path"], job["output_file_path"], job["error_type"], job["error_rate"], num_processes=NUM_PROCESSES)
                elif job["mode"] == "split":
                    split_train_test_file(job["input_file_path"], job["train_file_path"], job["test_file_path"], job["train_test_split_ratio"])
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