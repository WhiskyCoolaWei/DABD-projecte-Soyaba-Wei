import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.malaltia.crearMalaltia    import crearMalaltia
from gestio_medica.use_cases.malaltia.llistarMalalties  import llistarMalalties
from gestio_medica.use_cases.malaltia.associarMalaltia  import (
    associarMalaltiaADiagnostic, malaltiesDeDiagnostic)


@csrf_exempt
def malaltiaController(request):
    if request.method == 'GET':
        try:
            cerca     = request.GET.get('cerca', '')
            malalties = llistarMalalties(cerca)
            llista = [{"codi_cie": m.codi_cie,
                       "nom": m.nom,
                       "descripcio": m.descripcio} for m in malalties]
            return JsonResponse({"status": "èxit", "malalties": llista}, status=200)
        except Exception as e:
            return JsonResponse(
                {"status": "error_intern", "missatge": str(e)}, status=500)

    if request.method == 'POST':
        try:
            dades = json.loads(request.body)
            nova  = crearMalaltia(
                codi_cie   = dades['codi_cie'],
                nom        = dades['nom'],
                descripcio = dades.get('descripcio', ''),
            )
            return JsonResponse({
                "status"  : "èxit",
                "missatge": f"Malaltia '{nova.nom}' creada correctament."
            }, status=201)
        except ValueError as e:
            return JsonResponse(
                {"status": "error_negoci", "missatge": str(e)}, status=400)
        except KeyError as e:
            return JsonResponse(
                {"status": "error_validacio",
                 "missatge": f"Falta el camp obligatori: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse(
                {"status": "error_intern", "missatge": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "missatge": "Mètode no permès"}, status=405)


@csrf_exempt
def associarMalaltiaController(request, codi_diagnostic):
    if request.method == 'GET':
        try:
            relacions = malaltiesDeDiagnostic(codi_diagnostic)
            llista = [{"codi_cie"  : r.malaltia.codi_cie,
                       "nom"       : r.malaltia.nom,
                       "descripcio": r.malaltia.descripcio}
                      for r in relacions]
            return JsonResponse(
                {"status": "èxit", "malalties": llista}, status=200)
        except ValueError as e:
            return JsonResponse(
                {"status": "error_negoci", "missatge": str(e)}, status=404)
        except Exception as e:
            return JsonResponse(
                {"status": "error_intern", "missatge": str(e)}, status=500)

    if request.method == 'POST':
        try:
            dades    = json.loads(request.body)
            malaltia = associarMalaltiaADiagnostic(
                codi_diagnostic, dades['codi_cie'])
            return JsonResponse({
                "status"  : "èxit",
                "missatge": f"Malaltia '{malaltia.nom}' associada al diagnòstic {codi_diagnostic}."
            }, status=201)
        except ValueError as e:
            return JsonResponse(
                {"status": "error_negoci", "missatge": str(e)}, status=400)
        except KeyError as e:
            return JsonResponse(
                {"status": "error_validacio",
                 "missatge": f"Falta el camp obligatori: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse(
                {"status": "error_intern", "missatge": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "missatge": "Mètode no permès"}, status=405)