import os
import multiprocessing

from DataProcessLib.LanguageCleaner import LanguageCleaner

import os
import multiprocessing

def clean_file_chunk(input_queue, output_queue):
    while True:
        chunk_index, chunk = input_queue.get()
        if chunk is None:
            output_queue.put(None)  # Signal the main process that this worker is done
            break
        cleaned_chunk = LanguageCleaner.clean(chunk, "chinese", reserve_newline=True)
        output_queue.put((chunk_index, cleaned_chunk))


def clean_file_parallel(input_file_path, output_file_path, num_processes=4):
    chunk_size = 10000  # Adjust this according to your file size and available memory
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
        p = multiprocessing.Process(target=clean_file_chunk, args=(input_queue, output_queue))
        processes.append(p)
        p.start()

    # Collect and reorder cleaned chunks
    cleaned_chunks = [None] * chunk_index
    workers_done = 0
    while workers_done < num_processes:
        try:
            chunk_info = output_queue.get(timeout=1)  # Timeout to prevent hanging
            if chunk_info is None:
                workers_done += 1
            else:
                chunk_index, cleaned_chunk = chunk_info
                cleaned_chunks[chunk_index] = cleaned_chunk
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

if __name__ == "__main__":
    input_file_path = ".\\Plain_Text_Datasets\\Chinese_WebCrawlData_cc100.txt"
    output_file_path = ".\\Plain_Text_Datasets\\Chinese_WebCrawlData_cc100-ch.txt"
    num_processes = 4
    clean_file_parallel(input_file_path, output_file_path, num_processes)
