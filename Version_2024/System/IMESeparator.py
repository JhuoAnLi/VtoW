
from IMEDetector import IMEDetectorSVM


class IMESeparator:
    def __init__(self, separator):
        self.separator = separator
        self.my_bopomofo_detector = IMEDetectorSVM('..\\Model_dump\\bopomofo.pkl', '..\\Model_dump\\vectorizer_bopomofo.pkl')
        self.my_eng_detector = IMEDetectorSVM('..\\Model_dump\\english.pkl', '..\\Model_dump\\vectorizer_english.pkl')
        self.my_cangjie_detector = IMEDetectorSVM('..\\Model_dump\\cangjie.pkl', '..\\Model_dump\\vectorizer_cangjie.pkl')
        self.my_pinyin_detector = IMEDetectorSVM('..\\Model_dump\\pinyin.pkl', '..\\Model_dump\\vectorizer_pinyin.pkl')
    
    def separate(self, input_keystrokes: str)-> list[tuple[str, str]]:
        # input: "su3cl3,Hello, w,o,r,l,d"
        # output: [("bopomofo", "su3cl3"), ("english","Hello world")]
        self.my_bopomofo_detector.predict(input_keystrokes)
        
        pass
        # to do