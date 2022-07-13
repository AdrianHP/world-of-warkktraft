# opt_problem_viewer

Módulo simple para la visualización de resultados obtenidos de modelos de optimización.

## Características

- Da una mejor retroalimentación de los resultados del problema.
- Compara diferentes propuestas de solciones contra el óptimo encontrado del problema
- Extensible para cualquier solucionador de problemas de optimización

## ¿Cómo extender?

El módulo base tiene las clases y el flujo básico pensado para el funcionamiento del programa. Primero debe de extender la clase **Problema** de dicho módulo y proveer de las funciones que toma en el contructor. Si es necesario puede extender la clase **Variable** de acuerdo a sus necesidades.

### Ejemplo

En el módulo *gekko_implementation.py* se observa una implementación de dicho sistema con el solucionados de problemas de optimización **GEKKO**. En *gekko_example.py* se puede encontrar un ejemplo de problema resuelto.
