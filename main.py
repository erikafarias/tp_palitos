import random

def imprimir_piramide(piramide: list[list[str]]) -> None:
    """
        PRE: Recibe la lista de palitos que forman la pirámide
        POST: Imprime la pirámide centrada
    """
    for fila in range(len(piramide)):
        espacios_vacios: int = len(piramide) - len(piramide[fila])
        for espacio in range(espacios_vacios):
            print(' ', end='')
        for palito in range(len(piramide[fila])):
            print(piramide[fila][palito], end=' ')
        for espacio in range(espacios_vacios - 1):
            print(' ', end='')
        print()

def armar_piramide(cantidad_palitos: int) -> list[list[str]]:
    """
        PRE: Recibe un entero que representa la cantidad total de palitos
        de la pirámide, si el mismo no forma una pirámide perfecta,
        se eliminan los sobrantes
        POST: Devuelve la pirámide perfecta
    """
    piramide: list[list[str]] = []
    fila: int = 0
    palitos_agregados: int = 0
    seguir_agregando: bool = True
    while(seguir_agregando):
        fila_actual = []
        fila += 1
        for palito in range(fila):
            fila_actual.append('|')
            palitos_agregados += 1

        if(palitos_agregados <= cantidad_palitos):
            piramide.append(fila_actual)
        else:
            seguir_agregando = False

    return piramide

def definir_atributos_iniciales(piramide: list[list[str]]) -> list[list[dict]]:
    """
        PRE: Recibe la pirámide formada anteriormente
        POST: Devuelve una nueva lista de listas de diccionarios en los cuales se
        guardan atributos asociados a cada palito
    """
    piramide_con_atributos = []

    for fila in piramide:
        fila_actual = []
        for palito in fila:
            atributos = {
                'es_rojo': False,
                'esta_congelado': False,
                'contador_congelado': 0,
                'fue_eliminado': False
            }
            fila_actual.append(atributos)
        piramide_con_atributos.append(fila_actual)

    return piramide_con_atributos

def contar_palitos(piramide: list[list[str]]) -> int:
    """
        PRE: Recibe una pirámide
        POST: Devuelve la cantidad de palitos que forman esa pirámide
    """
    contador_palitos: int = 0
    for fila in piramide:
        for palito in piramide:
            if palito == '|':
                contador_palitos += 1

    return contador_palitos

def asignar_palitos_rojos(piramide_con_atributos: list[list[dict]], piramide: list[list[str]]) -> list[list[dict]]:
    """
            PRE: Recibe la pirámide y sus atributos con los valores por default
            POST: Modifica los atributos en la pirámide para setear los que corresponden a los palitos rojos
    """
    cantidad_palitos_total: int = contar_palitos(piramide)
    cantidad_palitos_rojos: int = round(cantidad_palitos_total * 0.3)
    palitos_rojos: list[int] = []

    while(len(palitos_rojos) < cantidad_palitos_rojos):
        palito_rojo: int = random.randint(1, cantidad_palitos_total)
        if palito_rojo not in palitos_rojos:
            palitos_rojos.append(palito_rojo)

    contador_palitos: int = 0
    for fila in piramide_con_atributos:
        for palito in fila:
            contador_palitos += 1
            if contador_palitos in palitos_rojos:
                piramide_con_atributos[fila][palito]['es_rojo'] = True

    return piramide_con_atributos

def main() -> None:

    #piramide = [['|'], ['|', '|'], ['|', '|', '|']]
    #piramide2 = [[' '], ['|', '|'], ['|', '|', '|']]
    #piramide3 = [[' '], ['|', ' '], ['|', '|', '|']]



    piramide: list[list[str]] = armar_piramide(13)
    piramide_con_atributos: list[list[dict]] = definir_atributos_iniciales(piramide)

    imprimir_piramide(piramide)
    print(piramide_con_atributos[0][0])


main()
