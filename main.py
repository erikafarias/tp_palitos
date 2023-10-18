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
    while (seguir_agregando):
        fila_actual = []
        fila += 1
        for palito in range(fila):
            fila_actual.append('|')
            palitos_agregados += 1

        if (palitos_agregados <= cantidad_palitos):
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
        for palito in fila:
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

    while (len(palitos_rojos) < cantidad_palitos_rojos):
        palito_rojo: int = random.randint(1, cantidad_palitos_total)
        if palito_rojo not in palitos_rojos:
            palitos_rojos.append(palito_rojo)

    contador_palitos: int = 0
    for fila in range(len(piramide_con_atributos)):
        for palito in range(len(piramide[fila])):
            contador_palitos += 1
            if contador_palitos in palitos_rojos:
                piramide_con_atributos[fila][palito]['es_rojo'] = True

    return piramide_con_atributos


def eliminar_palito(fila: int, columna: int, piramide_con_atributos: list[list[dict]],
                    piramide: list[list[str]]) -> tuple[list[list[dict]], list[list[str]]]:
    """
        PRE: Recibe la pirámide, sus atributos y las coordenadas donde se quiere eliminar el palito
        POST: Devuelve un booleano que indica si se eliminó correctamente el palito
    """
    try:
        if not piramide_con_atributos[fila][columna]['fue_eliminado']:
            if not piramide_con_atributos[fila][columna]['esta_congelado']:
                piramide_con_atributos[fila][columna]['fue_eliminado'] = True
                piramide[fila][columna] = ' '
            else:
                print('No se puede eliminar el palito seleccionado, está congelado!')
        else:
            print('El palito de esa posición ya fue eliminado. Por favor, seleccione uno válido')
    except IndexError:
        print('La posición seleccionada no es válida.')

    return piramide_con_atributos, piramide


def reacomodar_palitos(palitos_eliminados: list[list[int]], piramide_con_atributos: list[list[dict]],
                       piramide: list[list[str]]) -> tuple[list[list[dict]], list[list[str]]]:
    """
        PRE: Recibe las coordenadas de los palitos eliminados, la pirámide y sus atributos
        POST: Devuelve la pirámide reacomodada y sus atributos en una tupla, rellenando las filas inferiores
    """
    for eliminado in palitos_eliminados:
        continuar: bool = True
        for fila in range(len(piramide)):
            for palito in range(len(piramide[fila])):
                if piramide[fila][palito] == '|' and fila <= eliminado[0] and continuar:

                    # Relleno lugar del palito eliminado, también sus atributos con los valores del nuevo palito
                    piramide[eliminado[0]][eliminado[1]] = '|'
                    piramide_con_atributos[eliminado[0]][eliminado[1]] = piramide_con_atributos[fila][palito].copy()
                    # Elimino el palito superior. No utilizo el método eliminar_palito ya que no considero si está
                    # congelado y además le tengo que setear los valores por default
                    piramide[fila][palito] = ' '
                    piramide_con_atributos[fila][palito]['es_rojo'] = False
                    piramide_con_atributos[fila][palito]['esta_congelado'] = False
                    piramide_con_atributos[fila][palito]['contador_congelado'] = 0
                    piramide_con_atributos[fila][palito]['fue_eliminado'] = True

                    # Fuerzo la salida del bucle
                    continuar = False

    return piramide_con_atributos, piramide


def main() -> None:
    # piramide = [['|'], ['|', '|'], ['|', '|', '|']]
    # piramide2 = [[' '], ['|', '|'], ['|', '|', '|']]
    # piramide3 = [[' '], ['|', ' '], ['|', '|', '|']]

    piramide: list[list[str]] = armar_piramide(13)
    imprimir_piramide(piramide)

    piramide_con_atributos: list[list[dict]] = definir_atributos_iniciales(piramide)
    piramide_con_atributos = asignar_palitos_rojos(piramide_con_atributos, piramide)
    print(piramide_con_atributos)
    eliminar_palito(2, 2, piramide_con_atributos, piramide)
    imprimir_piramide(piramide)
    eliminar_palito(0, 1, piramide_con_atributos, piramide)
    imprimir_piramide(piramide)
    reacomodar_palitos([[2, 2]], piramide_con_atributos, piramide)
    imprimir_piramide(piramide)


    print(piramide_con_atributos)


main()
