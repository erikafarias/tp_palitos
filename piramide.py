import random
from colored import Fore, Back, Style
import os
import time

def crear_jugadores(cantidad_jugadores) -> list[dict]:
    """
        PRE: Recibe la cantidad de jugadores
        POST: Arma los jugadores en una lista de diccionarios y la devuelve
    """
    jugadores: list[dict] = []
    jugador: dict = {'palitos_retirados': 0,
                     'pierde_turno': False,
                     'es_maquina': True
                     }

    for i in range(cantidad_jugadores):
        jugador['numero_jugador'] = i
        jugadores.append(jugador.copy())

    jugadores[0]['es_maquina'] = False

    return jugadores


def armar_piramide(cantidad_palitos: int) -> list[list[dict]]:
    """
        PRE: Recibe un entero que representa la cantidad total de palitos
        de la pirámide, si el mismo no forma una pirámide perfecta,
        se eliminan los sobrantes
        POST: Devuelve la pirámide perfecta
    """
    piramide: list[list[dict]] = []
    fila: int = 0
    palitos_agregados: int = 0
    seguir_agregando: bool = True
    while seguir_agregando:
        fila_actual = []
        fila += 1
        for palito in range(fila):
            atributos = {
                'es_rojo': False,
                'esta_congelado': False,
                'contador_congelado': 0,
                'fue_eliminado': False
            }
            fila_actual.append(atributos)
            palitos_agregados += 1

        if palitos_agregados <= cantidad_palitos:
            piramide.append(fila_actual)
        else:
            seguir_agregando = False

    return piramide


def imprimir_piramide(piramide: list[list[dict]]) -> None:
    """
        PRE: Recibe la pirámide
        POST: Imprime la pirámide con palitos centrada
    """

    for fila in range(len(piramide)):
        espacios_vacios: int = len(piramide) - len(piramide[fila])
        print(f'{fila} ', end=' ')
        for espacio in range(espacios_vacios):
            print(' ', end='')
        for palito in range(len(piramide[fila])):
            if piramide[fila][palito]['fue_eliminado']:
                print(' ', end=' ')
            elif piramide[fila][palito]['esta_congelado']:
                print(f'{Fore.blue}|{Style.reset}', end=' ')
            elif piramide[fila][palito]['es_rojo']:
                print(f'{Fore.red}|{Style.reset}', end=' ')
            else:
                print('|', end=' ')
        for espacio in range(espacios_vacios - 1):
            print(' ', end='')
        print()


def contar_palitos(piramide: list[list[dict]]) -> int:
    """
        PRE: Recibe una pirámide
        POST: Devuelve la cantidad de palitos que forman esa pirámide
    """
    contador_palitos: int = 0
    for fila in piramide:
        for palito in fila:
            if not palito['fue_eliminado']:
                contador_palitos += 1

    return contador_palitos

def obtener_posicion_palitos(piramide: list[list[dict]]) -> list[list[int]]:
    palitos: list[list[int]] = []
    for fila in range(len(piramide)):
        for columna in range(len(piramide[fila])):
            if not piramide[fila][columna]['fue_eliminado']:
                palitos.append([fila, columna])

    return palitos

def contar_congelados(piramide: list[list[dict]]) -> int:
    contador_congelados: int = 0
    for fila in piramide:
        for palito in fila:
            if palito['esta_congelado']:
                contador_congelados += 1

    return contador_congelados




def asignar_palitos_rojos(piramide: list[list[dict]]) -> list[list[dict]]:
    """
            PRE: Recibe la pirámide con los valores por default
            POST: Modifica los atributos para setear los que corresponden a los palitos rojos
    """
    cantidad_palitos_total: int = contar_palitos(piramide)
    cantidad_palitos_rojos: int = round(cantidad_palitos_total * 0.3)
    palitos_rojos: list[int] = []

    while (len(palitos_rojos) < cantidad_palitos_rojos):
        palito_rojo: int = random.randint(1, cantidad_palitos_total)
        if palito_rojo not in palitos_rojos:
            palitos_rojos.append(palito_rojo)

    contador_palitos: int = 0
    for fila in range(len(piramide)):
        for palito in range(len(piramide[fila])):
            contador_palitos += 1
            if contador_palitos in palitos_rojos:
                piramide[fila][palito]['es_rojo'] = True

    return piramide


def eliminar_palito(piramide: list[list[dict]], jugador: dict) -> tuple[list[list[dict]], dict, list[int]]:
    """
        PRE: Recibe la pirámide y el jugador que va a eliminar el palito
        POST: Devuelve el palito eliminado, la piramide y el jugador con su contador de palitos eliminados +1
    """
    fila: int = 0
    columna: int = 0
    palito_eliminado: list[int] = []
    invalido: bool = True

    while invalido:
        if not jugador['es_maquina']:
            try:
                fila = int(input("Ingrese la fila donde se encuentra el palito a eliminar: "))
                columna = int(input("Ingrese la columna donde se encuentra el palito a eliminar: "))
            except ValueError:
                print('Debe ingresar un número entero')
        else:
            palitos_disponibles: list[list[int]] = obtener_posicion_palitos(piramide)
            numero: int = random.randint(0, len(palitos_disponibles)-1)
            palito_maquina: list[int] = palitos_disponibles[numero]
            fila: int = palito_maquina[0]
            columna: int = palito_maquina[1]

        try:
            if not piramide[fila][columna]['fue_eliminado']:
                if not piramide[fila][columna]['esta_congelado']:
                    piramide[fila][columna]['fue_eliminado'] = True
                    jugador['palitos_retirados'] += 1
                    palito_eliminado.append(fila)
                    palito_eliminado.append(columna)
                    print(f'Se eliminó el palito en la posición {fila},{columna}')
                    invalido = False
                else:
                    print('No se puede eliminar el palito seleccionado, está congelado!')
            else:
                print('El palito de esa posición ya fue eliminado. Por favor, seleccione uno válido')
        except IndexError:
            print('La posición seleccionada no es válida.')


    return piramide, jugador, palito_eliminado


def reacomodar_palitos(palitos_eliminados: list[list[int]], piramide: list[list[dict]]) -> list[list[dict]]:
    """
        PRE: Recibe las coordenadas de los palitos eliminados y la pirámide
        POST: Devuelve la pirámide reacomodada. Los palitos que se mueven conservan sus atributos
    """
    for eliminado in palitos_eliminados:
        continuar: bool = True
        for fila in range(len(piramide)):
            for palito in range(len(piramide[fila])):
                if not piramide[fila][palito]['fue_eliminado'] and fila <= eliminado[0] and continuar:
                    # Relleno lugar del palito eliminado, también copio los atributos con los valores del nuevo palito
                    piramide[eliminado[0]][eliminado[1]] = piramide[fila][palito].copy()
                    # Elimino el palito superior.
                    piramide[fila][palito]['es_rojo'] = False
                    piramide[fila][palito]['esta_congelado'] = False
                    piramide[fila][palito]['contador_congelado'] = 0
                    piramide[fila][palito]['fue_eliminado'] = True

                    # Una vez reacomodado el palito, no vuelve a entrar a la condición
                    continuar = False

    return piramide


def agregar_palitos(piramide: list[list[dict]], jugador: dict) -> list[list[dict]]:
    """
        PRE: Recibe la pirámide y el jugador (para saber si es la máquina)
        POST: Devuelve la pirámide con los palitos agregados
    """
    opcion_invalida: bool = True
    palitos_a_agregar: int = 0

    if not jugador['es_maquina']:
        while opcion_invalida:
            try:
                palitos_a_agregar = int(input('Ingrese la cantidad de palitos a agregar (de superarse la cantidad'
                                              ' inicial, se elimina el excedente): '))
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
            if piramide[fila][palito]['fue_eliminado'] and palitos_agregados < palitos_a_agregar:
                piramide[fila][palito]['fue_eliminado'] = False
                palitos_agregados += 1
    print(f'Se agregaron {palitos_agregados} palitos a la pirámide')
    imprimir_piramide(piramide)

    return piramide


def congelar_palitos(piramide: list[list[dict]]) -> list[list[dict]]:
    """
        PRE: Recibe la pirámide a modificar
        POST: Devuelve la pirámide con el 20% de los palitos congelados
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
    for fila in range(len(piramide)):
        for palito in range(len(piramide[fila])):
            contador_palitos += 1
            if contador_palitos in palitos_congelados:
                piramide[fila][palito]['esta_congelado'] = True
                piramide[fila][palito]['contador_congelado'] += 3

    return piramide


def eliminar_fila(piramide: list[list[dict]], jugador: dict) -> tuple[list[list[dict]], dict, list[list[int]]]:
    """
        PRE: Recibe la pirámide a modificar
        POST: Luego de pedir un número de fila, elimina la misma y devuelve la pirámide modificada
    """
    fila: int = 0
    opcion_invalida: bool = True
    contador_eliminados: int = 0
    palitos_eliminados: list[list[int]] = []

    if contar_palitos(piramide) == contar_congelados(piramide):
        print("Solo quedan palitos congelados! Se saltea turno")
    else:
        if not jugador['es_maquina']:
            while opcion_invalida:
                try:
                    fila = int(input("Ingrese la fila que desea eliminar (comienza en cero): "))
                    contador: int = 0
                    for palito in piramide[fila]:
                        if not palito['fue_eliminado'] and not palito['esta_congelado']:
                            contador += 1
                    if contador < 1:
                        print('La fila ingresada no es válida')
                    else:
                        opcion_invalida = False

                except ValueError:
                    print('Debe ingresar un número entero, mayor o igual a cero')

        else:
            fila = random.randint(0, len(piramide) - 1)
            print(f"Ingrese la fila que desea eliminar (comienza en cero): {fila}")


        for palito in range(len(piramide[fila])):
            if not piramide[fila][palito]['esta_congelado']:
                piramide[fila][palito]['fue_eliminado'] = True
                palitos_eliminados.append([fila, palito])
                contador_eliminados += 1
            else:
                print(f'El palito no se puede eliminar porque está congelado')

        jugador['palitos_retirados'] += contador_eliminados

    return piramide, jugador, palitos_eliminados

def limpiar_consola() -> None:
    """
    Método utilizado para limpiar la consola
    """
    if os.name == 'nt':  #Windows
        os.system('cls')
    elif os.name == 'posix':  #Linux
        os.system('clear')

def jugar_turno(piramide: list[list[dict]], jugador: dict, cantidad_palitos_inicial: int) -> tuple[list[list[dict]], dict]:
    """
        PRE: Recibe la pirámide, sus atributos y el jugador que va a jugar su turno
        POST: Devuelve los mismos datos, con las modificaciones que se le hayan hecho durante el turno
    """

    cantidad_palitos_a_eliminar: int = 0
    opcion_invalida: bool = True
    if not jugador['pierde_turno']:
        if not jugador['es_maquina']:
            print(f"Es tu turno de jugar:")
            imprimir_piramide(piramide)
            while opcion_invalida:
                try:
                    cantidad_palitos_a_eliminar = int(input('Ingrese la cantidad de palitos que quiere eliminar. '
                                                                 'Debe estar entre 1 y 3: '))
                    if cantidad_palitos_a_eliminar < 1 or cantidad_palitos_a_eliminar > 3:
                        print('Debe seleccionar una cantidad de palitos a eliminar entre 1 y 3')
                    else:
                        opcion_invalida = False
                except ValueError:
                    print('Debe ingresar un número entero, entre 1 y 3')
        else:
            print(f"Es turno del jugador Bot{jugador['numero_jugador']}")
            cantidad_palitos_a_eliminar = random.randint(1, 3)

        palitos_eliminados: list[list[int]] = []
        evento_disparado: bool = False
        for palito in range(cantidad_palitos_a_eliminar):
            if contar_palitos(piramide) == contar_congelados(piramide):
                print("Solo quedan palitos congelados! Se saltea turno")
            else:
                piramide, jugador, palito_eliminado = eliminar_palito(piramide, jugador)
                imprimir_piramide(piramide)
                palitos_eliminados.append(palito_eliminado)
                if contar_palitos(piramide) == 0:
                    if jugador['numero_jugador'] != 0:
                        print(f"Sacaste el último palito. El jugador Bot{jugador['numero_jugador']} es el perdedor!")
                    else:
                        print('Sacaste el último palito. Perdiste!')
                        palito = cantidad_palitos_a_eliminar
                else:
                    if not evento_disparado and piramide[palito_eliminado[0]][palito_eliminado[1]]['es_rojo']:
                        evento: int = random.randint(1, 6)
                        print('Eliminaste un palito rojo! Se dispara evento al azar. Tirando dado...')
                        print(f'Te tocó el número {evento}. ', end='')
                        print('Reacomodando palitos antes del evento...')
                        piramide = reacomodar_palitos(palitos_eliminados, piramide)
                        imprimir_piramide(piramide)
                        palitos_eliminados = []

                        if evento == 1:
                            print('El jugador pierde un turno')
                            jugador['pierde_turno'] = True
                        elif evento == 2:
                            print('Se dispara evento: "Agregar palitos"')
                            piramide = agregar_palitos(piramide, jugador)
                            imprimir_piramide(piramide)
                        elif evento == 3:
                            print('Se dispara evento: "Congelar palitos". Se congela el 20% de los palitos')
                            piramide = congelar_palitos(piramide)
                            imprimir_piramide(piramide)
                        elif evento == 4:
                            piramide, jugador, palitos_eliminados = eliminar_fila(piramide, jugador)
                            imprimir_piramide(piramide)
                            print('Reacomodando palitos...')
                            piramide = reacomodar_palitos(palitos_eliminados, piramide)
                            imprimir_piramide(piramide)
                        elif evento == 5:
                            print('Armamos una nueva pirámide del tamaño de la original')
                            piramide = armar_piramide(cantidad_palitos_inicial)
                            piramide = asignar_palitos_rojos(piramide)
                            imprimir_piramide(piramide)
                        elif evento == 6:
                            print('Safaste! No hace nada')

                        evento_disparado = True
                    else:
                        print('Reacomodando palitos...')
                        piramide = reacomodar_palitos(palitos_eliminados, piramide)
                        imprimir_piramide(piramide)
    else:
        print('Se saltea turno por evento de la ronda anterior')
        jugador['pierde_turno'] = False

    for fila in piramide:
        for palito in fila:
            if palito['contador_congelado'] != 0:
                palito['contador_congelado'] -= 1
                if palito['contador_congelado'] == 0:
                    palito['esta_congelado'] = False

    return piramide, jugador


def main() -> None:
    cantidad_palitos_inicial: int = 0
    opcion_invalida: bool = True
    cantidad_jugadores: int = 0

    print(f'Bienvenido al juego "estos palitos son un chino".')
    while opcion_invalida:
        try:
            cantidad_jugadores: int = int(
                input('Para comenzar debe seleccionar la cantidad de jugadores (controlados por '
                      'la máquina) con los cuales se enfrentará: '))
            cantidad_jugadores += 1
            if cantidad_jugadores <= 0 or cantidad_jugadores > 8:
                print('Debe seleccionar una cantidad de jugadores mayor o igual a 1 y menor o igual a 8')
            else:
                opcion_invalida = False
        except ValueError:
            print('Debe ingresar un número entero, mayor o igual a 1 y menor o igual a 8')

    jugadores: list[dict] = crear_jugadores(cantidad_jugadores)

    continuar: bool = True
    while continuar:
        cantidad_palitos_minima = round(((cantidad_jugadores + 2) * (cantidad_jugadores * 3)) / 2)
        try:
            print(f'Puede jugar con la cantidad mínima de palitos o elegir una nueva. '
                  f'Si desea elegir la cantidad, ingrese el número deseado, el mismo se ajustará '
                  f'para formar una pirámide perfecta. De lo contrario, ingrese {cantidad_palitos_minima}')
            cantidad_palitos_inicial = int(input('Por favor, ingrese la cantidad de palitos con la que desea jugar: '))
            if cantidad_palitos_minima > cantidad_palitos_inicial:
                print(f'Debe seleccionar una cantidad mayor o igual a {cantidad_palitos_minima}')
            else:
                continuar = False
        except ValueError:
            print(f'Debe ingresar un número entero, mayor o igual a {cantidad_palitos_minima}')

    piramide = armar_piramide(cantidad_palitos_inicial)
    piramide = asignar_palitos_rojos(piramide)
    imprimir_piramide(piramide)

    seguir_jugando: bool = True

    while (seguir_jugando):
            #Espera 20 segundos antes de limpiar la consola y empezar la siguiente ronda
            time.sleep(20)
            limpiar_consola()
            for jugador in range(cantidad_jugadores):
                if contar_palitos(piramide) == 0:
                    seguir_jugando = False
                else:
                    piramide, jugadores[jugador] = jugar_turno(piramide, jugadores[jugador], cantidad_palitos_inicial)


    mayor_cantidad_palitos: int = 0
    jugador_ganador: int = 0

    for jugador in range(cantidad_jugadores):
        print(f'El jugador {jugador} retiró {jugadores[jugador]["palitos_retirados"]} palitos')
        if jugadores[jugador]["palitos_retirados"] > mayor_cantidad_palitos:
            mayor_cantidad_palitos = jugadores[jugador]["palitos_retirados"]
            jugador_ganador = jugador
    print(f'El jugador que más palitos retiró es el número {jugador_ganador} con {mayor_cantidad_palitos} palitos eliminados')
    print('---------FIN DEL JUEGO-----------')


main()
