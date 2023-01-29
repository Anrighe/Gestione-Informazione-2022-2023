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

3) Dipendenze:
Package                      Versione utilizzata
---------------------------- -------------------
huggingface-hub              0.11.0
matplotlib                   3.6.2
matplotlib-inline            0.1.6
nltk                         3.7
numpy                        1.23.4
pandas                       1.5.1
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

4) Procedura d'installazione (con pip e da terminale linux):
    pip install torch
    pip install nltk
    pip install --upgrade packaging #(>= 20.9)
    pip install transformers
    pip install pyspellchecker
    pip install RangeSlider

    python3
    >>> nltk.download('punkt')
    >>> nltk.download('stopwords')
    >>> nltk.download('wordnet')

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

5) Uso dell'applicazione:
    5.a) Indicizzazione:
        Windows: py indexerStarter.py [dataset_file] [index_directory]
        Unix: python3 indexerStarter.py [dataset_file] [index_directory]

    5.b) Esecuzione GUI per ricerca:
        Windows: py main.py
        Unix: python3 main.py