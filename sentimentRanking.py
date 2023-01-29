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
        """
        self.__queryResult = queryResult
        self.__tokenInput = tokenInput

        self.__tokenProductTitle = []
        self.__tokenReviewTitle = []
        self.__tokenReviewContent = []

        self.__REVIEW_CONTENT_BOOST = reviewContentBoost    # Boost applied to the reviewContent matches
        self.__REVIEW_TITLE_BOOST = reviewTitleBoost        # Boost applied to the reviewTitle matches
        self.__PRODUCT_TITLE_BOOST = productTitleBoost      # Boost applied to the productTitle matches

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
        self.__freq = None

        self.__listResult = []

        print(self.__tokenInput)

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

    @property
    def boost(self):
        """Returns a dictionary containing the boost used for the ranking"""
        return({"REVIEW_CONTENT_BOOST": self.__REVIEW_CONTENT_BOOST,
                "REVIEW_TITLE_BOOST": self.__REVIEW_TITLE_BOOST,
                "PRODUCT_TITLE_BOOST": self.__PRODUCT_TITLE_BOOST})

    def __freqNorm(self, tokenList):
        """Norm 2 of the weight of each term contained in the tokenList"""
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

            if self.__tokenInput:  # Checks if the processed query contains something to avoid ranking documents with an empty query
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

                # Checking the norm of the document weights to avoid dividing by 0
                if self.__freqNormReviewContent != 0:
                    sim1 = self.__REVIEW_CONTENT_BOOST * (self.__freqReviewContent / (self.__freqNormReviewContent * self.__freqNormTokenInput))
                else:
                    sim1 = 0
                if self.__freqNormReviewTitle != 0:
                    sim2 = self.__REVIEW_TITLE_BOOST * (self.__freqReviewTitle / (self.__freqNormReviewTitle * self.__freqNormTokenInput))
                else:
                    sim2 = 0
                if self.__freqNormProductTitle != 0:
                    sim3 = self.__PRODUCT_TITLE_BOOST * (self.__freqProductTitle / (self.__freqNormProductTitle * self.__freqNormTokenInput))
                else:
                    sim3 = 0

                if self.__sentiment:
                    self.__sentimentValue = float(result[self.__sentimentType])
                    similarity = (sim1 + sim2 + sim3 + self.__sentimentValue) / (
                                self.__REVIEW_CONTENT_BOOST + self.__REVIEW_TITLE_BOOST + self.__PRODUCT_TITLE_BOOST + 1)
                else:
                    similarity = (sim1 + sim2 + sim3) / (
                                self.__REVIEW_CONTENT_BOOST + self.__REVIEW_TITLE_BOOST + self.__PRODUCT_TITLE_BOOST)

                self.__listResult.append((result, similarity))

            self.__listResult = sorted(self.__listResult, key=lambda x: x[1], reverse=True)
        return self.__listResult
