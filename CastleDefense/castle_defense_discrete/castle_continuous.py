# Siempre se tiene:
# - Recursos -> Usados generalmente para la construccion de la muralla
# - Trabajadores -> Usados generalmente para la construcion de la muralla
# - Ataques -> Cantidad de daño predefinido en cada día a la muralla

# Continuo
# - Trabajadores: Contruyen/Reparan la muralla en un cierto periodo de tiempo
# - Recursos: Son necesarios X recursos por unidad de muralla por cada uno
# - Variable: Tiempo asigando a los trabajadores para las diferentes tareas

# Nivel básico básico
# Sobrevivir un dia
# Una oleada, el problema seria como organizar los recursos y la fuerza
# de trabajo para poder resistir.

# Nivel básico
# Tengo una muralla que tengo que defender por una cierta cantidad de dias
# El nivel de la muralla siempre tiene que estar positivo
# Los enemigos atacan la muralla una cantidad predefinida

from typing import List
from gekko import GEKKO
import numpy as np
from castle import Recurso


class Tarea:
    def __init__(self, nombre: str, recursos: List[Recurso]) -> None:
        self.nombre = nombre
        self.recursos = recursos


modelo = GEKKO(remote=False)
modelo.options.SOLVER = 1  # APOPT is an MINLP solver
modelo.options.LINEAR = 1 # Is a MILP

trabajadores = 4
maximo_tiempo_asignado_por_trabajador_por_dia = 10

recursos_iniciales = np.array([
    Recurso("Recurso 1", 100), 
    Recurso("Recurso 2", 100)
])
nivel_inicial_de_muralla = 100

reparacion_muralla_por_unidad_de_tiempo = 10

tareas = [
    Tarea("Construir Muralla", [
        Recurso("Recurso 1", -10), 
        Recurso("Recurso 2", -10)
    ])
]

ataques_enemigos = np.array([100, 100])
duracion_de_ataques_en_dias = len(ataques_enemigos)


# Crear variables de tarea->dia->trabajador
tiempo_asignado_trabajadores_variable = {}
for tarea_k in tareas:
    for dia_i in range(duracion_de_ataques_en_dias):
        for trabajador_j in range(trabajadores):
            tiempo_asignado_trabajadores_variable[tarea_k.nombre, dia_i, trabajador_j] = \
                modelo.Var( # Tiempo asignado al trabajador j el día i en la tarea k 
                    lb=0, # No se puede tener una cantidad negativa de tiempo asignado
                    name=f"{tarea_k.nombre}->Dia {dia_i}->Trabajador {trabajador_j}")

# Crear variables de control sobre la muralla
cantidad_de_muralla_disponible = {}
for dia_i in range(duracion_de_ataques_en_dias):
    cantidad_de_muralla_disponible[dia_i] = modelo.Var( # Muralla el dia i
        # El primer día el valor es prefijado con la muralla inicial
        value=nivel_inicial_de_muralla if dia_i == 0 else None, # TODO Verificar si esto es que se mantiene constante
        lb=0, # No se puede tener una cantidad negativa de muralla
        name=f"Cantidad Muralla->Dia {dia_i}")
    
# Crear variables de recurso por día
cantidad_de_recursos_disponibles = {}
for recurso_l in recursos_iniciales:
    for dia_i in range(duracion_de_ataques_en_dias):
        cantidad_de_recursos_disponibles[recurso_l.nombre, dia_i] = modelo.Var(
            # El primer día el valor es prefijado con los recursos iniciales
            value=recurso_l.cantidad if dia_i == 0 else None,
            lb=0, # No se puede tener una cantidad negativa de recursos
            name=f"Recurso {recurso_l.nombre}->Dia {dia_i}"
        )

# Restricciones


# El tiempo asignado a los trabajadores tiene que ser menor o igual al tiempo máximo por día
for trabajador_j in range(trabajadores):
    for dia_i in range(duracion_de_ataques_en_dias):
        # Seleccionando las variables que representan las tareas del trabajador j en el día i
        tarea_dia_i_trabajador_j = np.array([
            variable 
            for (_, _dia_i, _trabajador_j),variable in tiempo_asignado_trabajadores_variable.items()
            if trabajador_j == _trabajador_j and dia_i == _dia_i
        ])
        modelo.Equation(modelo.sum(tarea_dia_i_trabajador_j) <= maximo_tiempo_asignado_por_trabajador_por_dia)


# Los recursos se tienen que asignar según lo que se gastó el día anterior

for dia_i in range(duracion_de_ataques_en_dias-1):
    for tarea_m in tareas:
        for trabajador_j in range(trabajadores):
            for recurso_l in recursos_iniciales:
                modelo.Equation(
                    modelo.sum(
                        x 
                        for (_tarea_m, _dia_i, _trabajador_j),y in tiempo_asignado_trabajadores_variable.items()
                    )
                )

# La cantidad de muralla se tiene que asignar segun lo que se desrtuyó/construyó el día anterior

# TODO


# Funcion objetivo
# Como tal en este problema lo que se quiere es que sea satisfacible, 
# pero si se le ponen requisitos extras la funcion objetivo seria relevante

# TODO


# Resolver el problema y sacar conclusiones

# TODO


# Otros
# - Ver otras posibles tareas, como por ejemplo reunir recursos
# - Hacer una API para este tipo de problemas, de ser posible lo más similar posible a l aya existente
# - Crear unos niveles que vayan aumentando la dificultad todos basados en esta API estilo CP
