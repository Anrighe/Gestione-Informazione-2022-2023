from math import sqrt
from nltk.tokenize import word_tokenize


class SentimentRanking:
    """Class that implements the sentiment ranking function"""
    def __init__(self, queryResult, tokenInput, sentiment, sentimentType, reviewContentBoost=1, reviewTitleBoost=1.5, productTitleBoost=2.5):
        """
        :param queryResult: Contains the result of the queries
        :param tokenInput: Tokenized user query
        :param sentiment: True if the user wants to filter by sentiment
        :param sentimentType: Contains the sentiment type the user is looking for (e.g.: 'positive')
        :param reviewContentBoost: Boost applied to the reviewContent matches
        :param reviewTitleBoost: Boost applied to the reviewTitle matches
        :param productTitleBoost: Boost applied to the productTitle matches
        """
        self.__queryResult = queryResult
        self.__tokenInput = tokenInput

        self.__tokenProductTitle = []
        self.__tokenReviewTitle = []
        self.__tokenReviewContent = []

        self.__reviewContentBoost = reviewContentBoost
        self.__reviewTitleBoost = reviewTitleBoost
        self.__productTitleBoost = productTitleBoost

        self.__freqProductTitle = 0
        self.__freqReviewTitle = 0
        self.__freqReviewContent = 0

        self.__freqNormProductTitle = 0
        self.__freqNormReviewTitle = 0
        self.__freqNormReviewContent = 0
        self.__freqNormTokenInput = 0

        self.__sentiment = sentiment
        self.__sentimentType = sentimentType
        self.__sentimentValue = 0

        self.__listResult = []

    @property
    def __freq(self):
        return (self.__freqProductTitle,
                self.__freqReviewTitle,
                self.__freqReviewContent,
                self.__freqNormProductTitle,
                self.__freqNormReviewTitle,
                self.__freqNormReviewContent,
                self.__freqNormTokenInput)

    @__freq.setter
    def __freq(self, value):
        self.__freqProductTitle = value
        self.__freqReviewTitle = value
        self.__freqReviewContent = value
        self.__freqNormProductTitle = value
        self.__freqNormReviewTitle = value
        self.__freqNormReviewContent = value
        self.__freqNormTokenInput = value

    def __freqNorm(self, tokenList):
        result = 0
        tokenSet = list(dict.fromkeys(tokenList))

        for token in tokenSet:
            result += tokenList.count(token) ** 2

        return sqrt(result)

    def calculateRank(self):
        """Implements the Sentiment Ranking function and calculates the rank of each document
        :return: The list of ordered documents
        """
        for result in self.__queryResult:  # Fixes a result (e.g.: negativity 0.9)
            self.__freq = 0

            self.__tokenProductTitle = word_tokenize(result["postProductTitle"])
            self.__tokenReviewTitle = word_tokenize(result["postReviewTitle"])
            self.__tokenReviewContent = word_tokenize(result["postReviewContent"])

            for word in self.__tokenInput:  # Fixes a word (e.g.: "fire")

                self.__freqProductTitle += self.__tokenProductTitle.count(word) * self.__tokenInput.count(word)
                self.__freqReviewTitle += self.__tokenReviewTitle.count(word) * self.__tokenInput.count(word)
                self.__freqReviewContent += self.__tokenReviewContent.count(word) * self.__tokenInput.count(word)

            self.__freqNormProductTitle = self.__freqNorm(self.__tokenProductTitle)
            self.__freqNormReviewTitle = self.__freqNorm(self.__tokenReviewTitle)
            self.__freqNormReviewContent = self.__freqNorm(self.__tokenReviewContent)
            self.__freqNormTokenInput = self.__freqNorm(self.__tokenInput)

            sim1 = self.__reviewContentBoost * (self.__freqReviewContent / (self.__freqNormReviewContent * self.__freqNormTokenInput))
            sim2 = self.__reviewTitleBoost * (self.__freqReviewTitle / (self.__freqNormReviewTitle * self.__freqNormTokenInput))
            sim3 = self.__productTitleBoost * (self.__freqProductTitle / (self.__freqNormProductTitle * self.__freqNormTokenInput))

            if self.__sentiment:
                self.__sentimentValue = float(result[self.__sentimentType])
                similarity = (sim1 + sim2 + sim3 + self.__sentimentValue) / (
                            self.__reviewContentBoost + self.__reviewTitleBoost + self.__productTitleBoost + 1)
            else:
                similarity = (sim1 + sim2 + sim3) / (
                            self.__reviewContentBoost + self.__reviewTitleBoost + self.__productTitleBoost)

            self.__listResult.append((result, similarity))

        self.__listResult = sorted(self.__listResult, key=lambda x: x[1], reverse=True)
        return self.__listResult
