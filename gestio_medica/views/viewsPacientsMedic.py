from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.metge.pacientsDeMedic import pacientsDeMedic


@csrf_exempt
def pacientsMedicController(request):
    """GET /metges/pacients/?dni_metge=X"""
    if request.method != 'GET':
        return JsonResponse({"status": "error", "missatge": "Metode no permes"}, status=405)

    dni_metge = request.GET.get('dni_metge')
    if not dni_metge:
        return JsonResponse({"status": "error_validacio",
                             "missatge": "Falta el parametre dni_metge"}, status=400)
    try:
        pacients = pacientsDeMedic(dni_metge.strip().upper())
        return JsonResponse({"status": "exit", "pacients": pacients}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
