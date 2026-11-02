from ast import literal_eval

from django.http import HttpResponseBadRequest
from django.shortcuts import render


COMBINACIONES_GANADORAS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def tres_en_raya(request):
    terminado = False

    if request.method == 'POST':
        try:
            tablero = literal_eval(request.POST['tablero'])
            turno = request.POST['turno']
            posicion = int(request.POST['posicion'])
        except (KeyError, ValueError, SyntaxError):
            return HttpResponseBadRequest('Datos de jugada no válidos.')

        if (
            not isinstance(tablero, list)
            or len(tablero) != 9
            or any(casilla not in ('-', 'X', 'O') for casilla in tablero)
            or turno not in ('X', 'O')
            or not 0 <= posicion < 9
        ):
            return HttpResponseBadRequest('Datos de jugada no válidos.')

        if tablero[posicion] == '-':
            tablero[posicion] = turno
            ganador = any(
                tablero[a] == tablero[b] == tablero[c] == turno
                for a, b, c in COMBINACIONES_GANADORAS
            )

            if ganador:
                mensaje = f'¡El jugador {turno} ha ganado!'
                terminado = True
            elif '-' not in tablero:
                mensaje = '¡Empate!'
                terminado = True
            else:
                turno = 'O' if turno == 'X' else 'X'
                mensaje = f'Turno de {turno}'
        else:
            mensaje = '¡Casilla ocupada! Elige otra.'
    else:
        tablero = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        turno = 'X'
        mensaje = 'Turno de X'

    contexto = {
        'tablero': tablero,
        'turno': turno,
        'mensaje': mensaje,
        'terminado': terminado,
    }
    return render(request, 'tres_en_raya/tres_en_raya.html', contexto)
