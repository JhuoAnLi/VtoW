
from typing import Union

from IMESeparator import IMESeparator
from IMEConverter import IMEConverter
from SVMClassification import (
    custom_tokenizer_bopomofo,
    custom_tokenizer_cangjie,
    custom_tokenizer_pinyin,
)


class IMEHandler():
    def __init__(self) -> None:
        self._bopomofo_converter = IMEConverter(".\\keystroke_mapping_dictionary\\bopomofo_dict_with_frequency.json")
        self._cangjie_converter = IMEConverter(".\\keystroke_mapping_dictionary\\cangjie_dict_with_frequency.json")
        self._pinyin_converter = IMEConverter(".\\keystroke_mapping_dictionary\\pinyin_dict.json")
        self._english_converter = IMEConverter(".\\keystroke_mapping_dictionary\\english_dict_with_frequency.json")
        self._separator = IMESeparator()
    
    def get_candidate_words(self, keystroke: str, prev_context: str = "") -> list[dict[str, Union[int, list[dict[str, Union[str, int]]]]]]:
        separate_possibilities = self._separator.separate(keystroke)
        output = []
        for separate_way in separate_possibilities:
            logical_sentence = []
            for method, keystroke in separate_way:
                if method == "bopomofo":
                    tokens = custom_tokenizer_bopomofo(keystroke)
                    for token in tokens:
                        logical_sentence.append([{**g, "method": "bopomofo"} for g in self._bopomofo_converter.get_candidates(token, 1, 2)])
                elif method == "cangjie":
                    tokens = custom_tokenizer_cangjie(keystroke)
                    for token in tokens:
                        logical_sentence.append([{**g, "method": "cangjie"} for g in self._cangjie_converter.get_candidates(token, 1, 2)])
                elif method == "pinyin":
                    tokens = custom_tokenizer_pinyin(keystroke)
                    for token in tokens:
                        logical_sentence.append([{**g, "method": "pinyin"} for g in self._pinyin_converter.get_candidates(token, 1, 2)])
                elif method == "english":
                    tokens = keystroke.split(" ")
                    for token in tokens:
                        logical_sentence.append([{**g, "method": "english"} for g in self._english_converter.get_candidates(token, 1, 2)])
                else:
                    raise ValueError("Invalid method: " + method)
                
            
            sum_distance = sum([g[0]["distance"] for g in logical_sentence])

            output.append({
                "total_distance": sum_distance,
                "sentence": logical_sentence
                })
    
        return output


if __name__ == "__main__":
    my_IMEHandler = IMEHandler()
    while True:
        user_keystroke = input("Input text: ")
        print(my_IMEHandler.get_candidate_words(user_keystroke))
        print("===")

