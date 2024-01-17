from collections import Counter
from transformers import BertTokenizer
import re

def tokenize_and_count(text, tokenizer):
    tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))
    word_freq = Counter(tokens)
    return word_freq

def main():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    with open('py\\test.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    text = re.sub(r'\W+', ' ', text)

    max_length = 512
    text_segments = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    partial_word_freqs = []
    for segment in text_segments:
        word_freq = tokenize_and_count(segment, tokenizer)
        partial_word_freqs.append(word_freq)

    total_word_freq = Counter()
    for word_freq in partial_word_freqs:
        total_word_freq += word_freq

    with open('py/output.txt', 'w', encoding='utf-8') as output_file:
        for word, freq in total_word_freq.most_common():
            output_file.write(f'{word}: {freq}\n')

if __name__ == '__main__':
    main()
