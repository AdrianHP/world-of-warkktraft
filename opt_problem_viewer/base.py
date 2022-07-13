from typing import *

class Variable:
    
    def __init__(self, 
                 nombre: str, 
                 valor: float = 0,
                 mensaje_si_falta: Optional[str] = None, 
                 mensaje_si_sobra: Optional[str] = None, 
                 mensaje_si_optimo: str = "Ok"):
        self.nombre = nombre
        self.valor = valor
        self.mensaje_si_falta = mensaje_si_falta if not None else f"Aumente el valor de {self.nombre}"
        self.mensaje_si_sobra = mensaje_si_sobra if not None else f"Disminuya el valor de {self.nombre}"
        self.mensaje_si_optimo = mensaje_si_optimo
        
    def __str__(self) -> str:
        return f"{self.nombre} = {self.valor}"

class Problema:
    
    def __init__(self, orientacion: str, evaluador: Callable[[List[Variable]], float], solucionador: Callable[[], Tuple[float,List[Variable]]]) -> None:
        self.orientacion = orientacion
        self.solucionador = solucionador
        self.evaluador = evaluador
    
    def solucionar(self) -> Tuple[float, List[Variable]]:
        """
        Soluciona el problema propuesto mostrando la orientacion del mismo. 
        En caso de no tener solucion el problema lanza una Exception.
        
        Devuelve el óptimo y la lista de Variables del `self.solucionador`
        """
        
        print(self.orientacion)
        
        try:
            opt, result = self.solucionador()
        except Exception as e:
            raise e
        
        print("Óptimo encontrado")
        print(opt)
        print()
        print("Valor de las variables para el óptimo hallado")
        for var in result:
            print(var)
        
        return opt, result
    
    def _comparar_asignaciones(self, asignaciones_opt_list: List[Variable], asignaciones_usuario_list: List[Variable]):
        asignaciones_opt = { x.nombre:x for x in asignaciones_opt_list }
        asignaciones_usuario = { y.nombre:y for y in asignaciones_usuario_list }

        print("Comparación del vector solución dado con el vector solución óptimo")
        for var_name in asignaciones_opt:
            opt_var = asignaciones_opt[var_name]
            opt_value = opt_var.valor
            user_var = asignaciones_usuario[var_name]
            user_value = user_var.valor
            diff = opt_value - user_value
            suggestion: Optional[str] = ""
            if abs(diff) <= 0.00001:
                suggestion = user_var.mensaje_si_optimo
            elif diff > 0:
                suggestion = user_var.mensaje_si_sobra
            else:
                suggestion = user_var.mensaje_si_falta


            print(f"{var_name}:")
            print("Óptimo:", opt_value, "Dado:", user_value)
            print("Diferencia:", diff, "Sugerencia:", suggestion)
            print()
        print()
            

    def _comparar_optimos(self, optimo: float, args_evaluacion: float):
        
        optimal_proportion = args_evaluacion/optimo

        print('El valor alcanzado con su asiganción es de', args_evaluacion)
        print('El valor óptimo del problema es', optimo)
        print(f"Su solución es {optimal_proportion*100:0.2f}% óptima, por lo que")

        if optimo < 0 or args_evaluacion < 0:
            print("ALERTA: El análisis entre óptimos está pensado para valores no negativos")
            return

        if optimal_proportion < 0.25:
            print('su solución es bastante mala con respecto al valor óptimo, es menos que la cuarta parte.')
        elif optimal_proportion < 0.5:
            print('su solución es mala con respecto al valor óptimo, es menos de la mitad.')
        elif optimal_proportion < 0.75:
            print('su solución es moderadamente mala con respecto al valor óptimo, es menos de 3/4 del óptimo')
        elif optimal_proportion < 0.90:
            print('su solución es aceptable, aunque se puede mejorar.')
        elif optimal_proportion < 0.95:
            print('su solución es buena, pero le falta un poco aún')
        elif optimal_proportion < 0.99:
            print('su solución es casi óptima')
        else:
            print('su solución es óptima')
            
    def evaluar(self, argumentos: List[Variable]) -> float:
        """
        Evalua la solución dada en los `argumentos` dando feedback sobre cómo mejorar
        """
        
        opt_val, opt_vector = self.solucionador()
        
        resultado = self.evaluador(argumentos)
        
        self._comparar_optimos(opt_val, resultado)
        
        self._comparar_asignaciones(opt_vector, argumentos)
        
        return resultado
        
        