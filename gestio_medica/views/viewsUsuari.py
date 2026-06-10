import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.usuari.crearUsuari  import crearUsuari
from gestio_medica.use_cases.usuari.loginUsuari   import loginUsuari


@csrf_exempt
def usuariController(request):
    if request.method != 'POST':
        return JsonResponse(
            {"status": "error", "missatge": "Mètode no permès"}, status=405)
    try:
        dades = json.loads(request.body)
        nou = crearUsuari(
            email       = dades['email'],
            contrasenya = dades['contrasenya'],
            dni         = dades['dni'],
        )
        return JsonResponse({
            "status"  : "èxit",
            "missatge": f"Usuari {nou.email} creat correctament."
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


@csrf_exempt
def loginController(request):
    if request.method != 'POST':
        return JsonResponse(
            {"status": "error", "missatge": "Mètode no permès"}, status=405)
    try:
        dades    = json.loads(request.body)
        resultat = loginUsuari(dades['email'], dades['contrasenya'])
        return JsonResponse({"status": "èxit", **resultat}, status=200)
    except ValueError as e:
        return JsonResponse(
            {"status": "error_negoci", "missatge": str(e)}, status=401)
    except KeyError as e:
        return JsonResponse(
            {"status": "error_validacio",
             "missatge": f"Falta el camp obligatori: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse(
            {"status": "error_intern", "missatge": str(e)}, status=500)
