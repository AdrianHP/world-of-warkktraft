from typing import List, Optional, Tuple, Callable
from .base import Problema, Variable
from gekko import GEKKO

class GEKKOVariable(Variable):
    
    def __init__(self, 
                 gekko_var: GEKKO.Var,
                 mensaje_si_falta: Optional[str] = None, 
                 mensaje_si_sobra: Optional[str] = None, 
                 mensaje_si_optimo: str = "Ok"):
        super().__init__(nombre = "", valor=0, mensaje_si_falta=mensaje_si_falta, mensaje_si_sobra=mensaje_si_sobra, mensaje_si_optimo=mensaje_si_optimo)
        self.gekko_var = gekko_var
    
    def get_nombre(self):
        return self.gekko_var.name
    
    def set_nombre(self, val):
        return

    nombre = property(get_nombre, set_nombre)
    
    def get_valor(self) -> float:
        return self.gekko_var.value.value[0]
    
    def set_valor(self, val):
        return

    valor = property(get_valor, set_valor)
    

class GEKKOProblema(Problema):
    
    def __init__(self, orientacion: str, crear_modelo: Callable[[], Tuple[GEKKO, List[GEKKOVariable]]]) -> None:
        super().__init__(orientacion, lambda x: self._eval(x), lambda: self._solve())
        self.crear_modelo = crear_modelo
    
    def _solve(self):
        modelo, variables = self.crear_modelo()
        modelo.solve(disp=False)
        return modelo.options.OBJFCNVAL, variables
    
    def _eval(self, valores: List[Variable]) -> float:
        modelo, variables = self.crear_modelo()
        for x in valores:
            for y in [v for v in variables if v.nombre == x.nombre]:
                modelo.Equation(y.gekko_var == x.valor)
        modelo.solve(disp=False)
        return modelo.options.OBJFCNVAL