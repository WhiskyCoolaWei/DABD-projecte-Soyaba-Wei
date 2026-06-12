import json
import random
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.cita.crearCita import crearCita
from gestio_medica.use_cases.cita.consultarCita import consultarCita
from gestio_medica.use_cases.cita.citesDisponibles import slotsDisponibles
from gestio_medica.use_cases.cita.citesDelMetge import citesDelMetge

# IMPORT EXCLUSIU D'EMERGÈNCIA: Importem el model per fer consultes directes si el cas d'ús no ho cobreix
from gestio_medica.models import Cita 

@csrf_exempt
def crearCitaController(request):

    if request.method == 'GET':
        # 1. CONTROL DE CITES FLOTANTS (Sense metge assignat)
        unassigned = request.GET.get('unassigned')
        if unassigned == 'true':
            try:
                cites_buides = Cita.objects.filter(dni_metge__isnull=True) | Cita.objects.filter(dni_metge='')
                llista = [{
                    "codi_cita"  : c.codi_cita,
                    "data"       : str(c.data),
                    "hora"       : str(c.hora)[:5],
                    "estat"      : c.estat,
                    "dni_pacient": c.dni_pacient,
                    "codi_centre": c.codi_centre
                } for c in cites_buides]
                return JsonResponse({"status": "èxit", "cites": llista}, status=200)
            except Exception as e:
                return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)

        # Slots disponibles per metge+data+centre
        dni_metge   = request.GET.get('dni_metge')
        data_str    = request.GET.get('data')
        codi_centre = request.GET.get('codi_centre')
        if dni_metge and data_str and codi_centre:
            try:
                slots = slotsDisponibles(dni_metge, data_str, codi_centre)
                return JsonResponse({"status": "exit", "slots": slots}, status=200)
            except Exception as e:
                return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)

        # Llistat de cites actives d'un metge propi
        if dni_metge and not data_str and not codi_centre:
            try:
                cites = citesDelMetge(dni_metge)
                llista = [{
                    "codi_cita"  : c.codi_cita,
                    "data"       : str(c.data),
                    "hora"       : str(c.hora)[:5],
                    "estat"      : c.estat,
                    "dni_pacient": c.dni_pacient,
                    "codi_centre": c.codi_centre,
                    "codi_sala"  : c.codi_sala if hasattr(c, 'codi_sala') else 'SALA-GEN' # Retornem sala
                } for c in cites]
                return JsonResponse({"status": "exit", "cites": llista}, status=200)
            except Exception as e:
                return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)

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
                    "dni_metge": cita.dni_metge.dni if hasattr(cita.dni_metge, 'dni') else cita.dni_metge,
                    "dni_pacient": cita.dni_pacient,
                    "codi_centre": cita.codi_centre,
                    "codi_sala": cita.codi_sala
                }
            }, status=200)
        except ValueError as e:
            return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
        
    elif request.method == 'PATCH':
        # 2. ACCIÓ MODIFICAR/ACTUALITZAR CITA (Estat o Metge)
        try:
            dades = json.loads(request.body)
            codi_cita = dades.get('codi_cita')
            dni_metge = dades.get('dni_metge')
            estat = dades.get('estat') # Canvi dinàmic d'estat ('finalitzada')

            if not codi_cita:
                return JsonResponse({"status": "error_validacio", "missatge": "Falta el camp codi_cita"}, status=400)

            try:
                cita = Cita.objects.get(codi_cita=codi_cita)
                
                if dni_metge:
                    cita.dni_metge = dni_metge
                if estat:
                    cita.estat = estat  # Actualitza si passa a finalitzada
                    
                cita.save()
                return JsonResponse({"status": "èxit", "missatge": "Cita actualitzada correctament pel personal facultatiu"}, status=200)
            except Cita.DoesNotExist:
                return JsonResponse({"status": "error_negoci", "missatge": "Aquesta cita ja no està disponible o ha estat eliminada"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)

    elif request.method != 'POST':
        return JsonResponse({"status": "error", "missatge": "Mètode no permès"}, status=405)
    
    # Mètode POST original per a creació (Ja guarda amb estat='pendent' i el dni_metge rebut del front)
    try:
        dades = json.loads(request.body)
        codi_cita = f"CT{random.randint(10000000, 99999999)}"
        
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