import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame, QTreeWidget, QTreeWidgetItem, QTextBrowser
from PyQt6.QtGui import QFont, QIcon

########################################################

selectedBook = ""
selectedChapter = ""

########################################################

connection = sqlite3.connect('bible.db')
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
layout.addWidget(sidebar)

########################################################

def onChapterClick(item):
    global selectedChapter

    selectedChapter = item.text(0)

    bible_view.setHtml(f"<h1 style='font-family: \"Malini\"'>{selectedBook} {selectedChapter}</h1>")

    cursor.execute("""SELECT verse_no, verse
            FROM verses WHERE book = ? and chapter = ?""",
                   [selectedBook, selectedChapter])
    
    scrollPos = bible_view.verticalScrollBar().value()

    verses = cursor.fetchall()

    for verse in verses:
        bible_view.append(f"""
        <p style='font-size: 23px; font-family: "Malini"'>
            {verse[0]}. {verse[1]}
        </p>
        """)

    bible_view.verticalScrollBar().setValue(scrollPos)

chaptersContainer = QTreeWidget()
chaptersContainer.setHeaderLabel("അദ്ധ്യായങ്ങൾ")
chaptersContainer.setFixedWidth(150)
chaptersContainer.itemClicked.connect(onChapterClick)
layout.addWidget(chaptersContainer)

########################################################

bible_view = QTextBrowser()
bible_view.setStyleSheet("""
    QTextBrowser { background: transparent; border: none; outline: none; }
    QTreeWidget { border: none; }
""")
layout.addWidget(bible_view)

window.setLayout(layout)

window.show()
window.setWindowIcon(QIcon("icon.png"))

sys.exit(app.exec())
