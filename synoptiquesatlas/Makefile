#/***************************************************************************
# SynoptiquesAtlas
# 
# Creation de synoptiques grille ou dynamique pour utiliser dans un atlas
#                             -------------------
#        begin                : 2012-02-22
#        copyright            : (C) 2012 by Experts SIG / Biotope
#        email                : dev-qgis@biotope.fr
# ***************************************************************************/
# 
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

# Makefile for a PyQGIS plugin 
# CONFIGURATION
PLUGIN_UPLOAD = $(CURDIR)/plugin_upload.py

# translation
I18N = i18n
SOURCES = synoptiquesatlas.py synoptiquesatlasdialog.py __init__.py ui_synoptiquesatlas.py ui_help_window.py ui_about_window.py 
TRANSLATIONS = $(I18N)/synoptiquesatlas_fr.ts

# global
PLUGINNAME = synoptiquesatlas

PY_FILES = synoptiquesatlas.py synoptiquesatlasdialog.py __init__.py

EXTRAS = icon.png about.png metadata.txt

UI_FILES = ui_synoptiquesatlas.py ui_help_window.py ui_about_window.py

RESOURCE_FILES = resources_rc.py

DOCUMENTATION = help


default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

%_rc.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<

# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at:
# $HOME/.qgis/python/plugins
deploy: compile transcompile
	mkdir -p $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(UI_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(RESOURCE_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vfr $(DOCUMENTATION) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vfr $(I18N) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)

# The dclean target removes compiled python files from plugin directory
# also delets any .svn entry
dclean:
	find $(HOME)/.qgis/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/.qgis/python/plugins/$(PLUGINNAME) -iname ".svn" -prune -exec rm -Rf {} \;

# The zip target deploys the plugin and creates a zip file with the deployed
# content. You can then upload the zip file on http://plugins.qgis.org
zip: deploy dclean 
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/.qgis/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)

# Create a zip package of the plugin named $(PLUGINNAME).zip. 
# This requires use of git (your plugin development directory must be a 
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=Version_0.3.2
package: compile
		rm -f $(PLUGINNAME).zip
		git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
		echo "Created package: $(PLUGINNAME).zip"

upload: zip
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

# transup
# update .ts translation files
transup:
	pylupdate4 Makefile

# transcompile
# compile translation files into .qm binary format
transcompile:
	lrelease $(I18N)/*.ts

# transclean
# deletes all .qm files
transclean:
	rm -f $(I18N)/*.qm
