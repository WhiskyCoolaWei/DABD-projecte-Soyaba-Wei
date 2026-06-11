import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.farmacia.consultarEstoc import consultarEstocFarmacia


@csrf_exempt
def farmaciaController(request):
    """GET /farmacies/?codi_centre=X — estoc de medicaments de la farmàcia."""

    if request.method != 'GET':
        return JsonResponse({"status": "error", "missatge": "Metode no permes"}, status=405)

    codi_centre = request.GET.get('codi_centre')
    if not codi_centre:
        return JsonResponse({
            "status": "error_validacio",
            "missatge": "Falta el parametre codi_centre"
        }, status=400)

    try:
        farmacia, estoc = consultarEstocFarmacia(codi_centre.strip().upper())
        llista = [
            {
                "codi_nacional"      : e.codi_nacional_id,
                "nom_comercial"      : e.codi_nacional.nom_comercial,
                "principi_actiu"     : e.codi_nacional.principi_actiu,
                "quantitat_disponible": e.quantitat_disponible
            }
            for e in estoc
        ]
        return JsonResponse({
            "status"     : "exit",
            "codi_centre": codi_centre.upper(),
            "estoc"      : llista
        }, status=200)

    except ValueError as e:
        return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
