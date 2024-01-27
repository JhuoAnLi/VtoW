from joblib import Parallel, delayed
from tqdm import tqdm
import os

class DataCutAndLabel:
    """
    This class is used to cut the data and label the data.
    """

    @staticmethod
    def cut_and_label(data_src_path: str, data_trg_path: str,size: int, label: str) -> None:
        """
        Cut the data from the source data with the given size, and save the data to the target data path.
        If the orginal length of the src data is less than the given size,
        join the line with the next line until the length of the line is greater than the given size.

        Args:
            data_src_path (str): the path of the source data
            data_trg_path (str): the path of the target data
            size (int): the size of the target data
            label (str): the label of the target data
        
        Raises:
            AssertionError: if the given size is less than 0

        Returns:
            None
        """

        assert size > 0, "The size of the target data must be greater than 0."
        with open(data_src_path, "r", encoding="utf-8") as f:
            with open(data_trg_path, "a", encoding="utf-8") as f2:
                line = f.readline()
                while line:
                    if len(line) > size:
                        f2.write(line[:size] + "\t" + label + "\n")
                        line = line[size:]
                    else:
                        line = line[:-1] + f.readline()

if __name__ == "__main__":
    SRC_DATASET_PATH = os.path.join(os.path.dirname(__file__) , ".\\Dataset\\Key_Stroke_Datasets\\")
    TARGET_DATASET_PATH = os.path.join(os.path.dirname(__file__) , ".\\Dataset\\Train_Datasets\\")
    CUT_SIZE = 20
    TARGET_LANGUAGE = "bopomofo"
    ERROR_RATE = 0

    files = ["bopomofo-news-0.txt", "cangjie-news-0.txt", "pinyin-news-0.txt", "english-0.txt"]

    target_file_name = "{}-{}.txt".format(TARGET_LANGUAGE, str(ERROR_RATE).replace(".", "_"))


    if not os.path.exists(TARGET_DATASET_PATH):
        print("Creating target dataset path: {}".format(TARGET_DATASET_PATH))
        for file in tqdm(files, desc="Processing files"):
            if file.startswith(TARGET_LANGUAGE):
                DataCutAndLabel.cut_and_label(SRC_DATASET_PATH + file, TARGET_DATASET_PATH + target_file_name, CUT_SIZE, "1")
            else:
                DataCutAndLabel.cut_and_label(SRC_DATASET_PATH + file, TARGET_DATASET_PATH + target_file_name, CUT_SIZE, "0")
    else:
        print("Target dataset path already exists: {}".format(TARGET_DATASET_PATH))
        print("Skipping cutting and labeling data.")
