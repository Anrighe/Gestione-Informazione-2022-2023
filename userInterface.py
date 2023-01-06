import os
import time
import tkinter
import pandas as pd
from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
from inputCleaner import InputCleaner
from searcher import SentimentSearcherRanker
from RangeSlider.RangeSlider import RangeSliderH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def timeDecorator(func):
    """Decorates a function and measures its execution time

    :param func: function that needs to be measured
    """
    def inner(self):
        start = time.perf_counter()
        func(self)
        end = time.perf_counter()
        self.resultInfo.config(text=f'{len(self.searchResult)} results\n({round(end-start, 4)} seconds)')
    return inner


class UserInterface:
    """Class that implements the GUI and acts as a **mediator**, by coordinating all other objects.

    (e.g.: When a interaction of a GUI object happens, the mediator notifies every other object that
    needs to know that event happened)
    """
    def __init__(self):
        """Class that implements the GUI and acts as a **mediator**, by coordinating all other objects.

        (e.g.: When a interaction of a GUI object happens, the mediator notifies every other object that
        needs to know that event happened)
        """

        self.__supportedOS = ['nt', 'posix']
        try:
            assert os.name in self.__supportedOS
            if os.name == 'nt':
                self.__fileSystemSeparator = WindowsFileSystemSeparator()
            elif os.name == 'posix':
                self.__fileSystemSeparator = PosixFileSystemSeparator()
        except AssertionError:
            self.__fileSystemSeparator = NotSupportedOS()

        self.__indexDir = 'sentimentIndex'  # setting the standard Index folder name
        self.__searched = False  # False if a search has never been done
        self.__sentiment = False  # False if the user isn't looking to filter by sentiment
        self.__sentimentType = ''  # Contains the sentiment type the user is looking for (e.g.: 'positive')
        self.userInput = ''

        self.__window = Tk()  # Creating Tkinter window
        self.__window.title(
            '''Progetto Gestione dell'Informazione 2022-2023  -  Search Engine per Recensioni di Prodotti Amazon  -  Enrico Marras (152336), Lorenzo Colli (153063), Mattia Lazzarini (152833)''')
        self.__window.geometry(
            self.__geometryCentered(1366, 800, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))

        self.__menuBar = Menu(self.__window)  # Creating the Menu Bar
        self.__window.config(menu=self.__menuBar)  # Displays the Menu in the window

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
        self.__docs.add_command(label='Logic Diagram', command=self.__openLogicDiagram)
        self.__docs.add_command(label='Benchmark', command=self.__openBenchmark)

        self.__fullFrame = Frame(self.__window)  # fullFrame contains: searchFrame, resultFrame
        self.__searchFrame = Frame(self.__fullFrame)  # searchFrame contains: simpleSearchFrame, sentimentSearchFrame

        # Search Bar and 'Search' Button
        self.__simpleSearchFrame = Frame(self.__searchFrame)  # simpleSearchFrame contains: searchField, searchButton
        self.__searchField = Entry(self.__simpleSearchFrame, width=35, font=('Microsoft Yi Baiti', 36))
        self.__searchButton = tkinter.Button(self.__simpleSearchFrame, text='Search', height=1, width=6, command=self.userQuery, font=('System', 18, 'bold'), fg='dark blue')
        self.__searchField.pack(side=LEFT)
        self.__searchButton.pack(side=RIGHT)

        # sentimentSearchFrame contains: sentiment multi-selection radio buttons, slider
        self.__sentimentSearchFrame = Frame(self.__searchFrame)

        # Sentiment Radio Buttons
        self.__positiveRadioButton = Radiobutton(self.__sentimentSearchFrame, text='Positive', value='1', command=self.__setPositiveSentimentType)
        self.__neutralRadioButton = Radiobutton(self.__sentimentSearchFrame, text='Neutral', value='2', command=self.__setNeutralSentimentType)
        self.__negativeRadioButton = Radiobutton(self.__sentimentSearchFrame, text='Negative', value='3', command=self.__setNegativeSentimentType)
        self.__noSentimentRadioButton = Radiobutton(self.__sentimentSearchFrame, text='No Sentiment', value='4', command=self.__setNoSentimentType)

        self.__style = Style()
        self.__style.configure('changeFgPositive.TRadiobutton', foreground='green', font=('System', 18, 'bold'))
        self.__positiveRadioButton['style'] = 'changeFgPositive.TRadiobutton'
        self.__style.configure('changeFgNeutral.TRadiobutton', foreground='orange', font=('System', 18, 'bold'))
        self.__neutralRadioButton['style'] = 'changeFgNeutral.TRadiobutton'
        self.__style.configure('changeFgNegative.TRadiobutton', foreground='red', font=('System', 18, 'bold'))
        self.__negativeRadioButton['style'] = 'changeFgNegative.TRadiobutton'
        self.__style.configure('changeFgNoSent.TRadiobutton', font=('System', 18, 'bold'))
        self.__noSentimentRadioButton['style'] = 'changeFgNoSent.TRadiobutton'

        # Horizontal range slider
        self.__leftHandle = DoubleVar()  # Left handle variable
        self.__rightHandle = DoubleVar()  # Right handle variable
        self.__slider = RangeSliderH(self.__sentimentSearchFrame,
                                     [self.__leftHandle, self.__rightHandle],
                                     Width=200, Height=65, padX=11,
                                     min_val=0, max_val=1, show_value=True, bgColor='white')

        # Title over the Search Bar
        self.__title = tkinter.Label(self.__searchFrame, text='Amazon Review Search Engine', fg='#6899c7', font=('System', 48, 'bold'))

        self.__positiveRadioButton.pack(side=LEFT, padx=20)
        self.__neutralRadioButton.pack(side=LEFT, padx=20)
        self.__negativeRadioButton.pack(side=LEFT, padx=20)
        self.__noSentimentRadioButton.pack(side=LEFT, padx=20)
        self.__slider.pack(side=LEFT, padx=30)
        self.__title.pack(side=TOP)

        self.__simpleSearchFrame.pack(side=TOP, pady=30)
        self.__sentimentSearchFrame.pack(side=TOP)
        self.__searchFrame.pack()

        self.__resultFrame = Frame(self.__fullFrame)  # resultFrame contains: resultFrameList, resultFrameDisplayer, statsFrame
        self.__resultFrameList = Frame(self.__resultFrame)  # resultFrameList contains: resultList and scrollbarList

        # The <<ListboxSelect>> event was designed to fire whenever the selection changes, no matter how it changes.
        # That could mean when the user selects something new in the listbox, or when the selection is removed from the listbox.
        # By setting 'exportselection' to False, the selection won't change just because another widget gets some or all of its data selected
        self.__resultList = Listbox(self.__resultFrameList, height=30, width=35, exportselection=False)
        self.__resultList.bind('<<ListboxSelect>>', self.__onListSelect)  # Binding the onListSelect to the even sequence <<ListboxSelect>>
        self.__scrollbarList = Scrollbar(self.__resultFrameList)  # Creating a Scrollbar and attaching it the result frame
        self.__resultList.config(yscrollcommand=self.__scrollbarList.set)
        self.__scrollbarList.config(command=self.__resultList.yview)

        # Adding the text displayer for the selected document
        self.__resultFrameDisplayer = Frame(self.__resultFrame)  # resultFrameDisplayer contains: resultDisplayer, scrollbarDisplayer
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

        # Adding the sentiment histogram for the selected document
        self.__statsFrame = Frame(self.__resultFrame)  # statsFrame contains: figure, resultInfo
        self.__figure = plt.Figure(figsize=(2.5, 2.5), dpi=100)
        self.__ax = self.__figure.add_subplot(111)
        self.__bar = FigureCanvasTkAgg(self.__figure, self.__statsFrame)
        self.__bar.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.__ax.clear()
        self.__setGraph(0.0, 0.0, 0.0, True)

        # Adding the search stats (# results, (time))
        self.__resultInfo = Label(self.__statsFrame, text='\n', font=('System', 18))
        self.__resultInfo.pack(side=BOTTOM, pady=83)

        self.__statsFrame.pack(side=LEFT)
        self.__fullFrame.pack(fill=BOTH, expand=True)

        self.__window.mainloop()

    @property
    def resultInfo(self):
        return self.__resultInfo

    @property
    def searchResult(self):
        return self.__searchResult

    @staticmethod
    def __terminate():
        exit(0)

    def __openProject(self):
        """Opens the progGestI-22-23.pdf file containing the project assignment"""
        os.startfile(f'Docs{self.__fileSystemSeparator.getSeparator()}progGestI-22-23.pdf')  # Duck Typing

    def __openReadme(self):
        """Opens the README.txt file"""
        os.startfile(f'Docs{self.__fileSystemSeparator.getSeparator()}README.txt')  # Duck Typing

    def __openLogicDiagram(self):
        """Opens the SchemaLogicoProgetto.png which contains the logic diagram representing the behaviour of this program"""
        os.startfile(f'Docs{self.__fileSystemSeparator.getSeparator()}SchemaLogicoProgetto.png')

    def __openBenchmark(self):
        """Opens the BENCHMARK.txt file"""
        os.startfile(f'Docs{self.__fileSystemSeparator.getSeparator()}BENCHMARK.txt')  # Duck Typing

    def __setPositiveSentimentType(self):
        """Triggered when the 'Positive' Radio Button is pressed"""
        self.__sentiment = True
        self.__sentimentType = 'positive'

    def __setNeutralSentimentType(self):
        """Triggered when the 'Neutral' Radio Button is pressed"""
        self.__sentiment = True
        self.__sentimentType = 'neutral'

    def __setNegativeSentimentType(self):
        """Triggered when the 'Negative' Radio Button is pressed"""
        self.__sentiment = True
        self.__sentimentType = 'negative'

    def __setNoSentimentType(self):
        """Triggered when the 'No Sentiment' Radio Button is pressed"""
        self.__sentiment = False
        self.__sentimentType = ''

    def __getEntryIndexData(self):
        """
        Sets indexDir to the input of the entry entryIndex, unless it's an empty string, which
        resets it to the original index name 'sentimentIndex'.

        If the directory does not exist shows a popup error, otherwise it destroys the topIndex window.
        """
        self.__indexDir = self.__entryIndex.get()
        if self.__indexDir == '':
            self.__indexDir = 'sentimentIndex'

        try:
            assert os.path.exists(self.__indexDir)
            self.__topIndex.destroy()
        except AssertionError:
            self.__popUpMissingIndex()

    def __setGraph(self, positive, neutral, negative, legendState):
        """
        Plots the Histogram with the sentiment of the selected document's values
        :param positive: Value of positivity of the selected document
        :param neutral: Value of neutrality of the selected document
        :param negative: Value of negativity of the selected document
        :param legendState: True if the legend will be displayed in the histogram
        """
        self.__dataFrame = pd.DataFrame({'Positive': [positive], 'Neutral': [neutral], 'Negative': [negative]})
        self.__ax.clear()
        self.__dataFrame.plot(kind='bar', legend=legendState, ax=self.__ax, color=['green', 'orange', 'red'])
        self.__bar.draw()

    def __onListSelect(self, event):
        """
        If at least one search has been successfully executed and the searchResult list isn't empty:
        it inserts the information of the document in the resultDisplayer, and it plots the required graph
        :param event: Selection of an element in the list
        """
        if self.__searched:
            if self.__searchResult:
                indexList = int(event.widget.curselection()[0])

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

    def __popUpIndexWindow(self):
        """Creates the popup for the 'SelectIndex' menu option"""
        self.__topIndex = Toplevel(self.__window)  # Creates a Toplevel window
        self.__topIndex.title('Select Index')
        self.__topIndex.geometry(self.__geometryCentered(350, 125, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))
        self.__topIndex.resizable(False, False)

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
        """Creates the error popup in case the query inserted by the user is an empty string"""
        self.__topMissingQuery = Toplevel(self.__window)  # Creates a Toplevel window
        self.__topMissingQuery.title('Missing query!')
        self.__topMissingQuery.geometry(self.__geometryCentered(250, 100, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))
        self.__topMissingQuery.resizable(False, False)

        self.__labelMissingQuery = Label(self.__topMissingQuery, text='Please insert a query before searching')
        self.__okMissingQuery = Button(self.__topMissingQuery, text='    Ok    ', command=lambda: self.__topMissingQuery.destroy())

        self.__okMissingQuery.pack(side=BOTTOM, pady=15)
        self.__labelMissingQuery.pack(side=BOTTOM, pady=0)

    def __popUpMissingIndex(self):
        """Creates the error popup in case the directory containing the index specified by the user is missing"""
        self.__topMissingIndex = Toplevel(self.__window)  # Creates a Toplevel window
        self.__topMissingIndex.title('Missing Index!')
        self.__topMissingIndex.geometry(self.__geometryCentered(250, 100, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()))
        self.__topMissingIndex.resizable(False, False)

        self.__labelMissingQuery = Label(self.__topMissingIndex, text='Please insert an existing directory')
        self.__okMissingQuery = Button(self.__topMissingIndex, text='    Ok    ', command=lambda: self.__topMissingIndex.destroy())

        self.__okMissingQuery.pack(side=BOTTOM, pady=15)
        self.__labelMissingQuery.pack(side=BOTTOM, pady=0)

    def userQuery(self):
        """
        Gets the user input in the searchField and if it isn't an empty string converts it into a valid query,
        searches the Index, orders the results with the ranking function and populates the resultList.
        If the query is missing shows a popup error
        """
        self.userInput = self.__searchField.get()

        if self.userInput != '':
            self.cleaner = InputCleaner(self.userInput, sentiment=self.__sentiment, slider=self.__slider.getValues(), sentimentType=self.__sentimentType)
            self.queryList = self.cleaner.query
            self.searcher = SentimentSearcherRanker(self.__indexDir, self.cleaner.tokenInput,
                                                    self.queryList, sentiment=self.__sentiment,
                                                    sentimentType=self.__sentimentType)

            self.__searchAndRank()  # Decorated by timeDecorator
            self.__searched = True
            self.__resultList.delete(0, END)  # Clears the result list

            for result in self.__searchResult:  # Adding results to the GUI list
                self.__resultList.insert(END, result[0]['originalReviewTitle'])
        else:
            self.__popUpMissingQuery()

    @staticmethod
    def __geometryCentered(windowWidth, windowHeight, screenWidth, screenHeight):
        """Sets the window position at the centre of the screen"""
        return '{}x{}+{}+{}'.format(windowWidth,
                                    windowHeight,
                                    int((screenWidth / 2) - (windowWidth / 2)),
                                    int((screenHeight / 2) - (windowHeight / 2)))

    @timeDecorator
    def __searchAndRank(self):
        """
        Calls the searcher that executes the search on the index and the ranking function
        which orders the result based on their score
        """
        self.searcher.search()
        self.__searchResult = self.searcher.ranking()


class WindowsFileSystemSeparator:
    """Class used for Duck Typing in the OS check"""
    @staticmethod
    def getSeparator():
        """:return: The file system separator for Windows-based system"""
        return '\\\\'


class PosixFileSystemSeparator:
    """Class used for Duck Typing in the OS check"""
    @staticmethod
    def getSeparator():
        """:return: The file system separator for Posix-based system"""
        return '/'


class NotSupportedOS:
    """Class used for Duck Typing in the OS check"""
    @staticmethod
    def getSeparator():
        """:return: OSError Exception meaning the current OS is not supported"""
        raise OSError
