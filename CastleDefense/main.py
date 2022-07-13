from typing import Any, Tuple
from castle_defense_discrete.castle_simulation import JuegoSimulacion
from castle_defense_discrete.castle import *
from castle_defense_discrete.castle_gekko import JuegoGEKKO
from levels import NIVELES_DIFICIL, NIVELES_FACIL, NIVELES_MEDIO, NIVELES_TEST

def juego1() -> JuegoGEKKO:
    """
    Prueba los fundamentos del juego
    """
    
    return JuegoGEKKO(NIVELES_TEST[0])

def juego2() -> JuegoGEKKO:
    """
    El juego prueba la dependencia de las armas
    """
    
    return JuegoGEKKO(NIVELES_TEST[1])

def juego3() -> JuegoSimulacion:
    """
    Simula el juego 1, ya con el usuario jugando
    """
    
    return JuegoSimulacion(NIVELES_TEST[0])

def juego4() -> JuegoSimulacion:
    """
    Simula el juego 2, ya con el usuario jugando
    """
    
    return JuegoSimulacion(NIVELES_TEST[1])

def juego5() -> JuegoGEKKO:
    """
    El juego prueba las armas iniciales
    """
    
    return JuegoGEKKO(NIVELES_TEST[3])


# juego = juego1()
# juego.correr()
# juego = juego2()
# juego.correr()
# juego = juego3()
# juego.correr()
# juego = juego4()
# juego.correr()
# juego = juego5()
# juego.correr()

def seleccionar_opcion(encabezado: str, opciones: Dict[str,Tuple[str,Any]]) -> Any:
    value = None

    def print_opciones():
        for x in opciones:
            nombre,_ = opciones[x]
            print(x,"->",nombre)
        print()

    print(encabezado)
    print()
    print_opciones()
    while True:
        seleccion = input(">> ")
        if seleccion not in opciones:
            print("Selección inválida, las opciones son:")
            print_opciones()
        else:
            _,value = opciones[seleccion]
            break
    return value

def main():
    metodo_de_juego = {
        "0": ("Método óptimo", JuegoGEKKO),
        "1": ("Jugador humano", JuegoSimulacion),
    }
    dificultad_de_juego = {
        "t": ("Test", NIVELES_TEST),
        "0": ("Fácil", NIVELES_FACIL),
        "1": ("Medio", NIVELES_MEDIO),
        "2": ("Difícil", NIVELES_DIFICIL),
    }

    print("Bienvenido a CastleDefense!!")
    print()

    tipo_de_juego = seleccionar_opcion("Seleccione el método de juego:", metodo_de_juego)
    niveles_de_dificultad = seleccionar_opcion("Seleccione la dificultad del nivel", dificultad_de_juego)

    niveles_de_dificultad = {str(i): (x.nombre, x) for i,x in enumerate(niveles_de_dificultad)}
    nivel_seleccionado = seleccionar_opcion("Seleccione el nivel", niveles_de_dificultad)

    juego = tipo_de_juego(nivel_seleccionado)

    juego.correr()

if __name__ == "__main__":
    main()