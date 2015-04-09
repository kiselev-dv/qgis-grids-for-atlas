qgis-grids-for-atlas
====================

Plugin for QGIS, which generates rectangles with extent of selected print layout which covers selected layer's features. So yo could create print layout for atlas page, then generate rectangles for pages.

Fork of GridsForAtlas QGIS plugin originally created by Experts SIG / Biotope

New features:
* Settings to generated overlapped atlas pages tiles
* References between tiles. (Properties with top, bottom, left, right... page numbers)

Known Bugs:
----------

* Project (and print layout extent) should be in one coordinate system.


Плагин к QGIS, генерирует прямоугольники по размеру участка карты из макета страницы, для всех объектов выбранного слоя. Достаточно создать макет одной страницы атласа, слой с покрытием, после чего можно сгенерировать прямоугольники которые будут соответсвовать будущим страницам атласа. 

Форк плагина  GridsForAtlas. Оригинальный плагин был создан Experts SIG / Biotope

Добавлены:
* Возможность указать процент перекрытия для генерируемых прямоугольников.
* В свойства прямоугольников добавлены ссылки на соседние (выше, ниже, правая, левая и т.д.) страницы.

Известные ошибки:
-----------------

* Проекция проекта, а точнее проекция в которой заданы границы печаемой области в макете страницы и проекция слоя покрытия должны совпадать. Вы можете изменить проекцию после генерации областей печати.
