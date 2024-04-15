from IMEDetector import IMEDetectorSVM
from SVMClassification import (
    custom_tokenizer_bopomofo,
    custom_tokenizer_cangjie,
    custom_tokenizer_pinyin,
)
from collections import Counter


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

    # def separate(self, input_keystrokes: str) -> list[list[str, str]]:
    #     results = []
    #     for seclen in range(3, 7):
    #         while seclen < len(input_keystrokes):
    #             former = input_keystrokes[:seclen]
    #             latter = input_keystrokes[seclen:]
    #             for method, detector in [
    #                 ("bopomofo", self.my_bopomofo_detector),
    #                 ("english", self.my_eng_detector),
    #                 ("cangjie", self.my_cangjie_detector),
    #                 ("pinyin", self.my_pinyin_detector),
    #             ]:
    #                 if (
    #                     detector.predict(former) == False
    #                     and detector.predict(latter) == True
    #                 ):
    #                     print(
    #                         method + " " + former + " " + str(detector.predict(former)),
    #                         latter + " " + str(detector.predict(latter)),
    #                     )
    #                     found = False
    #                     for j, (existing_method, existing_value) in enumerate(results):
    #                         if existing_method == method:
    #                             results[j] = [
    #                                 existing_method,
    #                                 existing_value + " " + latter,
    #                             ]
    #                             found = True
    #                             break
    #                     if not found:
    #                         results.append([method, latter])

    #                 elif (
    #                     detector.predict(former) == True
    #                     and detector.predict(latter) == False
    #                 ):
    #                     print(
    #                         method + " " + former + " " + str(detector.predict(former)),
    #                         latter + " " + str(detector.predict(latter)),
    #                     )
    #                     found = False
    #                     for j, (existing_method, existing_value) in enumerate(results):
    #                         if existing_method == method:
    #                             results[j] = [
    #                                 existing_method,
    #                                 existing_value + " " + former,
    #                             ]
    #                             found = True
    #                             break
    #                     if not found:
    #                         results.append([method, former])
    #                 elif (
    #                     detector.predict(former) == False
    #                     and detector.predict(latter) == False
    #                 ):
    #                     print(
    #                         method + " " + former + " " + str(detector.predict(former)),
    #                         latter + " " + str(detector.predict(latter)),
    #                     )
    #             seclen += seclen
    #     return results
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
                    print(
                        method + " " + former + " " + str(detector.predict(former)),
                        latter + " " + str(detector.predict(latter)),
                    )
                    former_method = method
                    for method, detector in [
                        ("bopomofo", self.my_bopomofo_detector),
                        ("english", self.my_eng_detector),
                        ("cangjie", self.my_cangjie_detector),
                        ("pinyin", self.my_pinyin_detector),
                    ]:
                        if detector.predict(latter) == True:
                            results.append([[former_method, former], [method, latter]])
        if len(results) == 0:
            results.append([[input_keystrokes]])
        return results

    def clean_results(results):
        cleaned_results = []
        for sublist in results:
            counts = Counter(sublist[1].split())

            common_words = set(
                word for word in counts if counts[word] > 1 or counts[word] == 1
            )

            cleaned_words = []
            for word in sublist[1].split():
                if word in common_words and word not in cleaned_words:
                    cleaned_words.append(word)

            cleaned_sublist = [sublist[0], " ".join(cleaned_words)]
            cleaned_results.append(cleaned_sublist)
        return cleaned_results


if __name__ == "__main__":
    my_separator = IMESeparator()
    input_text = "su3cl3 pinyin"
    while True:
        input_text = input("Enter text: ")
        results = my_separator.separate(input_text)
        print(results)
        # print(IMESeparator.clean_results(results))
