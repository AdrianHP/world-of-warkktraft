import numpy as np
import scipy.optimize._linprog as lin

# Función de costo
# Multiplicada por -1 para que scipy maximice
c = np.array([
    0.02, # Alcohol por litro de cerveza
    0.04 # Alcohol por litro de vino
]) * -1

# Restricciones de desigualdad
Ab = np.array([
    [ 0, 2], # Uva
    [ 1, 0], # Cebada
    [ 0.5, 1], # Levadura
    [-1,   0], # Bound inferior de cantidad de cerveza
    [ 0,  -1], # Bound inferior de cantidad de vino
])

b = np.array([
    30, # Cantidad de uva
    40, # Cantidad de cebada
    30, # Cantidad de levadura
    0, # Bound inferior de cantidad de cerveza
    0, # Bound inferior de cantidad de vino
])

print(lin.linprog(c, Ab, b)) # El resultado se multiplica por -1.