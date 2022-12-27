from indexer import Indexer
from inputCleaner import InputCleaner
from searcher import Searcher


class UserInterface:

    def __init__(self):
        self.index = Indexer('AmazonReviews.csv', 'sentimentIndex')
        self.userInput = ""

    def startIndexing(self):  # funzione di debug per far partire l'indicizzazione
        self.index.indexGenerator()

    def userQuery(self):
        sentiment = True
        sentimentType = 'positive'

        self.userInput = input('Please insert a user query:')
        self.cleaner = InputCleaner(self.userInput, sentiment=sentiment, sentimentType=sentimentType)
        self.queryList = self.cleaner.query
        self.searcher = Searcher('sentimentIndex', self.cleaner.tokenInput, self.queryList, sentiment=sentiment, sentimentType=sentimentType)
        self.searcher.search()
        resultList = self.searcher.ranking()

        for result in resultList:
            print(result)








