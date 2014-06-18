"""
/***************************************************************************
 SynoptiquesAtlasDialog
                                 A QGIS plugin
 Creation de synoptiques grille ou dynamique pour utiliser dans un atlas
                             -------------------
        begin                : 2012-02-22
        copyright            : (C) 2012 by Experts SIG / Biotope
        email                : dev-qgis@biotope.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_synoptiquesatlas import Ui_SynoptiquesAtlas
# create the dialog for zoom to point
class SynoptiquesAtlasDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_SynoptiquesAtlas()
        self.ui.setupUi(self)
