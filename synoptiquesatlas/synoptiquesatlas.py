"""
/***************************************************************************
 GridsForAtlas
                                 A QGIS plugin
 Creation de synoptiques grille ou dynamique pour utiliser dans un atlas
                              -------------------
        begin                : 2012-02-22
        copyright            : (C) 2012 by Experts SIG / Biotope
        email                : dev-qgis@biotope.fr

 Version 0.2.3
 
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
from __future__ import absolute_import
from builtins import object
import os
import math
# Import the PyQt and QGIS libraries
from qgis.PyQt.QtCore import QFileInfo, QCoreApplication, QObject, QVariant
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
# Initialize Qt resources from file resources.py
from . import resources_rc
# Import the code for the dialog
from .synoptiquesatlasdialog import SynoptiquesAtlasDialog
#from ui_help_window import Ui_help_window
from .ui_about_window import Ui_About_window

class SynoptiquesAtlas(object):

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    # a reference to our map canvas
    self.canvas = self.iface.mapCanvas()
    # Setup directory
    self.syn_atlas_plugin_dir = os.path.dirname(__file__)
    # Translation to English
    #locale = QSettings().value("locale/userLocale").toString()
    #self.myLocale = locale[0:2]
    #if QFileInfo(self.syn_atlas_plugin_dir).exists():
    #  localePath = self.syn_atlas_plugin_dir + "/i18n/synoptiquesatlas_" + self.myLocale + ".qm"
    #if QFileInfo(localePath).exists():
    #  self.translator = QTranslator()
    #  self.translator.load(localePath)
    #  if qVersion() > '4.3.3':
    #        QCoreApplication.installTranslator(self.translator)
    # create and show the dialog
    self.dlg = SynoptiquesAtlasDialog()

  def initGui(self):
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/synoptiquesatlas/icon.png"), \
      QCoreApplication.translate("synoptiquesatlas", "&Grids for Atlas"), self.iface.mainWindow())
    # Create action for about dialog
    self.action_about = QAction("A&bout...", self.iface.mainWindow())
    # Create action for help dialog
    self.action_help = QAction(QIcon(":/plugins/synoptiquesatlas/about.png"), QCoreApplication.translate("synoptiquesatlas", "&Help..."), self.iface.mainWindow())
    # connect the action to the run method
    self.action.triggered.connect(self.run)
    # connect about action to about dialog
    self.action_about.triggered.connect(self.showAbout)
    # connect help action to help dialog
    self.action_help.triggered.connect(self.showHelp)
    # connect signals
    self.dlg.ui.btnCreerSyno.clicked.connect(self.creerSyno)
    # layout changed, update maps
    # ajh: don't need this if we don't allow to select map
    self.dlg.ui.cbbComp.currentIndexChanged.connect(self.updateMaps)
    # refresh inLayer box
    self.dlg.ui.cbbInLayer.currentIndexChanged.connect(self.onLayerChange)
    # browse button
    self.dlg.ui.btnBrowse.clicked.connect(self.updateOutputDir)
    # refresh template button
    self.dlg.ui.btnUpdate.clicked.connect(self.updateLayouts)
    # show layout
    self.dlg.ui.btnShow.clicked.connect(self.showLayout)
    # show about dialog
    self.dlg.ui.aboutButton.clicked.connect(self.showAbout)
    # show help dialog
    self.dlg.ui.helpButton.clicked.connect(self.showHelp)
    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&Grids for Atlas", self.action)
    # Add about menu entry
    self.iface.addPluginToMenu("&Grids for Atlas", self.action_about)
    # add help menu entry
    self.iface.addPluginToMenu("&Grids for Atlas", self.action_help)

  def updateBoxes(self):
    self.updateLayers()
    self.updateLayouts
    self.updateMaps()

  def updateLayers(self):
    self.dlg.ui.cbbInLayer.clear()
    for layer in self.iface.mapCanvas().layers():
      #self.dlg.ui.cbbInLayer.addItem(layer.name(), QVariant(layer))
      self.dlg.ui.cbbInLayer.addItem(layer.name(), layer)

  # (c) Carson Farmer / fTools
  def getVectorLayerByName(self,myName):
    layermap = QgsProject.instance().mapLayers()
    for name, layer in layermap.items():
      if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
        if layer.isValid():
          return layer
        else:
          return None 

  def onLayerChange(self):
    self.cLayer = self.getVectorLayerByName(self.dlg.ui.cbbInLayer.currentText())

  def updateLayouts(self):
    #ajh: todo figure out how to make it automatically select the first Layout if there is one when starting the plugin
    self.dlg.ui.cbbComp.clear()
    projectInstance = QgsProject.instance()
    projectLayoutManager = projectInstance.layoutManager()
    self.layouts = projectLayoutManager.printLayouts()
    #ajh todo get this working
    for cv in self.layouts:
      #QMessageBox.information(self.iface.mainWindow(),"Info", \
      #    "testing")
      self.dlg.ui.cbbComp.addItem(cv.name(), cv)
    self.layout = self.dlg.ui.cbbComp.itemData(self.dlg.ui.cbbComp.currentIndex())#.toPyObject()

  def updateMaps(self):
    if self.dlg.ui.cbbComp.currentIndex() != -1:
      self.layout = self.layouts[self.dlg.ui.cbbComp.currentIndex()]

  def showLayout(self):
    iface.openLayoutDesigner(self.layout)

  def updateOutputDir(self):
    self.dlg.ui.lieOutDir.setText(QFileDialog.getExistingDirectory(self.dlg, \
      QCoreApplication.translate("synoptiquesatlas", "Choose output directory")))

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&Grids for Atlas",self.action)
    self.iface.removeToolBarIcon(self.action)
    # Remove about menu entry
    self.iface.removePluginMenu("&Grids for Atlas", self.action_about)
    # Remove help menu entry
    self.iface.removePluginMenu("&Grids for Atlas", self.action_help)

  def creerSyno(self):               
    if os.path.exists(self.dlg.ui.lieOutDir.text()):
      self.gridSynopt = self.dlg.ui.chkGrille.isChecked()
      self.dynSynopt = self.dlg.ui.chkDyn.isChecked()
      if self.gridSynopt or self.dynSynopt:
        if self.layouts:
          #ajh: we'll retain updateMaps() for this
          #self.layout = layouts[self.dlg.ui.cbbComp.currentIndex()]
          # ajh: we probably don't need to select the map; just use the referenceMap
          cmap = self.layout.referenceMap()
          if cmap:
            self.ladderHeight = cmap.extent().height()
            self.ladderWidth = cmap.extent().width()
            self.ladderOvrlpPercent = float(self.dlg.ui.overlapInp.text())
            if self.ladderOvrlpPercent < 100 and self.ladderOvrlpPercent >= 0:
              self.overlapW = self.ladderWidth * self.ladderOvrlpPercent / 100;
              self.overlapH = self.ladderHeight * self.ladderOvrlpPercent / 100;
              self.ladderWidth = self.ladderWidth - self.overlapW * 2.;
              self.ladderHeight = self.ladderHeight - self.overlapH * 2.;
              if self.cLayer:
                if self.cLayer.type() == 0:
                  self.crs = self.cLayer.crs()
                  self.URIcrs = "crs=" + self.crs.authid()
                  self.doBuffer()
                  #next 2 lines because of bug 
                  #http://gis.stackexchange.com/questions/87936/problem-creating-point-shapefiles-programmatically-using-python-in-qgis-2-2
                  #look at "and if we examine the extents:"
                  self.bcLayer.selectAll()
                  self.extent = self.bcLayer.boundingBoxOfSelected()
                  self.sLayer = self.addSynoFeatures()
                  self.fill_references(self.sLayer)
                  self.synopt_shape_path = self.dlg.ui.lieOutDir.text() + QCoreApplication.translate("synoptiquesatlas","/classic_grid.shp")
                  self.createPhysLayerFromList(self.synopt_shape_path, self.sLayer)
                  if self.gridSynopt:  
                    self.sLayer = self.loadQgsVectorLayer(self.synopt_shape_path, \
                      QCoreApplication.translate("synoptiquesatlas","classic grid"))
                  else:
                    self.sLayer = QgsVectorLayer(self.synopt_shape_path, QCoreApplication.translate("synoptiquesatlas","classic grid"), "ogr")                          
                    # TODO                
                    # Manage symbology
                    #if not hasattr(self.sLayer, 'isUsingRendererV2'):
                    #  QMessageBox.information(self.iface.mainWindow(),"Info", \
                    #  "La symbologie ne peut etre affichee vous utilisez une version ancienne de QGIS")
                    #elif layer.isUsingRendererV2():
                    # new symbology - subclass of QgsFeatureRendererV2 class
                    #  rendererV2 = layer.rendererV2()  
                  # Grid layer was created, access to the second stage
                  if self.dynSynopt:
                    self.finalSynopt_shape_path = self.dlg.ui.lieOutDir.text() + QCoreApplication.translate("synoptiquesatlas","/dyn_grid.shp")
                    self.intersect(self.bcLayer,self.sLayer)
                    self.createIntersectionLayer()
                    self.new_ladders_list = []
                    self.sLayer2 = self.centroidsToNewSyno(self.new_ladders_list)
                    self.parseSyno()
                    self.final_ladders_list = []
                    self.sLayer3 = self.centroidsToNewSyno(self.final_ladders_list)
                    self.fill_references(self.sLayer3)
                    self.createPhysLayerFromList(self.finalSynopt_shape_path, self.sLayer3)
                    self.sLayer3 = self.loadQgsVectorLayer(self.finalSynopt_shape_path, \
                      QCoreApplication.translate("synoptiquesatlas","dynamic grid"))
                else:
                  QMessageBox.information(self.iface.mainWindow(),"Info", \
                    QCoreApplication.translate("synoptiquesatlas","Coverage layer is not vector type"))
              else:
                QMessageBox.information(self.iface.mainWindow(),"Info", \
                  QCoreApplication.translate("synoptiquesatlas","Please select a coverage layer to generate grid"))
            else:
              QMessageBox.information(self.iface.mainWindow(),"Info", \
                QCoreApplication.translate("synoptiquesatlas","Overlap % must be between 0 and 100"))
          else:
              QMessageBox.information(self.iface.mainWindow(),"Info", \
                  QCoreApplication.translate("synoptiquesatlas","There is no map object for print layout selected"))
        else:
          QMessageBox.information(self.iface.mainWindow(),"Info", \
            QCoreApplication.translate("synoptiquesatlas","Please select a print layout, if none is active you have to create it"))
      else:
        QMessageBox.information(self.iface.mainWindow(),"Info", QCoreApplication.translate("synoptiquesatlas","Choose a grid type"))
    else:
      QMessageBox.information(self.iface.mainWindow(),"Info", QCoreApplication.translate("synoptiquesatlas","Please enter an existing OutFiles directory"))

  def doBuffer(self):
    maxDim = max(self.ladderHeight,self.ladderWidth)
    ratio = 1000./2970
    bufferLength = maxDim * ratio
    self.bcLayer = QgsVectorLayer("Polygon" + "?" + self.URIcrs, "buffer_layer", "memory")
    pr = self.bcLayer.dataProvider()
    pr.addAttributes([QgsField("ID_BUFFER", QVariant.Int)])
    i = 0    
    for feature in self.cLayer.dataProvider().getFeatures():
      fet = QgsFeature()
      bGeom = feature.geometry().buffer(bufferLength,2)
      fet.setGeometry(bGeom)
      pr.addFeatures([fet])
    self.bcLayer.commitChanges()
    self.bcLayer.updateExtents()

  def addSynoFeatures(self):
    layer = QgsVectorLayer("Polygon" + "?" + self.URIcrs, "grid_layer", "memory")
    #layer.setCrs(self.crs)
    pr = layer.dataProvider()
    pr.addAttributes([QgsField("ID_MAILLE", QVariant.Int), QgsField("row", QVariant.Int), QgsField("col", QVariant.Int)])
    layer.updateFields()
    # Initial settings
    provider_perimetre = self.cLayer.dataProvider()
    #feat_perimetre = QgsFeature()
    ladderHeight = self.ladderHeight
    ladderWidth = self.ladderWidth
    ladder_id = 0
    yMax = self.extent.yMaximum()
    yMin = yMax - ladderHeight
    widthSum = 0
    heightSum = 0
    row = 0
    # Build columns
    while heightSum < self.extent.height():
      widthSum = 0
      col = 0
      xMin = self.extent.xMinimum()
      xMax = xMin + ladderWidth
      # Build lines
      while widthSum < self.extent.width():
        # Create geometry
        ladder = QgsRectangle(xMin - self.overlapW, yMin - self.overlapH, xMax + self.overlapW, yMax + self.overlapH)
        request=QgsFeatureRequest()
        request.setFilterRect(ladder)
        for f in provider_perimetre.getFeatures(request):
          ladder_id = ladder_id + 1
          # Add ladder to layer
          fet = QgsFeature()
          fet.setAttributes([ladder_id, row, col])
          fet.setGeometry(QgsGeometry.fromRect(ladder))
          pr.addFeatures([fet])
          #ladder_list.append(fet)
        # Settings for next ladder
        xMin = xMin + ladderWidth
        xMax = xMax + ladderWidth
        widthSum = widthSum + ladderWidth
        col = col + 1
      heightSum = heightSum + ladderHeight
      yMin = yMin - ladderHeight
      yMax = yMax - ladderHeight
      row = row + 1
    layer.updateExtents()
    return layer

  def fill_references(self, layer):
    pr = layer.dataProvider()
    pr.addAttributes([QgsField("above", QVariant.Int), QgsField("below", QVariant.Int),
     QgsField("left", QVariant.Int), QgsField("right", QVariant.Int),
     QgsField("aboveleft", QVariant.Int), QgsField("aboveright", QVariant.Int),
     QgsField("belowleft", QVariant.Int), QgsField("belowright", QVariant.Int)])
    layer.updateFields()
    layer.startEditing()
    for feature in layer.getFeatures():
      neighbours = self.get_neighbour_features(feature, layer)
      positions = self.get_related_positions(feature, neighbours)
      for pos, f in positions.items():
        if not feature[pos]:
          feature[pos] = f['ID_MAILLE']
          layer.updateFeature(feature)
    layer.commitChanges()
    
       
  def get_neighbour_features(self, feature, layer):
    dp = layer.dataProvider()
    request = QgsFeatureRequest()
    request.setFilterRect(feature.geometry().buffer(self.ladderWidth / 100.,1).boundingBox())
    r = dp.getFeatures(request)
    return [f for f in r if f['ID_MAILLE'] != feature['ID_MAILLE']]

  def get_related_positions(self, base, neighbours):
    base_centroid = base.geometry().centroid().asPoint()
    positions = {}
    for n in neighbours:
      centroid = n.geometry().centroid().asPoint()
      dx = math.fabs(centroid.x() - base_centroid.x())
      dy = math.fabs(centroid.y() - base_centroid.y())
      horizontal = dx / self.ladderWidth > dy / self.ladderHeight
      
      position = ''
      if horizontal:
        position = 'left' if centroid.x() < base_centroid.x() else 'right'
        if dy > self.ladderHeight * 0.6:
          position = ('above' if centroid.y() > base_centroid.y() else 'below') + position
      else:
        position = 'above' if centroid.y() > base_centroid.y() else 'below'
        if dx > self.ladderWidth * 0.6:
          position = position + ('left' if centroid.x() < base_centroid.x() else 'right')

      if position: 
        #curent position already occupied
        if position in positions:
          curent = positions[position]
          c_centroid = curent.geometry().centroid().asPoint()
          dx2 = math.fabs(base_centroid.x() - c_centroid.x())
          dy2 = math.fabs(base_centroid.y() - c_centroid.y())
          if position is 'above' or position is 'below':
            #our new feature is closer to center of base feature
            if dx2 > dx:
              positions[position] = n
              positions[position + ('right' if c_centroid.x() > base_centroid.x() else 'left')] = curent
            #old feature is close to center of base feature
            else:
              positions[position + ('right' if centroid.x() > base_centroid.x() else 'left')] = n
          elif position is 'left' or position is 'right':
            #our new feature is closer to center of base feature
            if dy2 > dy:
              positions[position] = n
              positions[('above' if c_centroid.y() > base_centroid.y() else 'below') + position] = curent
            #old feature is close to center of base feature
            else:
              positions[('above' if centroid.y() > base_centroid.y() else 'below') + position] = n

        #position is free, just add our feature
        else:
          positions[position] = n

    return positions

  def createPhysLayerFromList(self, shapePath, layer):
    # Wite to file 
    error, error_string = QgsVectorFileWriter.writeAsVectorFormat(layer, shapePath, \
      "CP1250", layer.crs(), "ESRI Shapefile")
    if error != QgsVectorFileWriter.NoError:
      QMessageBox.information(self.iface.mainWindow(),"Info", \
        QCoreApplication.translate("synoptiquesatlas","Error when creating shapefile:\n") + shapePath + QCoreApplication.translate("synoptiquesatlas","\nPlease delete or rename the former grid layers"))

  def intersect(self, perimetre, calepinage):
  # Intersect between coverage and grid
    self.centroid_list = []
    self.splitted_fet_list = []
    i = 0    
    if perimetre and calepinage:
      provider_perimetre = perimetre.dataProvider()
      provider_calepinage = calepinage.dataProvider()
      # create the select statement
      #provider_calepinage.select([],self.extent)
      request=QgsFeatureRequest()
      request.setFilterRect(self.extent)
      # the arguments mean no attributes returned, and do a bbox filter with our buffered
      # rectangle to limit the amount of features
      for feat_perimetre in provider_perimetre.getFeatures():
        # if the feat geom returned from the selection intersects our point then put it in a list
        for feat_calepinage in provider_calepinage.getFeatures(request):
          # if the feat geom returned from the selection intersects our point then put it in a list
          if feat_perimetre.geometry().intersects(feat_calepinage.geometry()):
            a = feat_perimetre.geometry().intersection(feat_calepinage.geometry())
            self.centroid_list.append(a.centroid())
            fet = QgsFeature()
            fet.setGeometry(a)
            #fet.addAttribute(0, QVariant(i))
            self.splitted_fet_list.append(fet)
            i = i + 1

  def createIntersectionLayer(self):
    self.interLayer = QgsVectorLayer("Polygon" + "?" + self.URIcrs, "inter_layer", "memory")
    #self.interLayer.setCrs(self.crs)
    pr = self.interLayer.dataProvider()
    pr.addAttributes([QgsField("ID_INTER", QVariant.Int)])
    # Add features
    for fet in self.splitted_fet_list:
      pr.addFeatures([fet])
    self.interLayer.updateExtents()

  def centroidsToNewSyno(self, ladder_list):
    layer = QgsVectorLayer("Polygon" + "?" + self.URIcrs, "layer", "memory")
    #layer.setCrs(self.crs)
    pr = layer.dataProvider()
    pr.addAttributes([QgsField("ID_MAILLE", QVariant.Int)])
    layer.updateFields()
    ladderHeight = self.ladderHeight
    ladderWidth = self.ladderWidth
    ladder_id = 0
    for centr in self.centroid_list:
      pt = centr.asPoint()
      xMin = pt.x() - ladderWidth/2. - self.overlapW
      xMax = pt.x() + ladderWidth/2. + self.overlapW
      yMin = pt.y() - ladderHeight/2. - self.overlapH
      yMax = pt.y() + ladderHeight/2. + self.overlapH
      # Create geometry
      ladder = QgsRectangle(xMin, yMin, xMax, yMax)
      # Add ladder to layer
      fet = QgsFeature()
      fet.setGeometry(QgsGeometry.fromRect(ladder))
      fet.setAttributes([ladder_id])
      ladder_list.append(fet)
      pr.addFeatures([fet])
      ladder_id = ladder_id + 1
    layer.updateExtents()
    return layer

  def loadQgsVectorLayer(self, shapePath, layerName):
    layerToLoad = QgsVectorLayer(shapePath, layerName, "ogr")
    if not layerToLoad.isValid():
      QMessageBox.information(self.iface.mainWindow(),"Info", \
        QCoreApplication.translate("synoptiquesatlas","Error while loading layer ") + layerName + " !")
    else:
      QgsProject.instance().addMapLayer(layerToLoad)
      return layerToLoad

  def parseSyno(self):
    i = 0
    while i <= len(self.new_ladders_list) - 1:
      fet = self.splitted_fet_list[i]
      overlapped = False
      j = 0
      while j <= i - 1 and not overlapped:
        fet2 = self.new_ladders_list[j]
        # if geom is entirely overlapped by geom2, pop it from list, pop its centroid
        if fet2.geometry().contains(fet.geometry()):
          overlapped = True
        j = j + 1
      j = i + 1
      while j <= len(self.new_ladders_list) - 2 and not overlapped:
        fet2 = self.new_ladders_list[j]
        # if geom is entirely overlapped by geom2, pop it from list, pop its centroid
        if fet2.geometry().contains(fet.geometry()):
          overlapped = True
        j = j + 1
      if overlapped:
        self.splitted_fet_list.pop(i)
        self.new_ladders_list.pop(i)
        self.centroid_list.pop(i)
      else:
        i = i + 1

  def showHelp(self):
    showPluginHelp()

  def showAbout(self):
    """Show Synoptiques Atlas about dialog box"""
    adialog = QDialog()
    adialog.ui = Ui_About_window()
    adialog.ui.setupUi(adialog)
    adialog.show()
    result = adialog.exec_()
    del adialog

  # run method that performs all the real work
  def run(self):
    self.updateBoxes()
    # show the dialog
    self.dlg.show()
    result = self.dlg.exec_()
    # See if OK was pressed
    if result == 1:
      # do something useful (delete the line containing pass and
      # substitute with your code
      pass
