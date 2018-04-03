#!/usr/bin/env python

import os
from PyQt5.QtCore import (QDir, QDirIterator, QIODevice, QFile, QFileInfo, Qt, QTextStream,
                          QUrl)
from PyQt5.QtGui import QDesktopServices, QFont, QColor
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QComboBox,
                             QDialog, QFileDialog, QGridLayout, QHBoxLayout, QHeaderView, QLabel,
                             QProgressDialog, QPushButton, QSizePolicy, QTableWidget, QCheckBox,
                             QTableWidgetItem, QSpinBox, QMessageBox)


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # Initialize user settings
        self.recursivity = QDirIterator.Subdirectories
        self.recursivity_2 = QDirIterator.NoIteratorFlags
        self.dirFilters = (QDir.Dirs | QDir.NoDotAndDotDot)
        # to swap size and count in file view
        self.dirView = True
        self.subfolderLevel = 0

        # Row 0
        directoryLabel = QLabel("In folder:")
        self.directoryComboBox = self.createComboBox(os.getcwd())
        browseButton = self.createButton("&Browse...", self.browse)

        # Row 1
        filterLabel = QLabel("Filter:")
        self.filterComboBox = self.createComboBox('*')
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem("All")
        self.typeComboBox.addItem("Folders")
        self.typeComboBox.addItem("Files")
        self.typeComboBox.setCurrentIndex(1)
        self.typeComboBox.currentIndexChanged.connect(self.changeType)
        self.checkBox = QCheckBox("Subfolders")
        self.checkBox.toggle()
        self.checkBox.stateChanged.connect(self.changeRecursivity)
        self.findButton = self.createButton("&Find", self.find)

        # Row 2

        self.depthLabel = QLabel("Count files in subfolder number:")
        self.folderDepthSpinBox = QSpinBox()
        self.folderDepthSpinBox.valueChanged.connect(self.changeFolderDepth)
        self.checkBox_2 = QCheckBox("Files in all subfolders")
        self.checkBox_2.stateChanged.connect(self.changeRecursivity_2)

        # Row 3 Table
        self.createFilesTable()

        # Row 5
        self.filesFoundLabel = QLabel()
        saveButton = self.createButton("&Save", self.saveSheet)

        # Not implemented, for full text search
        self.textComboBox = self.createComboBox()
        textLabel = QLabel("Containing text:")

        mainLayout = QGridLayout()

        mainLayout.addWidget(directoryLabel, 0, 0, 1, 1)
        mainLayout.addWidget(self.directoryComboBox, 0, 1, 1, 5)

        # Row 1
        mainLayout.addWidget(filterLabel, 1, 0, 1, 1)
        mainLayout.addWidget(self.filterComboBox, 1, 1, 1, 5)
        mainLayout.addWidget(self.typeComboBox, 1, 6, 1, 1)
        mainLayout.addWidget(self.findButton, 1, 7, 1, 1)

        # Row 0
        mainLayout.addWidget(self.checkBox, 0, 6, 1, 1)
        mainLayout.addWidget(browseButton, 0, 7, 1, 1)

        # Row 2
        mainLayout.addWidget(self.depthLabel, 2, 4, 1, 1, Qt.AlignRight)
        mainLayout.addWidget(self.folderDepthSpinBox, 2, 5, 1, 1)
        mainLayout.addWidget(self.checkBox_2, 2, 6, 1, 2)

        # Table
        mainLayout.addWidget(self.filesTable, 4, 0, 1, 8)

        # Row 5
        mainLayout.addWidget(self.filesFoundLabel, 5, 0, 1, 4)

        mainLayout.addWidget(saveButton, 5, 7, 1, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("BDRC File Counter")
        self.resize(520, 440)
        # self.resize(442, 440)

    def changeRecursivity_2(self, state):
        if state == Qt.Checked:
            self.recursivity_2 = QDirIterator.Subdirectories
        else:
            self.recursivity_2 = QDirIterator.NoIteratorFlags

    def changeFolderDepth(self, value):
        self.subfolderLevel = value

    def changeType(self, typeIndex):
        if typeIndex == 0:
            self.dirFilters = (
                QDir.AllEntries | QDir.NoSymLinks | QDir.NoDotAndDotDot)
            self.dirView = False
            self.filesTable.setHorizontalHeaderLabels(("Item Path", "Size"))
            self.subfolderLevel = 0
            self.depthLabel.hide()
            self.folderDepthSpinBox.hide()

        elif typeIndex == 1:
            self.dirFilters = (QDir.Dirs | QDir.NoDotAndDotDot)
            self.dirView = True
            self.filesTable.setHorizontalHeaderLabels(
                ("Folder Path", "File Count"))
            self.depthLabel.show()
            self.folderDepthSpinBox.show()

        elif typeIndex == 2:
            self.dirFilters = (QDir.Files | QDir.NoSymLinks)
            self.dirView = False
            self.filesTable.setHorizontalHeaderLabels(("File Path", "Size"))
            self.subfolderLevel = 0
            self.depthLabel.hide()
            self.folderDepthSpinBox.hide()

    def changeRecursivity(self, state):
        if state == Qt.Checked:
            self.recursivity = QDirIterator.Subdirectories
        else:
            self.recursivity = QDirIterator.NoIteratorFlags

    def browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Find files",
                                                     os.getcwd())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(
                self.directoryComboBox.findText(directory))

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def find(self):
        self.filesTable.setRowCount(0)

        self.path = self.directoryComboBox.currentText()
        fileName = self.filterComboBox.currentText()
        files = []
        text = self.textComboBox.currentText()

        if not fileName:
            fileName = "*"
        fileName = fileName.split(", ")

        self.updateComboBox(self.directoryComboBox)
        self.updateComboBox(self.filterComboBox)
        self.updateComboBox(self.textComboBox)

        self.currentDir = QDir(self.path)

        self.it = QDirIterator(self.path, fileName,
                               self.dirFilters, self.recursivity)
        while self.it.hasNext():
            files.append(self.it.next())

        # For full text search, not used
        if text:
            files = self.findFiles(files, text)

        self.showFiles(files)

    # For full text search, not used
    def findFiles(self, files, text):
        progressDialog = QProgressDialog(self)

        progressDialog.setCancelButtonText("&Cancel")
        progressDialog.setRange(0, files.count())
        progressDialog.setWindowTitle("Find Files")

        foundFiles = []

        for i in range(files.count()):
            progressDialog.setValue(i)
            progressDialog.setLabelText(
                "Searching file number %d of %d..." % (i, files.count()))
            QApplication.processEvents()

            if progressDialog.wasCanceled():
                break

            inFile = QFile(self.currentDir.absoluteFilePath(files[i]))

            if inFile.open(QIODevice.ReadOnly):
                stream = QTextStream(inFile)
                while not stream.atEnd():
                    if progressDialog.wasCanceled():
                        break
                    line = stream.readLine()
                    if text in line:
                        foundFiles.append(files[i])
                        break

        progressDialog.close()

        return foundFiles

    def showFiles(self, files):
        for fn in files:
            file = QFile(self.currentDir.relativeFilePath(fn))
            # May change in countfile()
            self.pathToDisplay = fn

            if QFileInfo(file).isDir():
                size = self.countFiles(fn)
                if self.dirView:
                    sizeItem = QTableWidgetItem("%d" % size)
                else:
                    sizeItem = QTableWidgetItem("%d files" % size)
            else:
                size = QFileInfo(file).size()
                sizeItem = QTableWidgetItem(
                    "%d KB" % (int((size + 1023) / 1024)))

            fileNameItem = QTableWidgetItem(
                self.pathToDisplay.replace(self.path, '.'))
            fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)

            sizeItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

            # if self.pathToDisplay == fn and size == 0:
            #     self.filesTable.item(row, 0).setBackground(QColor(211,211,211))

        self.filesFoundLabel.setText(
            "%d matches. Double click to open." % len(files))

    def countFiles(self, folder):
        files = []

        if self.subfolderLevel > 0:
            import glob
            try:
                path = glob.glob('%s/%s' %
                                 (folder, '*/'*self.subfolderLevel))[0]
                self.pathToDisplay = path
            except:
                return 0
        else:
            path = folder

        it = QDirIterator(
            path, (QDir.Files | QDir.NoSymLinks), self.recursivity_2)
        while it.hasNext():
            files.append(it.next())

        count = len(files)
        return count

    def createButton(self, text, member):
        button = QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return comboBox

    def createFilesTable(self):
        self.filesTable = QTableWidget(0, 2)
        self.filesTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(
            ("Folder Path", "File Count"))
        self.filesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

        self.filesTable.cellActivated.connect(self.openFileOfItem)

    def saveSheet(self):
        import os
        import csv
        path = QFileDialog.getSaveFileName(
            self, 'Save CSV', os.getcwd(), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.filesTable.rowCount()):
                    row_data = []
                    for column in range(self.filesTable.columnCount()):
                        item = self.filesTable.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    row_data[0] = self.path + row_data[0][1:]
                    writer.writerow(row_data)
            QMessageBox.information(self, "Export Successful",
                                    "Your search result has been exported as a csv.")

    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)

        # Complete links to make them click
        path = self.path + item.text()[1:]
        QDesktopServices.openUrl(QUrl.fromLocalFile(
            self.currentDir.absoluteFilePath(path)))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
