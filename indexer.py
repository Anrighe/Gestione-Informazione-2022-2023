import whoosh.index
from whoosh.index import *
from whoosh.fields import *
import os
import csv
import localRoberta
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += " " + ele
    # return string
    return str1


def stringProcesser(string, wnl):
    tokenizedString = nltk.word_tokenize(string)
    porter = PorterStemmer()
    processedContent = []
    for t in tokenizedString:
        if not t in stopwords.words('english') and not t in processedContent:
            processedContent.append(porter.stem(wnl.lemmatize(t)))

    return listToString(processedContent)


schema = Schema(originalProductTitle=TEXT(stored=True),     # titolo originale del prodotto
                postProductTitle=TEXT(stored=False),         # titolo del prodotto dopo preprocessing
                reviewTitle=TEXT(stored=True),
                originalReviewContent=TEXT(stored=True),    # contenuto originale della recensione
                postReviewContent=TEXT(stored=False),        # contenuto della recensione dopo preprocessing
                positive=NUMERIC(float, 32, stored=True),
                neutral=NUMERIC(float, 32, stored=True),
                negative=NUMERIC(float, 32, stored=True))

if not os.path.exists("indexdir"):  # creates the directory indexdir if it does not exist
    os.mkdir("indexdir")
    ix = create_in("indexdir", schema)  # create_in() removes the index that has been created. In order to update use update_in() (NON SEMBRA ESISTERE??)
else:
    ix = whoosh.index.open_dir("indexdir")

writer = ix.writer()

with open("AmazonReviews.csv", encoding="utf8") as csv_file:

    counter = 0
    wnl = nltk.WordNetLemmatizer()

    csv_reader = csv.reader(csv_file, delimiter=",")
    next(csv_reader)  # skips the first row

    for i in range(ix.doc_count()):
        next(csv_reader)  # skips rows

    for row in csv_reader:
        productTitle = row[1]   # Product Title
        reviewTitle = row[17]   # Review Title
        reviewContent = row[16]   # Review Content

        processedContentString = stringProcesser(reviewContent, wnl)
        processedProductTitleString = stringProcesser(reviewTitle, wnl)

        try:
            results = localRoberta.localRoberta(reviewContent)
            #print(results) # debug
            print(ix.doc_count()+counter, "/", 41420)  # debug
            positiveScore = results["positive"]
            neutralScore = results["neutral"]
            negativeScore = results["negative"]

            print("preprocessed:", processedContentString)  # debug
            print("reviewContent:", reviewContent)  # debug

            writer.add_document(originalProductTitle=productTitle,
                                postProductTitle=processedProductTitleString,
                                reviewTitle=reviewTitle,
                                originalReviewContent=reviewContent,
                                postReviewContent=processedContentString,
                                positive=positiveScore,
                                neutral=neutralScore,
                                negative=negativeScore)
        except RuntimeError:
            print("Runtime error: reviewContent is too long for the sentiment analysis model")
        except KeyboardInterrupt:
            print("Keyboard Interrupt detected")
            writer.commit()
            exit(-1)

        counter = counter + 1

writer.commit()
