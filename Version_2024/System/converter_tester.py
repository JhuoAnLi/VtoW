from IMEConverter import IMEConverter
from multiprocessing import Pool
from tqdm import tqdm

my_bopomofo_IMEConverter = IMEConverter(".\\keystroke_mapping_dictionary\\bopomofo_dict_with_frequency.json")
my_cangjie_IMEConverter = IMEConverter(".\\keystroke_mapping_dictionary\\cangjie_dict_with_frequency.json")
my_pinyin_IMEConverter = IMEConverter(".\\keystroke_mapping_dictionary\\pinyin_dict_with_frequency.json")
my_english_IMEConverter = IMEConverter(".\\keystroke_mapping_dictionary\\english_dict_with_frequency.json")



def test_converter(test_keystroke, test_language, correct_label):


    if test_language == "bopomofo":
        result = my_bopomofo_IMEConverter.get_candidates(test_keystroke, 1, 2)
    elif test_language == "cangjie":
        result = my_cangjie_IMEConverter.get_candidates(test_keystroke, 1, 2)
    elif test_language == "pinyin":
        result = my_pinyin_IMEConverter.get_candidates(test_keystroke, 1, 2)
    elif test_language == "english":
        result = my_english_IMEConverter.get_candidates(test_keystroke, 1, 2)
    else:
        raise ValueError("Invalid language: " + test_language)
    

    for candidate in result:
        if candidate["word"] == correct_label:
            return (test_language, 1, (test_keystroke, test_language, correct_label))
    
    guess_words = " ".join([candidate["word"] for candidate in result])
    return (test_language, 0, (test_keystroke, test_language, correct_label, guess_words))

if __name__ == "__main__":
    test_data_path = ".\\..\\System_Test\\converter_test_r0-05.txt"

    test_conig = []
    job_list = []
    with open(test_data_path, "r", encoding="utf-8") as f:
        test_data = f.readlines()
        test_config = eval(test_data[0])
        test_data = test_data[1:]
        test_data = [line.strip() for line in test_data]
        for line in test_data:
            items = line.split("\t")
            if len(items) != 3:
                items.insert(0, "")
            test_keystroke, test_language, correct_label = items[0], items[1], items[2]
            job_list.append((test_keystroke, test_language, correct_label))


    outputs = []
    with tqdm(total=len(test_data)) as pbar:
        with Pool() as pool:
            results = []
            for job in job_list:
                results.append(pool.apply_async(test_converter, job))

            for result in results:
                outputs.append(result.get())
                pbar.update(1)


    correct_count = {"bopomofo": 0, "cangjie": 0, "pinyin": 0, "english": 0}
    save_wrong_output = []
    for output in outputs:
        language, correct, pairs = output
        if correct == 0:
            save_wrong_output.append(pairs)
        correct_count[language] += correct
    for language, correct in correct_count.items():
        print(f"{language}: {correct}/{test_config[language]}, Accuarcy: {correct/test_config[language]:.2f}")
    
    with open("converter_test_result.txt", "w", encoding="utf-8") as f:
        for output in save_wrong_output:
            f.write(f"{output}\n")
