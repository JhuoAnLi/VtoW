# -*- coding: utf-8 -*-

class CangjieKeyMap:
    def __init__(self):
        self.my_list = []
        self.setup_cangjie_key_map()

    def setup_cangjie_key_map(self) -> None:
        with open("Cangjie5.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open("Cangjie-markers.txt", "r", encoding="utf-8") as file2:
            lines2 = file2.readlines()
        
        lines += lines2
        for line in lines:
            parts = line.strip().split()

            if len(parts) == 2:
                word, cangjie_key = parts
                self.my_list.append((word, cangjie_key))

    def convert_to_cangjie_key(self, input:str) -> str:
        result = ""
        for char in input:
            converted = False
            for word, cangjie_key in self.my_list:
                if char == word:
                    result += cangjie_key + " "
                    converted = True
                    break
            if converted == False:
                result += char

        return result

if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    cangjie_key_map = CangjieKeyMap()
    
    print(cangjie_key_map.convert_to_cangjie_key("?"))

    # for line in lines:
        # print(cangjie_key_map.convert_to_cangjie_key(line.strip()))

    # with open ("Cangjie-markers.txt", "r", encoding="utf-8") as file:
    #     with open("Cangjie-markers2.txt", "w", encoding="utf-8") as file2:
    #         lines = file.readlines()
    #         for line in lines:
    #             parts = line.strip().split()
    #             if len(parts) == 2:
    #                 word, cangjie_key = parts
    #                 file2.write(word + "\t" + cangjie_key.lower() + "\n")