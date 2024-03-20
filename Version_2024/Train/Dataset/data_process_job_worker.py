import json

from DataProcessLib.LanguageCleaner import LanguageCleaner
from DataProcessLib.KeyStrokeConverter import KeyStrokeConverter
from DataProcessLib.TypoGenerater import TypoGenerater

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
                else:
                    raise ValueError("Invalid mode: " + job["mode"])
                
                print(f"Success: In {job['mode']}, save file to {job['output_file_path']}")
                job["status"] = "done"
            except Exception as e:
                print(f"Error: In {job['mode']}, {job['output_file_path']}")
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