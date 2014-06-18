# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_about_window.ui'
#
# Created: Fri May 25 16:27:11 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_About_window(object):
    def setupUi(self, About_window):
        About_window.setObjectName(_fromUtf8("About_window"))
        About_window.resize(400, 300)
        self.lbl_Biotope = QtGui.QLabel(About_window)
        self.lbl_Biotope.setGeometry(QtCore.QRect(70, 20, 271, 121))
        self.lbl_Biotope.setFrameShape(QtGui.QFrame.Box)
        self.lbl_Biotope.setFrameShadow(QtGui.QFrame.Raised)
        self.lbl_Biotope.setText(_fromUtf8(""))
        self.lbl_Biotope.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/synoptiquesatlas/Biotope_Origami.jpg")))
        self.lbl_Biotope.setScaledContents(True)
        self.lbl_Biotope.setObjectName(_fromUtf8("lbl_Biotope"))
        self.label = QtGui.QLabel(About_window)
        self.label.setGeometry(QtCore.QRect(70, 150, 291, 81))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(About_window)
        QtCore.QMetaObject.connectSlotsByName(About_window)

    def retranslateUi(self, About_window):
        About_window.setWindowTitle(QtGui.QApplication.translate("About_window", "About Grids for Atlas", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("About_window", "Biotope GIS Experts pole\n"
"dev-qgis@biotope.fr", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
