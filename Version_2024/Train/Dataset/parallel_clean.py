import os
import multiprocessing
from tqdm import tqdm

from DataProcessLib.LanguageCleaner import LanguageCleaner
from DataProcessLib.KeyStrokeConverter import KeyStrokeConverter
from DataProcessLib.TypoGenerater import TypoGenerater

import os
import multiprocessing


def clean_file_chunk(input_queue, output_queue):
    while True:
        chunk_index, chunk = input_queue.get()
        if chunk is None:
            output_queue.put(None)  # Signal the main process that this worker is done
            break
        cleaned_chunk = LanguageCleaner.clean(chunk, CLEAN_LANGUAGE, reserve_newline=True)
        output_queue.put((chunk_index, cleaned_chunk))


def convert_file_chuck(input_queue, output_queue):
    while True:
        chunk_index, chunk = input_queue.get()
        if chunk is None:
            output_queue.put(None)  # Signal the main process that this worker is done
            break
        cleaned_chunk = KeyStrokeConverter.convert(chunk, convert_type=CONVET_TO)
        output_queue.put((chunk_index, cleaned_chunk))

def gen_error_file_chunk(input_queue, output_queue):
    while True:
        chunk_index, chunk = input_queue.get()
        if chunk is None:
            output_queue.put(None)  # Signal the main process that this worker is done
            break
        cleaned_chunk = TypoGenerater.generate(chunk, error_rate=ERROR_RATE)
        output_queue.put((chunk_index, cleaned_chunk))


def file_parallel(input_file_path, output_file_path, chuck_job, num_processes=4):
    chunk_size = 10000  
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # Read the input file and split it into chunks
    with open(input_file_path, 'r', encoding='utf-8') as f:
        chunk_index = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            input_queue.put((chunk_index, chunk))
            chunk_index += 1

    # Add termination signals to the input queue
    for _ in range(num_processes):
        input_queue.put((None, None))

    # Process chunks in parallel
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=chuck_job, args=(input_queue, output_queue))
        processes.append(p)
        p.start()

    # Collect and reorder cleaned chunks
    cleaned_chunks = [None] * chunk_index
    workers_done = 0
    with tqdm(total=chunk_index) as pbar:
        while workers_done < num_processes:
            try:
                chunk_info = output_queue.get(timeout=1)  # Timeout to prevent hanging
                if chunk_info is None:
                    workers_done += 1
                else:
                    chunk_index, cleaned_chunk = chunk_info
                    cleaned_chunks[chunk_index] = cleaned_chunk
                    pbar.update(1)  # Update progress bar for each processed chunk
            except multiprocessing.TimeoutError:
                # Timeout occurred, check if processes are still alive
                alive_processes = [p.is_alive() for p in processes]
                if not any(alive_processes):
                    break  # All processes have terminated

    # Terminate any remaining processes
    for p in processes:
        if p.is_alive():
            p.terminate()
            p.join()
    
    # Write reordered cleaned chunks to the output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for cleaned_chunk in cleaned_chunks:
            if cleaned_chunk is not None:
                f.write(cleaned_chunk)

MODE = "gen_error" # "clean", "convert", "gen_error"
CONVET_TO="bopomofo"
ERROR_RATE = 0.1
CLEAN_LANGUAGE = "chinese"

if __name__ == "__main__":
    PLAIN_TEXT_DATASET_PATH = ".\\Plain_Text_Datasets\\"
    KEY_STROKE_DATASET_PATH = ".\\Key_Stroke_Datasets\\"
    NUM_PROCESSES = 4


    if MODE == "clean":
        file = "Chinese_gossip.txt"
        input_file_path = PLAIN_TEXT_DATASET_PATH + file
        output_file_path = PLAIN_TEXT_DATASET_PATH + file.replace(".txt", "-ch.txt")
        chunk_job = clean_file_chunk
    elif MODE == "convert":
        input_file_path = PLAIN_TEXT_DATASET_PATH + "Chinese_news-ch.txt"
        output_file_path = KEY_STROKE_DATASET_PATH + "{}-news-0.txt".format(CONVET_TO)
        chunk_job = convert_file_chuck
    elif MODE == "gen_error":
        input_file_path = KEY_STROKE_DATASET_PATH + "bopomofo-news-0.txt"
        output_file_path = KEY_STROKE_DATASET_PATH + "{}-news-{}.txt".format(CONVET_TO, str(ERROR_RATE).replace(".", "_"))
        chunk_job = gen_error_file_chunk
    else:
        raise ValueError(f"Invalid mode: {MODE}")

    file_parallel(input_file_path, output_file_path, chuck_job=chunk_job, num_processes=NUM_PROCESSES)