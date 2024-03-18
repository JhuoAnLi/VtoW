from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import random
from sklearn.metrics import accuracy_score
import threading
from tqdm import tqdm
import os
import joblib
from sklearn.metrics import confusion_matrix
import numpy as np


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip("\n").split("\t") for line in lines]


class IMEClassifier:
    def __init__(self, data):
        self.data = data
        self.labels = []
        self.vectorizer = TfidfVectorizer()
        self.classifiers = {}
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            [text for text, _ in self.data],
            [label for _, label in self.data],
            test_size=0.2,
            random_state=42,
        )
        self.labels = self.y_train
        self.X = self.vectorizer.fit_transform(self.X_train)

    def train_classifier(self):

        threads = []
        for label in set(self.labels):
            y_binary = [1 if l == label else 0 for l in self.labels]
            thread = threading.Thread(
                target=self.train_classifier_thread, args=(label, y_binary)
            )
            thread.start()
            threads.append(thread)
        for thread in tqdm(threads, desc="Training classifiers"):
            thread.join()

    def train_classifier_thread(self, label, y_binary):
        classifier = SVC(kernel="linear")
        classifier.fit(self.X, y_binary)
        self.classifiers[label] = classifier

    def validate_classifier(self):
        X_val_transformed = self.vectorizer.transform(self.X_val)
        predictions = {}
        for label, classifier in self.classifiers.items():
            y_val_binary = [1 if l == label else 0 for l in self.y_val]
            y_pred = classifier.predict(X_val_transformed)
            accuracy = accuracy_score(y_val_binary, y_pred)
            predictions[label] = {"accuracy": accuracy, "predicted_labels": y_pred}

        # Calculate the final accuracy
        final_accuracy = sum(
            prediction_info["accuracy"] for prediction_info in predictions.values()
        ) / len(predictions)
        print("Validation Accuracy:", final_accuracy * 100, "%")

    # output the decimal probability
    def predict(self, text):
        text_features = self.vectorizer.transform([text])
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

    def save_model(self, modelname):
        save_path = os.path.join(os.getcwd(), "Version_2024\\Model_dump\\")
        joblib.dump(self.classifiers, save_path + modelname)
        joblib.dump(self.vectorizer.get_params(), save_path + "vectorizer_" + modelname)

    def load_model(self, modelname):
        load_path = os.path.join(os.getcwd(), "Version_2024\\Model_dump\\")
        self.classifiers = joblib.load(load_path + modelname)
        vectorizer_config = joblib.load(load_path + "vectorizer_" + modelname)
        self.vectorizer.set_params(**vectorizer_config)
        # self.vectorizer.fit(self.X_train)


if __name__ == "__main__":

    filename = "Version_2024\\Train\\Dataset\\Train_Datasets\\bopomofo-0.txt"
    data = read_file(filename)
    random.seed(42)
    training_random_data = random.sample(data, 300000)
    # training_random_data_list = [(line[0], int(line[1])) for line in training_random_data]

    test_file_name = "Version_2024\\Train\\Dataset\\Train_Datasets\\bopomofo-cc100-0-len20-fortest.txt"
    temp_test_data = read_file(test_file_name)
    testing_random_data = random.sample(temp_test_data, 100000)
    testing_random_data_list = [(line[0], int(line[1])) for line in testing_random_data]

    relative_path = "Version_2024\\Model_dump"
    model_name = "Temp_model_bopomofo-0.pkl"
    if os.path.exists(os.path.join(os.getcwd(), relative_path, model_name)):
        loaded_classifier = IMEClassifier(training_random_data)
        loaded_classifier.load_model(model_name)
        print("Model loaded")
    else:
        text_classifier = IMEClassifier(training_random_data)
        text_classifier.train_classifier()
        text_classifier.validate_classifier()
        text_classifier.save_model(model_name)
        loaded_classifier = IMEClassifier(training_random_data)
        loaded_classifier.load_model(model_name)
        print("Model saved")
        print("Model loaded")

    # new_text = ["cl3", "jmam"]
    # for text in new_text:
    #     print("Test case:", text)
    #     prediction = loaded_classifier.predict(text)
    #     print("Predicted label:", prediction)

    print("Length of testing data:", len(testing_random_data_list))
    true_labels = []
    predicted_labels = []

    for text, true_label in testing_random_data_list:
        prediction = loaded_classifier.predict(text)
        true_labels.append(true_label)
        predicted_labels.append(int(prediction))

    conf_matrix = confusion_matrix(true_labels, predicted_labels)
    print("Confusion Matrix:")
    print(conf_matrix)

    accuracy = np.trace(conf_matrix) / np.sum(conf_matrix) * 100
    print("Test Accuracy:", accuracy)
