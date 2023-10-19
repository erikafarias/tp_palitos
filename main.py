import random

def crear_jugadores(cantidad_jugadores) -> list[dict]:
    jugadores: list[dict] = []
    jugador: dict = {'palitos_retirados': 0, 'pierde_turno': False, 'es_maquina': False}

    for i in range(cantidad_jugadores):
        jugadores.append(jugador)

    jugadores[0]['es_maquina'] = True

    return jugadores



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
        POST: Devuelve en una tupla la pirámide reacomodada, rellenando las filas inferiores, y sus nuevos atributos
    """
    for eliminado in palitos_eliminados:
        continuar: bool = True
        for fila in range(len(piramide)):
            for palito in range(len(piramide[fila])):
                if piramide[fila][palito] == '|' and fila <= eliminado[0] and continuar:
                    # Relleno lugar del palito eliminado, también copio los atributos con los valores del nuevo palito
                    piramide[eliminado[0]][eliminado[1]] = '|'
                    piramide_con_atributos[eliminado[0]][eliminado[1]] = piramide_con_atributos[fila][palito].copy()
                    # Elimino el palito superior. No utilizo el método eliminar_palito ya que en este caso no considero
                    # si está congelado y además le seteo los valores por default
                    piramide[fila][palito] = ' '
                    piramide_con_atributos[fila][palito]['es_rojo'] = False
                    piramide_con_atributos[fila][palito]['esta_congelado'] = False
                    piramide_con_atributos[fila][palito]['contador_congelado'] = 0
                    piramide_con_atributos[fila][palito]['fue_eliminado'] = True

                    # Fuerzo la salida del bucle
                    continuar = False

    return piramide_con_atributos, piramide


def agregar_palitos(piramide_con_atributos: list[list[dict]], piramide: list[list[str]], jugador: dict) -> tuple[
    list[list[dict]], list[list[str]]]:
    """
        PRE: Recibe las pirámides a modificar
        POST: Devuelve en una tupla las pirámides con los palitos agregados
    """
    opcion_invalida: bool = True
    palitos_a_agregar: int = 0

    if not jugador['es_maquina']:
        while opcion_invalida:
            try:
                palitos_a_agregar = int(input("Ingrese la cantidad de palitos a agregar: "))
                if palitos_a_agregar < 1:
                    print('La cantidad ingresada no es válida. Debe ser un número entero mayor o igual a uno')
                else:
                    opcion_invalida = False
            except ValueError:
                print('Debe ingresar un número entero mayor o igual a uno')
    else:
        palitos_a_agregar = random.randint(1, 60)
        print(f"Ingrese la cantidad de palitos a agregar: {palitos_a_agregar}")

    palitos_agregados: int = 0
    for fila in range(len(piramide) - 1, -1, -1):
        for palito in range(len(piramide[fila]) - 1, -1, -1):
            if piramide[fila][palito] == ' ' and palitos_agregados < palitos_a_agregar:
                piramide[fila][palito] = '|'
                piramide_con_atributos[fila][palito]['fue_eliminado'] = False
                palitos_agregados += 1
    print(f'Se agregaron {palitos_agregados} palitos a la pirámide')
    imprimir_piramide(piramide)

    return piramide_con_atributos, piramide


def congelar_palitos(piramide_con_atributos: list[list[dict]], piramide: list[list[str]]) -> tuple[list[list[dict]], list[list[str]]]:
    """
        PRE: Recibe las pirámides a modificar
        POST: Devuelve las pirámides con el 20% de los palitos congelados
    """
    cantidad_palitos: int = contar_palitos(piramide)
    porcentaje: int = round(cantidad_palitos * 0.2)
    palitos_a_congelar = porcentaje if porcentaje >= 1 else 1

    palitos_congelados: list[int] = []

    while (len(palitos_congelados) < palitos_a_congelar):
        palito_congelado: int = random.randint(1, cantidad_palitos)
        if palito_congelado not in palitos_congelados:
            palitos_congelados.append(palito_congelado)

    contador_palitos: int = 0
    for fila in range(len(piramide_con_atributos)):
        for palito in range(len(piramide[fila])):
            contador_palitos += 1
            if contador_palitos in palitos_congelados:
                piramide_con_atributos[fila][palito]['esta_congelado'] = True
                piramide_con_atributos[fila][palito]['contador_congelado'] += 3


    return piramide_con_atributos, piramide


def eliminar_fila(piramide_con_atributos: list[list[dict]], piramide: list[list[str]], jugador: dict):
    """
        PRE: Recibe las pirámides a modificar
        POST: Luego de pedir un número de fila, elimina la misma y devuelve las pirámides modificadas
    """
    #TODO: agregar logica de cantidad de palitos eliminada por el jugador
    fila: int = 0
    if not jugador['es_maquina']:
        while opcion_invalida:
            try:
                fila = int(input("Ingrese la fila que desea eliminar (comienza en cero): "))
                contador: int = 0
                for palito in range(len(piramide[fila])):
                    if piramide[fila][palito] == '|' and not piramide_con_atributos[fila][palito]['esta_congelado']:
                        contador += 1
                if contador < 1:
                    print('La fila ingresada no es válida')
                else:
                    opcion_invalida = False

            except ValueError:
                print('Debe ingresar un número entero, mayor o igual a cero')
    else:
        fila = random.randint(0, len(piramide)-1)
        print(f"Ingrese la fila que desea eliminar (comienza en cero): {fila}")

    for palito in range(len(piramide[fila])):
        if not piramide_con_atributos[fila][palito]['esta_congelado']:
            piramide[fila][palito] = ' '
            piramide_con_atributos[fila][palito]['fue_eliminado'] = True
        else:
            print(f'El palito en la posición [{fila}, {palito}] no se puede eliminar porque está congelado')

    return piramide_con_atributos, piramide

def main() -> None:
    # piramide = [['|'], ['|', '|'], ['|', '|', '|']]
    # piramide2 = [[' '], ['|', '|'], ['|', '|', '|']]
    # piramide3 = [[' '], ['|', ' '], ['|', '|', '|']]
    # jugadores: {list[dict[dict]]} = [
    # {'0': {
    #   palitos_retirados: 0,
    #   pierde_turno: False,
    #   es_maquina: False
    #   }
    # }]

    jugadores: list[dict] = [{'palitos_retirados': 0, 'pierde_turno': False, 'es_maquina': False},
                             {'palitos_retirados': 0, 'pierde_turno': False, 'es_maquina': True}]
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
    agregar_palitos(piramide_con_atributos, piramide, jugadores[1])

    print(piramide_con_atributos)

    ############################################################################
    piramide: list[list[str]] = []
    piramide_con_atributos: list[list[dict]] = []
    #jugadores: list[dict] = []
    cantidad_palitos_inicial: int = 0
    opcion_invalida: bool = True
    cantidad_jugadores: int = 0

    print(f'Bienvenido al juego "estos palitos son un chino".')
    while opcion_invalida:
        try:
            cantidad_jugadores: int = int(input('Para comenzar debe seleccionar la cantidad de jugadores (controlados por '
                                                'la máquina) con los cuales se enfrentará: '))
            if cantidad_jugadores <= 0 or cantidad_jugadores > 8:
                print('Debe seleccionar una cantidad de jugadores mayor o igual a 1 y menor o igual a 8')
            else:
                opcion_invalida: False
        except ValueError:
            print('Debe ingresar un número entero, mayor o igual a 1 y menor o igual a 8')

    jugadores: list[dict] = crear_jugadores(cantidad_jugadores)


main()
