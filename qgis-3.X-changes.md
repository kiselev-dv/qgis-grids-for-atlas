* Access print layout maps `layoutMaps = [m for m in project.layoutManager().printLayouts()[0].items() if isinstance(m, QgsLayoutItemMap)]`

* Extent of the map `layoutMaps[0].extent()`
