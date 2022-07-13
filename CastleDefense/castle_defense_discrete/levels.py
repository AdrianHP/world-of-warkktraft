from castle import *


def __juego_prueba1() -> Nivel:
    """
    Prueba la el flujo básico de construcción de niveles.
    
    Fijarse en los comentarios que indican formas alternativas de construccion de
    los niveles
    """
    recursos = [
        Recurso("Madera", 100),
        Recurso("Hierro", 100),
        Recurso("Cuero", 100),
    ]
    # recursos = { # Se puede usar un diccionario para los recursos
    #     "Madera": 100,
    #     "Hierro": 100,
    #     "Cuero": 100,
    # }

    armas = [
        Arma(10, None, "Hacha", [
            Recurso("Madera", 15),
            Recurso("Hierro", 5),
            Recurso("Cuero", 0), # Se puede omitir si no se pone
        ], Artesano(1), Guerrero(1)),
        Arma(10, None, "Espada", [
            Recurso("Hierro", 15), # El orden no tiene que ser el mismo
            Recurso("Madera", 5),
        ], Artesano(1), 1), # Se puede simplemente poner el número 
        Arma(30, None, "Catapulta", { # Como diccionario también funciona
            "Madera": 10,
            "Hierro": 20,
            "Cuero": 20,
        }, 2, Guerrero(2)), # También en el artesano
    ]

    castillo = Castillo(Artesano(10), Guerrero(10), recursos, armas)

    ataque_enemigo = [
        # Paz
        0, # Se puede poner un número normal
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        # Ataque
        AtaqueEnemigo(10),
        AtaqueEnemigo(10),
        AtaqueEnemigo(10),
        AtaqueEnemigo(150),
    ]

    estrategia = EstrategiaEnemiga(ataque_enemigo)
    
    return Nivel("Prueba 1", Nivel.FACIL, estrategia, castillo) 


def __juego_prueba2() -> Nivel:
    """
    Prueba la dependencia de las armas a la hora de ser construidas.
    """
    recursos = [
        Recurso("Oro", 1000)
    ]
    
    arma1 = Arma(0, None, "Parte1", [Recurso("Oro", 100)], Artesano(2), Guerrero(10000))
    arma2 = Arma(0, arma1, "Parte2", [Recurso("Oro", 200)], Artesano(3), Guerrero(10000))
    arma3 = Arma(100, arma2, "ArmaFinal", [Recurso("Oro", 200)], Artesano(4), Guerrero(2))
    
    castillo = Castillo(Artesano(8), Guerrero(5), recursos, [arma1,arma2,arma3])
    
    estrategia = EstrategiaEnemiga([
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(200),
    ])

    return Nivel("Prueba 2", Nivel.FACIL, estrategia, castillo) 


def __juego_prueba3() -> Nivel:
    """
    Prueba las armas iniciales
    """
    recursos = [
        Recurso("Oro", 0)
    ]
    
    arma1 = Arma(0, None, "Parte1", [Recurso("Oro", 100)], Artesano(2), Guerrero(10000))
    arma2 = Arma(0, arma1, "Parte2", [Recurso("Oro", 200)], Artesano(3), Guerrero(10000))
    arma3 = Arma(100, arma2, "ArmaFinal", [Recurso("Oro", 200)], Artesano(4), Guerrero(2))
    
    armas_iniciales = { # No se tienen que asignar las armas de las que dependen, pero estas se crearan automaticamente
        arma3.nombre: 2,
    }
    
    castillo = Castillo(Artesano(8), Guerrero(5), recursos, [arma1,arma2,arma3], armas_iniciales)
    
    estrategia = EstrategiaEnemiga([
        AtaqueEnemigo(200),
    ])

    return Nivel("Prueba 3", Nivel.FACIL, estrategia, castillo) 

def __juego_prueba4() -> Nivel:
    """
    Prueba la recoleccion de recursos 
    """
    recursos = [
        Recurso("Oro", 0, 100)
    ]
    
    arma1 = Arma(10, None, "Parte1", [Recurso("Oro", 100)], Artesano(1), Guerrero(1))
    
    castillo = Castillo(Artesano(3), Guerrero(5), recursos, [arma1])
    
    estrategia = EstrategiaEnemiga([
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(0),
        AtaqueEnemigo(40),
    ])

    return Nivel("Prueba 4", Nivel.FACIL, estrategia, castillo) 

NIVELES_TEST = [
    __juego_prueba1(),
    __juego_prueba2(),
    __juego_prueba3(),
    __juego_prueba4(),
]

# TODO
NIVELES_FACIL = [

]

# TODO
NIVELES_MEDIO = [

]

# TODO
NIVELES_DIFICIL = [
    
]