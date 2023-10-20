import random


def crear_jugadores(cantidad_jugadores) -> list[dict]:
    """
        PRE: Recibe la cantidad de jugadores
        POST: Arma los jugadores en una lista de diccionarios y la devuelve
    """
    jugadores: list[dict] = []
    jugador: dict = {'palitos_retirados': 0, 'pierde_turno': False, 'es_maquina': True}

    for i in range(cantidad_jugadores):
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
        for espacio in range(espacios_vacios):
            print(' ', end='')
        for palito in range(len(piramide[fila])):
            if piramide[fila][palito]['fue_eliminado']:
                print(' ', end=' ')
            elif piramide[fila][palito]['esta_congelado']:
                # TODO usar colored para pintar palitos congelados
                print('|', end=' ')
            elif piramide[fila][palito]['es_rojo']:
                # TODO usar colored para pintar palitos rojos, ver si se puede modificar
                # para mostrarlos solo cuando se los selecciona
                print('|', end=' ')
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


def reacomodar_palitos(palitos_eliminados: list[tuple[int]], piramide: list[list[dict]]) -> list[list[dict]]:
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
                    # Elimino el palito superior. No utilizo el método eliminar_palito ya que en este caso no considero
                    # si está congelado y le seteo valores por default al lugar que queda vacío
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


def eliminar_fila(piramide: list[list[dict]], jugador: dict):
    """
        PRE: Recibe la pirámide a modificar
        POST: Luego de pedir un número de fila, elimina la misma y devuelve la pirámide modificada
    """
    #TODO: agregar logica de cantidad de palitos eliminada por el jugador
    fila: int = 0
    opcion_invalida: bool = True

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
        fila = random.randint(0, len(piramide)-1)
        print(f"Ingrese la fila que desea eliminar (comienza en cero): {fila}")

    contador_eliminados: int = 0
    for palito in piramide[fila]:
        if not palito['esta_congelado']:
            palito['fue_eliminado'] = True
            contador_eliminados += 1
        else:
            print(f'El palito no se puede eliminar porque está congelado')

    jugador['palitos_retirados'] += contador_eliminados

    return piramide, jugador



