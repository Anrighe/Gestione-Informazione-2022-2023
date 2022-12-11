from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.query import NumericRange
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

def stringProcesser(string):
    wnl = nltk.WordNetLemmatizer()
    tokenizedString = nltk.word_tokenize(string)
    porter = PorterStemmer()
    processedContent = []
    for t in tokenizedString:
        if not t in stopwords.words('english') and not t in processedContent:
            processedContent.append(porter.stem(wnl.lemmatize(t)))

    return listToString(processedContent)

#TODO: capire cosa fa questa funzione
def myscore_fn(searcher, fieldname, text, matcher):
    """
    My weighting function
    """
    # currently just taking frequency count
    freq = matcher.value_as("frequency")
    print("freq: ", freq)

    # What I want to do is to return
    #        freq + myscore
    # where myscore is the field as define in the Schema below.
    return freq


ix = open_dir("indexdir")
pos_weighting = scoring.FunctionWeighting(myscore_fn)
searcher = ix.searcher(weighting=pos_weighting)

#searcher = ix.searcher(weighting=scoring.BM25F) #Con weighting=scoring. si inseriscono altre funzioni di ranking custom
#print(list(searcher.lexicon("content"))) #stampa il vocabolario delle parole che va a indicizzare
parser = QueryParser("postReviewContent", schema=ix.schema)

queryInput = "postReviewContent:" + stringProcesser("children").replace(" ", "") #non sono comunque riuscito ad aggiungere la u di utf8 prima della query

#query = parser.parse(u"postReviewContent:child") # Per query testuali
query = parser.parse(queryInput)
results = searcher.search(query)


#query1 = NumericRange(u"negative", start=0.001, end=0.08)  # Per query numeriche
#results = searcher.search(query1, sortedby="negative", limit=None, reverse=True)

#query2 = NumericRange(u"negative", start=0.2, end=0.3)  # Per query numeriche
#results2 = searcher.search(query2, sortedby="negative", limit=None, reverse=True)

#allResults = results2
#allResults.extend(results)

counter = 0

if len(results) == 0:
    print("No results")
else:
    #counter = 0

    for j in results:
        print(j)
    #    counter += 1
    #print("RESULTS:", counter)

    #counter = 0

    #for y in results2:
    #    print(y)
    #    counter += 1
    #print("RESULTS2:", counter)

    #counter = 0

    #for x in allResults:
        #print(x)
        #counter += 1
    #print("ALLRESULTS:", counter)
