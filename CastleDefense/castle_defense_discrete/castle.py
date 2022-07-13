"""
API para crear niveles del juego
"""

from typing import Dict, List, Optional, Tuple, Union
    
class Habitante:
    """
    Representa la `cantidad` de habitantes de tipo `nombre` para determinada acción
    """
    def __init__(self, nombre: str, cantidad: int) -> None:
        self.nombre = nombre
        self.cantidad = cantidad
      
    def __repr__(self) -> str:
        return str(self)
          
    def __str__(self) -> str:
        return f"{self.nombre}, Cantidad: {self.cantidad}"

class Artesano(Habitante):
    """
    Representa la `cantidad` de habitantes Artesanos para determinada acción
    """
    def __init__(self, cantidad: int) -> None:
        super().__init__("Artesano", cantidad)

class Guerrero(Habitante):
    """
    Representa la `cantidad` de habitantes Guerreros para determinada acción
    """
    def __init__(self, cantidad: int) -> None:
        super().__init__("Guerrero", cantidad)

class Recurso:
    """
    Representa la `cantidad` de recursos de tipo `nombre` para determinada acción.

    Representa la `cantidad` de recursos disponibles y su capacidad de recolección por turno
    """

    def __init__(self, nombre: str, cantidad: int, capacidad_recoleccion: int = 0) -> None:
        self.nombre = nombre
        self.cantidad = cantidad
        self.capacidad_recoleccion = capacidad_recoleccion

    def __str__(self) -> str:
        return f"Recurso: {self.nombre}, Cantidad: {self.cantidad}, Recoleccion: {self.capacidad_recoleccion}"
    
    def __repr__(self) -> str:
        return str(self)
    
    def copy(self) -> 'Recurso':
        return Recurso(self.nombre, self.cantidad, self.capacidad_recoleccion)

class Arma:
    """
    Representa el `ataque` de un arma de tipo `nombre`. Describe la dependencia de construcción de 
    dicha arma, la cantidad de artesanos y querreros necesarios para hacerla funcionar y los recursos necesarios
    para hacerla
    """

    def __init__(self, ataque:int, depende: Optional["Arma"], nombre: str, recursos: Union[List[Recurso], Dict[str, int]], artesanos: Union[int,Artesano], guerreros: Union[int,Guerrero]) -> None:
        self.ataque = ataque
        self.depende = depende
        self.nombre = nombre
        self.recursos = _convertir_a_lista_recurso(recursos)
        self.artesanos = _convertir_en_artesano_guerrero(artesanos, Artesano)
        self.guerreros = _convertir_en_artesano_guerrero(guerreros, Guerrero)
        
    def __str__(self) -> str:
        return f"Arma: {self.nombre}, Ataque: {self.ataque}, Depende: {self.depende.nombre if self.depende else 'NONE'}, Artesanos: {self.artesanos.cantidad}, Guerreros: {self.guerreros.cantidad}, Recursos: {self.recursos}"
    
    def __repr__(self) -> str:
        return str(self)
    
class Castillo:
    """
    Representa el castillo a defender. Contiene toda la información inicial
    necesaria.
    """
    def __init__(self, artesanos: Union[int,Artesano]
                     , guerreros: Union[int,Guerrero]
                     , recursos: Union[List[Recurso], Dict[str, int]]
                     , armas: List[Arma]
                     , armas_iniciales: Dict[str,int] = None) -> None:
        self.recursos = _convertir_a_lista_recurso(recursos)
        self.artesanos = _convertir_en_artesano_guerrero(artesanos, Artesano)
        self.guerreros = _convertir_en_artesano_guerrero(guerreros, Guerrero)
        self.armas = armas
        self.armas_iniciales = armas_iniciales if armas_iniciales else {}
        self._acomodar_datos_castillo()


    def _acomodar_datos_castillo(self):
        """
        Realiza una modificación al `castillo` añadiendo supuestos básicos del modelo
        y realiza comprobaciones básicas
        """

        # Ordenar los recursos del castillo por nombre para que coincidan en índice 
        # con los recursos de las armas
        self.recursos.sort(key=lambda x: x.nombre) 

        cant_tipos_recursos = len(self.recursos)
        
        for arma in self.armas:
            # Añadir recursos faltantes 
            nuevos_recursos = []
            for recurso_original in self.recursos:
                # Se les asigna una copia de los recursos originales para que este recurso contenga toda la informacion necesaria
                nuevo_recurso = recurso_original.copy()
                try:
                    recurso = next(x for x in arma.recursos if x.nombre == recurso_original.nombre)
                    nuevo_recurso.cantidad = recurso.cantidad
                except StopIteration:
                    # Añadir con costo 0 los recursos que no se definieron en las armas
                    nuevo_recurso.cantidad = 0
                nuevos_recursos.append(nuevo_recurso)
            arma.recursos = nuevos_recursos
            
            # Ordenar los recursos del castillo por nombre para que coincidan en índice con los recursos del castillo
            arma.recursos.sort(key=lambda x: x.nombre)
            if cant_tipos_recursos != len(arma.recursos):
                raise Exception(f"La cantidad de tipos de recursos en el arma {arma.nombre} es diferente a la cantidad de tipos de recursos definida. Esto puede significar algún error en los nombres de los recursos al crear el arma o la omisión de alguno en la definición de estos")

        nombre_de_armas = set([x.nombre for x in self.armas])
        for arma,inicial in self.armas_iniciales.items():
            if inicial < 0:
                raise Exception(f"La cantidad inicial del arma {arma} no puede ser negativa")
            if arma not in nombre_de_armas:
                raise Exception(f"El arma {arma} se encuentra en armas iniciales pero no está definido en las armas")
                
        # Si no está definida en las armas iniciales significa que la cantidad inicial es 0
        for arma_faltante in nombre_de_armas.difference(self.armas_iniciales.keys()):
            self.armas_iniciales[arma_faltante] = 0
            
        # Añadir las dependencias de las armas iniciales.
        for arma in self._orden_topologico(self.armas):
            if arma.depende is not None:
                self.armas_iniciales[arma.depende.nombre] += self.armas_iniciales[arma.nombre]

    def _orden_topologico(self, armas: List[Arma]) -> List[Arma]:
        grados_entrada = {x.nombre: 1 if any(y for y in armas if y.depende is not None and y.depende.nombre == x.nombre) else 0 for x in armas}
        orden_topologico = []
        while grados_entrada:
            nivel_cero = [x for x in grados_entrada if grados_entrada[x] == 0]
            orden_topologico.extend(nivel_cero)
            for depen in [x.depende for x in armas if 
                          x.nombre in nivel_cero and 
                          x.depende is not None and 
                          x.depende.nombre in grados_entrada]:
                grados_entrada[depen.nombre] -= 1
            for arma in nivel_cero:
                grados_entrada.__delitem__(arma)
        return [next(x for x in armas if x.nombre == y) for y in orden_topologico]
                

class AtaqueEnemigo:
    """
    Representa un solo ataque enemigo con su `poder`.
    """
    def __init__(self, poder: int) -> None:
        self.poder = poder

    def __str__(self) -> str:
        return f"Ataque: {self.poder}"

class EstrategiaEnemiga:
    """
    Representa la estrategia completa del enemigo durante todo el juego. Consiste en una
    lista de AtaqueEnemigo, la cual es el ataque realizado en eel i-esimo turno. 
    """
    def __init__(self, ataques: List[Union[AtaqueEnemigo,int]]) -> None:
        self.ataques = [AtaqueEnemigo(x) if isinstance(x, int) else x for x in ataques]



class Nivel:
    """
    Representa una estructura que agrupa metadatos sobre el juego a realizar.
    """

    FACIL = 1
    MEDIO = 2
    DIFICIL = 3

    def __init__(self, nombre: str, dificultad:int, estrategia_enemiga: EstrategiaEnemiga, castillo: Castillo) -> None:
        self.nombre = nombre
        self.dificultad = dificultad
        self.estrategia_enemiga = estrategia_enemiga
        self.castillo = castillo

# 
ResultModelo = Tuple[Dict[int,Dict[str,int]],Dict[int,Dict[str,int]],Dict[int,Dict[str,int]]]

class Modelo:
    """
    Representa el modelo final para la solución del problema.
    """
    def solve(self) -> ResultModelo:
        raise NotImplementedError()

class Juego:
    """
    Representa la instancia de juego que realizará nivel.
    """
    def __init__(self, nivel: Nivel) -> None:
        self.nivel = nivel

    @property
    def castillo(self):
        return self.nivel.castillo

    @property
    def estrategia_enemiga(self):
        return self.nivel.estrategia_enemiga
              
    def print_prologo(self):
        recursos = [str(x) for x in self.castillo.recursos]
        artesanos = self.castillo.artesanos.cantidad
        guerreros = self.castillo.guerreros.cantidad
        armas = [str(x) for x in self.castillo.armas]
        dias_de_espera = len(self.estrategia_enemiga.ataques)
        dias_de_llegada = next(i for i,x in enumerate(self.estrategia_enemiga.ataques) if x.poder!=0) if any(x for x in self.estrategia_enemiga.ataques if x.poder!=0) else dias_de_espera

        sep = "\n"
        pr = f"""Estás en un castillo que será asediado por una fuerza que te supera, 
por suerte tu salvación se encuentra a unos {dias_de_espera} días de espera. 
Tu misión es resistir hasta que lleguen los refuerzos. En los almacenes del 
castillo se tienes unos recursos:

{sep.join(recursos)} 

Entre tus filas cuentas con una fuerza de {artesanos} artesanos para 
confeccionar las armas necesarias y {guerreros} guerreros para defenderte. 

Las armas se pueden demorar varios días en construirse y necesitan 
ser utilizadas por uno o varios guerreros para que sean efectivas.

Las armas que están disponibles son: 

{sep.join(armas)} 

El enemigo tardará unos {dias_de_llegada} días en llegar y luego atacará 
en oleadas cada vez más fuertes, aprovecha el tiempo que tienes para 
irte preparando para la dura batalla, construye armas que puedan 
contener las arremetidas furiosas de los malvados que quieren tomar
las vidas de tus súbditos, en las batallas asígnales estas armas 
a tus guerreros para que puedan luchar. 

Si todo sale bien seguro saldrás victorioso.

Suerte, esperemos que no queden solo ruinas para los aliados."""
        print(pr)

    
    def print_situacion(self):
        print()
        print(f"Se espera un ataque de {len(self.estrategia_enemiga.ataques)} dias")
        print(f"Cuentas inicialmente con:")
        print(f"Recursos")
        for r in self.castillo.recursos:
            print(r)
        print()
        print(f"Armas")
        for a in self.castillo.armas:
            print(a)
        print()
        print(f"Habitantes")
        print(self.castillo.artesanos)
        print(self.castillo.guerreros)
    
    def correr(self):
        self.print_prologo()
        self.print_situacion()
        modelo = self.generar_modelo()
        modelo.solve()
    
    def generar_modelo(self)->Modelo:
        raise NotImplementedError


def _convertir_a_lista_recurso(dict_recurso: Union[List[Recurso], Dict[str, int]]) -> List[Recurso]:
    if isinstance(dict_recurso, dict):
        return [Recurso(x, dict_recurso[x]) for x in dict_recurso]
    return dict_recurso

def _convertir_en_artesano_guerrero(numero: Union[int, Artesano, Guerrero], tipo_esperado) -> Union[Artesano, Guerrero]:
    if isinstance(numero, int):
        return tipo_esperado(numero)    
    return numero
