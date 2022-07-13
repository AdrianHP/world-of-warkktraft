# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Clase Práctica
# 
# ## Juego de Tronos
# 
# %% [markdown]
# ## Problema de ejemplo
# 
# Tyrion Lannister se está quedando sin bebidas alcohólicas, entonces haciendo alusión a su célebre frase, “Eso se lo que hago, bebo y sé cosas” quiere hacer su propia bebida. Para esto cuenta con 30 libras de uvas, 40 libras de cebada y con 30 libras de levadura. Él conoce que para crear un litro de cerveza necesita 1 libra de cebada y 0.5 libras de levadura, mientras que para crear vino los requisitos son 2 libras de uva y 1 libra de levadura. Conociendo que la cerveza tiene un nivel de alcohol de 2% y el vino 4%, ¿cuál es la mejor manera de distribuir los recursos para crear la mayor cantidad de alcohol?
# 
# Resutados:
# - Cerveza: 30
# - Uva: 15
# - Máxima cantidad de alcohol: 1.2

# %%
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

# %% [markdown]
# ## Infratructura
# 
# La comparación se basa en la premisa de que los valores óptimos de las variables y el óptimo de las funciones de los problemas están restringidos en los positivos. 

# %%
# Install a conda package in the current Jupyter kernel
import sys
# !conda install --yes --prefix {sys.prefix} numpy

from typing import Callable, List, Optional, Tuple
from gekko import GEKKO
import numpy as np
import gekko


def unfold_list(obj):
    try:
        if isinstance(obj, gekko.gk_variable.GKVariable):
            raise TypeError
        if isinstance(obj, tuple):
            yield from obj
        else:
            for x in obj:
                yield from unfold_list(x)
    except TypeError:
        yield obj

def asignar_puntuacion(opt1, opt2, func_eval1, func_eval2, opt, maxim=False, verbose=True):
    punto_probl_eq1 = 0
    punto_probl_eq2 = 0

    if opt1 is None and opt2 is not None:
        print("La solución dada por el equipo 1 no es factible")
        print(f"La solución dada por el equipo 2 es factible: {opt2}")
        print(f"El equipo 2 gana 1 punto!!")
        punto_probl_eq2 += 1
    elif opt1 is not None and opt2 is None:
        print(f"La solución dada por el equipo 1 es factible: {opt1}")
        print("La solución dada por el equipo 2 no es factible")
        print(f"El equipo 1 gana 1 punto!!")
        punto_probl_eq1 += 1
    elif opt1 is None and opt2 is None:
        print(f"Ambos equipos dieron soluciones no factibles")
        dif1 = abs(func_eval1 - opt)
        dif2 = abs(func_eval2 - opt)
        print("La diferencia entre el óptimo y la evaluación del equipo 1 fue", dif1)
        print("La diferencia entre el óptimo y la evaluación del equipo 2 fue", dif2)
        if dif1 == dif2:
            print(f"Los equipos no ganan puntos :(")
        elif dif1 < dif2:
            print("El equipo 1 se acerca más al óptimo, gana 0.5 puntos!")
            punto_probl_eq1 += 0.5
        else:
            print("El equipo 2 se acerca más al óptimo, gana 0.5 puntos!")
            punto_probl_eq2 += 0.5

    elif opt1 == opt2:
        print(f"Ambos equipos dieron soluciones factibles e iguales: {opt1}")
        print(f"Los equipos 1 y 2 ganan 1 punto cada uno!!")
        punto_probl_eq2 += 1
        punto_probl_eq1 += 1
    elif maxim:
        if opt1 > opt2: # Maximizando
            print(f"El equipo 1 obtuvo mejor resultado maximizando que el equipo 2: {opt1} > {opt2}")
            print(f"El equipo 1 gana 1 punto!!")
            punto_probl_eq1 += 1
        else:
            print(f"El equipo 2 obtuvo mejor resultado maximizando que el equipo 1: {opt1} < {opt2}")
            print(f"El equipo 2 gana 1 punto!!")
            punto_probl_eq2 += 1
    else:
        if opt1 < opt2: # Minimizando
            print(f"El equipo 1 obtuvo mejor resultado minimizando que el equipo 2: {opt1} < {opt2}")
            print(f"El equipo 1 gana 1 punto!!")
            punto_probl_eq1 += 1
        else:
            print(f"El equipo 2 obtuvo mejor resultado minimizando que el equipo 1: {opt1} > {opt2}")
            print(f"El equipo 2 gana 1 punto!!")
            punto_probl_eq2 += 1
            
    return punto_probl_eq1, punto_probl_eq2

def comparar_problemas(problema, arg_eq1, arg_eq2, maxim=False, unfold=False):
    print("Equipo 1:")
    print()
    probl_eq1_opt, _, opt_probl, vector_opt_probl, user_eval1 = problema.compare(arg_eq1, unfold=unfold)
    print()

    print("Equipo 2:")
    print()
    probl_eq2_opt, _, _, _, user_eval2 = problema.compare(arg_eq2, unfold=unfold)
    print()

    #Puntuacion de los equipos en el ejercicio 1
    punto_probl_eq1, punto_probl_eq2 = asignar_puntuacion(probl_eq1_opt, probl_eq2_opt, user_eval1, user_eval2, opt_probl, maxim=maxim)
    
    return probl_eq1_opt, probl_eq2_opt, opt_probl, vector_opt_probl, punto_probl_eq1, punto_probl_eq2

class ProblemManager:
    def __init__(self, solver:Callable[[Optional[float],], float], args_fetcher:Callable[[], Tuple[float,]]) -> None:
        self.solver = solver
        self.args_fetcher = args_fetcher

    def solve(self, *args):
        max = self.solver(*args)
        return max

    def compare_assigantions(self, opt_assignations, user_assignations):
        opt_assignations = {x.name:x.value.value[0] for x in opt_assignations}
        user_assignations = {x:y for x,y in zip(opt_assignations,user_assignations)}
        abs_diff = 0

        print("Comparación del vector solución dado con el vector solución óptimo")
        for var_name in opt_assignations:
            opt_value = opt_assignations[var_name]
            user_value = user_assignations[var_name]
            diff = opt_value - user_value
            suggestion = ""
            if abs(diff) <= 0.00001:
                suggestion = "Todo bien :)"
            elif diff > 0:
                suggestion = f"Aumentar el valor de {var_name}"
            else:
                suggestion = f"Disminuir el valor de {var_name}"
            abs_diff += abs(diff)

            print(f"{var_name}:")
            print("Óptimo:", opt_value, "Dado:", user_value)
            print("Diferencia:", diff, "Sugerencia:", suggestion)
        print()
        print("Diferencia absoluta entre las asiganciones y el vector óptimo:", abs_diff)
        print()

    def compare(self, user_args=None, unfold=False):
        if unfold:
            opt, vector_variables, _ = self.solve(None, *user_args[1:])
        else:
            opt, vector_variables, _ = self.solve()

        if opt is None:
            raise Exception("El problema original no tiene solución")

        vector_variables = [x for x in unfold_list(vector_variables)]

        print("Asignación óptima:")
        for v in vector_variables:
            print(v.name, ":", v.value)
        
        if user_args is None:
            user_args = self.args_fetcher()

        user_args = [x for x in unfold_list(user_args if not unfold else user_args[0])]

        self.compare_assigantions(vector_variables, user_args)

        user_opt, _, user_eval = self.solve(user_args)
        
        optimal_proportion = user_eval/opt

        print('El valor alcanzado con su asiganción es de', user_eval)
        print('El valor óptimo del problema es', opt)
        
        if user_opt is None:
            print('Su solución no es factible!!!!')
        else:
            print(f"Su solución es {optimal_proportion*100:0.2f}% óptima, por lo que")

            if optimal_proportion < 0 - 0.00000001:
                raise Exception("La naturaleza de los problemas dados no admite óptimos negativos")

            if optimal_proportion < 0.25:
                print('Su solución es bastante mala con respecto al valor óptimo, es menos que la cuarta parte.')
            elif optimal_proportion < 0.5:
                print('Su solución es mala con respecto al valor óptimo, es menos de la mitad.')
            elif optimal_proportion < 0.75:
                print('Su solución es moderadamente mala con respecto al valor óptimo, es menos de 3/4 del óptimo')
            elif optimal_proportion < 0.90:
                print('Su solución es aceptable, aunque se puede mejorar.')
            elif optimal_proportion < 0.95:
                print('Su solución es buena, pero le falta un poco aún')
            elif optimal_proportion < 0.99:
                print('Su solución es casi óptima')
            elif optimal_proportion <= 1 + .0000001:
                print('Su solución es óptima')

        user_args = [x for x in unfold_list(user_args)]
        
        return user_opt, user_args, opt, vector_variables, user_eval


class ClassManager:

    def __init__(self) -> None:
        self.exercise_points = {}

    def register_result(self, exercise_name, problem_manager, args1, args2, **kwargs):
        probl_eq1_opt, probl_eq2_opt, opt_probl, vector_opt_probl, punto_probl_eq1, punto_probl_eq2 =     comparar_problemas(problem_manager, args1, args2, **kwargs)
        self.exercise_points[exercise_name] = (punto_probl_eq1, punto_probl_eq2)

    def print_result(self):
        equipo1 = [x for (x,_) in self.exercise_points.values()]
        equipo2 = [y for (_,y) in self.exercise_points.values()]

        print("Puntos equipo 1:", equipo1)

        print("Puntos equipo 2:", equipo2)

        ganador = "1" if equipo1 > equipo2 else "2" if equipo1 < equipo2 else "1 y 2"

        print("Felicidades equipo", ganador, "por participar y ganar en la lucha contra los caminantes blancos")

class_manager = ClassManager()

# %% [markdown]
# # Problemas
# 
# Luego de dar solución al modelo del problema, rellenar las secciones de los argumentos con los valores dados por los estudiantes a las variables de decisión. Al final se dará a conocer el resultado final dada la cantidad de puntos.
# 
# %% [markdown]
# ## 1. Casa Mormont
# 
# En la preparación de la batalla se necesitan armas para que los guerreros puedan defenderse del ejército de caminantes blancos. Para esto se tienen escasos recursos, así que hay que usarlos sabiamente. Entre las reservas y el trabajo se logró reunir:
# 
# - 600000 unidades de hierro
# - 400000 unidades de madera
# - 800000 unidades de cuero
# 
# Los herreros y artesanos nos brindan una tabla que muestra la cantidad de materia prima necesaria para construir cada arma y el daño que reporta cada una.
# 
# | Arma      | Hierro | Madera | Cuero | Daño |
# | --------- | ------ | ------ | ----- | ---- |
# | Espada    | 10     | 2      | 4     | 15   |
# | Arco      | 2      | 10     | 5     | 10   |
# | Catapulta | 30     | 100    | 50    | 80   |
# 
# 1. Ayude a darle el mejor uso a estos recursos, diciéndoles a los jefes de la casa la cantidad de espadas, arcos y catapultas que necesitan construir para maximizar el daño que realizan.
# 2. Se quiere tener modelo que generalice el problema anterior en términos de la cantidad de tipos de materiales y cantidad de tipos de armas. Proponga un modelo que haga esta generalización.

# %%
# Ejercicio 1

def mormont_house_solve(armas=None):
    
    if not armas:
        swords=None; bows=None; catapults=None
    else:
        swords, bows, catapults = armas
    
    #1 Mormont House
    #resourses
    iron = 600000
    wood = 400000
    leather = 800000
    
    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP
    
    test = True if  swords is not None and bows is not None and catapults is not None else False
    
    #variables
    sword = modelo.Var (lb = 0, integer = True ,name='sword' )
    bow = modelo.Var (lb = 0, integer = True ,name='bow')
    catapult = modelo.Var (lb = 0, integer = True ,name='catapult')

    #restricciones 
    modelo.Equation(10*sword + 2*bow + 80*catapult <= iron)
    modelo.Equation(2*sword + 10*bow + 100*catapult <= wood)
    modelo.Equation(15*sword + 10*bow + 50*catapult <= leather)
    
    #test
    if test:
        modelo.Equation(sword==swords)
        modelo.Equation(bow==bows)
        modelo.Equation(catapult==catapults)
    

    #funcion objetivo
    def f(x,y,z):
        return 15*x + 10*y + 80*z

    modelo.Maximize(f(sword,bow,catapult))
    
    try:
        modelo.solve(disp=False)
        return -modelo.options.OBJFCNVAL, [sword, bow, catapult], -modelo.options.OBJFCNVAL
    except:
        return None, None, f(swords, bows, catapults)

def mormont_house_input():
    print('Según tus habilidades como estratega militar que cantidad de cada arma se debería construir')
    swords =int(input('Espadas:'))
    bows =int(input('Arcos:'))
    catapults =int(input('Catapultas:'))
    return [swords, bows, catapults]

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_1_equipo_1 = [
    0, # Espadas
    0, # Arcos
    0, # Catapultas
]

argumentos_problema_1_equipo_2 = [
    0, # Espadas
    0, # Arcos
    0, # Catapultas
]

problema_1 = ProblemManager(mormont_house_solve, mormont_house_input)
class_manager.register_result("Ejercicio 1 - Casa Mormont", problema_1, 
                                argumentos_problema_1_equipo_1, 
                                argumentos_problema_1_equipo_2, 
                                maxim=True)

# %% [markdown]
# ## 2. Casa Greyjoy
# 
# Un importante recurso para la contienda es la comida. Los soldados y la mano de obra son muchos y cada uno necesita ser alimentado para poder trabajar y luchar contra los temibles caminantes blancos. Esta responsabilidad cae sobre Casa Greyjoy. Los cálculos estiman que para hacer una comida para una persona se necesitan:
# 
# - 60 gramos de proteína
# - 120 gramos de carbohidratos
# - 20 gramos de aceite
# - 1.5 litros de agua
# 
# Para satisfacer esta demanda se tienen un conjunto de alimentos y ganado a disposición, cada uno aportando diferentes cantidades de nutrientes.
# 
# | Recurso       | Proteína | Carbohidratos | Aceite | Costo |
# | ------------- | -------- | ------------- | ------ | ----- |
# | Trigo         | 10       | 40            | 20     | 10    |
# | Ganado vacuno | 100      | 10            | 50     | 60    |
# | Encurtidos    | 20       | 30            | 10     | 30    |
# | Agua          | -        | -             | -      | 5     |
# 
# 1. Sabiendo que se espera un ejército de alrededor 60 000 personas, proponga a los jefes de la casa una manera de cumplir con los requerimientos con el menor costo posible.
# 2. Se quiere tener modelo que generalice el problema anterior en términos de la cantidad de tipos de nutrientes y cantidad de tipos de recursos. Proponga un modelo que haga esta generalización.

# %%
# Ejercicio 2
def greyjoy_house_solve(comida=None):
    
    if not comida:
        trigo=None; ganado=None; encurtidos=None; agua=None
    else:
        trigo, ganado, encurtidos, agua = comida
    
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

    test = True if not trigo is None and not encurtidos is None and not ganado is None and not agua is None else False
    
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

    if test:
        modelo.Equation(_trigo==trigo)
        modelo.Equation(_encurtidos==encurtidos)
        modelo.Equation(_ganado==ganado)
        modelo.Equation(_agua==agua)

    def f(x, y, z, w):
        return x * nutrientes_costo[0][3] + y * nutrientes_costo[1][3] + z * nutrientes_costo[2][3] + w * nutrientes_costo[3][3]

    # Función objetivo
    modelo.Minimize(f(_trigo, _ganado, _encurtidos, _agua))

    try:
        modelo.solve(disp=False)
        return modelo.options.OBJFCNVAL, e_vars, modelo.options.OBJFCNVAL
    except:
        return None, None, f(trigo, ganado, encurtidos, agua)

def greyjoy_house_input():
    print('Segun tu habilidad como gastronomo, que cantidad de alimentos se deberia producir')
    trigo = int(input('Trigo:'))
    ganado = int(input('Ganado:'))
    encurtidos = int(input('Encurtidos:'))
    agua = int(input('Agua:'))
    return [trigo, ganado, encurtidos, agua]

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_2_equipo_1 = [
    0, # Trigo
    0, # Ganado
    0, # Encurtido
    0, # Agua
]

argumentos_problema_2_equipo_2 = [
    0, # Trigo
    0, # Ganado
    0, # Encurtido
    0, # Agua
]

problema_2 = ProblemManager(greyjoy_house_solve, greyjoy_house_input)
class_manager.register_result("Ejercicio 2 - Casa Greyjoy", problema_2, 
                                argumentos_problema_2_equipo_1, 
                                argumentos_problema_2_equipo_2)

# %% [markdown]
# ## 3. Casa Targaryen
# 
# El fuego valiryo posee un gran poder ofensivo, este fuego verde arde incluso en el agua y es incapaz de extinguirlo una vez se prende, solo terminando de arder cuando se consume completamente. Las armas imbuidas en este elemento presentan un poder ofensivo superior y además pueden ser usado como bombas incendiarias, así que la producción de este es indispensable. Para fabricar el fuego valiryo se necesita mezclar ciertos ingredientes cuyos nombres no fueron revelados, pero, se conoce la proporción de estos en diferentes recursos naturales:
# 
# | Recurso           | Ingrediente 1 | Ingrediente 2 | Ingrediente 3 | Costo |
# | ----------------- | ------------- | ------------- | ------------- | ----- |
# | Aceite de ballena | 40%           | 10%           | 30%           | 40    |
# | Polvo de dragón   | 10%           | 5%            | 50%           | 70    |
# | Pelo de caballo   | 15%           | 35%           | 5%            | 30    |
# 
# Los alquimistas tienen destilados ya:
# 
# - Ingrediente 1: 15 litros
# - Ingrediente 2: 30 litros
# - Ingrediente 3: 10 litros
# 
# El porcentaje del fuego valiryo se revela que es:
# 
# - Ingrediente 1: 20%
# - Ingrediente 2: 35%
# - Ingrediente 3: 45%
# 
# El fuego valiryo está conformado por un 30% de Ingrediente 1, 20% de Ingrediente 2 y 50% de Ingrediente 3. Como dato adicional los alquimistas necesitan procesar el residuo de los recursos para conservar la pureza del fuego, para esto se tiene un costo extra de 5 por cada unidad de material de desecho. Se cuenta como residuo las cantidades que no son ingredientes del fuego que sale del procesamiento de los recursos, por ejemplo el uno de una unidad de aceite de ballena produce 0.2 unidades de residuo.
# 
# 1. Ayude a los alquimistas a crear 100 unidades de fuego valiryo con el menor costo posible para enfrentar al enemigo.

# %%
# Ejercicio 3
def targaryen_house_solve(materiales=None):
    
    if not materiales:
        aceite=None; dragon=None; caballo=None; ingrediente1=None; ingrediente2=None; ingrediente3=None
    else:
        aceite, dragon, caballo, ingrediente1, ingrediente2, ingrediente3 = materiales
    
    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP

    test = True if  aceite is not None and dragon is not None and caballo is not None else False

    #datos
    total = 100
    costo_remanente = 5

    matriz_mezcla = np.array([
        [.40,.10,.30], # Aceite ballena
        [.10,.05,.50], # Polvo de Dragón
        [.15,.35,.05], # Pelo de caballo
        [1,0,0], # Ingrediente 1
        [0,1,0], # Ingrediente 2
        [0,0,1], # Ingrediente 3
    ])

    remanente = np.array([1 - sum(x) for x in matriz_mezcla])

    costos = np.array([
        40, # Aceite ballena
        70, # Polvo de Dragón
        30, # Pelo de caballo
        0, # Ingrediente 1
        0, # Ingrediente 2
        0, # Ingrediente 3
    ])

    topes_de_ingredientes_puros = np.array([
        15, # Ingrediente 1
        30, # Ingrediente 2
        10, # Ingrediente 3
    ])

    porciento_fuego_val = np.array([
        0.3, # Ingrediente 1
        0.2, # Ingrediente 2
        0.5, # Ingrediente 3
    ])

    #variables
    oil = modelo.Var (lb = 0 ,name='aceite' )
    dra = modelo.Var (lb = 0 ,name='dragon')
    horse = modelo.Var (lb = 0,name='caballo')
    ing1 = modelo.Var (lb = 0 ,name='ingrediente 1')#ing1 30%
    ing2 = modelo.Var (lb = 0 ,name='ingrediente 2')#ing2 20%
    ing3 = modelo.Var (lb = 0 ,name='ingrediente 3')#ing3 50%
    variables = np.array([oil, dra, horse, ing1, ing2, ing3])

    #restricciones 

    # Restricciones de mezcla
    transp = matriz_mezcla.transpose()
    for i in range(len(porciento_fuego_val)):
        modelo.Equation(modelo.sum(transp[i] * variables) == porciento_fuego_val[i] * total)

    # Restricciones de disponibilidad de ingredientes
    for i in range(3,len(variables)):
        modelo.Equation(variables[i] <= topes_de_ingredientes_puros[i-3])

    if test:
        modelo.Equation(oil==aceite)
        modelo.Equation(dra==dragon)
        modelo.Equation(horse==caballo)
        modelo.Equation(ing1==ingrediente1)
        modelo.Equation(ing2==ingrediente2)
        modelo.Equation(ing3==ingrediente3)

    #funcion objetivo
    def f(oil,dra,horse, ingr1, ingr2, ingr3):
        sol = np.array([oil,dra,horse, ingr1, ingr2, ingr3])
        return modelo.sum(costos * sol) + costo_remanente * modelo.sum(remanente * sol)

    modelo.Minimize(f(oil,dra,horse, ing1, ing2, ing3))

    try:
        modelo.solve(disp=False)
        return modelo.options.OBJFCNVAL, [oil, dra, horse, ing1, ing2, ing3], modelo.options.OBJFCNVAL
    except:
        return None, None, f(aceite, dragon, caballo, ingrediente1, ingrediente2, ingrediente3)

def targaryen_house_input():
    print('Según tus habilidades como alquimista,como se debería hacer la compra de los ingrediente')
    oil =int(input('Aceite de ballena: '))
    dra =int(input('Polvo de Dragon: '))
    horse =int(input('Piel de caballo:'))
    ing1 =int(input('Ingrediente 1:'))
    ing2 =int(input('Ingrediente 2:'))
    ing3 =int(input('Ingrediente 3:'))
    return [oil, dra, horse, ing1, ing2, ing3]

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_3_equipo_1 = [
    0, # Aceite de ballena
    0, # Polvo de Dragón
    0, # Piel de caballo
    0, # Ingrediente 1
    0, # Ingrediente 2
    0, # Ingrediente 3
]

argumentos_problema_3_equipo_2 = [
    0, # Aceite de ballena
    0, # Polvo de Dragón
    0, # Piel de caballo
    0, # Ingrediente 1
    0, # Ingrediente 2
    0, # Ingrediente 3
]

problema_3 = ProblemManager(targaryen_house_solve, targaryen_house_input)
class_manager.register_result("Ejercicio 3 - Casa Targaryen", problema_3, 
                                argumentos_problema_3_equipo_1, 
                                argumentos_problema_3_equipo_2)

# %% [markdown]
# ## 4. Casa Baratheon
# 
# Es hora de reunir todos los recursos y tropas. Para esto se conoce que hacen falta trasladar las armas, comida, soldados y fuego valiryo desde Bravos, Pentos y Highgarden hacia Storm´s End, King´s Landing y Casterly Rock desde donde finalmente llegarán a Winterfell. El traslado está condicionado por diferentes situaciones, clima, calidad del camino, tipo de recurso, que hacen que se tenga un desgaste de los recursos en el traslado en dependencia del destino. Este desgaste se observa:
# 
# Armas:
# 
# | Lugares | Storm's End  | King's Landing  | Casterly Rock  |
# | ------- | ---- | ---- | ---- |
# | Braavos     | 5    | 10   | 7    |
# | Pentos     | 10   | 20   | 10   |
# | Highgarden     | 7    | 10   | 7    |
# 
# Comida:
# 
# | Lugares | Storm's End  | King's Landing  | Casterly Rock  |
# | ------- | ---- | ---- | ---- |
# | Braavos     | 25   | 20   | 15   |
# | Pentos     | 20   | 17   | 10   |
# | Highgarden     | 15   | 10   | 5    |
# 
# Soldados:
# 
# | Lugares | Storm's End  | King's Landing  | Casterly Rock  |
# | ------- | ---- | ---- | ---- |
# | Braavos     | 10   | 7    | 7    |
# | Pentos     | 7    | 10   | 9   |
# | Highgarden     | 7    | 9    | 8    |
# 
# Fuego valiryo:
# 
# | Lugares | Storm's End  | King's Landing  | Casterly Rock  |
# | ------- | ---- | ---- | ---- |
# | Braavos     | 30   | 25   | 25   |
# | Pentos     | 25   | 5    | 5    |
# | Highgarden     | 25   | 5    | 5    |
# 
# En total se quieren trasladar 51 000 armas, 285 000 unidades de comida, 60 000 soldados, 100 unidades de fuego valiryo.
# 
# 1. Diga dónde se tienen que asignar los recursos y tropas para que el desgaste del transporte sea lo menor posible.
# 2. Para mitigar el desgaste de los caminos, estos tienen algunas restricciones sobre la cantidad de recursos que pueden ser transportados por ellos. Se tienen que transportar como mínimo en cada camino unas 35000 unidades de cualquier tipo de recusros o tropas. ¿Cuál sería la nueva asignación?

# %%
# Ejercicio 4
def baratheon_house_solve(recursos_caminos=None, preservar_caminos=False):
    
    # Datos
    names = ['armas', 'comida', 'soldados', 'fuego_valiryo']
    
    necesario_recursos = [51000, 285000, 60000, 100]
    costo_caminos = [
        [
            [5, 10, 7],
            [10, 20, 10],
            [7, 10, 7]
        ],
        [
            [25, 20, 15],
            [20, 17, 10],
            [15, 10, 5]
        ],
        [
            [10, 7, 7],
            [7, 10, 9],
            [7, 9, 8]
        ],
        [
            [30, 25, 25],
            [25, 5, 5],
            [25, 5, 5]
        ]
    ]
    min_por_camino = 35000

    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP

    test = True if not recursos_caminos is None else False

    # Variables de decisión
    _vars = [[[None for _ in range(3)] for _ in range(3)] for _ in range(4)]

    for i in range(len(_vars)):
        for j in range(len(_vars[i])):
            for l in range(len(_vars[i][j])):
                _vars[i][j][l] = modelo.Var(lb=0, integer=True, name=(names[i] + '_' + str(j) + '_' + str(l)))

    # Restricciones de demanda
    eq = 0
    for i in range(len(_vars)):
        for j in range(len(_vars[i])):
            for l in range(len(_vars[i][j])):
                eq += _vars[i][j][l]

        modelo.Equation(eq == necesario_recursos[i])
        eq = 0

    # Restricciones de balanceo de demanda entre caminos
    if preservar_caminos:
        i = j = l = 0
        for j in range(len(_vars[0])):
            for l in range(len(_vars[0][j])):
                for i in range(len(_vars)):
                    eq += _vars[i][j][l]

                modelo.Equation(eq >= min_por_camino)
                eq = 0

    if test:
        index = 0
        for i in range(len(_vars)):
            for j in range(len(_vars[i])):
                for l in range(len(_vars[i][j])):
                    modelo.Equation(recursos_caminos[index]==_vars[i][j][l])
                    index+=1

    def f(matrix):
        ret = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for l in range(len(matrix[i][j])):
                    ret += matrix[i][j][l] * costo_caminos[i][j][l]

        return ret

    # Función objetivo
    modelo.Minimize(f(_vars))

    try:
        modelo.solve(disp=False)
        return modelo.options.OBJFCNVAL, _vars, modelo.options.OBJFCNVAL
    except:
        return None, None, f(np.array(recursos_caminos).reshape((4,3,3)))

def baratheon_house_input():
    names = ['armas', 'comida', 'soldados', 'fuego_valiryo']
    print('Se intentara preservar los caminos?')
    print('1 - Si')
    print('2 - No')
    while True:
        raw = input()
        try:
            ans = int(raw)
        
        except:
            print('Escriba una entrada correcta')

        if ans == 1:
            preservar = True
            break

        elif ans == 2:
            preservar = False
            break

        else:
            print('Escriba una entrada correcta')


    min = baratheon_house_solve(preservar_caminos=preservar)
    print('Segun el analisis que haz realizado sobre los caminos, cual seria la distribucion de recursos a enviar por cada ruta?')
    print()
    user_ans = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(4)]
    for i in range(len(user_ans)):
        for j in range(len(user_ans[i])):
            for l in range(len(user_ans[i][j])):
                user_ans[i][j][l] = int(input('Escriba la cantidad de ' + names[i] + ' a enviar por la ruta comenzando en el lugar 1.' + str(j + 1) + ' y terminando en el lugar 2.' + str(l + 1) + ': '))

    return user_ans


# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_4_equipo_1 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    
], False

argumentos_problema_4_equipo_2 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
], False

problema_4 = ProblemManager(baratheon_house_solve, baratheon_house_input)

print("Inciso a)")
print()
class_manager.register_result("Ejercicio 4 a) - Casa Baratheon", problema_4, 
                                argumentos_problema_4_equipo_1, 
                                argumentos_problema_4_equipo_2,
                                unfold=True)


# %%
argumentos_problema_4_2_equipo_1 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    
], True

argumentos_problema_4_2_equipo_2 = [
    [ # Transporte de Armas
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Comida
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Soldados
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    [ # Transporte de Fuego Valiryo
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
], True

print("Inciso b)")
print()
class_manager.register_result("Ejercicio 4 b) - Casa Baratheon", problema_4, 
                                argumentos_problema_4_2_equipo_1, 
                                argumentos_problema_4_2_equipo_2,
                                unfold=True)

# %% [markdown]
# ## 5. Casa Tully
# 
# La fuerza secundaria está esperando en las fortalezas Storm's End, King's Landing y Casterly Rock. Para hacer el viaje se tienen las siguientes rutas:
# 
# 
# Rutas:
# 
# | Origen | Destino | Capacidad |
# | --- | --- | --- |
# | The Twins (Violeta) | Winterfell | 0 |
# | Storm's End (Negro) | King's Landing | 0 |
# | Storm's End | The Dreadfort | 0 |
# | Iron Islands (Rojo) | The Twins | 0 |
# | King's Landing (Salmón) | The Dreadfort | 0 |
# | King's Landing | The Eyrie | 0 |
# | King's Landing | Riverrun | 0 |
# | Riverrun (Celeste) | The Twins | 0 |
# | Riverrun | The Eyrie | 0 |
# | Casterly Rock (Verde) | Iron Islands | 0 |
# | Casterly Rock | Riverrun | 0 |
# | The Eyrie (Morado) | The Twins | 0 |
# | The Eyrie | Riverrun | 0 |
# | The Dreadfort (Azul) | Winterfell | 0 |
# 
# ![images/Poniente.jpg](images/Poniente.jpg)
# 
# Soldados iniciales:
# 
# | Lugar de partida | Cantidad de soldados |
# | --- | --- |
# | Storm's End | 0 |
# | King's Landing | 0 |
# | Casterly Rock | 0 |
# 
# 1. Se necesitan trasladar la mayor cantidad de soldados a Winterfell de manera tal de que las rutas no pasen más de cierta cantidad de soldados. ¿De qué forma es posible hacer esto?

# %%
# Ejercicio 5
def tully_house_solve(assigned_soldiers=None):
    if assigned_soldiers is None:
        assigned_soldiers = []

    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP
    
    # Constantes

    # Grafo no dirigido de lugares
    paths = {
        "The Twins": {
            "Winterfell":40000, 
        },
        "Storm's End": {
            "King's Landing":20000,
            "The Dreadfort":20000,
            },
        "Iron Islands": {
            "The Twins":10000,
            },
        "King's Landing": {
            "The Dreadfort":20000,
            "Riverrun":10000,
            "The Eyrie":10000,
            },
        "Riverrun": {
            "The Twins":20000,
            "The Eyrie":20000,
            },
        "Casterly Rock": {
            "Iron Islands":10000,
            "Riverrun":10000,
            },
        "The Eyrie": {
            "The Twins":10000,
            "Riverrun":10000,
            },
        "The Dreadfort": {
            "Winterfell":20000,
            },
        "Winterfell": {},
    }

    # Soldados iniciales
    initial_soldiers = {
        "The Twins": 0, # House Frey
        "Iron Islands": 0, # House Greyjoy
        "Storm's End": 30000, # House Baratheon
        "King's Landing": 30000, # House Targaryen
        "Riverrun": 0, # House Tully
        "Casterly Rock": 30000, # House Lannister
        "The Eyrie": 0, # House Arryn
        "The Dreadfort": 0, # House Bolton
        "Winterfell": 0, # House Stark
    }

    # Este lugar ficticio se conecta con los lugares originales mediante aristas 
    # Con el peso correspondiente a la cantidad de soldados
    paths["Nodo Inicial"] = {place:initial_amount for place, initial_amount in initial_soldiers.items()}
    # Todos los soldados salen de un lugar ficticio creado por el bien del modelo
    initial_soldiers["Nodo Inicial"] = sum(initial_soldiers.values())

    # Completar las aristas faltantes con 0
    for key1 in paths:
        for key2 in paths:
            if key2 not in paths[key1]:
                paths[key1][key2] = 0

    places = list(paths.keys())
    places.sort()

    # Variables
    soldiers_ij = { 
        source_place: {
            dest_place:
            modelo.Var(lb=0, integer=True, name=f"Soldados que pasan desde {source_place} a {dest_place}") 
                for dest_place in places
            } 
            for source_place in places 
        }

    # Restricciones

    for source in places:
        for dest in places:
            # Los soldados que van de source a dest no puede ser más que el peso de la arista
            modelo.Equation(soldiers_ij[source][dest] <= paths[source][dest])
    
    for place in [x for x in places if x not in ["Nodo Inicial", "Winterfell"]]:
        # Lo que entra en el nodo es igual a lo que sale
        modelo.Equation(modelo.sum([soldiers_ij[place][x] for x in places]) == modelo.sum([soldiers_ij[x][place] for x in places]))

    # Restricciones de usuario
    if assigned_soldiers:
        index = 0
        for source in places:
            for dest in places:
                modelo.Equation(soldiers_ij[source][dest] == assigned_soldiers[index])
                index+=1

    def f(soldiers, model_sum=True):
        if model_sum:
            return modelo.sum([soldiers[place]["Winterfell"] for place in places])
        else:
            return sum([soldiers[place]["Winterfell"] for place in places])

    # Función objetivo
    modelo.Maximize(f(soldiers_ij))

    try:
        modelo.solve(disp=False)
        return -modelo.options.OBJFCNVAL, [soldiers_ij[x][y] for x in places for y in places], -modelo.options.OBJFCNVAL
    except:
        soldier_dict = {}
        index = 0
        for source in places:
            soldier_dict[source] = {}
            for dest in places:
                soldier_dict[source][dest] = assigned_soldiers[index]
                index+=1
        return None, None, f(soldier_dict, False)

def tully_house_input():
    print("Introduce los nombres de salida y destino y la cantidad de soldados a transportar separados por ,:")
    asigancion = []
    entrada = True
    while entrada:
        entrada = input("Salida, Destino, Cantidad: ")
        salida, destino, cant = [x.strip() for x in entrada.split(',')]
        asigancion.append((salida, destino, int(cant)))
    return asigancion

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None
places = [
    'Winterfell',
    'The Twins',
    'The Eyrie',
    'The Dreadfort',
    "Storm's End",
    'Riverrun',
    'Nodo Inicial',
    "King's Landing",
    'Iron Islands',
    'Casterly Rock',
]
places.sort()

# Argumentos con las aristas del problema

argumentos_problema_5_equipo_1 = [
    ("The Twins", "Winterfell", 0),
    ("Storm's End", "King's Landing", 0),
    ("Storm's End", "The Dreadfort", 0),
    ("Iron Islands", "The Twins", 0),
    ("King's Landing", "The Dreadfort", 0),
    ("King's Landing", "Riverrun", 0),
    ("King's Landing", "The Eyrie", 0),
    ("Riverrun", "The Twins", 0),
    ("Riverrun", "The Eyrie", 0),
    ("Casterly Rock", "Iron Islands", 0),
    ("Casterly Rock", "Riverrun", 0),
    ("The Eyrie", "The Twins", 0),
    ("The Eyrie", "Riverrun", 0),
    ("The Dreadfort", "Winterfell", 0),
]

argumentos_problema_5_equipo_2 = [
    ("The Twins", "Winterfell", 0),
    ("Storm's End", "King's Landing", 0),
    ("Storm's End", "The Dreadfort", 0),
    ("Iron Islands", "The Twins", 0),
    ("King's Landing", "The Dreadfort", 0),
    ("King's Landing", "Riverrun", 0),
    ("King's Landing", "The Eyrie", 0),
    ("Riverrun", "The Twins", 0),
    ("Riverrun", "The Eyrie", 0),
    ("Casterly Rock", "Iron Islands", 0),
    ("Casterly Rock", "Riverrun", 0),
    ("The Eyrie", "The Twins", 0),
    ("The Eyrie", "Riverrun", 0),
    ("The Dreadfort", "Winterfell", 0),
]

# Asignando los valores al nodo inicial por defecto
iniciales_equipo_1 = {
    "King's Landing": sum(val for (source, dest, val) in argumentos_problema_5_equipo_1 if source == "King's Landing"), 
    "Storm's End": sum(val for (source, dest, val) in argumentos_problema_5_equipo_1 if source == "Storm's End"), 
    "Casterly Rock": sum(val for (source, dest, val) in argumentos_problema_5_equipo_1 if source == "Casterly Rock")
}

iniciales_equipo_2 = {
    "King's Landing": sum(val for (source, dest, val) in argumentos_problema_5_equipo_2 if source == "King's Landing"), 
    "Storm's End": sum(val for (source, dest, val) in argumentos_problema_5_equipo_2 if source == "Storm's End"), 
    "Casterly Rock": sum(val for (source, dest, val) in argumentos_problema_5_equipo_2 if source == "Casterly Rock")
}

# Completar los huecos
for x in places:
    for y in places:
        if x == "Nodo Inicial" and y in iniciales_equipo_1:
            argumentos_problema_5_equipo_1.append((x,y,iniciales_equipo_1[y]))
        elif not any(_ for (source,dest,_) in argumentos_problema_5_equipo_1 if x==source and y==dest):
            argumentos_problema_5_equipo_1.append((x,y,0))
            
        if x == "Nodo Inicial" and y in iniciales_equipo_2:
            argumentos_problema_5_equipo_2.append((x,y,iniciales_equipo_2[y]))
        elif not any(_ for (source,dest,_) in argumentos_problema_5_equipo_2 if x==source and y==dest):
            argumentos_problema_5_equipo_2.append((x,y,0))

argumentos_problema_5_equipo_1_ = []
argumentos_problema_5_equipo_2_ = []

# Ordenando los argumentos
for x in places:
    for y in places:
        valor1 = next(valor for (source,dest,valor) in argumentos_problema_5_equipo_1 if x==source and y==dest)
        valor2 = next(valor for (source,dest,valor) in argumentos_problema_5_equipo_2 if x==source and y==dest)
        argumentos_problema_5_equipo_1_.append(valor1)
        argumentos_problema_5_equipo_2_.append(valor2)

argumentos_problema_5_equipo_1 = argumentos_problema_5_equipo_1_,
argumentos_problema_5_equipo_2 = argumentos_problema_5_equipo_2_,

problema_5 = ProblemManager(tully_house_solve, tully_house_input)
class_manager.register_result("Ejercicio 5 - Casa Tully", problema_5, 
                                argumentos_problema_5_equipo_1, 
                                argumentos_problema_5_equipo_2, 
                                maxim=True,
                                unfold=True)

# %% [markdown]
# ## 6. Casa Stark
# 
# Ya se encuentran todos los recursos en Winterfell, listos para la batalla, el frío y la oscuridad cubren todo. Los exploradores regresan de su misión informando que los caminantes blancos atacarán en 12 oleadas y calculan el estimado de fuerza de cada una de ellas:
# 
# | Oleada | 1    | 2    | 3    | 4    | 5    | 6     | 7     | 8    | 9    | 10   | 11   | 12   |
# | ------ | ---- | ---- | ---- | ---- | ---- | ----- | ----- | ---- | ---- | ---- | ---- | ---- |
# | Fuerza | 2000 | 3000 | 4000 | 6000 | 8000 | 10000 | 10000 | 6000 | 4000 | 3000 | 2000 | 2000 |
# 
# Se sabe que cada soldado puede derrotar a un caminante blanco antes de perecer, además se tiene un lugar inicialmente vacío en las cercanías del campo de batalla, ahí las tropas pueden actuar como una fuerza de acción rápida además den descansar y reparar sus armas para continuar luchando, aunque por desgracia este lugar tiene un máximo de 5000 hombres. Las tropas se van enviando constantemente en cada oleada para reforzar la ofensiva. Debido al proceso de movilización, aumentar la cantidad de hombres que se envían a la batalla en cada oleada tiene un costo de 1 por hombre y disminuirlo de 0.5. 
# 
# 1. Realice un plan de lucha que permita ganar la batalla con el mínimo de costo posible.
# 2. Para que Arya pueda dar el golpe final se tiene que tener en la última oleada una diferencia de poder ganadora para los caminantes blancos de 1000, para que el jefe se confíe y salga al campo de batalla. Teniendo esto en cuenta, ¿qué cambios le harías a la estrategia?

# %%
# Ejercicio 6
def stark_house_solve(waves_values=None, arya=False):
    if waves_values is None:
        waves_values = []

    modelo = GEKKO(remote=False)
    modelo.options.SOLVER = 1  # APOPT is an MINLP solver
    modelo.options.LINEAR = 1 # Is a MILP

    # Constantes
    wave_strength_i = np.array([2000, 3000, 4000, 6000, 8000, 10000, 10000, 6000, 4000, 3000, 2000, 2000])
    waves_amount = len(wave_strength_i)
    max_refuge_capacity = 5000
    arya_threshold = 1000

    # Variables
    men_sent_wave_i = np.array([modelo.Var(lb=0, integer=True, name=f"Hombres enviados oleada {i}") for i in range(waves_amount)])
    # Aux variables para eliminar módulo
    positive_z_i = np.array([modelo.Var(lb=0, name=f"Diferencia positiva oleada {i+1}-{i}") for i in range(waves_amount-1)])
    negative_z_i = np.array([modelo.Var(ub=0, name=f"Diferencia negativa oleada {i+1}-{i}") for i in range(waves_amount-1)])

    # Restricciones
    def z_i(i):
        return men_sent_wave_i[i+1] - men_sent_wave_i[i]

    def all_men_k(k):
        """
        Devuelve la expresión de todos los hombres enviados hasta la oleada k
        """
        return (k+1)*men_sent_wave_i[0] + modelo.sum([(k - i)*(z_i(i)) for i in range(k)])

    def all_wave_strength_k(k):
        """
        Devuelve la expresión de toda la fuerza de las oleadas hasta la oleada k
        """
        return modelo.sum(wave_strength_i[:k+1])
    
    # Restricciones de variables
    for i in range(waves_amount-1):
        modelo.Equation(z_i(i) == positive_z_i[i] + negative_z_i[i])

    # Restricciones de capacidad
    for i in range(waves_amount):
        modelo.Equation(all_men_k(i) - all_wave_strength_k(i) <= max_refuge_capacity)
        modelo.Equation(all_men_k(i) - all_wave_strength_k(i) >= 0)

    # Restriccion de Arya
    if arya:
        modelo.Equation(all_wave_strength_k(waves_amount-1) - all_men_k(waves_amount-2) >= arya_threshold) 

    # Restricciones de usuario
    for i,restr in enumerate(waves_values):
        modelo.Equation(men_sent_wave_i[i] == restr)

    # Función objetivo
    modelo.Minimize(modelo.sum([0.75 * (positive_z_i[i] - negative_z_i[i]) + 0.25 * z_i(i) for i in range(waves_amount-1)]))

    try:
        modelo.solve(disp=False)
        return modelo.options.OBJFCNVAL, men_sent_wave_i, modelo.options.OBJFCNVAL
    except:
        waves_zi = np.array([waves_values[i+1] - waves_values[i] for i in range(len(waves_values)-1)])
        return None, None, sum(x if x >= 0 else 0.5 * -x for x in waves_zi)

def stark_house_input():
    print("Introduce la cantidad de guerreros a enviar en cada oleada:")
    guerreros = []
    for i in range(12):
        guerreros.append(int(input(f"Oleada {i+1}: ")))
    return guerreros

# Poner a mano los argumentos dichos por los estudiantes o se pueden poner mediente input seteando los argumentos a None

argumentos_problema_6_equipo_1 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], False

argumentos_problema_6_equipo_2 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], False

print("Inciso a)")
print()
problema_6 = ProblemManager(stark_house_solve, stark_house_input)
class_manager.register_result("Ejercicio 6 a) - Casa Stark", problema_6, 
                                argumentos_problema_6_equipo_1, 
                                argumentos_problema_6_equipo_2,
                                unfold=True)


# %%
argumentos_problema_6_2_equipo_1 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], True

argumentos_problema_6_2_equipo_2 = [
    0, # Hombres enviados oleada 1
    0, # Hombres enviados oleada 2
    0, # Hombres enviados oleada 3
    0, # Hombres enviados oleada 4
    0, # Hombres enviados oleada 5
    0, # Hombres enviados oleada 6
    0, # Hombres enviados oleada 7
    0, # Hombres enviados oleada 8
    0, # Hombres enviados oleada 9
    0, # Hombres enviados oleada 10
    0, # Hombres enviados oleada 11
    0, # Hombres enviados oleada 12
], True

print("Inciso b)")
print()
class_manager.register_result("Ejercicio 6 b) - Casa Stark", problema_6, 
                                argumentos_problema_6_2_equipo_1, 
                                argumentos_problema_6_2_equipo_2,
                                unfold=True)

# %% [markdown]
# # Conlcusión
# 
# Conteo de puntos y dar resultados

# %%
class_manager.print_result()


# %%



