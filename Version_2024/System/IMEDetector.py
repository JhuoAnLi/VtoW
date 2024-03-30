import os

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from abc import ABC, abstractmethod
import re

def not_implemented_yet_decorator(func):
    def wrapper(*args, **kwargs):
        print(f'Function {func.__name__} is not implemented yet.')
        return func(*args, **kwargs)
    return wrapper

def custom_tokenizer_bopomofo(text):  # fix: depand on the tokenizer using in training
    if not text:
        return []
    pattern = re.compile(r"(?<=3|4|6|7| )")
    tokens = pattern.split(text)
    tokens = [token for token in tokens if token]
    if tokens[-1].find("§") != -1:
        tokens.pop()

    return tokens

class IMEDetector(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def load_model(self, model_path: str) -> None:
        pass

    @abstractmethod
    def predict(self, input: str) -> str:
        pass


class IMEDetectorSVM(IMEDetector):
    def __init__(self, svm_model_path:str, tfidf_vectorizer_path:str) -> None:
        super().__init__()
        self.classifiers = None
        self.vectorizer = None
        self.load_model(svm_model_path, tfidf_vectorizer_path)


    def load_model(self, svm_model_path: str, tfidf_vectorizer_path:str) -> None:
        try:
            self.classifiers = joblib.load(svm_model_path)
            print(f'Model loaded from {svm_model_path}')
            self.vectorizer = joblib.load(tfidf_vectorizer_path)
            print(f'Vectorizer loaded from {tfidf_vectorizer_path}')

        except Exception as e:
            print(f'Error loading model and vectorizer.')
            print(e)


    def predict(self, input: str) -> str:
        text_features = self.vectorizer.transform([input])
        predictions = {}
        correct_predictions = 0
        total_predictions = 0
        for label, classifier in self.classifiers.items():
            prediction = classifier.decision_function(text_features)[0]
            predictions[label] = prediction
            if prediction == label:
                correct_predictions += 1
            total_predictions += 1
        # print("Predictions:", predictions)
        return max(predictions, key=predictions.get)
    
if __name__ == "__main__":
    my_bopomofo_detector = IMEDetectorSVM('..\\Model_dump\\bopomofo.pkl', '..\\Model_dump\\vectorizer_bopomofo.pkl')
    input_text = "su3cl3"
    while True:
        input_text = input('Enter text: ')
        print("Is bopomofo:", True if my_bopomofo_detector.predict(input_text) == "1" else False)
