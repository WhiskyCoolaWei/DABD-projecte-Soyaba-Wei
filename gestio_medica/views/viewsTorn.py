from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.torn.tornsDelMetge import tornsDelMetge


@csrf_exempt
def tornController(request):
    if request.method == 'GET':
        dni_metge   = request.GET.get('dni_metge')
        codi_centre = request.GET.get('codi_centre')
        if not dni_metge:
            return JsonResponse(
                {"status": "error_validacio",
                 "missatge": "Falta dni_metge"}, status=400)
        try:
            torns = tornsDelMetge(dni_metge, codi_centre)
            llista = [{
                "codi_torn"  : t.codi_torn,
                "dia_nom"    : t.dia_setmana,
                "hora_inici" : str(t.hora_inici)[:5],
                "hora_fi"    : str(t.hora_fi)[:5],
                "data_inici" : str(t.data_inici),
                "data_fi"    : str(t.data_fi),
                "codi_centre": t.codi_centre_id,
                "nom_centre" : t.codi_centre.nom,
            } for t in torns]
            return JsonResponse(
                {"status": "exit", "torns": llista}, status=200)
        except Exception as e:
            return JsonResponse(
                {"status": "error_intern", "missatge": str(e)}, status=500)
    return JsonResponse(
        {"status": "error", "missatge": "Metode no permes"}, status=405)
