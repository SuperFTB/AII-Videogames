# AII-Videogames
Este es un trabajo para la asignatura AII. El cual consiste en un sistema Web de información hecho en Django y Boostrapt 3 en el que el back-end hace scarping de los productos de las páginas en Steam, GOG.com y El Corte Inglés para hacer una comparativa de precios entre dichas páginas. Para hacer el filtrado de productos se hizo uso de la librería de *full-text seacrh* llamada Whoosh. También se hizo un intento de sistema de recomendación que no funciona del todo bien, pues se ejecutó sobre máquinas de no más de 8GB y se quedaron cortas.

Por otro lado, se usó SQLite para la persistencia, pero da mal rendimiento, pues contiene más de 40 mil productos a fecha de diciembre de 2017.
