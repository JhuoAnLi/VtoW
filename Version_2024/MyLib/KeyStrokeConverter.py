import os

from pypinyin import pinyin, lazy_pinyin, Style


class KeyStrokeConverter:

    @classmethod
    def convert(cls, input_string:str, convert_type:str) -> str:
        """
        Convert the input string to the specified type of keystroke

        Args:
            input_string (str): The input string
            convert_type (str): The type of keystroke to convert to. 
                                Valid values are "english", "cangjie", "bopomofo", "pinyin"
        
        Raises: 
            ValueError: If convert_type is not valid
        
        Returns:
            str: The converted string
        """


        if convert_type == "english":
            converted_string = cls._StringToEnglishKey(input_string)
        elif convert_type == "cangjie":
            converted_string = cls._StringToCangjieKey(input_string)
        elif convert_type == "bopomofo":
            converted_string = cls._StringToBopomofoKey(input_string)
        elif convert_type == "pinyin":
            converted_string = cls._StringToPinyinKey(input_string)
        else:
            raise ValueError("Invalid convert_type: " + convert_type)

        return converted_string
    

    @classmethod
    def _StringToCangjieKey(cls, input_string:str) -> str:

        def setup_cangjie_key_map() -> dict:  # todo: make the dict not load every time
            files = ["Cangjie5.txt", "Cangjie-markers.txt"]

            cangjie_key_map_dict = {}
            for filename in files:
                with open(os.path.dirname(__file__) + "\\" + filename, "r", encoding="utf-8") as file:
                    for line in file:
                        parts = line.strip().split()
                        if len(parts) == 2:
                            word, cangjie_key = parts
                            cangjie_key_map_dict.setdefault(word, cangjie_key)

            return cangjie_key_map_dict

        cangjie_map_dict = setup_cangjie_key_map()
        result = ' '.join(cangjie_map_dict.get(char, char) for char in input_string)

        return result


    @classmethod
    def _StringToBopomofoKey(cls, input_string: str) -> str:

        def bopomofo_to_keystroke(bopomofo: str) -> str:
            map = {
                "ㄅ": "1", "ㄆ": "q", "ㄇ": "a",
                "ㄈ": "z", "ㄉ": "2", "ㄊ": "w",
                "ㄋ": "s", "ㄌ": "x", "ㄍ": "e",
                "ㄎ": "d", "ㄏ": "c", "ㄐ": "r",
                "ㄑ": "f", "ㄒ": "v", "ㄓ": "5",
                "ㄔ": "t", "ㄕ": "g", "ㄖ": "b",
                "ㄗ": "y", "ㄘ": "h", "ㄙ": "n",
                "ㄚ": "8", "ㄛ": "i", "ㄜ": "k",
                "ㄝ": ",", "ㄞ": "9", "ㄟ": "o",
                "ㄠ": "l", "ㄡ": ".", "ㄢ": "0",
                "ㄣ": "p", "ㄤ": ";", "ㄥ": "/",
                "ㄦ": "-", "ㄧ": "u", "ㄨ": "j",
                "ㄩ": "m", "ˊ": "6", "ˇ": "3",
                "ˋ": "4",  "˙": "7",
            }

            keystroke = ""
            try:
                if bopomofo[0] in cls.full_width_map.keys():  # if the word is full width speical character
                    for word in bopomofo:
                        keystroke += cls.full_width_map.get(word, word)
                else:
                    for word in bopomofo:
                        keystroke += map.get(word, word)
                    
                    if not keystroke.endswith(("6", "3", "4", "7")):  # if the word is tone 1 add a space
                        keystroke += " "
                
            except KeyError:
                    print("Invalid bopomofo: " + bopomofo)

                    # raise ValueError("Invalid bopomofo: " + bopomofo)
            
            return keystroke
        
        BOPOMOFO_result = [pin[0] for pin in pinyin(input_string, style=Style.BOPOMOFO)]
        result = [bopomofo_to_keystroke(word) for word in BOPOMOFO_result]
        result = "".join(result)

        return result


    @classmethod
    def _StringToPinyinKey(cls, input_string:str) -> str:
        PINYIN_result = ""
        for pin in pinyin(input_string, style=Style.NORMAL):
            PINYIN_result += pin[0]
        print(PINYIN_result)

        return PINYIN_result


    @classmethod
    def _StringToEnglishKey(cls, input_string: str) -> str:
        return input_string

    full_width_map = {
        "１": "1", "２": "2", "３": "3",
        "４": "4", "５": "5", "６": "6",
        "７": "7", "８": "8", "９": "9",
        "０": "0", 
        
        
        "，": "<ctrl>,", "。": "<ctrl>.",
        "、": "<ctrl>'",
        "；": "<ctrl>;", "：": "<ctrl>:",
        "？": "<ctrl>?", "！": "<ctrl>!",
        "（": "(",       "）": ")",  # fixme: not sure if this is correct 
        "【": '<ctrl>[', "】": '<ctrl>]',
        "｛": '<ctrl>{', "｝": '<ctrl>}',


        "「": "<ctrl>[", "」": "<ctrl>]",  # fixme: not sure if this is correct
    }

    @classmethod
    def _full_width_to_half_width(cls, input_char: str) -> str:
            return cls.full_width_map.get(input_char, input_char)


if __name__ == '__main__':
    input_string = "頒行政院長陳建仁今（16）日出席「112年鳳凰獎楷模表揚典禮」，頒獎表揚74名獲獎義消"
    convert_type = "bopomofo"
    print(KeyStrokeConverter.convert(input_string, convert_type))