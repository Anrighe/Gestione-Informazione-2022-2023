  ____   _____     _     ____   __  __  _____
 |  _ \ | ____|   / \   |  _ \ |  \/  || ____|
 | |_) ||  _|    / _ \  | | | || |\/| ||  _|
 |  _ < | |___  / ___ \ | |_| || |  | || |___
 |_| \_\|_____|/_/   \_\|____/ |_|  |_||_____|

Progetto di Gestione dell'Informazione - 2022/2023

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1) Progetto: Amazon Review Search Engine
    Applicazione per l'indicizzazione di recensioni
    di prodotti Amazon e ricerca da interfaccia
    grafica.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2) Partecipanti:
Cognome     Nome        Matricola
----------- ----------- ---------
Marras      Enrico      152336
Colli       Lorenzo     153063
Lazzarini   Mattia      152833

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3) Contenuto Archivio:
.
├── AmazonReviews.csv: Dataset su cui lavora il search engine
├── Docs
│   ├── AmazonReviews.DCG: Calcoli inerenti ai valori di DCG per ogni query
│   ├── AmazonReviews.QUE: Lista delle query eseguite per i benchmark
│   ├── AmazonReviews.REL: Lista per ogni query dei documenti risultanti
│   ├── AmazonReviews.STP: Lista delle stopwords utilizzate
│   ├── README.txt
│   ├── SchemaLogicoProgetto.png: Breve schema grafico riguardante la struttura del progetto
│   ├── progGestI-22-23.pdf: Consegna del progetto
│   └── rankingFunction.png: Versione ad 'alto livello' della funzione di ranking usata
├── indexer.py
├── indexerStarter.py
├── inputCleaner.py
├── main.py
├── searcher.py
├── sentimentIndex
├── sentimentRanking.py
├── stringProcesser.py
└── userInterface.py

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4) Dipendenze:
Package                      Versione utilizzata
---------------------------- -------------------
huggingface-hub              0.11.0
matplotlib                   3.6.2
matplotlib-inline            0.1.6
nltk                         3.7
numpy                        1.23.4
pandas                       1.5.1
packaging                    >= 20.9
pip                          22.3.1
pyspellchecker               0.7.1
RangeSlider                  2021.7.4
scipy                        1.9.3
torch                        1.13.0
transformers                 4.24.0
Whoosh                       2.7.4

Il progetto è stato sviluppato su Python 3.10.7

Testato su:
- Windows 10 21H2
- Windows 11 21H2
- Ubuntu 20.04.5 LTS
- MacOS 13.2

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

5) Procedura d'installazione (con pip3 e da terminale linux):
    pip3 install torch
    pip3 install whoosh
    pip3 install nltk
    pip3 install --upgrade packaging
    pip3 install transformers
    pip3 install pyspellchecker
    pip3 install RangeSlider

    python3
    >>> nltk.download('punkt')
    >>> nltk.download('stopwords')
    >>> nltk.download('wordnet')

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

6) Uso dell'applicazione:
    6.a) Indicizzazione:
        Windows: py indexerStarter.py [dataset_file] [index_directory]
        Unix: python3 indexerStarter.py [dataset_file] [index_directory]

    6.b) Esecuzione GUI per ricerca:
        Windows: py main.py
        Unix: python3 main.py
        
All'interno dell'archivio sono presenti due script Python principali:

   indexerStarter.py -> avvia l'Indicizzazione (6.a) creando una cartella,
      se non già presente, di nome [index_directory]. È già presente una 
      directory "sentimentIndex" che contiene tutti i documenti del .csv 
      indicizzati.

  main.py -> (6.b) una volta eseguito, si renderà necessario specificare
      il percorso assoluto della cartella contenente l'indice nell'apposito
      menú "File". Di default verrà selezionata la cartella "sentimentIndex".
      Se la directory contenente l'indice è situata all'interno del progetto, 
      non sará necessario specificare l'intero percorso, ma solo il nome.
