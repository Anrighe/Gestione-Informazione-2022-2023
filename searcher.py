from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path
from whoosh import scoring
from whoosh.query import NumericRange

# es query "document" nel field title ma non "interesting" nel content

ix = open_dir("indexdir")

searcher = ix.searcher(weighting=scoring.BM25F) #Con weighting=scoring. si inseriscono altre funzioni di ranking custom
#print(list(searcher.lexicon("content"))) #stampa il vocabolario delle parole che va a indicizzare
parser = QueryParser("reviewContent", schema=ix.schema)
#query = parser.parse(u"reviewContent:love") # Per query testuali
query = NumericRange(u"negative", start=0.001, end=None) # Per query numeriche
results = searcher.search(query, limit=None)
if len(results) == 0:
    print("Empty result!!")
else:
    for x in results:
        print(x)