import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QTreeWidget, QTreeWidgetItem, QTextBrowser, QTabWidget, QLineEdit, QListWidget
from PyQt6.QtGui import QFont, QIcon
import os

########################################################

selectedBook = ""
selectedChapter = ""

########################################################

connection = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/' + 'bible.db')
cursor = connection.cursor()

cursor.execute("SELECT book_mal_name FROM books WHERE book_cat = 'OLD';")
OTBooks = cursor.fetchall()

cursor.execute("SELECT book_mal_name FROM books WHERE book_cat = 'NEW';")
NTBooks = cursor.fetchall()

########################################################

app = QApplication(sys.argv)
app.setFont(QFont("Malini", 13))

window = QWidget()
window.setWindowTitle("Bible")

layout = QHBoxLayout()

########################################################

tabs = QTabWidget()
tabs.setFixedWidth(430)
layout.addWidget(tabs)

tab1 = QWidget()
tab1Layout = QHBoxLayout()

tab2 = QWidget()
tab2Layout = QVBoxLayout()

########################################################

def onBookClick(item):
    global selectedBook

    selectedBook = item.text(0)

    if item.parent() is not None:
        cursor.execute("SELECT chapter_count FROM books WHERE book_mal_name = ?", [selectedBook])
        chapters = cursor.fetchall()

        chaptersContainer.clear()

        for book in [str(i) for i in range(1, chapters[0][0] + 1)]:
            QTreeWidgetItem(chaptersContainer, [book])

sidebar = QTreeWidget()
sidebar.setHeaderLabel("പുസ്‍തകങ്ങൾ")
sidebar.setFixedWidth(250)

OTItem = QTreeWidgetItem(sidebar, ["പഴയ നിയമം"])
OTItem.setFont(0, QFont("Malini", 15, weight=QFont.Weight.Bold))
OTItem.setExpanded(True)

for book in OTBooks:
    QTreeWidgetItem(OTItem, [book[0]])

NTItem = QTreeWidgetItem(sidebar, ["പുതിയ നിയമം"])
NTItem.setFont(0, QFont("Malini", 15, weight=QFont.Weight.Bold))
NTItem.setExpanded(True)

for book in NTBooks:
    QTreeWidgetItem(NTItem, [book[0]])

sidebar.itemClicked.connect(onBookClick)
tab1Layout.addWidget(sidebar)

########################################################

def setBibleText(chapter, book=None):
    global selectedBook
    global selectedChapter

    if book is not None:
        selectedBook = book

    selectedChapter = chapter

    bible_view.setHtml(f"<h1>{selectedBook} {selectedChapter}</h1>")

    cursor.execute("""SELECT verse_no, verse, heading
            FROM verses WHERE book = ? and chapter = ?""",
                   [selectedBook, selectedChapter])
    
    scrollPos = bible_view.verticalScrollBar().value()

    verses = cursor.fetchall()

    for verse in verses:
        if verse[2] != '':
            bible_view.append(f"<h2><u>{(verse[2])}</u></h2>")

        bible_view.append(f"""
        <p style='font-size: 22px; font-family: "Malini"'>
            {verse[0]}. {verse[1]}
        </p>
        """)

    bible_view.verticalScrollBar().setValue(scrollPos)

chaptersContainer = QTreeWidget()
chaptersContainer.setHeaderLabel("അദ്ധ്യായങ്ങൾ")
chaptersContainer.setFixedWidth(150)
chaptersContainer.itemClicked.connect(lambda item: setBibleText(chapter=item.text(0)))
tab1Layout.addWidget(chaptersContainer)

tab1.setLayout(tab1Layout)
tabs.addTab(tab1, "✞")

########################################################

def searchBible():
    text = searchBar.text()

    search_text = f"%{text}%"
    cursor.execute("""
        SELECT book, chapter, verse_no, verse FROM verses
        WHERE verse LIKE ?
    """,
    [search_text])
    verses = cursor.fetchall()

    for v in verses:
        searchResults.addItem(f"{v[0]} {v[1]}:{v[2]}\n{v[3]}")

def resultClick(item):
    result = item.text().split()

    setBibleText(chapter=result[1].split(":")[0], book=result[0])

searchBar = QLineEdit()
searchBar.setPlaceholderText("Search")
searchBar.returnPressed.connect(searchBible)

searchResults = QListWidget()
searchResults.itemClicked.connect(resultClick)

tab2Layout.addWidget(searchBar)
tab2Layout.addWidget(searchResults)
tab2.setLayout(tab2Layout)
tabs.addTab(tab2, "")
tab_icon = QIcon.fromTheme("edit-find")
tabs.setTabIcon(1, tab_icon)

########################################################

bible_view = QTextBrowser()
bible_view.setStyleSheet("""
    QTextBrowser { background: transparent; border: none; outline: none; }
    QTreeWidget { border: none; }
""")
layout.addWidget(bible_view)

window.setLayout(layout)

window.show()
window.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + '/' + "bible.png"))

sys.exit(app.exec())
