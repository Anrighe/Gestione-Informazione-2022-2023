import nltk
from nltk.tokenize import word_tokenize
from stringProcesser import stringProcesser


class InputCleaner:
    def __init__(self, input, sentiment, slider, sentimentType=''):
        self.__rawUserInput = input  ## e.g: Apple Watched 8
        self.__wnl = nltk.WordNetLemmatizer()
        self.__processedUserInput = stringProcesser(self.__rawUserInput, self.__wnl, True)  # e.g.: apple watch 8

        self.__tokenInput = word_tokenize(self.__processedUserInput)  # contains tokenized processed input words

        self.__processedProductTitle = self.__processedUserInput.replace(' ', ' OR postProductTitle:')
        self.__processedReviewTitle = self.__processedUserInput.replace(' ', ' OR postProductTitle:')
        self.__processedReviewContent = self.__processedUserInput.replace(' ', ' OR postProductTitle:')

        self.__queryList = [f'postProductTitle:{self.__processedProductTitle}',
                            f'postReviewTitle:{self.__processedReviewTitle}',
                            f'postReviewContent:{self.__processedReviewContent}']

        if sentiment:
            self.__queryList.append(f'{sentimentType}:[{round(slider[0],2)} TO {round(slider[1],2)}]')

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










