from whoosh import qparser, index
from whoosh.qparser import QueryParser
from sentimentRanking import SentimentRanking


class Searcher:

    def __init__(self, indexDir, tokenInput, queryList, sentiment, sentimentType):
        self.__indexDir = indexDir
        self.__ix = index.open_dir(indexDir)
        self.__searcher = self.__ix.searcher()
        self.__parser = QueryParser(sentimentType, self.__ix.schema)
        self.__queryList = queryList
        self.__sentiment = sentiment
        self.__tokenInput = tokenInput
        self.__sentimentType = sentimentType

    def search(self):

        self.__finalResult = self.__searcher.search(self.__parser.parse(self.__queryList[0]), limit=None)
        self.__finalResult.extend(self.__searcher.search(self.__parser.parse(self.__queryList[1]), limit=None))
        self.__finalResult.extend(self.__searcher.search(self.__parser.parse(self.__queryList[2]), limit=None))

        if self.__sentiment:

            #TODO: EFFETTUARE CONTROLLI PRIMA DI CANCELLARE I COMMENTI SOTTOSTANTI
            #self.__ix = index.open_dir(self.__indexDir)
            #self.__parser = qparser.QueryParser(self.__sentimentType, self.__ix.schema)
            #self.__sentimentQuery = self.__parser.parse(self.__queryList[3])
            #self.__searcher = self.__ix.searcher()

            #self.__resultSentiment = self.__searcher.search(self.__sentimentQuery)


            self.__resultSentiment = self.__searcher.search(self.__parser.parse(self.__queryList[3]))

            if self.__resultSentiment.is_empty():  # the function filter doesn't actually filter if resultSentiment is empty
                self.__finalResult = self.__resultSentiment
            else:
                self.__finalResult.filter(self.__resultSentiment)  # intersection

        #for i in self.__finalResult: #debug
            #print(i)

        #print(self.__tokenInput) #debug

    def ranking(self):
        ranker = SentimentRanking(self.__finalResult, self.__tokenInput, self.__sentiment, self.__sentimentType)
        resultList = ranker.calculateRank()
        return resultList























