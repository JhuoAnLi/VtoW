from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer


class TextClassifier:
    def __init__(self, file_path_0, file_path_1, file_path_2, file_path_3):
        self.text_splitter_0 = TextSplitter(file_path_0)
        self.text_splitter_1 = TextSplitter(file_path_1)
        self.text_splitter_2 = TextSplitter(file_path_2)
        self.text_splitter_3 = TextSplitter(file_path_3)
        self.data = []
        self.labels = []
        self.vectorizer = TfidfVectorizer()
        self.classifiers = {}

    def train_classifier(self):
        # change the label of different training datasets
        self.text_splitter_0.read_file(1)  # bopomofo
        self.text_splitter_1.read_file(0)  # English
        self.text_splitter_2.read_file(0)  # cangjie
        self.text_splitter_3.read_file(0)  # pinyin
        self.data = (
            self.text_splitter_0.get_data()
            + self.text_splitter_1.get_data()
            + self.text_splitter_2.get_data()
        )
        # print(self.data)
        self.labels = [label for _, label in self.data]

        X = self.vectorizer.fit_transform([text for text, _ in self.data])
        print(self.vectorizer.get_feature_names_out())
        print(X.shape)
        # print(type(X))
        # print(X)
        for label in set(self.labels):
            y_binary = [1 if l == label else 0 for l in self.labels]
            classifier = SVC(kernel="linear")
            classifier.fit(X, y_binary)
            self.classifiers[label] = classifier

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
        print("Predictions:", predictions)
        return max(predictions, key=predictions.get)

    # output the rounded decimal probability
    def predict_rounded(self, text):
        text_features = self.vectorizer.transform([text])
        predictions = {}
        correct_predictions = 0
        total_predictions = 0
        for label, classifier in self.classifiers.items():
            prediction = classifier.predict(text_features)[0]
            predictions[label] = prediction
            if prediction == label:
                correct_predictions += 1
            total_predictions += 1
        print("Rounded Predictions:", predictions)
        return max(predictions, key=predictions.get)


class TextSplitter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def read_file(self, label):
        with open(self.file_path, "r", encoding="utf-8") as file:
            current_fragment = ""
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.strip()
                remaining_space = 20 - len(current_fragment)
                if len(line) >= remaining_space:
                    current_fragment += line[:remaining_space]
                    self.data.append((current_fragment, label))
                    current_fragment = ""
                    line = line[remaining_space:]
                    while len(line) >= 20:
                        self.data.append((line[:20], label))
                        line = line[20:]
                    current_fragment = line
                else:
                    current_fragment += line

    def get_data(self):
        return self.data


if __name__ == "__main__":
    file_path_0 = "Version_2024\\MyTrainLib\\test.txt"
    file_path_1 = "Version_2024\\MyTrainLib\\test2.txt"
    file_path_2 = "Version_2024\\MyTrainLib\\test3.txt"
    file_path_3 = "Version_2024\\MyTrainLib\\test4.txt"

    classifier = TextClassifier(file_path_0, file_path_1, file_path_2, file_path_3)
    classifier.train_classifier()

    # test case
    text = ["4b4fu3m06fm", "former", "hqm omrl"]
    for line in text:
        print("\nText:", line)
        prediction = classifier.predict(line)
        prediction_rounded = classifier.predict_rounded(line)
        print("Final Output Label:", prediction)
        # print("text:", line)
        # print("Prediction:", prediction)
        # print("Rounded Prediction:", prediction_rounded)
