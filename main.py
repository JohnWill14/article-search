from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

import json

from nlpUtil import process_papers
from fileUtil import write_datas
from nlpUtil import prepareTextFromPath

from nlpUtil import searchBm25


import hashlib

from wordcloud import WordCloud
import matplotlib.pyplot as plt

search = ""
textsTokens = []

most_common = []

def openFile():
    filenames, _ = QFileDialog.getOpenFileNames()
    papers_datas = process_papers(filenames)
    given_repeticion = []
    for paper in papers_datas:
        for  item in datas:
            if item["id"] == paper["id"]:
                given_repeticion.append(item)
                break

    for item in given_repeticion:
        datas.remove(item)

    datas.extend(papers_datas)
    write_datas(datas)
    loadItensFromFile()
    search()

def search():
    query = main.stringline.text()
    print("Searching...", query)
    if len(textsTokens) == 0:
        for item in datas:
            tokens = prepareTextFromPath(item['path'])
            textsTokens.append(tokens)
    ans = []
    if query != "":
        freq = searchBm25(query, textsTokens)

        novaFreq = {}
        for idx, item in enumerate(freq):
            novaFreq.update({idx: item})

        list_Index = {k: v for k, v in sorted(novaFreq.items(), key=lambda item: item[1], reverse=True)}

        for i in list_Index:
            if novaFreq[i] != 0:
                ans.append(datas[i])
    else:
        ans = datas

    setFrame(ans)
    updateTable(ans)
def setFrame(datas):
    if len(datas) == 0:
        main.frame.close()
        main.frame_progress.close()
    else:
        main.frame.show()
        main.frame_progress.show()

def updateTable(datasForTable):
    datasTable = []
    for item in datasForTable:
        data = {"name": item['title']}

        datasTable.append(data)

    main.tableWidget.setRowCount(len(datasTable))

    row = 0
    for e in datasTable:
        main.tableWidget.setItem(row, 0, QTableWidgetItem(e['name']))
        row += 1

def loadItensFromFile():
    try:
        with open('data.txt', 'r') as myfile:
            data = myfile.read()
            loads = json.loads(data)
            print(loads)
        return json.loads(data)
    except:
        return []

def itemClicked(item):
    row = item.row()
    text = main.tableWidget.item(row, 0).text()
    h = hashlib.shake_256(text.encode())
    id = h.hexdigest(20)

    for json in datas:
        if json['id'] == id:
            item = json
            break


    article.labelTitle.setText(item['title'])
    article.textObjective.setText(item['objective'])
    article.textMethod.setText("\n\n ".join(item['method']))
    article.textProblem.setText("\n\n ".join(item['problem']))
    article.textContribute.setText("\n\n ".join(item['contributes']))
    article.textReference.setText(item['references'])
    article.setWindowTitle(item['title'])
    article.labelPath.setText(item['path'])

    article.pushShowFreq.clicked.connect(lambda: showWordCloud(item['most_common']))

    article.show()

def showWordCloud(most_common):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(most_common))

    # Display the generated word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    datas = loadItensFromFile()

    app = QtWidgets.QApplication([])
    main = uic.loadUi('main.ui')

    article = uic.loadUi('article.ui')
    setFrame(datas)

    main.actionExit.triggered.connect(main.close)
    main.actionadd_paper.triggered.connect(openFile)

    updateTable(datas)
    main.searchButton.clicked.connect(search)

    main.tableWidget.itemClicked.connect(itemClicked)

    main.show()
    app.exec()