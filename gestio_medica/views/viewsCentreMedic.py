from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.centremedic.llistarCentres import llistarCentres


@csrf_exempt
def centreMedicController(request):
    if request.method == 'GET':
        try:
            centres = llistarCentres()
            llista  = [{"codi_centre": c.codi_centre, "nom": c.nom}
                       for c in centres]
            return JsonResponse({"status": "exit", "centres": llista}, status=200)
        except Exception as e:
            return JsonResponse(
                {"status": "error_intern", "missatge": str(e)}, status=500)
    return JsonResponse(
        {"status": "error", "missatge": "Metode no permes"}, status=405)
