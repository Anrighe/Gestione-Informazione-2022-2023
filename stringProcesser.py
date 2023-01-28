import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def stringProcesser(string, wnl, removeDuplicates=False):
    """Applies Tokenization, removal of stopwords Lemmatization and Stemming to a string
    :param string: Generic String
    :param wnl: Lemmatizer
    :param removeDuplicates: If True checks and removes duplicate words
        When False  -> Indexing
        When True   -> User Query

    Doctest example:
    >>> import nltk
    >>> stringProcesser("Apple Apple Watched 10!?..", nltk.WordNetLemmatizer(), True)
    'appl watch 10'
    """
    if isinstance(string, str):
        # removes all the punctuation from the string expect for the char "-" and "*"
        noPunctuation = string.translate(str.maketrans('', '', '''!"#$%&\'()+,./:;<=>?@[\\]^_`{|}~'''))
        noPunctuation = noPunctuation.replace(" - ", " ")  # Only replaces the occurrences of " - " with a whitespace

        token = nltk.word_tokenize(noPunctuation)
        porter = PorterStemmer()
        processedContent = []
        for t in token:
            if removeDuplicates and (t not in stopwords.words('english') and porter.stem(wnl.lemmatize(t)) not in processedContent):
                processedContent.append(porter.stem(wnl.lemmatize(t)))
            elif removeDuplicates is False and t not in stopwords.words('english'):
                processedContent.append(porter.stem(wnl.lemmatize(t)))
    else:
        raise TypeError

    return " ".join(processedContent)
