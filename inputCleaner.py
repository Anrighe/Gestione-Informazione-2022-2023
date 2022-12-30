import nltk
from nltk.tokenize import word_tokenize
from stringProcesser import stringProcesser


class InputCleaner:
    """Processes the user input converting it into a valid format for Whoosh's query language"""
    def __init__(self, userInput, sentiment, slider, sentimentType=''):
        """
        :param userInput: Input of the user of the search bar
        :param sentiment: True if the user wants to filter by sentiment
        :param slider: Contains the slider values for dynamic sentiment filtering
        :param sentimentType: # Contains the sentiment type the user is looking for (e.g.: 'positive')
        """
        self.__rawUserInput = userInput  # e.g: 'Apple Watched 8'
        self.__wnl = nltk.WordNetLemmatizer()
        self.__processedUserInput = stringProcesser(self.__rawUserInput, self.__wnl, True)  # e.g.: 'apple watch 8'

        self.__tokenInput = word_tokenize(self.__processedUserInput)  # Contains tokenized processed input words

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
        """queryList contains the formatted queries that needs to be executed on the Searcher"""
        return self.__queryList

    @property
    def tokenInput(self):
        return self.__tokenInput
