import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from gestio_medica.use_cases.medicament.consultarMedicament import consultarMedicament

@csrf_exempt
def medicamentController(request):
    
    # CONSULTAR MEDICAMENT (GET) 
    if request.method == 'GET':
        nom = request.GET.get('nom_comercial')
        actiu = request.GET.get('principi_actiu')
        
        try:
            medicaments = consultarMedicament(filtre_nom=nom, filtre_actiu=actiu)
            
            llista = []
            for m in medicaments:
                llista.append({
                    "codi_nacional": m.codi_nacional,
                    "nom_comercial": m.nom_comercial,
                    "principi_actiu": m.principi_actiu
                })
                
            return JsonResponse({"status": "èxit", "medicaments": llista}, status=200)
            
        except Exception as e:
            return JsonResponse({"status": "error_intern", "missatge": str(e)}, status=500)

