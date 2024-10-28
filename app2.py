from collections import Counter
from math import log

ngram_size = 2

def preprocess_georgian_text(text):
    words = text.split()
    words = [word for word in words if word.isalpha()]
    return words

def padd_words(word, ngram_size):
    return '*' * (ngram_size - 1) + word + '*' * (ngram_size - 1)

def extract_ngrams(words, ngram_size):
    ngrams = []
    for temp in words:
        word = padd_words(temp, ngram_size)
        for i in range(len(word) - ngram_size + 1):
            ngrams.append(word[i:i + ngram_size])
    return ngrams


def get_ngram_frequencies(ngrams):
    return Counter(ngrams)


def ngram_stem(word, ngram_freq, corpus_word_count):
    max_freq = 0
    best_stem = word
    best_idf = 0

    for i in range(len(word), 0, -1):
        stem = word[:i]
        if stem in ngram_freq:
            ngram_count = ngram_freq[stem]
            idf = log(corpus_word_count / (ngram_count + 1))  # Calculate IDF
            if ngram_count * idf > max_freq * best_idf:
                max_freq = ngram_count
                best_stem = stem
                best_idf = idf

    return best_stem

def apply_ngram_stemmer(corpus, ngram_size):
    # Preprocess the corpus
    words = preprocess_georgian_text(corpus)
    corpus_word_count = len(words)

    # Extract n-grams and their frequencies
    ngram_freq = get_ngram_frequencies(extract_ngrams(words, ngram_size))

    # Apply the N-Gram Stemmer with IDF
    stemmed_words = [(word, ngram_stem(word, ngram_freq, corpus_word_count)) for word in words]

    return stemmed_words


def write_stemmed_words_to_file(word_stem_pairs, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for original_word, stemmed_word in word_stem_pairs:
            file.write(f"{original_word} -> {stemmed_word}\n")

# file_name = "wiki_small.txt"
file_name = "test.txt"

with open(file_name, "r", encoding="utf8") as fr:
    georgian_corpus = fr.read()

word_stem_pairs = apply_ngram_stemmer(georgian_corpus, ngram_size)

output_file_path = "stemmed_words.txt"
write_stemmed_words_to_file(word_stem_pairs, output_file_path)

if __name__ == "__main__":
    # g = extract_ngrams(["საქართველო"], ngram_size)
    # print(g)
    pass