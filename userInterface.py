from indexer import Indexer
from searcher import Searcher
from inputCleaner import InputCleaner
from tkinter import *
from tkinter.ttk import *
import tkinter


class UserInterface:

    def __init__(self):
        self.__indexDir = 'sentimentIndex'
        self.__datasetName = 'AmazonReviews.csv'
        self.__sentiment = False
        self.__sentimentType = ''
        self.index = Indexer(self.__datasetName, self.__indexDir)
        self.userInput = ''
        self.__window = Tk()
        self.__window.title(
            '''Progetto Gestione dell'Informazione 2022-2023  -  Search Engine per Recensioni di Prodotti Amazon  -  Enrico Marras (152336), Lorenzo Colli (153063), Mattia Lazzarini (152833)''')

        self.__window.geometry(
            self.__geometryCentered(1366, 768, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))


        self.__menuBar = Menu(self.__window)

        # Adding File Menu and commands
        self.__file = Menu(self.__menuBar, tearoff=0)
        self.__menuBar.add_cascade(label='File', menu=self.__file)
        self.__file.add_command(label='Select Index...', command=self.__popUpIndexWindow)
        self.__file.add_command(label='Select Dataset...', command=self.__popUpDatasetWindow)
        self.__file.add_separator()
        self.__file.add_command(label='Exit', command=self.__terminate)

        # Adding Docs Menu and commands
        self.__docs = Menu(self.__menuBar, tearoff=0)
        self.__menuBar.add_cascade(label='Docs', menu=self.__docs)
        self.__docs.add_command(label='Project', command=self.__openProject)
        self.__docs.add_separator()
        self.__docs.add_command(label='README', command=self.__openReadme)
        self.__docs.add_command(label='Benchmark', command=self.__openBenchmark)

        self.__window.config(menu=self.__menuBar)  # displays the Menu

        self.__fullFrame = Frame(self.__window)
        self.__searchFrame = Frame(self.__fullFrame)

        self.__simpleSearchFrame = Frame(self.__searchFrame)
        self.__searchField = Entry(self.__simpleSearchFrame, width=35, font=('Microsoft Yi Baiti', 36))
        self.__searchButton = tkinter.Button(self.__simpleSearchFrame, text='Search', height=3, width=10, command=self.userQuery)
        self.__searchField.pack(side=LEFT)
        self.__searchButton.pack(side=RIGHT)


        self.__sentimentSearchFrame = Frame(self.__searchFrame)

        self.__positiveRadioButton = Radiobutton(self.__sentimentSearchFrame, text="Positive", value="1", command=self.__setPositiveSentimentType)
        self.__neutralRadioButton = Radiobutton(self.__sentimentSearchFrame, text="Neutral", value="2", command=self.__setNeutralSentimentType)
        self.__negativeRadioButton = Radiobutton(self.__sentimentSearchFrame, text="Negative", value="3", command=self.__setNegativeSentimentType)
        self.__noSentimentRadioButton = Radiobutton(self.__sentimentSearchFrame, text="No Sentiment", value="4", command=self.__setNoSentimentType)

        self.__positiveRadioButton.pack(side=LEFT, padx=5)
        self.__neutralRadioButton.pack(side=LEFT, padx=5)
        self.__negativeRadioButton.pack(side=LEFT, padx=5)
        self.__noSentimentRadioButton.pack(side=LEFT, padx=5)


        self.__simpleSearchFrame.pack(pady=30)
        self.__sentimentSearchFrame.pack()

        self.__searchFrame.pack()
        self.__fullFrame.pack()

        self.__window.mainloop()



    def __terminate(self):
        exit(0)

    def __openProject(self):
        import os
        os.startfile('Docs\\progGestI-22-23.pdf')

    def __openReadme(self):
        import os
        os.startfile('Docs\\README.txt')

    def __openBenchmark(self):
        import os
        os.startfile('Docs\\BENCHMARK.txt')

    def __setPositiveSentimentType(self):
        self.__sentiment = True
        self.__sentimentType = 'positive'

    def __setNeutralSentimentType(self):
        self.__sentiment = True
        self.__sentimentType = 'neutral'

    def __setNegativeSentimentType(self):
        self.__sentiment = True
        self.__sentimentType = 'negative'

    def __setNoSentimentType(self):
        self.__sentiment = False
        self.__sentimentType = ''


    def __getEntryIndexData(self):
        self.__indexDir = self.__entryIndex.get()
        if self.__indexDir == '':
            self.__datasetName = 'sentimentIndex'
        self.__topIndex.destroy()

    def __popUpIndexWindow(self):
        self.__topIndex = Toplevel(self.__window)  # Create a Toplevel window
        self.__topIndex.title('Select Index')
        self.__topIndex.geometry(self.__geometryCentered(350, 125, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))

        self.__entryFrameIndex = Frame(self.__topIndex)
        self.__labelIndexTop = Label(self.__entryFrameIndex, text='Please insert the name of the directory containing the Index')
        self.__labelIndexBot = Label(self.__entryFrameIndex, text='\n*The directory needs to be in the same folder of the source files')
        self.__entryIndex = Entry(self.__entryFrameIndex, width=25, font='16') # Create an Entry Widget in the Toplevel window

        self.__labelIndexBot.pack(side=BOTTOM)
        self.__entryIndex.pack(side=BOTTOM)
        self.__labelIndexTop.pack(side=BOTTOM)
        self.__entryIndex.pack(pady=5)
        self.__entryFrameIndex.pack(side=TOP)

        self.__buttonFrameIndex = Frame(self.__topIndex)  # Creates a Frame for the buttons
        self.__okIndex = Button(self.__buttonFrameIndex, text='    Ok    ', command=self.__getEntryIndexData)
        self.__okIndex.pack(side=LEFT, padx=10, pady=5)
        self.__cancelIndex = Button(self.__buttonFrameIndex, text='Cancel', command=lambda: self.__topIndex.destroy())
        self.__cancelIndex.pack(side=RIGHT, padx=10, pady=5)
        self.__buttonFrameIndex.pack(side=BOTTOM)


    def __getEntryDatasetData(self):
        self.__datasetName = self.__entryDataset.get()
        if self.__datasetName == '':
            self.__datasetName = 'AmazonReviews.csv'
        self.__topDataset.destroy()
    def __popUpDatasetWindow(self):
        self.__topDataset = Toplevel(self.__window)  # Create a Toplevel window
        self.__topDataset.title('Select Dataset')
        self.__topDataset.geometry(self.__geometryCentered(350, 125, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))

        self.__entryFrameDataset = Frame(self.__topDataset)
        self.__labelDatasetTop = Label(self.__entryFrameDataset, text='Please insert the name of the dataset file (.csv)')
        self.__labelDatasetBot = Label(self.__entryFrameDataset, text='\n*The dataset needs to be in the same folder of the source files')
        self.__entryDataset = Entry(self.__entryFrameDataset, width=25, font='16') # Create an Entry Widget in the Toplevel window

        self.__labelDatasetBot.pack(side=BOTTOM)
        self.__entryDataset.pack(side=BOTTOM)
        self.__labelDatasetTop.pack(side=BOTTOM)
        self.__entryDataset.pack(pady=5)
        self.__entryFrameDataset.pack(side=TOP)

        self.__buttonFrameDataset = Frame(self.__topDataset)  # Creates a Frame for the buttons
        self.__okDataset = Button(self.__buttonFrameDataset, text='    Ok    ', command=self.__getEntryDatasetData)
        self.__okDataset.pack(side=LEFT, padx=10, pady=5)
        self.__cancelDataset = Button(self.__buttonFrameDataset, text='Cancel', command=lambda: self.__topDataset.destroy())
        self.__cancelDataset.pack(side=RIGHT, padx=10, pady=5)
        self.__buttonFrameDataset.pack(side=BOTTOM)



    def startIndexing(self):  # funzione di debug per far partire l'indicizzazione
        self.index.indexGenerator()

    def userQuery(self):
        self.userInput = self.__searchField.get()
        print(f'QUERY:{self.userInput}')
        print(f'SENTIMENT:({self.__sentiment}, {self.__sentimentType})')

        self.cleaner = InputCleaner(self.userInput, sentiment=self.__sentiment, sentimentType=self.__sentimentType)
        self.queryList = self.cleaner.query
        self.searcher = Searcher('sentimentIndex', self.cleaner.tokenInput, self.queryList, sentiment=self.__sentiment, sentimentType=self.__sentimentType)
        self.searcher.search()
        resultList = self.searcher.ranking()

        for result in resultList:
            print(result)


    def __geometryCentered(self, windowWidth, windowHeight, screenWidth, screenHeight):
        return '{}x{}+{}+{}'.format(windowWidth,
                                    windowHeight,
                                    int((screenWidth / 2) - (windowWidth / 2)),
                                    int((screenHeight / 2) - (windowHeight / 2)))





