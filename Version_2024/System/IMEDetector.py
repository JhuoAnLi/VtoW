import os

import joblib
from abc import ABC, abstractmethod

def not_implemented_yet_decorator(func):
    def wrapper(*args, **kwargs):
        print(f'Function {func.__name__} is not implemented yet.')
        return func(*args, **kwargs)
    return wrapper

@not_implemented_yet_decorator
class IMEDetector(ABC):
    @not_implemented_yet_decorator
    def __init__(self) -> None:
        self.classifiers = None
        self.vectorizer = None

    @not_implemented_yet_decorator
    def load_model(self, model_path: str) -> None:
        pass

    @not_implemented_yet_decorator
    def predict(self, input: str) -> str:
        pass


class IMEDetectorSVM(IMEDetector):
    def __init__(self) -> None:
        super().__init__()

    def load_model(self, svm_model_path: str, tfidf_vectorizer_path:str) -> None:
        try:
            self.classifiers = joblib.load(svm_model_path)
            print(f'Model loaded from {svm_model_path}')



            self.vectorizer.fit([text for text, _ in self.data])
        except Exception as e:
            print(f'Error loading model from {model_path}')
            print(e)


    def predict(self, input: str) -> str:
        pass