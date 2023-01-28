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
    """Class used for indexing the supplied dataset"""
    __schema = Schema(originalProductTitle=TEXT(stored=True),   # original title of the product
                      postProductTitle=TEXT(stored=True),       # title of the product after processing
                      originalReviewTitle=TEXT(stored=True),    # original title of the review
                      postReviewTitle=TEXT(stored=True),        # title of the review after processing
                      originalReviewContent=TEXT(stored=True),  # original content of the review
                      postReviewContent=TEXT(stored=True),      # content of the review after processing
                      positive=NUMERIC(float, stored=True),     # value of positivity of the originalReviewContent
                      neutral=NUMERIC(float, stored=True),      # value of neutrality of the originalReviewContent
                      negative=NUMERIC(float, stored=True))     # value of negativity of the originalReviewContent

    def __init__(self, fileName, indexName):
        """
        :param fileName: dataset file (.csv)
        :param indexName: directory in which the Indexing will take place
        """
        self.__csvReader = None
        self.__sentiment = None
        self.__negativeScore = None
        self.__positiveScore = None
        self.__neutralScore = None
        if not os.path.exists(indexName):
            os.mkdir(indexName)  # creates a new 'indexName' directory if it does not exist
            self.__ix = create_in(indexName, Indexer.__schema)  # creates or overwrites the index in the specified directory
        else:
            self.__ix = whoosh.index.open_dir(indexName)  # opens the existing index

        self.__writer = self.__ix.writer()
        self.__counter = 0  # Counts how many documents have been indexed in the current session
        self.__fileName = fileName
        self.__wnl = nltk.WordNetLemmatizer()
        self.__productTitle = ''
        self.__reviewTitle = ''
        self.__reviewContent = ''
        self.__processedProductTitle = ''
        self.__processedReviewTitle = ''
        self.__processedReviewContent = ''

    @staticmethod
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

        labels = [row[1] for row in csvreader if len(row) > 1]
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        ranking = np.argsort(scores)
        ranking = ranking[::-1]

        return {labels[ranking[0]]: scores[ranking[0]], labels[ranking[1]]: scores[ranking[1]], labels[ranking[2]]: scores[ranking[2]]}

    def indexGenerator(self):
        """Opens the supplied dataset, process the content and inserts it into the index"""
        with open(self.__fileName, encoding='utf8') as csvFile:
            self.__counter = 0
            self.__csvReader = csv.reader(csvFile, delimiter=',')
            next(self.__csvReader)  # Skips the first row, which only contains information about the columns

            for i in range(self.__ix.doc_count()):
                next(self.__csvReader)  # Skips rows so that the indexing starts from where it left off

            for row in self.__csvReader:
                self.__productTitle = row[1]  # Original Product Title
                self.__reviewTitle = row[17]  # Original Review Title
                self.__reviewContent = row[16]  # Original Review Content

                self.__processedProductTitle = stringProcesser(self.__productTitle, self.__wnl)
                self.__processedReviewTitle = stringProcesser(self.__reviewTitle, self.__wnl)
                self.__processedReviewContent = stringProcesser(self.__reviewContent, self.__wnl)

                try:
                    self.__sentiment = Indexer.__sentimentAnalyzer(self.__reviewContent)
                    print(f'{self.__ix.doc_count()+self.__counter}')  # Prints the current amount of indexed documents
                    self.__positiveScore = self.__sentiment['positive']
                    self.__neutralScore = self.__sentiment['neutral']
                    self.__negativeScore = self.__sentiment['negative']

                    self.__writer.add_document(originalProductTitle=self.__productTitle,
                                               postProductTitle=self.__processedProductTitle,
                                               originalReviewTitle=self.__reviewTitle,
                                               postReviewTitle=self.__processedReviewTitle,
                                               originalReviewContent=self.__reviewContent,
                                               postReviewContent=self.__processedReviewContent,
                                               positive=self.__positiveScore,
                                               neutral=self.__neutralScore,
                                               negative=self.__negativeScore)
                except RuntimeError:
                    print('Runtime error: The review content of the current document is too long for the sentiment analysis model')
                except KeyboardInterrupt:
                    print('Keyboard Interrupt detected\nCommitting changes, please wait.')
                    self.__writer.commit()
                    print('Changes committed, exiting...')
                    exit(-1)

                self.__counter += 1

        print('Committing changes, please wait.')
        self.__writer.commit()
        print('Changes committed, exiting...')
