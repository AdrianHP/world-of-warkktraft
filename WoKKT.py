import numpy as np
import scipy.optimize as opt 
import time

## PARAMETROS DEL PROBLEMA ##

cubita_super_cubano_mix = .5
cubita_super_colombiano_mix = .5
cubita_deluxe_cubano_mix = .25
cubita_deluxe_colombiano_mix = .75

total_cafe_colombiano = 200
total_cafe_cubano = 300

tiempo_de_produccion_deluxe = 10/9
tiempo_de_produccion_super = 1

total_de_produccion_super = 500

ganancia_super = 9
ganancia_deluxe = 11

## DESCRIPCION DEL PROBLEMA ##

program_description = \
f"""
Una empacadora de café mezcla café colombiano y café cubano 
para ofertar dos tipos de nuevas marcas: Cubita super y Cubita 
deluxe. Cada Kilogramo de Cubita Super contiene {cubita_super_colombiano_mix} Kg. de café 
colombiano y {cubita_super_cubano_mix} Kg. de café cubano, mientras que cada Kg. de 
Cubita deluxe contiene {cubita_deluxe_cubano_mix} kg. 
de café cubano y {cubita_deluxe_colombiano_mix} de café 
colombiano. Se dispone de {total_cafe_colombiano} Kg. de café colombiano 
y {total_cafe_cubano} Kg. de café cubano. La producción de un Kg. 
del café deluxe requiere {tiempo_de_produccion_deluxe} del tiempo 
que requiere el procesamiento de {tiempo_de_produccion_super} Kg. de café super 
en la mezcladora y se  conoce que si sólo se produjera café super 
podrían mezclarse {total_de_produccion_super}Kg. Si la ganancia por Kg. de Cubita super 
es {ganancia_super} centavos y la de Cubita deluxe es {ganancia_deluxe} centavos. Cuántos Kg
de cada marca deben producirse para maximizar la ganancia? 
"""

## MODELO DEL PROBLEMA ##

cafe_c = np.array([
    ganancia_super, 
    ganancia_deluxe,
])

cafe_A_ub = np.array([
    [cubita_super_colombiano_mix, cubita_deluxe_colombiano_mix],
    [cubita_super_cubano_mix, cubita_deluxe_cubano_mix],
    [tiempo_de_produccion_super, tiempo_de_produccion_deluxe],
    [-1,0],
    [0,-1],
])
cafe_b_ub = np.array([
    total_cafe_colombiano,
    total_cafe_cubano,
    total_de_produccion_super,
    0,
    0,
])
cafe_A_ub_meaning = [
    "No tienes suficiente café colombiano para producir lo pactado",
    "No tienes suficiente café cubano para producir lo pactado",
    "No te alcanza el tiempo para producir lo pactado",
    "No puedes hacer cantidades negativas de café super",
    "No puedes hacer cantidades negativas de café deluxe",
]

cafe_A_eq = None

cafe_b_eq = None

cafe_A_eq_meaning = None

## UTILES DE OPTIMIZACION ##

solution_meaning = {
    0 : "Optimization proceeding nominally.",
    1 : "Iteration limit reached.",
    2 : "Problem appears to be infeasible.",
    3 : "Problem appears to be unbounded.",
    4 : "Numerical difficulties encountered.",
}

def solve_linear_problem(maximizar, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None):
    if maximizar:
        c = -c.copy()
    sol = opt.linprog(c, A_ub, b_ub, A_eq, b_eq)
    if maximizar:
        sol.fun = -sol.fun
    return sol

def get_infringed_rules(sol, A_ub=None, b_ub=None, A_eq=None, b_eq=None, A_ub_meaning=None, A_eq_meaning=None):
    infringed_rules = { "ub" : [], "eq" : []}

    # Determina las condiciones de desigualdad infringidas
    if A_ub is not None and A_ub.any() and b_ub is not None and b_ub.any():
        mul = A_ub @ sol <= b_ub
        infringed_rules["ub"] = [i + 1 for i in range(len(mul)) if not mul[i]]
    # Determina las condiciones de igualdad infringidas
    if A_eq is not None and A_eq.any() and b_eq is not None and b_eq.any():
        mul = A_eq @ sol == b_eq
        infringed_rules["eq"] = [i + 1 for i in range(len(mul)) if not mul[i]]
    if A_ub_meaning:
        infringed_rules["ub"] = [A_ub_meaning[i-1] for i in infringed_rules["ub"]]
    if A_eq_meaning:
        infringed_rules["eq"] = [A_eq_meaning[i-1] for i in infringed_rules["eq"]]
    return infringed_rules

# Solucion al problema
cafe_solution = solve_linear_problem(True, cafe_c, cafe_A_ub, cafe_b_ub, cafe_A_eq, cafe_b_eq)

## UTILES DE CONSOLA ##

def show_spinner():
    n = 5
    while n>0:
        for i in '|\\-/':
            print('\b' + i, end="")
            time.sleep(.1)
        n -= 1  

def get_number_console(placeholder):
    while True:
        try:
            value = float(input(placeholder))
            return value
        except Exception as e:
            print(e)

def show_cafe_solution_report(cafe_super, cafe_deluxe):
    user_solution = np.array([cafe_super, cafe_deluxe])
    
    true_cafe_super, true_cafe_deluxe = cafe_solution.x
    ganancia_max = cafe_solution.fun
    ganancia_hecha = cafe_c @ user_solution
    feasible_original_problem = cafe_solution.success
    infringed_rules = get_infringed_rules(user_solution, cafe_A_ub, cafe_b_ub, cafe_A_eq, cafe_b_eq, cafe_A_ub_meaning, cafe_A_eq_meaning)
    feasible_user_solution = len(infringed_rules["eq"]) + len(infringed_rules["ub"]) == 0
    feasible_answer = True

    if feasible_user_solution:
        print("La ganancia recibida fue",ganancia_hecha)
        print("Solución dada de café super:" ,cafe_super)
        print("Solución dada de café deluxe:",cafe_deluxe)
    else:
        errores = infringed_rules["ub"] + infringed_rules["eq"]
        if len(errores) > 0:
            print("La solución no es válida debido a:\n" + "\t\n".join([str(x) for x in errores]))
        print()
        feasible_answer = False
    
    if feasible_answer:
        if ganancia_max>ganancia_hecha*4:
            print('Tu solución es bastante mala con respecto a la ganancia máxima posible, es menos que la cuarta parte.La ganancia máxima era de',ganancia_max)
        elif ganancia_max>ganancia_hecha*2:
            print('Tu solución es mala con respecto a la gancia máxima posible,es menos de la mitad.La ganancia máxima era de',ganancia_max)
       
        elif ganancia_max<ganancia_hecha*1.5:
            print('Tu solución es bastante buena, la ganancia máxima era de',ganancia_max)
        elif ganancia_max<ganancia_hecha+5:
            print('Tu solución es óptima')
    else:
        if feasible_original_problem:

            print("La ganancia máxima es",ganancia_max)
            print("Solución esperada de café super:" ,true_cafe_super)
            print("Solución esperada de café deluxe:",true_cafe_deluxe)
        else:
            print("El problema original no pudo ser resuelto debido a", solution_meaning[cafe_solution.status])    
        print()
   

def run():
    
    print("Bienvenidos a la Fábrica de Café .")
    
    print(f"Como nuevo jefe de operaciones de la fábrica de café se le asigna la siguiente tarea:")
    print()
    print(program_description)
    print()
    print("Entonces, cuánto, según tu basta experiencia en manejo del café, hace falta")
    print("producir por cada tipo de café para lograr un buen resultado?")
    print()
    
    cafe_super = get_number_console("Cuánto mandarías a hacer de café super: ")
    cafe_deluxe = get_number_console("Cuánto mandarías a hacer de café deluxe: ")
    
    print()
    print("Y sus hombres empezaron el día con las instrucciones de hacer")
    print(f"{cafe_super} Kg de café super y {cafe_deluxe} Kg de café deluxe")
    
    print()
    # show_spinner()
    print()
    
    show_cafe_solution_report(cafe_super, cafe_deluxe)
    
if __name__ == "__main__":
    run()