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
import re


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip("\n").split("\t") for line in lines]


def custom_tokenizer_bopomofo(text):
    if not text:
        return []
    pattern = re.compile(r"(?<=3|4|6|7| )")
    tokens = pattern.split(text)
    tokens = [token for token in tokens if token]
    if tokens[-1].find("§") != -1:
        tokens.pop()

    return tokens


def custom_tokenizer_cangjie(text):
    if not text:
        return []
    pattern = re.compile(r"(?<=[ ])")
    tokens = pattern.split(text)
    tokens = [token for token in tokens if token]
    if tokens[-1].find("§") != -1:
        tokens.pop()
    return tokens


def custom_tokenizer_pinyin(text):
    if not text:
        return []
    tokens = []
    pattern = re.compile(
        r"(?:[bpmfdtnlgkhjqxzcsyw]|[zcs]h)?(?:[aeiouv]?ng|[aeiou](?![aeiou])|[aeiou]?[aeiou]?r|[aeiou]?[aeiou]?[aeiou])"
    )
    matches = re.findall(pattern, text)
    tokens.extend(matches)
    if tokens and tokens[-1].find("§") != -1:
        tokens.pop()
    return tokens


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

    def train_classifier(self):

        threads = []
        self.labels = self.y_train
        self.X = self.vectorizer.fit_transform(self.X_train)
        for label in set(self.labels):
            y_binary = [1 if l == label else 0 for l in self.labels]
            thread = threading.Thread(
                target=self.train_classifier_thread, args=(label, y_binary)
            )
            thread.start()
            threads.append(thread)
        for thread in tqdm(threads, desc="Training classifiers"):
            thread.join()
        print(
            "Number of tokens in TfidfVectorizer: ",
            len(self.vectorizer.get_feature_names_out()),
        )
        print("Features: ")
        for features in self.vectorizer.get_feature_names_out()[:100]:
            print(features)

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

    # def predict(self, text):
    #     text_features = self.vectorizer.transform([text])
    #     predictions = {}
    #     correct_predictions = 0
    #     total_predictions = 0
    #     for label, classifier in self.classifiers.items():
    #         prediction = classifier.decision_function(text_features)[0]
    #         predictions[label] = prediction
    #         if prediction == label:
    #             correct_predictions += 1
    #         total_predictions += 1
    #     # print("Predictions:", predictions)
    #     return max(predictions, key=predictions.get)

    def predict(self, input: str, positive_bound: float = 1, neg_bound: float = -0.5):
        text_features = self.vectorizer.transform([input])
        predictions = {}
        for label, classifier in self.classifiers.items():
            prediction = classifier.decision_function(text_features)[0]
            predictions[label] = prediction
        # print("Predictions:", predictions)

        if predictions["1"] > positive_bound or (neg_bound < predictions["1"] < 0):
            return 1
        else:
            return 0

    def save_model(self, modelname):
        save_path = os.path.join(os.getcwd(), "Version_2024\\Model_dump\\")
        joblib.dump(self.classifiers, save_path + modelname)
        joblib.dump(self.vectorizer, save_path + "vectorizer_" + modelname)

    def load_model(self, modelname):
        load_path = os.path.join(os.getcwd(), "Version_2024\\Model_dump\\")
        self.classifiers = joblib.load(load_path + modelname)
        self.vectorizer = joblib.load(load_path + "vectorizer_" + modelname)


if __name__ == "__main__":

    file_1 = "Version_2024\\Train\\Dataset\\Train_Datasets\\labeled_english_0_train.txt"
    file_2 = (
        "Version_2024\\Train\\Dataset\\Train_Datasets\\labeled_english_r0-1_train.txt"
    )
    data_1 = read_file(file_1)
    data_2 = read_file(file_2)
    random.seed(42)
    training_random_data_1 = random.sample(data_1, 450000)
    training_random_data_2 = random.sample(data_2, 150000)
    training_random_data = training_random_data_1 + training_random_data_2
    training_random_data_list = [
        (line[0], int(line[1])) for line in training_random_data
    ]

    test_file_name = (
        "Version_2024\\Train\\Dataset\\Test_Datasets\\labeled_english_0_test.txt"
    )
    temp_test_data = read_file(test_file_name)
    testing_random_data = random.sample(temp_test_data, 50000)
    testing_random_data_list = [(line[0], int(line[1])) for line in testing_random_data]

    print("Test Dataset: labeled_bopomofo_0_test.txt, 100000 Samples")

    relative_path = "Version_2024\\Model_dump"
    model_name = "temp_english_8adj.pkl"

    if os.path.exists(os.path.join(os.getcwd(), relative_path, model_name)):
        loaded_classifier = IMEClassifier(training_random_data)
        loaded_classifier.load_model(model_name)
        print(model_name)
        print("Model loaded")
    else:
        print("Total Train Dataset: 480000 Samples")
        print("Train Dataset 1: labeled_pinyin_0_train, 360000 Samples")
        print("Train Dataset 2: labeled_pinyin_r0-1_train, 120000 Samples")
        print()
        print("Validation Dataset: 120000 Samples")
        text_classifier = IMEClassifier(training_random_data)
        text_classifier.train_classifier()
        text_classifier.validate_classifier()
        text_classifier.save_model(model_name)
        loaded_classifier = IMEClassifier(training_random_data)
        loaded_classifier.load_model(model_name)
        print(model_name)
        print("Model saved")
        print("Model loaded")

    # new_text = ["cl3", "jmam","weather"]
    # for text in new_text:
    #     print("Test case:", text)
    #     prediction = loaded_classifier.predict(text)
    #     print("Predicted label:", prediction)

    print("Length of testing data:", len(testing_random_data_list))
    true_labels = []
    predicted_labels = []

    with open("english_error0_prediction_errors.txt", "w", encoding="utf-8") as f:
        for text, true_label in testing_random_data_list:
            prediction = loaded_classifier.predict(text)
            true_labels.append(true_label)
            predicted_labels.append(int(prediction))

        for text, true_label, predicted_label in zip(
            testing_random_data_list, true_labels, predicted_labels
        ):
            if true_label != predicted_label:
                f.write("Text: {}\n".format(text))
                f.write("True Label: {}\n".format(true_label))
                f.write("Predicted Label: {}\n".format(predicted_label))
                f.write("\n")

    conf_matrix = confusion_matrix(true_labels, predicted_labels)
    print("Confusion Matrix:")
    print("\t  Predicted 0\t Predicted 1")
    print("True 0\t", conf_matrix[0, 0], "\t\t", conf_matrix[0, 1])
    print("True 1\t", conf_matrix[1, 0], "\t\t", conf_matrix[1, 1])

    accuracy = np.trace(conf_matrix) / np.sum(conf_matrix) * 100
    print("Test Accuracy:", accuracy)
