from nltk import word_tokenize, PorterStemmer

stemmer = PorterStemmer()


def tokenizer(sentance):
    return word_tokenize(sentance)


def stem(word):
    return stemmer.stem(word.lower())
