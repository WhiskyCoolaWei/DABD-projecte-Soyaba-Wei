import json
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.prescripcio.crearPrescripcio import crearPrescripcio
from gestio_medica.use_cases.prescripcio.consultarPrescripcio import consultarPrescripcioPerCodi
from gestio_medica.use_cases.prescripcio.llistarPrescripcions import llistarPrescripcions

@csrf_exempt
def prescripcioController(request):
    if request.method == 'GET':
        codi_individual = request.GET.get('codi_individual')
        
        if codi_individual:
            try:
                p = consultarPrescripcioPerCodi(codi_individual)
                return JsonResponse({
                    "status": "èxit",
                    "prescripcio": {
                        "codi_prescripcio": p.codi_prescripcio,
                        "codi_tractament": p.codi_tractament,
                        "codi_nacional": p.codi_nacional,
                        "dosi": p.dosi,
                        "frequencia": p.frequencia,
                        "durada": p.durada,
                        "estat": p.estat
                    }
                }, status=200)
            except ValueError as e:
                return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=404)
        
        else:
            try:
                # Recollim els filtres exactes de la URL de medicaments i tractaments
                filtre_codi = request.GET.get('codi_prescripcio')
                filtre_trac = request.GET.get('codi_tractament')
                filtre_nac = request.GET.get('codi_nacional')
                ordenar_per = request.GET.get('ordenar_per')
                num_pagina = request.GET.get('pagina', 1)

                prescripcions_totals = llistarPrescripcions(
                    codi_prescripcio=filtre_codi,
                    codi_tractament=filtre_trac,
                    codi_nacional=filtre_nac,
                    ordenar_per=ordenar_per
                )

                paginator = Paginator(prescripcions_totals, 20)
                
                try:
                    pagina_actual = paginator.page(num_pagina)
                except EmptyPage:
                    pagina_actual = paginator.page(paginator.num_pages)

                llista = []
                for p in pagina_actual.object_list:
                    llista.append({
                        "codi_prescripcio": p.codi_prescripcio,
                        "codi_tractament": p.codi_tractament,
                        "codi_nacional": p.codi_nacional,
                        "dosi": p.dosi,
                        "frequencia": p.frequencia,
                        "durada": p.durada,
                        "estat": p.estat
                    })

                return JsonResponse({
                    "status": "èxit",
                    "prescripcions": llista,
                    "paginacio": {
                        "pagina_actual": pagina_actual.number,
                        "total_pagines": paginator.num_pages,
                        "te_anterior": pagina_actual.has_previous(),
                        "te_seguent": pagina_actual.has_next()
                    }
                }, status=200)
            except Exception as e:
                return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            dades = json.loads(request.body)
            
            nova_p = crearPrescripcio(
                codi_prescripcio=dades['codi_prescripcio'],
                codi_tractament=dades['codi_tractament'],
                codi_nacional=dades['codi_nacional'],
                dosi=dades['dosi'],
                frequencia=dades['frequencia'],
                durada=dades['durada'],
                estat=dades.get('estat', 'activa')
            )
            
            return JsonResponse({
                "status": "èxit",
                "missatge": f"Prescripció {nova_p.codi_prescripcio} guardada correctament."
            }, status=201)
            
        except ValueError as e:
            return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=400)
        except KeyError as e:
            return JsonResponse({"status": "error_validacio", "missatge": f"Falta el camp: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
            
    else:
        return JsonResponse({"status": "error", "missatge": "Mètode no permès"}, status=405)