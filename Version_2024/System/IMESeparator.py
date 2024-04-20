from IMEDetector import IMEDetectorSVM
from SVMClassification import (
    custom_tokenizer_bopomofo,
    custom_tokenizer_cangjie,
    custom_tokenizer_pinyin,
)
from collections import Counter
import re
from tqdm import tqdm


class IMESeparator:
    def __init__(self):
        # self.separator = separator
        self.my_bopomofo_detector = IMEDetectorSVM(
            "..\\Model_dump\\bopomofo_8adj.pkl",
            "..\\Model_dump\\vectorizer_bopomofo_8adj.pkl",
        )
        self.my_eng_detector = IMEDetectorSVM(
            "..\\Model_dump\\english_8adj.pkl",
            "..\\Model_dump\\vectorizer_english_8adj.pkl",
        )
        self.my_cangjie_detector = IMEDetectorSVM(
            "..\\Model_dump\\cangjie_8adj.pkl",
            "..\\Model_dump\\vectorizer_cangjie_8adj.pkl",
        )
        self.my_pinyin_detector = IMEDetectorSVM(
            "..\\Model_dump\\pinyin_8adj.pkl",
            "..\\Model_dump\\vectorizer_pinyin_8adj.pkl",
        )

    def separate(self, input_keystrokes: str) -> list[list[str, str]]:
        results = []
        for seclen in range(3, len(input_keystrokes) + 1):
            former = input_keystrokes[:seclen]
            latter = input_keystrokes[seclen:]
            for method, detector in [
                ("bopomofo", self.my_bopomofo_detector),
                ("english", self.my_eng_detector),
                ("cangjie", self.my_cangjie_detector),
                ("pinyin", self.my_pinyin_detector),
            ]:
                if (
                    detector.predict(former) == True
                    and detector.predict(latter) == False
                ):
                    # print(
                    #     method + " " + former + " " + str(detector.predict(former)),
                    #     latter + " " + str(detector.predict(latter)),
                    # )
                    former_method = method
                    for method, detector in [
                        ("bopomofo", self.my_bopomofo_detector),
                        ("english", self.my_eng_detector),
                        ("cangjie", self.my_cangjie_detector),
                        ("pinyin", self.my_pinyin_detector),
                    ]:
                        if detector.predict(latter) == True:
                            results.append([(former_method, former), (method, latter)])
        if len(results) == 0:
            results.append(
                [
                    ("bopomofo", input_keystrokes),
                    ("english", input_keystrokes),
                    ("cangjie", input_keystrokes),
                    ("pinyin", input_keystrokes),
                ]
            )
        return results


def read_labels(file_path):
    labels = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                input_text, label_str = line.split("\t©©©\t")
                labels.append([input_text, label_str.strip()])
            except ValueError:
                pass
    return labels


def check_accuracy(label_file, my_separator):
    labels = read_labels(label_file)
    total_lines = len(labels)
    print("Total lines: %d" % total_lines)
    match_count = 0
    for label in tqdm(labels, desc="Processing", unit=" line"):
        input_text = label[0]
        expected_label_pairs = re.findall(r"\([^)]*\)", label[1])
        results = my_separator.separate(input_text)
        for result in results:
            temp_len = 0
            for pairs in expected_label_pairs:
                if eval(pairs) in result:
                    temp_len += 1
            if temp_len == len(expected_label_pairs):
                match_count += 1
                print(results)
                print("Check1: ",result,"Check2: ",expected_label_pairs)
                break
        # print("Match count: %d" % match_count)
    accuracy = match_count / total_lines
    return accuracy


if __name__ == "__main__":
    my_separator = IMESeparator()
    accuracy = check_accuracy("..\\System_Test\\labled_mix_ime.txt", my_separator)
    print("Accuracy: ", accuracy)
