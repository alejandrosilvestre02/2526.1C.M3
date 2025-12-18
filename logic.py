"""Plantilla con las funciones que el alumnado debe completar para M3.

La capa gráfica llama a estas funciones para mover el estado del juego. No es
necesario crear clases; basta con manipular listas, diccionarios y tuplas.
"""
from __future__ import annotations

import random
from typing import Dict, List, Tuple

STATE_HIDDEN = "hidden"
STATE_VISIBLE = "visible"
STATE_FOUND = "found"

Card = Dict[str, str]
Board = List[List[Card]]
Position = Tuple[int, int]
GameState = Dict[str, object]


def build_symbol_pool(rows: int, cols: int) -> List[str]:
    """Crea la lista de símbolos necesaria para rellenar todo el tablero.

    Sugerencia: parte de un listado básico de caracteres y duplícalo tantas
    veces como parejas necesites. Después baraja el resultado.
    """
    casillas = rows * cols
    if casillas % 2 != 0:
        raise ValueError("El tablero no puede crearse")

    parejas = casillas // 2

    simbolos = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",]

    if parejas > len(simbolos):
        # Repetición de la lista de simbolos
        multiplier = (parejas + len(simbolos) - 1) // len(simbolos)
        symbols = (simbolos * multiplier)[:parejas]
    else:
        symbols = simbolos[:parejas]

    total_casillas = []
    # Duplica los símbolos para tener las parejas
    for s in symbols:
        total_casillas.append(s)
        total_casillas.append(s)

    random.shuffle(total_casillas)
    return total_casillas


def create_game(rows: int, cols: int) -> GameState:
    """Genera el diccionario con el estado inicial del juego.

    El estado debe incluir:
    - ``board``: lista de listas con cartas (cada carta es un dict con
      ``symbol`` y ``state``).
    - ``pending``: lista de posiciones descubiertas en el turno actual.
    - ``moves``: contador de movimientos realizados.
    - ``matches``: parejas acertadas.
    - ``total_pairs``: número total de parejas disponibles.
    - ``rows`` / ``cols``: dimensiones del tablero.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("Filas y columnas deben ser positivas")

    tablero = build_symbol_pool(rows, cols)
    board = []
    it = iter(tablero)
    for r in range(rows):
        row = []
        for c in range(cols):
            symbol = next(it)
            card: Card = {"symbol": symbol, "state": STATE_HIDDEN}
            row.append(card)
        board.append(row)

    game = {
        "board": board,
        "pending": [],
        "moves": 0,
        "matches": 0,
        "total_pairs": (rows * cols) // 2,
        "rows": rows,
        "cols": cols,
    }
    return game



def reveal_card(game: GameState, row: int, col: int) -> bool:
    """Intenta descubrir la carta ubicada en ``row``, ``col``.

    Debe devolver ``True`` si el estado ha cambiado (es decir, la carta estaba
    oculta y ahora está visible) y ``False`` en cualquier otro caso. No permitas
    dar la vuelta a más de dos cartas simultáneamente.
    """
    board = game.get("board", [])
    rows = len(board)
    cols = len(board[0]) if rows else 0

    if not (0 <= row < rows and 0 <= col < cols):
        return False

    card = board[row][col]
    state = card.get("state")

    pending = game.get("pending", [])

    # Si la carta es visible o ya está encotrada, no se le da la vuelta
    # Solo se pueden ver dos cartas por turno
    # Cada posicion solo se añade una vez
    if state == STATE_FOUND or state == STATE_VISIBLE:
        return False
    
    if len(pending) >= 2:
        return False

    pos = (row, col)
    if pos in pending:
        return False

    card["state"] = STATE_VISIBLE
    pending.append(pos)
    game["pending"] = pending
    return True



def resolve_pending(game: GameState) -> Tuple[bool, bool]:
    """Resuelve el turno si hay dos cartas pendientes.

    Devuelve una tupla ``(resuelto, pareja_encontrada)``. Este método debe
    ocultar las cartas si son diferentes o marcarlas como ``found`` cuando
    coincidan. Además, incrementa ``moves`` y ``matches`` según corresponda.
    """

    pending = game.get("pending", [])

    (r1, c1), (r2, c2) = pending
    board: Board = game.get("board", [])
    card1 = board[r1][c1]
    card2 = board[r2][c2]

    # Sacamos los símbolos de ambas cartas
    symbol1 = card1.get("symbol")
    symbol2 = card2.get("symbol")

    game["moves"] = int(game.get("moves", 0)) + 1

    if symbol1 == symbol2:
        card1["state"] = STATE_FOUND
        card2["state"] = STATE_FOUND
        game["matches"] = int(game.get("matches", 0)) + 1
        game["pending"] = []
        return True, True

    # No coinciden, se ocultan
    card1["state"] = STATE_HIDDEN
    card2["state"] = STATE_HIDDEN
    game["pending"] = []
    return True, False


def has_won(game: GameState) -> bool:
    """Indica si se han encontrado todas las parejas."""
    matches = int(game.get("matches", 0))
    total = int(game.get("total_pairs", 0) or 0)
    return total > 0 and matches >= total
