from whoosh.searching import Results
import time
from indexer import Indexer
from searcher import SentimentSearcherRanker
from inputCleaner import InputCleaner
from tkinter import *
from tkinter.ttk import *
import tkinter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from RangeSlider.RangeSlider import RangeSliderH, RangeSliderV


def timeDecorator(func):
    def inner(self):
        start = time.perf_counter()
        func(self)
        end = time.perf_counter()
        self.resultInfo.config(text=f'{len(self.searchResult)} results\n({round(end-start, 4)} seconds)')
    return inner


class UserInterface:
    def __init__(self):
        self.__indexDir = 'sentimentIndex'
        self.__datasetName = 'AmazonReviews.csv'
        self.__searched = False
        self.__sentiment = False
        self.__sentimentType = ''
        self.index = Indexer(self.__datasetName, self.__indexDir)
        self.userInput = ''
        self.__window = Tk()
        self.__window.title(
            '''Progetto Gestione dell'Informazione 2022-2023  -  Search Engine per Recensioni di Prodotti Amazon  -  Enrico Marras (152336), Lorenzo Colli (153063), Mattia Lazzarini (152833)''')

        self.__window.geometry(
            self.__geometryCentered(1366, 800, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))

        #self.__window.configure(background='gray')  #changes the background of the main window to gray

        self.__menuBar = Menu(self.__window)

        # Adding File Menu
        self.__file = Menu(self.__menuBar, tearoff=0)
        self.__menuBar.add_cascade(label='File', menu=self.__file)
        self.__file.add_command(label='Select Index...', command=self.__popUpIndexWindow)
        self.__file.add_separator()
        self.__file.add_command(label='Exit', command=self.__terminate)

        # Adding Docs Menu
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
        self.__searchButton = tkinter.Button(self.__simpleSearchFrame, text='Search', height=1, width=6, command=self.userQuery, font=('System', 18, 'bold'), fg='dark blue')
        self.__searchField.pack(side=LEFT)
        self.__searchButton.pack(side=RIGHT)

        self.__sentimentSearchFrame = Frame(self.__searchFrame)

        self.__positiveRadioButton = Radiobutton(self.__sentimentSearchFrame, text='Positive', value='1', command=self.__setPositiveSentimentType)
        self.__neutralRadioButton = Radiobutton(self.__sentimentSearchFrame, text='Neutral', value='2', command=self.__setNeutralSentimentType)
        self.__negativeRadioButton = Radiobutton(self.__sentimentSearchFrame, text='Negative', value='3', command=self.__setNegativeSentimentType)
        self.__noSentimentRadioButton = Radiobutton(self.__sentimentSearchFrame, text='No Sentiment', value='4', command=self.__setNoSentimentType)

        # Horizontal range slider
        self.__leftHandle = DoubleVar()  # left handle variable
        self.__rightHandle = DoubleVar()  # right handle variable
        self.__slider = RangeSliderH(self.__sentimentSearchFrame,
                                     [self.__leftHandle, self.__rightHandle],
                                     Width=200, Height=65, padX=11,
                                     min_val=0, max_val=1, show_value=True) # es: bgColor='#660000' per cambiare colore


        self.__style = Style()
        self.__style.configure('changeFgPositive.TRadiobutton', foreground='green', font=('System', 18, 'bold'))
        self.__positiveRadioButton['style'] = 'changeFgPositive.TRadiobutton'
        self.__style.configure('changeFgNeutral.TRadiobutton', foreground='orange', font=('System', 18, 'bold'))
        self.__neutralRadioButton['style'] = 'changeFgNeutral.TRadiobutton'
        self.__style.configure('changeFgNegative.TRadiobutton', foreground='red', font=('System', 18, 'bold'))
        self.__negativeRadioButton['style'] = 'changeFgNegative.TRadiobutton'
        self.__style.configure('changeFgNoSent.TRadiobutton', font=('System', 18, 'bold'))
        self.__noSentimentRadioButton['style'] = 'changeFgNoSent.TRadiobutton'

        self.__title = tkinter.Label(self.__searchFrame, text='Amazon Review Search Engine', fg='#2CDFD4', font=('System', 48, 'bold'))

        self.__positiveRadioButton.pack(side=LEFT, padx=20)
        self.__neutralRadioButton.pack(side=LEFT, padx=20)
        self.__negativeRadioButton.pack(side=LEFT, padx=20)
        self.__noSentimentRadioButton.pack(side=LEFT, padx=20)

        self.__slider.pack(side=LEFT, padx=30)  # or grid or place method could be used

        self.__title.pack(side=TOP)
        self.__simpleSearchFrame.pack(side=TOP, pady=30)
        self.__sentimentSearchFrame.pack(side=TOP)

        self.__searchFrame.pack()

        self.__resultFrame = Frame(self.__fullFrame)

        self.__resultFrameList = Frame(self.__resultFrame)

        # The <<ListboxSelect>> event was designed to fire whenever the selection changes, no matter how it changes.
        # That could mean when the user selects something new in the listbox, or when the selection is removed from the listbox.
        # By setting exportselection to False, the selection won't change just because another widget gets some or all of its data selected
        self.__resultList = Listbox(self.__resultFrameList, height=30, width=35, exportselection=False)
        self.__resultList.bind('<<ListboxSelect>>', self.__onListSelect)
        self.__scrollbarList = Scrollbar(self.__resultFrameList)  # Creating a Scrollbar and attaching it the result frame
        self.__resultList.config(yscrollcommand=self.__scrollbarList.set)
        self.__scrollbarList.config(command=self.__resultList.yview)


        self.__resultFrameDisplayer = Frame(self.__resultFrame)
        self.__resultDisplayer = Text(self.__resultFrameDisplayer, height=30, width=65, wrap=WORD)
        self.__resultDisplayer.tag_config('reviewTitle', foreground='blue', font=('System', 30, 'bold', 'underline'))
        self.__resultDisplayer.tag_config('productTitle', foreground='dark blue', font=('System', 25, 'bold'))
        self.__resultDisplayer.tag_config('reviewContent', font=('System', 20))

        self.__scrollbarDisplayer = Scrollbar(self.__resultFrameDisplayer)
        self.__resultDisplayer.config(yscrollcommand=self.__scrollbarDisplayer.set)
        self.__scrollbarDisplayer.config(command=self.__resultDisplayer.yview)

        self.__resultList.pack(side=LEFT, fill=BOTH, expand=True, pady=20)
        self.__scrollbarList.pack(side=LEFT, fill=BOTH, expand=True, pady=20)  # Adding Scrollbar to the right of the result list
        self.__resultFrameList.pack(side=LEFT)

        self.__resultDisplayer.pack(side=LEFT)
        self.__scrollbarDisplayer.pack(side=RIGHT, fill=BOTH, expand=True)
        self.__resultFrameDisplayer.pack(side=LEFT)
        self.__resultFrame.pack()


        self.__statsFrame = Frame(self.__resultFrame)

        self.__figure = plt.Figure(figsize=(2.5, 2.5), dpi=100)
        self.__ax = self.__figure.add_subplot(111)
        self.__bar = FigureCanvasTkAgg(self.__figure, self.__statsFrame)
        self.__bar.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.__ax.clear()
        self.__setGraph(0.0, 0.0, 0.0, True)

        self.__resultInfo = Label(self.__statsFrame, text='\n', font=('System', 18))
        self.__resultInfo.pack(side=BOTTOM, pady=83)

        self.__statsFrame.pack(side=LEFT)
        self.__fullFrame.pack()
        self.__window.mainloop()

    @property
    def resultInfo(self):
        return self.__resultInfo

    @property
    def searchResult(self):
        return self.__searchResult

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
            self.__indexDir = 'sentimentIndex'
        self.__topIndex.destroy()

    def __setGraph(self, positive, neutral, negative, legendState):
        self.__dataFrame = pd.DataFrame({'Positive': [positive], 'Neutral': [neutral], 'Negative': [negative]})
        self.__ax.clear()
        self.__dataFrame.plot(kind='bar', legend=legendState, ax=self.__ax, color=['green', 'orange', 'red'])
        self.__bar.draw()

    def __onListSelect(self, event):
        if self.__searched:
            if self.__searchResult:
                indexList = int(event.widget.curselection()[0])
                #value = event.widget.get(indexList) #debug

                self.__resultDisplayer.config(state=NORMAL)
                self.__resultDisplayer.delete('1.0', END)
                self.__resultDisplayer.insert(1.0, self.__searchResult[indexList][0]['originalReviewContent'], 'reviewContent')
                self.__resultDisplayer.insert(1.0, '\n\n')
                self.__resultDisplayer.insert(1.0, self.__searchResult[indexList][0]['originalProductTitle'], 'productTitle')
                self.__resultDisplayer.insert(1.0, '\n\n')
                self.__resultDisplayer.insert(1.0, self.__searchResult[indexList][0]['originalReviewTitle'], 'reviewTitle')
                self.__resultDisplayer.config(state=DISABLED)

                self.__setGraph(self.__searchResult[indexList][0]['positive'],
                                self.__searchResult[indexList][0]['neutral'],
                                self.__searchResult[indexList][0]['negative'], False)

                #print(f'You selected item {indexList}: '{value}'')  # debug

    def __popUpIndexWindow(self):
        self.__topIndex = Toplevel(self.__window)  # Creates a Toplevel window
        self.__topIndex.title('Select Index')
        self.__topIndex.geometry(self.__geometryCentered(350, 125, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))

        self.__entryFrameIndex = Frame(self.__topIndex)
        self.__labelIndexTop = Label(self.__entryFrameIndex, text='Please insert the name of the directory containing the Index')
        self.__labelIndexBot = Label(self.__entryFrameIndex, text='\n*The directory needs to be in the same folder of the source files')
        self.__entryIndex = Entry(self.__entryFrameIndex, width=25, font='16')  # Creates an Entry Widget in the Toplevel window

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

    def __popUpMissingQuery(self):
        self.__topMissingQuery = Toplevel(self.__window)  # Creates a Toplevel window
        self.__topMissingQuery.title('Missing query!')
        self.__topMissingQuery.geometry(self.__geometryCentered(250, 100, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))

        self.__labelMissingQuery = Label(self.__topMissingQuery, text='Please insert a query before searching')
        self.__okMissingQuery = Button(self.__topMissingQuery, text='    Ok    ', command=lambda: self.__topMissingQuery.destroy())

        self.__okMissingQuery.pack(side=BOTTOM, pady=15)
        self.__labelMissingQuery.pack(side=BOTTOM, pady=0)


    def startIndexing(self):  # funzione di debug per far partire l'indicizzazione
        self.index.indexGenerator()

    def userQuery(self):
        self.userInput = self.__searchField.get()
        print(f'QUERY:{self.userInput}')
        print(f'SENTIMENT:({self.__sentiment}, {self.__sentimentType})')

        if self.userInput != '':
            self.cleaner = InputCleaner(self.userInput, sentiment=self.__sentiment, slider=self.__slider.getValues(), sentimentType=self.__sentimentType)
            self.queryList = self.cleaner.query
            self.searcher = SentimentSearcherRanker('sentimentIndex', self.cleaner.tokenInput, self.queryList, sentiment=self.__sentiment, sentimentType=self.__sentimentType)

            self.__searchAndRank()
            self.__searched = True

            self.__resultList.delete(0, END)

            for result in self.__searchResult:  # adding results to the GUI list
                self.__resultList.insert(END, result[0]['originalReviewTitle'])
                print(result)
        else:
            self.__popUpMissingQuery()

    def __geometryCentered(self, windowWidth, windowHeight, screenWidth, screenHeight):
        return '{}x{}+{}+{}'.format(windowWidth,
                                    windowHeight,
                                    int((screenWidth / 2) - (windowWidth / 2)),
                                    int((screenHeight / 2) - (windowHeight / 2)))

    @timeDecorator
    def __searchAndRank(self):
        self.searcher.search()
        self.__searchResult = self.searcher.ranking()

