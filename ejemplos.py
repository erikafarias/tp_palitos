#Ejemplo piramide con dos palitos y 2 jugadores

piramide: list[list[dict]] = [
    [{'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False}],
    [{'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False},
     {'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False}],
    [{'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False},
     {'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False},
     {'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False}],
    [{'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False},
     {'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False},
     {'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False},
     {'es_rojo': False,'esta_congelado': False, 'contador_congelado': 0, 'fue_eliminado': False}]]


jugadores: list[dict] = [
    {'palitos_retirados': 0, 'pierde_turno': False, 'es_maquina': False, 'numero_jugador': 0},
    {'palitos_retirados': 0, 'pierde_turno': False, 'es_maquina': True, 'numero_jugador': 1}
]

