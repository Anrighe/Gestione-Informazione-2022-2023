import nltk
from nltk.tokenize import word_tokenize
from stringProcesser import stringProcesser


class InputCleaner:
    def __init__(self, input, sentiment, sentimentType=""):
        self.__rawUserInput = input  ## e.g: Apple Watched 8
        self.__wnl = nltk.WordNetLemmatizer()
        self.__processedUserInput = stringProcesser(self.__rawUserInput, self.__wnl, True)  ## e.g.: apple watch 8

        self.__tokenInput = nltk.word_tokenize(self.__processedUserInput)  # contains tokenized postprocessed input words

        self.processedUserInput = self.processedUserInput.replace(' ', ' OR ')

        self.__queryList = [f'postProductTitle:{self.processedUserInput}',
                            f'postReviewTitle:{self.processedUserInput}',
                            f'postReviewContent:{self.processedUserInput}']

        if sentiment:
            self.__queryList.append(f'{sentimentType}:[0.33 TO 1.0]')

    @property
    def processedUserInput(self):
        return self.__processedUserInput

    @processedUserInput.setter
    def processedUserInput(self, value):
        self.__processedUserInput = value

    @property
    def query(self):
        return self.__queryList

    @property
    def tokenInput(self):
        return self.__tokenInput










