import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.diagnostic.crearDiagnostic import crearDiagnostic
from gestio_medica.use_cases.diagnostic.consultarDiagnostic import consultarDiagnosticPerCodi

@csrf_exempt
def crearDiagnosticController(request):

    if request.method == 'GET':
        codi = request.GET.get('codi_diagnostic')
        
        if not codi:
            return JsonResponse({"status": "error_validacio", "missatge": "Falta el paràmetre 'codi_diagnostic'"}, status=400)
            
        try:
            d = consultarDiagnosticPerCodi(codi)
            return JsonResponse({
                "status": "èxit",
                "diagnostic": {
                    "codi_diagnostic": d.codi_diagnostic,
                    "codi_cita": d.codi_cita_id,               # Relació amb la Cita
                    "descripcio": d.descripcio,
                }
            }, status=200)
        except ValueError as e:
            return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
        
    if request.method != 'POST':
        return JsonResponse({"status": "error", "missatge": "Mètode no permès"}, status=405)
    
    try:
        dades = json.loads(request.body)
        codi_diagnostic = dades.get('codi_diagnostic')
        descripcio = dades.get('descripcio')
        notes_cliniques = dades.get('notes_cliniques')
        codi_cita = dades.get('codi_cita')

        if not all([codi_diagnostic, descripcio, codi_cita]):
            return JsonResponse({"status": "error_validacio", "missatge": "Falten camps obligatoris"}, status=400)

        ndiagnostic = crearDiagnostic(
            codi_diagnostic=codi_diagnostic,
            descripcio=descripcio,
            notes_cliniques=notes_cliniques,
            codi_cita=codi_cita
        )

        return JsonResponse({
            "status": "èxit",
            "missatge": f"Diagnòstic {ndiagnostic.codi_diagnostic} creat correctament"
        }, status=201)
    
    except ValueError as e:
        return JsonResponse({
            "status": "error_negoci",
            "missatge": str(e)
        }, status=400)
    except KeyError as e:
        return JsonResponse({
            "status": "error_validacio",
            "missatge": f"Falta el camp obligatori: {str(e)}"
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "status": "error_intern",
            "missatge": f"Error intern del servidor: {str(e)}"
        }, status=500)