from whoosh import qparser, index
from whoosh.qparser import QueryParser
from sentimentRanking import SentimentRanking
from abc import ABC, abstractmethod


class BaseSearcher(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def search(self):
        pass


class SentimentSearcher(BaseSearcher):

    def __init__(self, indexDir, tokenInput, queryList, sentiment, sentimentType):
        self._indexDir = indexDir
        self._ix = index.open_dir(indexDir)
        self._searcher = self._ix.searcher()
        self._parser = QueryParser(sentimentType, self._ix.schema)
        self._queryList = queryList
        self._sentiment = sentiment
        self._tokenInput = tokenInput
        self._sentimentType = sentimentType

    def search(self):

        self._finalResult = self._searcher.search(self._parser.parse(self._queryList[0]), limit=None)
        self._finalResult.extend(self._searcher.search(self._parser.parse(self._queryList[1]), limit=None))
        self._finalResult.extend(self._searcher.search(self._parser.parse(self._queryList[2]), limit=None))

        if self._sentiment:
            self._resultSentiment = self._searcher.search(self._parser.parse(self._queryList[3]))

            if self._resultSentiment.is_empty():  # the function filter doesn't actually filter if resultSentiment is empty
                self._finalResult = self._resultSentiment
            else:
                self._finalResult.filter(self._resultSentiment)  # intersection

        for i in self._finalResult: #debug
            print(i)

        #print(self._tokenInput) #debug


class SentimentSearcherRanker(SentimentSearcher):

    def __init__(self, indexDir, tokenInput, queryList, sentiment, sentimentType):
        super().__init__(indexDir, tokenInput, queryList, sentiment, sentimentType)

    def search(self):
        super().search()

    def ranking(self):
        ranker = SentimentRanking(self._finalResult, self._tokenInput, self._sentiment, self._sentimentType)
        resultList = ranker.calculateRank()
        return resultList























