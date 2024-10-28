import re


def preprocess_text(text):
    text = re.sub(r'[^\u10A0-\u10FF\s]', '', text)

    words = text.split()
    words = [word for word in words if len(word) > 1]

    return list(set(words))


def generate_ngrams(word, n=2):
    padded_word = '*' * (n - 1) + word + '*' * (n - 1)
    return [padded_word[i:i + n] for i in range(len(padded_word) - n + 1)]


def dice_coefficient(word1, word2, n=2):
    ngrams1 = set(generate_ngrams(word1, n))
    ngrams2 = set(generate_ngrams(word2, n))

    common = len(ngrams1.intersection(ngrams2))
    total = len(ngrams1) + len(ngrams2)

    if total == 0:
        return 0.0

    return (2.0 * common) / total


def cluster_words(words, threshold=0.06):
    clusters = []

    for word in words:
        found_cluster = False

        # Compare with existing clusters
        for cluster in clusters:
            # Compare with the representative (smallest word) of each cluster
            if dice_coefficient(cluster[0], word) >= threshold:
                cluster.append(word)
                found_cluster = True
                break

        # If no cluster found, create a new cluster with this word as the representative
        if not found_cluster:
            clusters.append([word])

    # Extract the smallest word in each cluster as the stem
    stems = {min(cluster, key=len) for cluster in clusters}

    return stems, clusters


def ngram_stemmer(text, n=2, threshold=0.06):
    words = preprocess_text(text)

    stems, clusters = cluster_words(words, threshold)

    return stems, clusters


if __name__ == "__main__":
    # Example Georgian text (replace with actual text data)
    with open("SampleText.txt", "r", encoding="utf8") as fr:
        georgian_text = fr.read()

    # Run the N-gram stemmer on the sample text
    stems, clusters = ngram_stemmer(georgian_text, n=2, threshold=0.06)

    print("Extracted Stems:")
    print(stems)

    print("\nClusters:")
    for cluster in clusters:
        print(cluster)
