from whoosh.index import create_in, open_dir
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

if not os.path.exists("indexdir"):  # se non esiste la cartella indexdir la crea
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)  # Cancella l'indice che è stato creato, non aggiorna || update_in() per aggiornare
writer = ix.writer()

with open("AmazonReviews.csv", encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    firstLine = True

    maxEntries = 30 #stops importing from csv after the specified amount of entries
    counter = 0

    for row in csv_reader:
        if not firstLine:

            productTitle = row[1]   # Product Title
            reviewTitle = row[17]   # Review Title
            reviewContent = row[16]   # Review Content

            try:
                results = localRoberta.localRoberta(reviewContent)
                print(results)  # debug
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
                print("Runtime error: reviewContent is too long for the sentiment analysis model", e)

            counter = counter + 1
            if counter > maxEntries:
                break
        else:
            firstLine = False

writer.commit()