import sys
from indexer import Indexer

# Script Arguments:
# The first argument is the dataset file (.csv)
# The second argument is the folder in which the Indexing will take place
if __name__ == "__main__":
    indexer = Indexer(sys.argv[1], sys.argv[2])
    indexer.indexGenerator()
