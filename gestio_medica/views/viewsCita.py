import json
import random
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.cita.crearCita import crearCita
from gestio_medica.use_cases.cita.consultarCita import consultarCita

@csrf_exempt
def crearCitaController(request):

    if request.method == 'GET':
        codi_cita = request.GET.get('codi_cita')
        
        if not codi_cita:
            return JsonResponse({"status": "error_validacio", "missatge": "Falta el paràmetre codi_cita"}, status=400)
            
        try:
            cita = consultarCita(codi_cita)
            return JsonResponse({
                "status": "èxit",
                "cita": {
                    "codi_cita": cita.codi_cita,
                    "data": str(cita.data),
                    "hora": str(cita.hora),
                    "estat": cita.estat,
                    "dni_metge": cita.dni_metge.dni,
                    "dni_pacient": cita.dni_pacient,
                    "codi_centre": cita.codi_centre,
                    "codi_sala": cita.codi_sala
                }
            }, status=200)
        except ValueError as e:
            return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
        

    elif request.method != 'POST':
        return JsonResponse({"status": "error", "missatge": "Mètode no permès"}, status=405)
    
    try:
        dades = json.loads(request.body)
        codi_cita = f"CT{timestamp}{random.randint(10, 99)}"
        
        data_str = dades.get('data')
        hora_str = dades.get('hora')
        dni_pacient = dades.get('dni_pacient')
        dni_metge = dades.get('dni_metge')
        codi_centre = dades.get('codi_centre')
        codi_sala = dades.get('codi_sala', 'SALA-GEN')
        estat = 'pendent'

        if not all([codi_cita, data_str, hora_str, estat, dni_metge, dni_pacient, codi_centre, codi_sala]):
            return JsonResponse({"status": "error_validacio", "missatge": "Falten camps obligatoris"}, status=400)

        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        hora = datetime.strptime(hora_str, "%H:%M").time()

        ncita = crearCita(
            codi_cita=codi_cita,
            data=data,
            hora=hora,
            estat=estat,
            dni_metge=dni_metge,
            dni_pacient=dni_pacient,
            codi_centre=codi_centre,
            codi_sala=codi_sala
        )

        return JsonResponse({
            "status": "èxit",
            "missatge": f"Reserva realitzada. Codi de seguiment: {ncita.codi_cita}",
            "codi_cita": ncita.codi_cita
        }, status=201)
    
    except ValueError as e:
        return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)