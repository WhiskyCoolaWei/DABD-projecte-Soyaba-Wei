from django.db import connection


def pacientsDeMedic(dni_metge: str):
    """Pacients que han tingut cites finalitzades amb aquest metge."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT ON (c.dni_pacient)
                   c.dni_pacient,
                   p.nom,
                   p.cognoms,
                   p.telefon,
                   c.data AS ultima_cita
            FROM cita c
            JOIN persona p ON c.dni_pacient = p.dni
            WHERE c.dni_metge = %s
              AND c.estat = 'finalitzada'
            ORDER BY c.dni_pacient, c.data DESC
        """, [dni_metge])
        rows = cursor.fetchall()

    return [
        {
            'dni'        : row[0],
            'nom'        : row[1],
            'cognoms'    : row[2],
            'telefon'    : row[3],
            'ultima_cita': str(row[4]) if row[4] else ''
        }
        for row in rows
    ]
