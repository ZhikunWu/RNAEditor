# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ressources/InputTab.ui'
#
# Created: Mon Nov  4 15:28:17 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QSizePolicy
from PyQt4.QtGui import QGridLayout, QVBoxLayout
from Helper import Parameters


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class DropListWidget(QtGui.QListWidget):
    def __init__(self, type, parent=None):
        super(DropListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(72, 72))
        
        #enable multiple selection
        #self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        #enable drag and drop
        #self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        
        #set sorting enabled
        self.setSortingEnabled(True)

    def dragEnterEvent(self, event):
        """
            Only accepts Files if they are valid 
        """
        if event.mimeData().hasUrls:
            isFastq=True
            for url in event.mimeData().urls():
                url = url.toString()
                urlSuffix = url.split(".")[-1]
                if urlSuffix not in ["fastq","fq","bam"]:
                    isFastq=False
            if isFastq:
                event.setDropAction(QtCore.Qt.CopyAction)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
            self.sortItems()
        else:
            event.ignore()
            
    def dropFirstItem(self):
        if self.count() > 0:
            return self.takeItem(0)
    
    def dropLastItems(self,n):
        if self.count() > 0:
            return self.takeItem(self.count()-1)

class InputTab(QtGui.QWidget):
    
    def __init__(self,control):
        
        self.control=control
        super(InputTab,self).__init__()
        
        self.createMenu()
        self.createComponents()
        self.createLayout()
        self.createConnects()
        
        
        
    def createMenu(self):
        pass
    
    def createComponents(self):

        #m_pMyWidget->setStyleSheet("background-color:black;");
        
        """
        InputFiles Layout on the left Side
        """
        self.refGenomeLabel = QtGui.QLabel("ref. Genome:")
        self.refGenomeTextBox = QtGui.QLineEdit()
        self.refGenomeButton = QtGui.QPushButton(self.tr("..."))
        
        self.gtfFileLabel = QtGui.QLabel("GTF File:")
        self.gtfFileTextBox = QtGui.QLineEdit()
        self.gtfFileButton = QtGui.QPushButton(self.tr("..."))
        
        self.dbsnpLabel = QtGui.QLabel("dbSNP:")
        self.dbsnpTextBox = QtGui.QLineEdit()
        self.dbsnpButton = QtGui.QPushButton(self.tr("..."))
        
        self.hapmapLabel = QtGui.QLabel("Hapmap:")
        self.hapmapTextBox = QtGui.QLineEdit()
        self.hapmapButton = QtGui.QPushButton(self.tr("..."))
        
        self.omniLabel = QtGui.QLabel("Omni:")
        self.omniTextBox = QtGui.QLineEdit()
        self.omniButton = QtGui.QPushButton(self.tr("..."))
        
        self.espLabel = QtGui.QLabel("ESP:")
        self.espTextBox = QtGui.QLineEdit()
        self.espButton = QtGui.QPushButton(self.tr("..."))
        
        self.aluRegionsLabel = QtGui.QLabel("Alu Regions:")
        self.aluRegionsTextBox = QtGui.QLineEdit()
        self.aluRegionsButton = QtGui.QPushButton(self.tr("..."))
        
        self.sourceDirLabel = QtGui.QLabel("Source Directory")
        self.sourceDirTextBox = QtGui.QLineEdit()
        self.sourceDirButton = QtGui.QPushButton(self.tr("..."))
        
        self.verticalLine = QtGui.QFrame()
        self.verticalLine.setFrameStyle(QtGui.QFrame.HLine)
        self.verticalLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        
        self.outputLabel = QtGui.QLabel("Output directory")
        self.outputTextBox = QtGui.QLineEdit()
        self.outputButton = QtGui.QPushButton(self.tr("..."))
        #self.button.setStyleSheet("background-color:red;")
    

        """
        Drop Files Section
        """
        self.dropList = DropListWidget(self)
        self.dropList.setAcceptDrops(True)
        
        
        
        """
        Settings Layout on the bottom
        """
        self.threadsLabel = QtGui.QLabel("Threads:")
        self.threadsSpinBox = QtGui.QSpinBox()
        self.threadsSpinBox.setRange(1,30)
        self.threadsSpinBox.setValue(4)

        self.maxDiffLabel = QtGui.QLabel("max Diff Rate:")
        self.maxDiffLabel.setToolTip("Error rate in percentage")
        self.maxDiffSpinBox = QtGui.QDoubleSpinBox()
        self.maxDiffSpinBox.setToolTip("Error rate in percentage")
        self.maxDiffSpinBox.setRange(0.01,0.2)
        self.maxDiffSpinBox.setSingleStep(0.01)
        self.maxDiffSpinBox.setValue(0.04)
        
        self.seedLabel = QtGui.QLabel("Seed Diff:")
        self.seedLabel.setToolTip("Maximum number of mismatches in the seed sequence")
        self.seedSpinBox = QtGui.QSpinBox()
        self.seedSpinBox.setToolTip("Maximum number of mismatches in the seed sequence")
        self.seedSpinBox.setRange(1,10)
        self.seedSpinBox.setValue(2)
        
        self.standCallLabel = QtGui.QLabel("Stand Call:")
        self.seedLabel.setToolTip("The minimum phred-scaled confidence threshold at which variants should be considered as true")
        self.standCallSpinBox = QtGui.QSpinBox()
        self.standCallSpinBox.setToolTip("The minimum phred-scaled confidence threshold at which variants should be considered as true")
        self.standCallSpinBox.setRange(1,30)
        self.standCallSpinBox.setValue(2)
        
        self.standEmitLabel = QtGui.QLabel("Stand Emit:")
        self.standEmitLabel.setToolTip("The minimum phred-scaled confidence threshold at which variants should be emitted")
        self.standEmitSpinBox = QtGui.QSpinBox()
        self.standEmitSpinBox.setToolTip("The minimum phred-scaled confidence threshold at which variants should be emitted")
        self.standEmitSpinBox.setRange(1,30)
        self.standEmitSpinBox.setValue(2)
        
        self.edgeDistanceLabel = QtGui.QLabel("min edge distance:")
        self.edgeDistanceLabel.setToolTip("The minimum distance of the editing site from the read edge")
        self.edgeDistanceSpinBox = QtGui.QSpinBox()
        self.edgeDistanceSpinBox.setToolTip("The minimum distance of the editing site from the read edge")
        self.edgeDistanceSpinBox.setRange(0,15)
        self.edgeDistanceSpinBox.setValue(3)
        
        self.pairedCheckBox = QtGui.QCheckBox("paired-end Sequencing")
        self.overwriteCheckBox = QtGui.QCheckBox("Overwrite existing Files")
        self.overwriteCheckBox.setChecked(True)
        self.keepTempCheckBox = QtGui.QCheckBox("Keep temporary Files")
        
        #Start Button
        self.startButton = QtGui.QPushButton(self.tr("Start New Analysis"))

    def createLayout(self):
        #drop Part
        self.dropList.setStyleSheet("border: 1px solid black")
        
        
        #create right Side
        self.inputFilesLayout = QGridLayout()
        self.inputFilesLayout.addWidget(self.gtfFileLabel,1,1)
        self.inputFilesLayout.addWidget(self.gtfFileTextBox,1,2)
        self.inputFilesLayout.addWidget(self.gtfFileButton,1,3)
        
        self.inputFilesLayout.addWidget(self.refGenomeLabel,2,1)
        self.inputFilesLayout.addWidget(self.refGenomeTextBox,2,2)
        self.inputFilesLayout.addWidget(self.refGenomeButton,2,3)
        
        self.inputFilesLayout.addWidget(self.dbsnpLabel,3,1)
        self.inputFilesLayout.addWidget(self.dbsnpTextBox,3,2)
        self.inputFilesLayout.addWidget(self.dbsnpButton,3,3)
        
        self.inputFilesLayout.addWidget(self.hapmapLabel,4,1)
        self.inputFilesLayout.addWidget(self.hapmapTextBox,4,2)
        self.inputFilesLayout.addWidget(self.hapmapButton,4,3)
        
        self.inputFilesLayout.addWidget(self.omniLabel,5,1)
        self.inputFilesLayout.addWidget(self.omniTextBox,5,2)
        self.inputFilesLayout.addWidget(self.omniButton,5,3)
        
        self.inputFilesLayout.addWidget(self.espLabel,6,1)
        self.inputFilesLayout.addWidget(self.espTextBox,6,2)
        self.inputFilesLayout.addWidget(self.espButton,6,3)
        
        self.inputFilesLayout.addWidget(self.aluRegionsLabel,7,1)
        self.inputFilesLayout.addWidget(self.aluRegionsTextBox,7,2)
        self.inputFilesLayout.addWidget(self.aluRegionsButton,7,3)
        
        self.inputFilesLayout.addWidget(self.sourceDirLabel,8,1)
        self.inputFilesLayout.addWidget(self.sourceDirTextBox,8,2)
        self.inputFilesLayout.addWidget(self.sourceDirButton,8,3)
        
        self.inputFilesLayout.addWidget(self.verticalLine,9,1,1,3)
        self.inputFilesLayout.setRowMinimumHeight(9,20)
        
        self.inputFilesLayout.addWidget(self.outputLabel,10,1)
        self.inputFilesLayout.addWidget(self.outputTextBox,10,2)
        self.inputFilesLayout.addWidget(self.outputButton,10,3)
        
        
        self.inputFilesLayout.setColumnMinimumWidth(2,100)
        self.inputFilesLayout.setRowStretch(9,1)
        
        self.inputFilesWidget = QtGui.QWidget()
        self.inputFilesWidget.setLayout(self.inputFilesLayout)
        self.inputFilesWidget.setStyleSheet(".QWidget{border: 1px solid black}")

        
        #create settings layout
        self.settingsLayout = QGridLayout()
        self.settingsLayout.addWidget(self.threadsLabel,1,1)
        self.settingsLayout.addWidget(self.threadsSpinBox,1,2)
        self.settingsLayout.addWidget(self.maxDiffLabel,2,1)
        self.settingsLayout.addWidget(self.maxDiffSpinBox,2,2)
        self.settingsLayout.addWidget(self.seedLabel,3,1)
        self.settingsLayout.addWidget(self.seedSpinBox,3,2)
        
        self.settingsLayout.addWidget(self.standCallLabel,1,3)
        self.settingsLayout.addWidget(self.standCallSpinBox,1,4)
        self.settingsLayout.addWidget(self.standEmitLabel,2,3)
        self.settingsLayout.addWidget(self.standEmitSpinBox,2,4)
        self.settingsLayout.addWidget(self.edgeDistanceLabel,3,3)
        self.settingsLayout.addWidget(self.edgeDistanceSpinBox,3,4)
        
        self.settingsLayout.addWidget(self.pairedCheckBox,1,5)
        self.settingsLayout.addWidget(self.keepTempCheckBox,2,5)
        self.settingsLayout.addWidget(self.overwriteCheckBox,3,5)
        
        self.settingsLayout.setColumnStretch(2,1)
        self.settingsLayout.setColumnStretch(6,5)
        
        
        self.settingsWidget = QtGui.QWidget()
        self.settingsWidget.setLayout(self.settingsLayout)
        

        
        #self.settingsLayout.setColumnStretch(3,1)
        
        #create central Layout
        self.centralLayout = QGridLayout()
        self.centralLayout.setRowStretch(1,1)
        self.centralLayout.setColumnStretch(1,1)
        self.centralLayout.addWidget(self.dropList,1,1)
        
        
        
        self.centralLayout.addWidget(self.inputFilesWidget, 1,2)
        self.centralLayout.addWidget(self.settingsWidget, 2, 1, 1, 2)
        self.centralLayout.addWidget(self.startButton,3,2)
        self.setLayout(self.centralLayout)
        
        
        
        
        
    def createConnects(self):
        self.refGenomeButton.clicked.connect(lambda: self.control.openFileDialog(self.refGenomeTextBox))
        self.dbsnpButton.clicked.connect(lambda: self.control.openFileDialog(self.dbsnpTextBox))
        self.hapmapButton.clicked.connect(lambda: self.control.openFileDialog(self.hapmapTextBox))
        self.omniButton.clicked.connect(lambda: self.control.openFileDialog(self.omniTextBox))
        self.espButton.clicked.connect(lambda: self.control.openFileDialog(self.espTextBox))
        self.aluRegionsButton.clicked.connect(lambda: self.control.openFileDialog(self.aluRegionsTextBox))
        
        self.outputButton.clicked.connect(lambda: self.control.openFolderDialog(self.outputTextBox))
        self.sourceDirButton.clicked.connect(lambda: self.control.openFolderDialog(self.sourceDirTextBox))
        
        self.startButton.clicked.connect(self.control.newAssay)
        
        self.connect(self.dropList, QtCore.SIGNAL("dropped"), self.control.fileDropped)
        
    def createDefaults(self):
        p=Parameters()
        
        self.gtfFileTextBox.setText(p.gtfFile)
        self.refGenomeTextBox.setText(p.refGenome)   
        self.dbsnpTextBox.setText(p.dbsnp)
        self.hapmapTextBox.setText(p.hapmap)
        self.omniTextBox.setText(p.omni)
        self.espTextBox.setText(p.esp)
        self.aluRegionsTextBox.setText(p.aluRegions)
        self.outputTextBox.setText(p.output)
        self.sourceDirTextBox.setText(p.sourceDir)
        
        self.threadsSpinBox.setValue(p.threads)
        self.maxDiffSpinBox.setValue(p.maxDiff)
        self.seedSpinBox.setValue(p.seedDiff)
        self.standCallSpinBox.setValue(p.standCall)
        self.standEmitSpinBox.setValue(p.standEmit)
        self.pairedCheckBox.setChecked(p.paired)
        self.keepTempCheckBox.setChecked(p.keepTemp)
        self.overwriteCheckBox.setChecked(p.overwrite)
            
            
if __name__ == '__main__':
    import sys, os
    print(os.getcwd())
    app = QtGui.QApplication(sys.argv) 
    mainWindow = InputTab()
    mainWindow.show() 
    sys.exit(app.exec_())
   
