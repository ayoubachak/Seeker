# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QTabWidget

# creating main window class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # creating a QWebEngineView
        self.browser = QWebEngineView()

        # setting dev tools
        dev_tools_page = QWebEnginePage(self.browser)
        self.browser.page().setDevToolsPage(dev_tools_page)

        # setting default browser url as google
        self.browser.setUrl(QUrl("http://duckduckgo.com"))

        # adding action when url get changed
        self.browser.urlChanged.connect(self.update_urlbar)

        # adding action when loading is finished
        self.browser.loadFinished.connect(self.update_title)

        # Attempt for the tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        # add the QWebEngineView to a new tab
        index = self.tabs.addTab(self.browser, "New Tab")
        # set the new tab as the current tab
        self.tabs.setCurrentIndex(index)

        # creating a status bar object
        self.status = QStatusBar()

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")

        # adding this tool bar tot he main window
        self.addToolBar(navtb)

        # adding actions to the tool bar
        # creating a action for back
        back_btn = QAction("Back", self)

        # setting status tip
        back_btn.setStatusTip("Back to previous page")

        # adding action to the back button
        # making browser go back
        back_btn.triggered.connect(self.browser.back)

        # adding this action to tool bar
        navtb.addAction(back_btn)

        # similarly for forward action
        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")

        # adding action to the next button
        # making browser go forward
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # similarly for reload action
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")

        # adding action to the reload button
        # making browser to reload
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # similarly for home action
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.setStatusTip("Open a new tab")
        new_tab_btn.triggered.connect(self.new_tab)
        navtb.addAction(new_tab_btn)

        close_tab_btn = QAction("Close Tab", self)
        close_tab_btn.setStatusTip("Close the current tab")
        close_tab_btn.triggered.connect(lambda: self.closeTab(self.tabs.currentIndex()))
        navtb.addAction(close_tab_btn)

        # adding a separator in the tool bar
        navtb.addSeparator()

        # creating a line edit for the url
        self.urlbar = QLineEdit()

        # adding action when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # adding this to the tool bar
        navtb.addWidget(self.urlbar)

        # adding stop action to the tool bar
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")

        # adding action to the stop button
        # making browser to stop
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # showing all the components
        self.show()


    # method for updating the title of the window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Achak Browser" % title)


    # method called by the home action
    def navigate_home(self):

        # open the google
        self.browser.setUrl(QUrl("http://www.google.com"))

    # method called by the line edit when return key is pressed
    def navigate_to_url(self):

        # getting url and converting it to QUrl object
        q = QUrl(self.urlbar.text())

        # if url is scheme is blank
        if q.scheme() == "":
            # set url scheme to html
            q.setScheme("http")

        # set the url to the browser
        self.browser.setUrl(q)

    # method for updating url
    # this method is called by the QWebEngineView object
    def update_urlbar(self, q):

        # setting text to the url bar
        self.urlbar.setText(q.toString())

        # setting cursor position of the url bar
        self.urlbar.setCursorPosition(0)

    def new_tab(self):
        # creating a QWebEngineView
        browser = QWebEngineView()

        # setting dev tools
        dev_tools_page = QWebEnginePage(browser)
        browser.page().setDevToolsPage(dev_tools_page)

        # setting default browser url as duckduckgo
        browser.setUrl(QUrl("http://duckduckgo.com"))

        # adding action when url get changed
        browser.urlChanged.connect(self.update_urlbar)

        # adding action when loading is finished
        browser.loadFinished.connect(self.update_title)

        # add the QWebEngineView to a new tab
        index = self.tabs.addTab(browser, "New Tab")

        # set the new tab as the current tab
        self.tabs.setCurrentIndex(index)

    def closeTab(self, index):
        # remove the tab at the given index
        self.tabs.removeTab(index)


# creating a pyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Achak Browser")

# creating a main window object
window = MainWindow()

# loop
app.exec_()
