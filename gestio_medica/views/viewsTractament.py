import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.tractament.crearTractament import crearTractament
from gestio_medica.use_cases.tractament.consultarTractament import consultarTractament

@csrf_exempt
def consultarTractamentController(request):
    if request.method != 'GET':
        return JsonResponse({"status": "error", "missatge": "Mètode no permès. Requerit GET"}, status=405)
    
    try:
        codi_tractament = request.GET.get('codi_tractament')
        
        if not codi_tractament:
             return JsonResponse({
                 "status": "error_validacio", 
                 "missatge": "Falta el paràmetre obligatori: codi_tractament"
             }, status=400)
        
        dades_tractament = consultarTractament(codi_tractament)
        
        return JsonResponse({
            "status": "èxit",
            "missatge": "Tractament trobat correctament.",
            "data": dades_tractament
        }, status=200) 
        
    except ValueError as e:
        return JsonResponse({
            "status": "error_negoci",
            "missatge": str(e)
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            "status": "error_intern",
            "missatge": f"Error intern del servidor: {str(e)}"
        }, status=500)


@csrf_exempt
def crearTractamentController(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codi_tractament = data.get('codi_tractament')
            data_inici = data.get('data_inici')
            data_fi_prevista = data.get('data_fi_prevista')
            indicacions = data.get('indicacions') 
            codi_diagnostic = data.get('codi_diagnostic')
            
            if not all([codi_tractament, data_inici, data_fi_prevista, codi_diagnostic]):
                return JsonResponse({'status': 'error', 'message': 'Falten camps obligatoris al JSON.'}, status=400)
            

            nou_tractament = crearTractament(
                codi_tractament = codi_tractament,
                data_inici = data_inici,
                data_fi_prevista = data_fi_prevista,
                indicacions = indicacions,
                codi_diagnostic = codi_diagnostic
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Tractament creat correctament.',
                'data': {
                    'codi_tractament': nou_tractament.codi_tractament
                }
            }, status=201)
            
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Format JSON malmès o invàlid.'}, status=400)
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error intern del servidor: {str(e)}'}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Mètode no permès. Requerit POST.'}, status=405)