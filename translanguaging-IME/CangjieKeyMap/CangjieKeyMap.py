# -*- coding: utf-8 -*-

class CangjieKeyMap:
    def __init__(self):
        self.my_list = []
        self.setup_cangjie_key_map()

    def setup_cangjie_key_map(self) -> None:
        with open("Cangjie5.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open("Cangie-markers.txt", "r", encoding="utf-8") as file2:
            lines2 = file2.readlines()
        
        lines += lines2
        for line in lines:
            parts = line.strip().split()

            if len(parts) == 2:
                key, value = parts
                self.my_list.append((key, value))

    def convert_to_cangjie_key(self, input:str) -> str:
        result = ""
        for char in input:
            for cangjie, value in self.my_list:
                if char == value:
                    result += cangjie
        return result

if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    cangjie_key_map = CangjieKeyMap()

    for line in lines:
        print(cangjie_key_map.convert_to_cangjie_key(line.strip()))