from whoosh.index import create_in
from whoosh.fields import *
import os
import csv
import localRoberta

schema = Schema(productTitle=TEXT(stored=True),
                reviewTitle=TEXT(stored=True),
                reviewContent=TEXT(stored=True),
                positive=NUMERIC(float, 32, stored=True),
                neutral=NUMERIC(float, 32, stored=True),
                negative=NUMERIC(float, 32, stored=True))

if not os.path.exists("indexdir"):  # creates the directory indexdir if it does not exist
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)  # create_in() removes the index that has been created. In order to update use update_in()
writer = ix.writer()

with open("AmazonReviews.csv", encoding="utf8") as csv_file:

    maxEntries = 10  # stops importing from csv after the specified amount of entries
    counter = 0

    csv_reader = csv.reader(csv_file, delimiter=",")
    next(csv_reader) # skips the first row

    for row in csv_reader:
        productTitle = row[1]   # Product Title
        reviewTitle = row[17]   # Review Title
        reviewContent = row[16]   # Review Content
        print(reviewContent)
        try:
            results = localRoberta.localRoberta(reviewContent)
            #print(results)  # debug
            print(counter+1, "/", maxEntries)  # debug
            positiveScore = results["positive"]
            neutralScore = results["neutral"]
            negativeScore = results["negative"]
            writer.add_document(productTitle=productTitle,
                                reviewTitle=reviewTitle,
                                reviewContent=reviewContent,
                                positive=positiveScore,
                                neutral=neutralScore,
                                negative=negativeScore)
        except RuntimeError as e:
            print("Runtime error: reviewContent is too long for the sentiment analysis model. ", e)

        counter = counter + 1
        if counter >= maxEntries:
            break

writer.commit()
