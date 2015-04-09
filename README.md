qgis-grids-for-atlas
====================

Fork of GridsForAtlas QGIS plugin originally created by Experts SIG / Biotope

New features:
* Settings to generated overlapped atlas pages tiles
* References between tiles. (Properties with top, bottom, left, right... page numbers)

Known Bugs:
----------

* Project (and print layout extent) should be in one coordinate system.
 

qgis-grids-for-atlas (RU)
====================

Форк плагина  GridsForAtlas. Оригинальный плагин был создан Experts SIG / Biotope

Добавлены:
* Возможность указать процент перекрытия для генерируемых прямоугольников.
* В свойства прямоугольников добавлены ссылки на соседние (выше, ниже, правая, левая и т.д.) страницы.

Известные ошибки:
-----------------

* Проекция проекта, а точнее проекция в которой заданы границы печаемой области в макете страницы и проекция слоя покрытия должны совпадать. Вы можете изменить проекцию после генерации областей печати.
