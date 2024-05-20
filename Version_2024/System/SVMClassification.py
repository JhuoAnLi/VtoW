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
from sklearn.feature_extraction.text import TfidfVectorizer
from torch.utils.data import DataLoader, Dataset
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import torch.optim as optim
model_name = "dl_pinyin"

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


# class IMEClassifier:
#     def __init__(self, data):
#         self.data = data
#         self.labels = []
#         self.vectorizer = TfidfVectorizer()
#         self.classifiers = {}
#         self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
#             [text for text, _ in self.data],
#             [label for _, label in self.data],
#             test_size=0.2,
#             random_state=42,
#         )

#     def train_classifier(self):

#         threads = []
#         self.labels = self.y_train
#         self.X = self.vectorizer.fit_transform(self.X_train)
#         for label in set(self.labels):
#             y_binary = [1 if l == label else 0 for l in self.labels]
#             thread = threading.Thread(
#                 target=self.train_classifier_thread, args=(label, y_binary)
#             )
#             thread.start()
#             threads.append(thread)
#         for thread in tqdm(threads, desc="Training classifiers"):
#             thread.join()
#         print(
#             "Number of tokens in TfidfVectorizer: ",
#             len(self.vectorizer.get_feature_names_out()),
#         )
#         print("Features: ")
#         for features in self.vectorizer.get_feature_names_out()[:100]:
#             print(features)

#     def train_classifier_thread(self, label, y_binary):
#         classifier = SVC(kernel="linear")
#         classifier.fit(self.X, y_binary)
#         self.classifiers[label] = classifier

#     def validate_classifier(self):
#         X_val_transformed = self.vectorizer.transform(self.X_val)
#         predictions = {}
#         for label, classifier in self.classifiers.items():
#             y_val_binary = [1 if l == label else 0 for l in self.y_val]
#             y_pred = classifier.predict(X_val_transformed)
#             accuracy = accuracy_score(y_val_binary, y_pred)
#             predictions[label] = {"accuracy": accuracy, "predicted_labels": y_pred}

#         # Calculate the final accuracy
#         final_accuracy = sum(
#             prediction_info["accuracy"] for prediction_info in predictions.values()
#         ) / len(predictions)
#         print("Validation Accuracy:", final_accuracy * 100, "%")

#     def predict(self, input: str, positive_bound: float = 1, neg_bound: float = -0.5):
#         text_features = self.vectorizer.transform([input])
#         predictions = {}
#         for label, classifier in self.classifiers.items():
#             prediction = classifier.decision_function(text_features)[0]
#             predictions[label] = prediction
#         # print("Predictions:", predictions)

#         if predictions["1"] > positive_bound or (neg_bound < predictions["1"] < 0):
#             return 1
#         else:
#             return 0

#     def save_model(self, modelname):
#         save_path = os.path.join(os.getcwd(), "Version_2024\\Model_dump\\")
#         joblib.dump(self.classifiers, save_path + modelname)
#         joblib.dump(self.vectorizer, save_path + "vectorizer_" + modelname)


#     def load_model(self, modelname):
#         load_path = os.path.join(os.getcwd(), "Version_2024\\Model_dump\\")
#         self.classifiers = joblib.load(load_path + modelname)
#         self.vectorizer = joblib.load(load_path + "vectorizer_" + modelname)
class SparseTensorDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx].to_dense(), self.y[idx]


class IMEClassifier_Deep_Learning:
    def __init__(self, data):
        self.data = data
        self.vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer_pinyin)
        # self.vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer_bopomofo)
        # self.vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer_cangjie)
        # self.vectorizer = TfidfVectorizer()
        self.classifiers = {}
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            [text for text, _ in self.data],
            [label for _, label in self.data],
            test_size=0.2,
            random_state=42,
        )
        self.X_train_tfidf = self.vectorizer.fit_transform(self.X_train)
        self.X_val_tfidf = self.vectorizer.transform(self.X_val)

        self.le = LabelEncoder()
        self.y_train_enc = self.le.fit_transform(self.y_train)
        self.y_val_enc = self.le.transform(self.y_val)

        self.y_train_cat = torch.tensor(self.y_train_enc, dtype=torch.long)
        self.y_val_cat = torch.tensor(self.y_val_enc, dtype=torch.long)

        self.X_train_tensor = self._sparse_matrix_to_tensor(self.X_train_tfidf)
        self.X_val_tensor = self._sparse_matrix_to_tensor(self.X_val_tfidf)

        self.best_val_accuracy = 0.0

    def _sparse_matrix_to_tensor(self, sparse_matrix):
        sparse_matrix = sparse_matrix.tocoo()
        values = sparse_matrix.data
        indices = np.vstack((sparse_matrix.row, sparse_matrix.col))
        i = torch.LongTensor(indices)
        v = torch.FloatTensor(values)
        shape = sparse_matrix.shape
        return torch.sparse_coo_tensor(i, v, torch.Size(shape)).to(device)

    def build_model(self, input_shape, num_classes):
        model = nn.Sequential(
            nn.Linear(input_shape, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
            nn.Softmax(dim=1),
        )
        return model.to(device)

    def train_classifier(self):
        input_shape = self.X_train_tensor.shape[1]
        num_classes = len(set(self.y_train_cat.numpy()))
        self.model = self.build_model(input_shape, num_classes)

        batch_size = 32
        train_dataset = SparseTensorDataset(self.X_train_tensor, self.y_train_cat)
        val_dataset = SparseTensorDataset(self.X_val_tensor, self.y_val_cat)

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        epochs = 10
        for epoch in range(epochs):
            self.model.train()
            total_loss = 0
            train_loader_tqdm = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}")
            for X_batch, y_batch in train_loader_tqdm:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                optimizer.zero_grad()
                output = self.model(X_batch)
                loss = criterion(output, y_batch)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                train_loader_tqdm.set_postfix({"Loss": total_loss / len(train_loader)})

            avg_loss = total_loss / len(train_loader)

            # Validation after each epoch
            self.model.eval()
            val_loss = 0
            correct = 0
            total = 0
            with torch.no_grad():
                for X_batch, y_batch in val_loader:
                    X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                    outputs = self.model(X_batch)
                    loss = criterion(outputs, y_batch)
                    val_loss += loss.item()
                    _, predicted = torch.max(outputs, 1)
                    total += y_batch.size(0)
                    correct += (predicted == y_batch).sum().item()
            avg_val_loss = val_loss / len(val_loader)
            accuracy = 100 * correct / total

            print(
                f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss}, Val Loss: {avg_val_loss}, Accuracy: {accuracy}%"
            )
            with open(
                "..\\System_Test\\dl_english_log.txt", "a", encoding="utf-8"
            ) as f:
                f.write(
                    f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss}, Val Loss: {avg_val_loss}, Accuracy: {accuracy}%\n"
                )

            if accuracy > self.best_val_accuracy:
                self.best_val_accuracy = accuracy
                self.save_best_model(model_name)

    def validate_classifier(self):
        self.load_model(model_name)

        self.model.eval()
        val_dataset = SparseTensorDataset(self.X_val_tensor, self.y_val_cat)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

        correct = 0
        total = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                outputs = self.model(X_batch)
                _, predicted = torch.max(outputs, 1)
                total += y_batch.size(0)
                correct += (predicted == y_batch).sum().item()

        accuracy = 100 * correct / total
        print("Validation Accuracy:", accuracy, "%")

    def predict(self, input_text):
        self.model.eval()
        input_tfidf = self.vectorizer.transform([input_text])
        input_tensor = self._sparse_matrix_to_tensor(input_tfidf).to_dense()
        with torch.no_grad():
            output = self.model(input_tensor)
            _, predicted = torch.max(output, 1)
        return self.le.inverse_transform(predicted.cpu().numpy())[0]

    def save_best_model(self, modelname):
        print("Saving model...")
        save_path = os.path.join("..", "Model_dump")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        torch.save(self.model.state_dict(), os.path.join(save_path, modelname + ".pth"))
        joblib.dump(self.vectorizer, os.path.join(save_path, "vectorizer_" + modelname + ".pkl"))
        joblib.dump(self.le, os.path.join(save_path, "label_encoder_" + modelname + ".pkl"))

    def load_model(self, modelname):
        load_path = os.path.join("..", "Model_dump")
        input_shape = self.X_train_tensor.shape[1]
        num_classes = len(set(self.y_train_cat.numpy()))
        self.model = self.build_model(input_shape, num_classes)
        self.model.load_state_dict(
            torch.load(os.path.join(load_path, modelname + ".pth"))
        )
        self.vectorizer = joblib.load(
            os.path.join(load_path, "vectorizer_" + modelname + ".pkl")
        )
        self.le = joblib.load(
            os.path.join(load_path, "label_encoder_" + modelname + ".pkl")
        )


if __name__ == "__main__":

    file_1 = "..\\Train\\Dataset\\Train_Datasets\\labeled_pinyin_0_train.txt"
    file_2 = "..\\Train\\Dataset\\Train_Datasets\\labeled_pinyin_r0-1_train.txt"
    data_1 = read_file(file_1)
    data_2 = read_file(file_2)
    random.seed(42)
    training_random_data_1 = random.sample(data_1, 450000)
    training_random_data_2 = random.sample(data_2, 150000)
    training_random_data = training_random_data_1 + training_random_data_2

    relative_path = "..\\Model_dump"
    

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)
    
    if os.path.exists(relative_path + "/" + "vectorizer_" + model_name + ".pkl"):
        loaded_classifier = IMEClassifier_Deep_Learning(training_random_data)
        loaded_classifier.load_model(model_name)
        print(model_name)
        print("Model loaded")
    else:
        print("Not found model")
        print("Total Train Dataset: 480000 Samples")
        print("Train Dataset 1 : 360000 Samples")
        print("Train Dataset 2 : 120000 Samples")
        print("Validation Dataset: 120000 Samples")
        loaded_classifier = IMEClassifier_Deep_Learning(training_random_data)
        loaded_classifier.train_classifier()
        loaded_classifier.validate_classifier()

    # new_text = ["cl3", "jmam", "weather"]
    # for text in new_text:
    #     print("Test case:", text)
    #     prediction = loaded_classifier.predict(text)
    #     print("Predicted label:", prediction)

    test_file_name = "..\\Train\\Dataset\\Test_Datasets\\labeled_pinyin_r0-1_test.txt"
    temp_test_data = read_file(test_file_name)
    testing_random_data = random.sample(temp_test_data, 50000)
    testing_random_data_list = [(line[0], int(line[1])) for line in testing_random_data]

    print("Length of testing data:", len(testing_random_data_list))
    true_labels = []
    predicted_labels = []

    # with open("english_error0_prediction_errors.txt", "w", encoding="utf-8") as f:
    for text, true_label in testing_random_data_list:
        prediction = loaded_classifier.predict(text)
        true_labels.append(true_label)
        predicted_labels.append(int(prediction))

        # for text, true_label, predicted_label in zip(
        #     testing_random_data_list, true_labels, predicted_labels
        # ):
        #     if true_label != predicted_label:
        #         f.write("Text: {}\n".format(text))
        #         f.write("True Label: {}\n".format(true_label))
        #         f.write("Predicted Label: {}\n".format(predicted_label))
        #         f.write("\n")

    conf_matrix = confusion_matrix(true_labels, predicted_labels)
    print("Confusion Matrix:")
    print("\t  Predicted 0\t Predicted 1")
    print("True 0\t", conf_matrix[0, 0], "\t\t", conf_matrix[0, 1])
    print("True 1\t", conf_matrix[1, 0], "\t\t", conf_matrix[1, 1])

    accuracy = np.trace(conf_matrix) / np.sum(conf_matrix) * 100
    print("Test Accuracy:", accuracy)
