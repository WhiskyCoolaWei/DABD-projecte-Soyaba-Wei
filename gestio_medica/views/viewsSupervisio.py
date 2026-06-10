import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.supervisio.crearSupervisio import (
    crearSupervisio, supervisorsDe, supervisatsDe)


@csrf_exempt
def supervisioController(request):
    """
    GET  /supervisio/?dni_supervisor=X  → llista supervisats d'un metge
    GET  /supervisio/?dni_supervisat=X  → llista supervisors d'un metge
    POST /supervisio/                   → crear nova relació de supervisió
    """
    if request.method == 'GET':
        try:
            dni_supervisat = request.GET.get('dni_supervisat')
            dni_supervisor = request.GET.get('dni_supervisor')

            if dni_supervisat:
                relacions = supervisorsDe(dni_supervisat)
                llista = [{"dni"    : r.dni_supervisor.dni,
                           "nom"    : r.dni_supervisor.nom,
                           "cognoms": r.dni_supervisor.cognoms}
                          for r in relacions]
                return JsonResponse(
                    {"status": "èxit", "supervisors": llista}, status=200)

            if dni_supervisor:
                relacions = supervisatsDe(dni_supervisor)
                llista = [{"dni"    : r.dni_supervisat.dni,
                           "nom"    : r.dni_supervisat.nom,
                           "cognoms": r.dni_supervisat.cognoms}
                          for r in relacions]
                return JsonResponse(
                    {"status": "èxit", "supervisats": llista}, status=200)

            return JsonResponse(
                {"status": "error",
                 "missatge": "Cal passar dni_supervisat o dni_supervisor."}, status=400)

        except ValueError as e:
            return JsonResponse(
                {"status": "error_negoci", "missatge": str(e)}, status=404)
        except Exception as e:
            return JsonResponse(
                {"status": "error_intern", "missatge": str(e)}, status=500)

    if request.method == 'POST':
        try:
            dades = json.loads(request.body)
            supervisor, supervisat = crearSupervisio(
                dades['dni_supervisor'],
                dades['dni_supervisat'],
            )
            return JsonResponse({
                "status"  : "èxit",
                "missatge": f"{supervisor.nom} ara supervisa a {supervisat.nom}."
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
