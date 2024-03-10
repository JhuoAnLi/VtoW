import re

class LanguageCleaner:
    @staticmethod
    def cleanChinese(input_string:str) -> str:
        """
        Clean the input string to only contain Chinese characters and punctuation

        Args:
            input_string (str): The input string

        Returns:
            str: The cleaned string
        """
        return re.sub(r"[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", "", input_string)
    
    @staticmethod
    def cleanEnglish(input_string:str) -> str:
        """
        Clean the input string to only contain English characters, punctuation and numbers

        Args:
            input_string (str): The input string

        Returns:
            str: The cleaned string
        """
        return re.sub(r"[^a-zA-Z0-9\.,\?! ]", "", input_string)


if __name__ == '__main__':
    test_input = "頒行政院長陳建仁今（16）日出席「112年鳳凰獎楷模表揚典禮」，頒獎表揚74名獲獎義消"
    print(LanguageCleaner.cleanChinese(test_input))
