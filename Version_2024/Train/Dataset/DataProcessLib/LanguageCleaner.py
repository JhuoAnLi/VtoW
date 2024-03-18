import re
import warnings

def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"\033[91m"+ "Call to deprecated function {func.__name__}" + "\033[0m", category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper

# Set warnings to raise an error by default
warnings.simplefilter('error', DeprecationWarning)

class LanguageCleaner:
    @staticmethod
    @deprecated
    def cleanChinese(input_string:str) -> str:
        """
        Clean the input string to only contain Chinese characters and punctuation
        but not the newline

        Args:
            input_string (str): The input string

        Returns:
            str: The cleaned string
        """

        return re.sub(r"[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\n]", "", input_string)

    @staticmethod
    @deprecated
    def cleanEnglish(input_string:str) -> str:
        """
        Clean the input string to only contain English characters, punctuation and numbers

        Args:
            input_string (str): The input string

        Returns:
            str: The cleaned string
        """
        return re.sub(r"[^a-zA-Z0-9\.,\?! ]", "", input_string)

    @staticmethod
    def clean(input_string:str, language:str, reserve_newline:bool) -> str:
        """
        Clean the input string to only contain the specified language characters and punctuation

        Args:
            input_string (str): The input string
            language (str): The language to reserve, "chinese" or "english"
            reserve_newline (bool): Whether to reserve the newline character

        Returns:
            str: The cleaned string
        """

        if language == "chinese":  # fix: make newline regex more readable, separate the logic
            pattern = r"[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\n]" if reserve_newline else r"[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]"
        elif language == "english":
            pattern = r"[^a-zA-Z0-9\.,\?! \n]" if reserve_newline else r"[^a-zA-Z0-9\.,\?! ]"
        else:
            raise ValueError("Error: language '{}' is not supported".format(language))

        return re.sub(pattern, "", input_string)

if __name__ == '__main__':
    test_input = "★ 內建智慧晶片可自動切換和雙系統接上即可使用"
    print(LanguageCleaner.cleanChinese(test_input))
