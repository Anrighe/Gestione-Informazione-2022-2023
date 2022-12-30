import os
import csv
import nltk
import whoosh
import numpy as np
import urllib.request
from scipy.special import softmax
from transformers import AutoTokenizer
from stringProcesser import stringProcesser
from whoosh.index import open_dir, create_in
from whoosh.fields import TEXT, NUMERIC, Schema
from transformers import AutoModelForSequenceClassification


class Indexer:
    __schema = Schema(originalProductTitle=TEXT(stored=True),       # original title of the product
                      postProductTitle=TEXT(stored=True),           # title of the product after processing
                      originalReviewTitle=TEXT(stored=True),        # original title of the review
                      postReviewTitle=TEXT(stored=True),            # title of the review after processing
                      originalReviewContent=TEXT(stored=True),      # original content of the review
                      postReviewContent=TEXT(stored=True),          # content of the review after processing
                      positive=NUMERIC(float, stored=True),     # value of positivity of the originalReviewContent
                      neutral=NUMERIC(float, stored=True),      # value of neutrality of the originalReviewContent
                      negative=NUMERIC(float, stored=True))     # value of negativity of the originalReviewContent

    def __init__(self, fileName, indexName):
        if not os.path.exists(indexName):  # creates the 'indexName' directory if it does not exist
            os.mkdir(indexName)
            self.__ix = create_in(indexName, Indexer.__schema)  # creates or overwrites the index in the specified directory
        else:
            self.__ix = whoosh.index.open_dir(indexName)

        # TODO: Aggiungere property per __ix

        self.__writer = self.__ix.writer()
        self.__counter = 0  # counts how many documents have been indexed in the current session
        self.__fileName = fileName

    @staticmethod  # TODO: DA TESTARE
    def __sentimentAnalyzer(text):

        if not isinstance(text, str):
            raise TypeError

        task = 'sentiment'
        MODEL = f'cardiffnlp/twitter-roberta-base-{task}'
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        mapping_link = f'https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt'  # downloads the label mapping

        with urllib.request.urlopen(mapping_link) as f:
            html = f.read().decode('utf-8').split('\n')
            csvreader = csv.reader(html, delimiter='\t')

        labels = [row[1] for row in csvreader if len(row) > 1]  ##TODO: da togliere dalla versione non OOP
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        ranking = np.argsort(scores)
        ranking = ranking[::-1]

        return {labels[ranking[0]]: scores[ranking[0]], labels[ranking[1]]: scores[ranking[1]], labels[ranking[2]]: scores[ranking[2]]}

    def indexGenerator(self):
        with open(self.__fileName, encoding='utf8') as csvFile:

            self.__counter = 0
            wnl = nltk.WordNetLemmatizer()

            csvReader = csv.reader(csvFile, delimiter=',')
            next(csvReader)  # skips the first row, which only contains information about the columns

            for i in range(self.__ix.doc_count()):
                next(csvReader)  # skips rows so that the indexing starts from where it left off

            for row in csvReader:
                productTitle = row[1]  # Original Product Title
                reviewTitle = row[17]  # Original Review Title
                reviewContent = row[16]  # Original Review Content

                processedProductTitle = stringProcesser(productTitle, wnl)
                processedReviewTitle = stringProcesser(reviewTitle, wnl)
                processedReviewContent = stringProcesser(reviewContent, wnl)

                try:
                    sentiment = Indexer.__sentimentAnalyzer(reviewContent)
                    print(sentiment) # debug
                    print(f"{self.__ix.doc_count()+self.__counter} / 41420")  # debug
                    positiveScore = sentiment['positive']
                    neutralScore = sentiment['neutral']
                    negativeScore = sentiment['negative']

                    print('preprocessed:', processedReviewContent)  # debug
                    print('reviewContent:', reviewContent)  # debug

                    self.__writer.add_document(originalProductTitle=productTitle,
                                               postProductTitle=processedProductTitle,
                                               originalReviewTitle=reviewTitle,
                                               postReviewTitle=processedReviewTitle,
                                               originalReviewContent=reviewContent,
                                               postReviewContent=processedReviewContent,
                                               positive=positiveScore,
                                               neutral=neutralScore,
                                               negative=negativeScore)
                except RuntimeError:
                    print('Runtime error: reviewContent is too long for the sentiment analysis model')
                except KeyboardInterrupt:
                    print('Keyboard Interrupt detected')
                    self.__writer.commit()
                    exit(-1)

                self.__counter += 1

        self.__writer.commit()


