from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.historialClinic.consultarHistorialClinic import consultarHistorialClinic
from gestio_medica.models import Diagnostic, Tractament

@csrf_exempt
def historialClinicController(request):
    if request.method == 'GET':
        dni = request.GET.get('dni')
        dni_metge = request.GET.get('dni_metge') # Capturamos el filtro del médico
        
        if not dni:
            return JsonResponse({"status": "error", "missatge": "Falta el DNI del pacient."}, status=400)
            
        try:
            # Enviamos ambos parámetros al caso de uso
            historial, cites = consultarHistorialClinic(
                dni_pacient=dni.strip().upper(), 
                dni_metge=dni_metge.strip().upper() if dni_metge else None
            )
            
            # (El resto del bucle de construcción del JSON se queda exactamente IGUAL)
            registre_cites = []
            for cita in cites:
                diagnostics_de_cita = Diagnostic.objects.filter(codi_cita=cita)
                llista_diagnostics = []
                for diag in diagnostics_de_cita:
                    tractaments_de_diag = Tractament.objects.filter(diagnostic=diag)
                    llista_tractaments = []
                    for trac in tractaments_de_diag:
                        llista_tractaments.append({
                            "codi_tractament": trac.codi_tractament,
                            "data_inici": trac.data_inici.strftime('%d/%m/%Y'),
                            "data_fi_prevista": trac.data_fi_prevista.strftime('%d/%m/%Y'),
                            "indicacions": trac.indicacions
                        })
                    llista_diagnostics.append({
                        "codi_diagnostic": diag.codi_diagnostic,
                        "descripcio": diag.descripcio,
                        "notes_cliniques": diag.notes_cliniques,
                        "tractaments": llista_tractaments
                    })
                registre_cites.append({
                    "codi_cita": cita.codi_cita,
                    "data": cita.data.strftime('%d/%m/%Y'),
                    "hora": cita.hora.strftime('%H:%M'),
                    "estat": cita.estat,
                    "dni_metge": cita.dni_metge_id,
                    "diagnostics": llista_diagnostics
                })
            
            return JsonResponse({
                "status": "èxit",
                "historial": {
                    "codi_historial": historial.codi_historial,
                    "dni_pacient": historial.dni_pacient_id,
                    "nom_pacient": f"{historial.dni_pacient.nom} {historial.dni_pacient.cognoms}",
                    "allergies": historial.allergies or "Cap coneguda",
                    "grup_sanguini": historial.grup_sanguini or "No informat",
                    "antecedents": historial.antecedents or "Sense antecedents d'interès",
                    "malalties_croniques": historial.malalties_croniques or "Cap"
                },
                "historial_clinic_complet": registre_cites
            }, status=200)
            
        except ValueError as e:
            return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
            
    return JsonResponse({"status": "error", "missatge": "Mètode no permès."}, status=405)