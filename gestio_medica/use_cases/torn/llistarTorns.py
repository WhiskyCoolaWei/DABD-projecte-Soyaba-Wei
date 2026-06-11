from datetime import date
from django.db import connection
from gestio_medica.models import Torn


def llistarTornsDe(dni_metge: str):
    avui = date.today()

    torns = list(
        Torn.objects
        .filter(dni_metge=dni_metge, data_fi__gte=avui)
        .select_related('codi_centre')
        .order_by('codi_centre', 'dia_setmana')
    )

    if not torns:
        return []

    centres_ids = list(set(t.codi_centre_id for t in torns))

    # Sala on el metge TÉ l'especialitat requerida (evita RS8)
    with connection.cursor() as cursor:
        placeholders = ','.join(['%s'] * len(centres_ids))
        cursor.execute(
            f"""SELECT DISTINCT ON (c.codi_centre) c.codi_centre, c.codi_sala
                FROM consulta c
                JOIN metgeespecialitat me ON c.codi_especialitat = me.codi_especialitat
                WHERE c.codi_centre IN ({placeholders})
                AND me.dni = %s
                ORDER BY c.codi_centre, c.codi_sala""",
            centres_ids + [dni_metge]
        )
        salas = {row[0]: row[1] for row in cursor.fetchall()}

    resultat = []
    for t in torns:
        cid = t.codi_centre_id
        if cid not in salas:
            continue
        resultat.append({
            'codi_torn'  : t.codi_torn,
            'codi_centre': cid,
            'nom_centre' : t.codi_centre.nom,
            'dia_nom'    : str(t.dia_setmana),
            'hora_inici' : t.hora_inici.strftime('%H:%M'),
            'hora_fi'    : t.hora_fi.strftime('%H:%M'),
            'data_fi'    : str(t.data_fi),
            'codi_sala'  : salas[cid],
        })
    return resultat
