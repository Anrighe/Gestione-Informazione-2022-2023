from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os
import csv


schema = Schema(gameTitle=TEXT(stored=True),
                content=TEXT(stored=True))

if not os.path.exists("indexdir"):  # se non esiste la cartella indexdir la crea
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)  # Cancella l'indice che è stato creato, non aggiorna|| update_in() per aggiornare
writer = ix.writer()

with open("datasetSteam.csv", encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    firstLine = True

    maxEntries = 1000 #stops importing from csv after the specified amount of entries
    counter = 0

    for row in csv_reader:
        if not firstLine:

            #row[0]  appid
            #row[1]  gameTitle
            #row[2]  content
            writer.add_document(gameTitle=row[1], content=row[2])
            counter = counter + 1
            if counter > maxEntries:
                break
        else:
            firstLine = False

writer.commit()



