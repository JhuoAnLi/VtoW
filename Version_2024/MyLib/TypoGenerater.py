
import random

class TypoGenerater:

    @staticmethod
    def generate(input_string:str, error_rate:float) -> str:
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
            "1", "q", "a", "z", "2", "w", "s", "x", 
            "3", "e", "d", "c", "4", "r", "f", "v",
            "5", "t", "g", "b", "6", "y", "h", "n",
            "7", "u", "j", "m", "8", "i", "k", ",",
            "9", "o", "l", ".", "0", "p", ";", "/",
            "-", "[", "'", "=", "]", 
        ]

        typo_index = []
        for i in range(len(input_string)):
            if random.random() < error_rate:
                typo_index.append(i)


        for i in typo_index:
            e = random.randrange(0, 4)
            if e == 0:  # Swap
                if i < len(input_string) - 1:
                    input_string = input_string[:i] + input_string[i + 1] + input_string[i] + input_string[i + 2:]
            elif e == 1:  # Delete
                if i < len(input_string) - 1:
                    input_string = input_string[:i] + input_string[i + 1:]
            elif e == 2:  # Add
                input_string = input_string[:i] + random.choice(KEYSTROKES) + input_string[i:]
            elif e == 3:  # Replace
                input_string = input_string[:i] + random.choice(KEYSTROKES) + input_string[i + 1:]
            else:
                raise ValueError("e should be between 0 and 3, Should not reach here")

        return input_string
    

if __name__ == '__main__':
    input_string = "n"
    count = 0
    SAMPLE_SIZE = 1000
    for i in range(SAMPLE_SIZE):
        reuslt = TypoGenerater.generate(input_string, 0.01)
        if reuslt != input_string:
            count += 1
    print("Error rate: {}/{} : {}".format(count, SAMPLE_SIZE, count / SAMPLE_SIZE))
        
