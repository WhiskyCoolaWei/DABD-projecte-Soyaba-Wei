import json
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from gestio_medica.use_cases.pacient.crearPacient import crearPacient
from gestio_medica.use_cases.pacient.consultarPacient import consultarPacientPerDni
from gestio_medica.use_cases.pacient.llistarPacients import llistarPacients

@csrf_exempt
def pacientController(request):
    
    # CONSULTAR PACIENT (GET)
    if request.method == 'GET':
        try:
            # Recogemos parámetros de filtros, ordenación y paginación
            filtre_dni = request.GET.get('dni')
            filtre_nom = request.GET.get('nom')
            filtre_cognoms = request.GET.get('cognoms')
            ordenar_per = request.GET.get('ordenar_per') # Puede ser 'citas_activas' o '-citas_activas'
            num_pagina = request.GET.get('pagina', 1)

            # Invocamos el caso de uso con la lógica de negocio
            pacients_totals = llistarPacients(
                dni=filtre_dni,
                nom=filtre_nom,
                cognoms=filtre_cognoms,
                ordenar_per=ordenar_per
            )

            # Paginamos los resultados de 10 en 10 para que sea cómodo
            paginator = Paginator(pacients_totals, 10)
            try:
                pagina_actual = paginator.page(num_pagina)
            except EmptyPage:
                pagina_actual = paginator.page(paginator.num_pages)

            # Construimos la lista final inyectando el nuevo campo calculado
            llista = []
            for p in pagina_actual.object_list:
                llista.append({
                    "dni": p.dni,
                    "nom": p.nom,
                    "cognoms": p.cognoms,
                    "data_naixement": p.data_naixement.strftime('%d/%m/%Y') if p.data_naixement else None,
                    "telefon": p.telefon,
                    "correu": p.correu,
                    "citas_activas": p.citas_activas  # <-- ¡Enviamos el contador al Front!
                })

            return JsonResponse({
                "status": "èxit",
                "pacients": llista,
                "paginacio": {
                    "pagina_actual": pagina_actual.number,
                    "total_pagines": paginator.num_pages,
                    "te_anterior": pagina_actual.has_previous(),
                    "te_seguent": pagina_actual.has_next()
                }
            }, status=200)

        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)

    # CREAR PACIENT (POST) 
    elif request.method == 'POST':
        try:
            dades = json.loads(request.body)
            dni = dades.get('dni')
            nom = dades.get('nom')
            cognoms = dades.get('cognoms')
            data_naixement = dades.get('data_naixement')
            telefon = dades.get('telefon')
            adreca = dades.get('adreca')
            correu = dades.get('correu')

            if not all([dni, nom, cognoms, data_naixement, telefon, adreca, correu]):
                return JsonResponse({"status": "error_validacio", "missatge": "Falten camps obligatoris per omplir."}, status=400)

            npacient = crearPacient(
                dni=dni.strip().upper(),
                nom=nom.strip(),
                cognoms=cognoms.strip(),
                data_naixement=data_naixement,
                telefon=telefon.strip(),
                adreca=adreca.strip(),
                correu=correu.strip()
            )

            return JsonResponse({
                "status": "èxit",
                "missatge": f"Pacient {npacient.nom} {npacient.cognoms} registrat correctament amb èxit."
            }, status=201)
            
        except ValueError as e:
            return JsonResponse({"status": "error_negoci", "missatge": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)
            
    else:
        return JsonResponse({"status": "error", "missatge": "Mètode no permès."}, status=405)