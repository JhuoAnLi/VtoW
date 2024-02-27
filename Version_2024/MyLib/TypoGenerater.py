import random


def character_mapping(input: str) -> list[str]:
    if input == "1":
        return ["2", "q", "w"]
    elif input == "2":
        return ["1", "3", "q", "w", "e"]
    elif input == "3":
        return ["2", "4", "w", "e", "r"]
    elif input == "4":
        return ["3", "5", "e", "r", "t"]
    elif input == "5":
        return ["4", "6", "r", "t", "y"]
    elif input == "6":
        return ["5", "7", "t", "y", "u"]
    elif input == "7":
        return ["6", "8", "y", "u", "i"]
    elif input == "8":
        return ["7", "9", "u", "i", "o"]
    elif input == "9":
        return ["8", "0", "i", "o", "p"]
    elif input == "0":
        return ["9", "-", "o", "p", "["]
    elif input == "-":
        return ["0", "=", "p", "[", "]"]
    elif input == "=":
        return ["-", "\\", "[", "]"]
    elif input == "q" or input == "Q":
        return ["1", "2", "w", "a", "s"]
    elif input == "w" or input == "W":
        return ["1", "2", "3", "q", "a", "s", "d"]
    elif input == "e" or input == "E":
        return ["2", "3", "4", "w", "s", "d", "f"]
    elif input == "r" or input == "R":
        return ["3", "4", "5", "e", "d", "f", "g"]
    elif input == "t" or input == "T":
        return ["4", "5", "6", "r", "f", "g", "h"]
    elif input == "y" or input == "Y":
        return ["5", "6", "7", "t", "g", "h", "j"]
    elif input == "u" or input == "U":
        return ["6", "7", "8", "y", "h", "j", "k"]
    elif input == "i" or input == "I":
        return ["7", "8", "9", "u", "j", "k", "l"]
    elif input == "o" or input == "O":
        return ["8", "9", "0", "i", "k", "l", ";"]
    elif input == "p" or input == "P":
        return ["9", "0", "-", "o", "l", ";", "'"]
    elif input == "[":
        return ["0", "-", "=", "p", ";", "'", "]"]
    elif input == "]":
        return ["-", "=", "[", "'", "\\"]
    elif input == "a" or input == "A":
        return ["q", "w", "s", "z", "x"]
    elif input == "s" or input == "S":
        return ["q", "w", "e", "a", "d", "z", "x", "c"]
    elif input == "d" or input == "D":
        return ["w", "e", "r", "s", "f", "x", "c", "v"]
    elif input == "f" or input == "F":
        return ["e", "r", "t", "d", "g", "c", "v", "b"]
    elif input == "g" or input == "G":
        return ["r", "t", "y", "f", "h", "v", "b", "n"]
    elif input == "h" or input == "H":
        return ["t", "y", "u", "g", "j", "b", "n", "m"]
    elif input == "j" or input == "J":
        return ["y", "u", "i", "h", "k", "n", "m", ","]
    elif input == "k" or input == "K":
        return ["u", "i", "o", "j", "l", "m", ",", "."]
    elif input == "l" or input == "L":
        return ["i", "o", "p", "k", ";", ".", "/"]
    elif input == ";":
        return ["o", "p", "[", "l", "'", ".", "/"]
    elif input == "'":
        return ["p", "[", "]", ";", "/"]
    elif input == "z" or input == "Z":
        return ["a", "s", "x"]
    elif input == "x" or input == "X":
        return ["a", "s", "d", "z", "c"]
    elif input == "c" or input == "C":
        return ["s", "d", "f", "x", "v"]
    elif input == "v" or input == "V":
        return ["d", "f", "g", "c", "b"]
    elif input == "b" or input == "B":
        return ["f", "g", "h", "v", "n"]
    elif input == "n" or input == "N":
        return ["g", "h", "j", "b", "m"]
    elif input == "m" or input == "M":
        return ["h", "j", "k", "n", ","]
    elif input == ",":
        return ["j", "k", "l", "m", "."]
    elif input == ".":
        return ["k", "l", ";", ",", "/"]
    elif input == "/":
        return ["l", ";", "'", "."]
    else:
        return [
            "1",
            "q",
            "a",
            "z",
            "2",
            "w",
            "s",
            "x",
            "3",
            "e",
            "d",
            "c",
            "4",
            "r",
            "f",
            "v",
            "5",
            "t",
            "g",
            "b",
            "6",
            "y",
            "h",
            "n",
            "7",
            "u",
            "j",
            "m",
            "8",
            "i",
            "k",
            ",",
            "9",
            "o",
            "l",
            ".",
            "0",
            "p",
            ";",
            "/",
            "-",
            "[",
            "'",
            "=",
            "]",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]


class TypoGenerater:

    @staticmethod
    def generate_8adjacency(input_string: str, error_rate: float) -> str:

        if not (0 <= error_rate <= 1):
            raise ValueError("error_rate should be between 0 and 1")

        KEYSTROKES = [
            "1",
            "q",
            "a",
            "z",
            "2",
            "w",
            "s",
            "x",
            "3",
            "e",
            "d",
            "c",
            "4",
            "r",
            "f",
            "v",
            "5",
            "t",
            "g",
            "b",
            "6",
            "y",
            "h",
            "n",
            "7",
            "u",
            "j",
            "m",
            "8",
            "i",
            "k",
            ",",
            "9",
            "o",
            "l",
            ".",
            "0",
            "p",
            ";",
            "/",
            "-",
            "[",
            "'",
            "=",
            "]",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        typo_index = []
        for i in range(len(input_string)):
            try :
                if random.random() < error_rate:
                    typo_index.append(i)
            except IndexError:
                print("IndexError: ", i, input_string)

        for i in typo_index:
            if i >= len(input_string):
                i=random.randrange(0, len(input_string))
            e = random.randrange(0, 4)
            try :
                if e == 0:  # Swap
                    if i < len(input_string) - 1:
                        input_string = (
                            input_string[:i]
                            + input_string[i + 1]
                            + input_string[i]
                            + input_string[i + 2 :]
                        )
                elif e == 1:  # Delete
                    if i < len(input_string) - 1:
                        input_string = input_string[:i] + input_string[i + 1 :]
                elif e == 2:  # Add
                    input_string = (
                        input_string[:i] + random.choice(KEYSTROKES) + input_string[i:]
                    )
                elif e == 3:  # Replace
                    input_string = (
                        input_string[:i]
                        + random.choice(character_mapping(input_string[i]))
                        + input_string[i + 1 :]
                    )
                else:
                    raise ValueError(
                        "error rate should be between 0 and 3, Should not reach here"
                    )
            except IndexError:
                print("IndexError: ", i, input_string)

        return input_string

    @staticmethod
    def generate(input_string: str, error_rate: float) -> str:
        """
        Generate typos for the input string

        Args:
            input_string (str): The input string
            error_rate (float): The error rate (0 <= error_rate <= 1)

        Raises:
            ValueError: If error_rate is not between 0 and 1
        Returns:
            str: The string with typos
        """

        if not (0 <= error_rate <= 1):
            raise ValueError("error_rate should be between 0 and 1")

        KEYSTROKES = [
            "1",
            "q",
            "a",
            "z",
            "2",
            "w",
            "s",
            "x",
            "3",
            "e",
            "d",
            "c",
            "4",
            "r",
            "f",
            "v",
            "5",
            "t",
            "g",
            "b",
            "6",
            "y",
            "h",
            "n",
            "7",
            "u",
            "j",
            "m",
            "8",
            "i",
            "k",
            ",",
            "9",
            "o",
            "l",
            ".",
            "0",
            "p",
            ";",
            "/",
            "-",
            "[",
            "'",
            "=",
            "]",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]

        typo_index = []
        for i in range(len(input_string)):
            if random.random() < error_rate:
                typo_index.append(i)

        for i in typo_index:
            e = random.randrange(0, 4)
            if e == 0:  # Swap
                if i < len(input_string) - 1:
                    input_string = (
                        input_string[:i]
                        + input_string[i + 1]
                        + input_string[i]
                        + input_string[i + 2 :]
                    )
            elif e == 1:  # Delete
                if i < len(input_string) - 1:
                    input_string = input_string[:i] + input_string[i + 1 :]
            elif e == 2:  # Add
                input_string = (
                    input_string[:i] + random.choice(KEYSTROKES) + input_string[i:]
                )
            elif e == 3:  # Replace
                input_string = (
                    input_string[:i] + random.choice(KEYSTROKES) + input_string[i + 1 :]
                )
            else:
                raise ValueError("e should be between 0 and 3, Should not reach here")

        return input_string


if __name__ == "__main__":
    input_string = "n"
    count = 0
    SAMPLE_SIZE = 1000
    for i in range(SAMPLE_SIZE):
        reuslt = TypoGenerater.generate(input_string, 0.01)
        if reuslt != input_string:
            count += 1
    print("Error rate: {}/{} : {}".format(count, SAMPLE_SIZE, count / SAMPLE_SIZE))
