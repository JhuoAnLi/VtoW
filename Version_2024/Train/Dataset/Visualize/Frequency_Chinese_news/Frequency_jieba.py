from collections import Counter
import jieba
import re

def tokenize_and_count(text):
    tokens = jieba.cut(text)
    word_freq = Counter(tokens)
    return word_freq

def main():
    with open('py\\test.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    text = re.sub(r'\W+', ' ', text)

    max_length = 512
    text_segments = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    partial_word_freqs = []
    for segment in text_segments:
        word_freq = tokenize_and_count(segment)
        partial_word_freqs.append(word_freq)

    total_word_freq = Counter()
    for word_freq in partial_word_freqs:
        total_word_freq += word_freq

    with open('py/output_jieba.txt', 'w', encoding='utf-8') as output_file:
        for word, freq in total_word_freq.most_common():
            output_file.write(f'{word}: {freq}\n')

if __name__ == '__main__':
    jieba.setLogLevel(20)
    main()
