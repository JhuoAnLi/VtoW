from gensim.models import word2vec
import gensim
import os


if __name__ == "__main__":
    sg = 0
    win_size = 2
    vector_size = 300
    epochs = 10

    if os.path.exists("word2vec.model"):
        model = gensim.models.Word2Vec.load("word2vec.model")
        print(model.wv.most_similar("早安", topn=10))
    else:
        sentences = word2vec.LineSentence(
            "..\\Train\\Dataset\\Plain_Text_Datasets\\Chinese_WebCrawlData_cc100.txt"
        )
        model = word2vec.Word2Vec(
            sentences,
            vector_size=vector_size,
            window=win_size,
            sg=sg,
            min_count=1,
            epochs=epochs,
        )
        model.save("word2vec.model")
