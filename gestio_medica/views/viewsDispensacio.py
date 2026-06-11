import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.dispensacio.crearDispensacio import crearDispensacio


@csrf_exempt
def dispensacioController(request):
    """POST /dispensacions/ — dispensar un medicament per una prescripcio activa."""

    if request.method != 'POST':
        return JsonResponse({"status": "error", "missatge": "Metode no permes"}, status=405)

    try:
        dades = json.loads(request.body)
        nova  = crearDispensacio(
            codi_centre      = dades['codi_centre'],
            codi_tractament  = dades['codi_tractament'],
            codi_nacional    = dades['codi_nacional'],
            quantitat        = int(dades['quantitat']),
        )
        return JsonResponse({
            "status"          : "exit",
            "missatge"        : f"Medicament dispensat correctament.",
            "codi_dispensacio": nova.codi_dispensacio,
            "data_lliurament" : str(nova.data_lliurament),
        }, status=201)

    except ValueError as e:
        return JsonResponse({"status": "error_negoci",    "missatge": str(e)}, status=400)
    except KeyError   as e:
        return JsonResponse({"status": "error_validacio", "missatge": f"Falta el camp: {str(e)}"}, status=400)
    except Exception  as e:
        return JsonResponse({"status": "error_intern",    "missatge": str(e)}, status=500)
