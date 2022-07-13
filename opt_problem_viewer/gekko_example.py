from typing import List, Optional, Tuple, Callable
from .gekko_implementation import GEKKOProblema, GEKKOVariable
from gekko import GEKKO

def construir_problema() -> GEKKOProblema:
    def modelo_variable_construir():
        # Datos
        total_ppl = 60000
        proteinas = 60 * total_ppl
        carbohidratos = 120 * total_ppl
        aceite = 20 * total_ppl
        agua = 1.5 * total_ppl

        totals = [proteinas, carbohidratos, aceite]

        nutrientes_costo = [
            [10, 40, 20, 10],
            [100, 10, 50, 60],
            [20, 30, 10, 30],
            [0, 0, 0, 5]
        ]

        modelo = GEKKO(remote=False)
        modelo.options.SOLVER = 1
        modelo.options.LINEAR = 1

        # Variables de decisión
        _trigo = modelo.Var(lb=0, integer=True, name='trigo')
        _ganado = modelo.Var(lb=0, integer=True, name='ganado')
        _encurtidos = modelo.Var(lb=0, integer=True, name='encurtidos')
        _agua = modelo.Var(lb=0, integer=True, name='agua')

        e_vars = [_trigo, _ganado, _encurtidos, _agua]

        # Restricciones de demanda
        eq = 0
        for i in range(3):
            for j in range(3):
                eq += e_vars[j] * nutrientes_costo[j][i]

            modelo.Equation(eq >= totals[i])
            eq = 0

        modelo.Equation(_agua >= agua)

        def f(x, y, z, w):
            return x * nutrientes_costo[0][3] + y * nutrientes_costo[1][3] + z * nutrientes_costo[2][3] + w * nutrientes_costo[3][3]

        # Función objetivo
        modelo.Minimize(f(_trigo, _ganado, _encurtidos, _agua))
        
        return modelo, [GEKKOVariable(x) for x in [_trigo, _ganado, _encurtidos, _agua]]
    return GEKKOProblema("Problema Greyjoy de Clase Práctica", modelo_variable_construir)

prob = construir_problema()

opt, vector_opt = prob.solucionar()
opt2 = prob.evaluar(vector_opt)
