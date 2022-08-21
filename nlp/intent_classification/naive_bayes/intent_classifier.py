import json
from lib2to3.pgen2 import token
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# from nlp.intent_classification.nltk_utils import tokenizer
import pickle

from nltk import word_tokenize, PorterStemmer

stemmer = PorterStemmer()

stop_words = ["?", ".", "!", ","]


def tokenizer(sentance):
    return word_tokenize(sentance)


def stem(word):
    return stemmer.stem(word.lower())


def preprocess(sentance: str) -> str:
    tokens = tokenizer(sentance=sentance)
    tokens = [stem(token) for token in tokens if token not in stop_words]
    sentance = " ".join(tokens)

    return sentance


print("model imported")


class NaiveByasModel:
    def __init__(self,) -> None:
        '''
        description: None

        Inputs: None

        Ouputs: None

        '''
        self.saving_location = "nlp/intent_classification/naive_bayes/pre_trained_model/"
        self.model = None
        self.countVectorizer = None
        self.tfidf_transformer = None
        self.intets = None

        self.load_models()

    def find_intent(self, command: str) -> str:
        '''
        description:
            find the intent of the command

        Inputs:
            command = "your command or query"

        Outputs:
            return intent

            `if this intent has low probability then return "not a command"`
        '''

        command = [preprocess(command)]
        print(command)
        command = self.countVectorizer.transform(command)
        command = self.tfidf_transformer.transform(command)

        proba = self.model.predict_proba(command)

        if proba.max() < 0.2:
            return "not a command"

        return self.intets[np.argmax(proba)]

    def load_models(self):
        '''
        description:
            load the pretrained model

        Inputs: None
        Outputs : None

        '''
        self.model = pickle.load(
            open(self.saving_location + '/model.pkl', 'rb'))

        self.tfidf_transformer = pickle.load(
            open(self.saving_location + '/tfidf_transformer.pkl', 'rb'))

        self.countVectorizer = pickle.load(
            open(self.saving_location + '/countVectorizer.pkl', 'rb'))

        self.intets = pickle.load(
            open(self.saving_location + '/intents.pkl', 'rb'))


#################

class TrainModel:
    def __init__(self, intents_json_file) -> None:
        '''
        description:
            None

        Inputs:
            intent_json_file = "your intent json file"

        Ouputs:
            return x_train,_train

        '''
        # models and encoders saving location
        self.saving_location = "nlp/intent_classification/naive_bayes/pre_trained_model/"
        self.intents = intents_json_file
        self.training_data = self.load_training_data()

        self.x_train, self.y_train = self.training_data

        self.naive_bayes_classifier = MultinomialNB()

        self.train()

    def load_training_data(self):
        '''
        description:
            it convert the json file into x_train, y_train

        Inputs:
           None

        Ouputs:
            return ( x_train, y_train )
        '''
        with open(self.intents, "r") as f:
            intents = json.load(f)

        # vocab = []
        tags = []
        train_data = []
        text_courps = []

        for intent in intents["intents"]:
            tag = intent["tag"]
            tags.append(tag)
            for pattern in intent["patterns"]:
                pattern = preprocess(pattern)
                print(pattern)
                text_courps.append(pattern)
                words = np.array(tokenizer(pattern))
                # vocab.extend(words)
                train_data.append((words, tag))

        count = CountVectorizer()
        word_count = count.fit_transform(text_courps)

        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        tfidf_transformer.fit(word_count)
        tf_idf_vector = tfidf_transformer.transform(word_count)

        x_train = tf_idf_vector.toarray()
        y_train = np.array(train_data)[:, 1]
        y_train = list(y_train)

        # encoding each intent names to numeric number
        for i in range(len(y_train)):
            y_train[i] = tags.index(y_train[i])

        data = np.concatenate(
            (x_train, np.array(y_train).reshape(-1, 1)), axis=1)

        np.random.shuffle(data)

        x_train = data[:, :-1]
        y_train = data[:, -1]

        print("data transformed")
        print(x_train[0], y_train)

        pickle.dump(tfidf_transformer, open(
            self.saving_location + 'tfidf_transformer.pkl', 'wb'))

        pickle.dump(count, open(
            self.saving_location + 'countVectorizer.pkl', 'wb'))

        pickle.dump(tags, open(
            self.saving_location + 'intents.pkl', 'wb'))

        return x_train, y_train

    def train(self):
        '''
        desciption:
            it train the model using x_train and y_train and
            save the model in pre_trained_model folder

        Inputs: None
        Outputs: None
        '''
        self.naive_bayes_classifier.fit(self.x_train, self.y_train)

        pickle.dump(self.naive_bayes_classifier, open(
            self.saving_location + 'model.pkl', 'wb'))

        print("model trained")


if __name__ == "__main__":
    intents_json_file = "nlp/intent_classification/intents.json"
    trainmodel = TrainModel(intents_json_file=intents_json_file)
    trainmodel.train()

    model = NaiveByasModel()
    while True:
        p = input("command : ")
        intent = model.find_intent(command=p)

        print(intent)
