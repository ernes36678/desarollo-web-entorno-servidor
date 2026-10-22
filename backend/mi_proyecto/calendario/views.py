from datetime import datetime

from django.shortcuts import render


MESES = (
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
)

DIAS = (
    'lunes',
    'martes',
    'miércoles',
    'jueves',
    'viernes',
    'sábado',
    'domingo',
)


def calendario(request, fecha):
    try:
        fecha_usuario = datetime.strptime(fecha, '%d-%m-%Y').date()
        if fecha_usuario.strftime('%d-%m-%Y') != fecha:
            raise ValueError
    except ValueError:
        return render(
            request,
            'calendario/error.html',
            {'fecha': fecha, 'formato': 'DD-MM-AAAA'},
            status=400,
        )

    return render(
        request,
        'calendario/fecha.html',
        {
            'dia': fecha_usuario.day,
            'mes': MESES[fecha_usuario.month - 1],
            'ano': fecha_usuario.year,
            'mensaje': DIAS[fecha_usuario.weekday()],
        },
    )
