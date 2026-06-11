from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.torn.llistarTorns import llistarTornsDe


@csrf_exempt
def tornController(request):
    """GET /torns/?dni_metge=X"""
    if request.method != 'GET':
        return JsonResponse({"status": "error", "missatge": "Metode no permes"}, status=405)

    dni_metge = request.GET.get('dni_metge')
    if not dni_metge:
        return JsonResponse({"status": "error_validacio", "missatge": "Falta el parametre dni_metge"}, status=400)

    try:
        torns = llistarTornsDe(dni_metge.strip().upper())
        return JsonResponse({"status": "exit", "torns": torns}, status=200)
    except ValueError as e:
        return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
