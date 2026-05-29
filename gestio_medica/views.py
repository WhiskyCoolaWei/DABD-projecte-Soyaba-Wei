import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# ==================================================
# ==================================================
#   IMPORTAMOS LOS METODOS DEFINIDOS, LOS CASOS DE USO.

from .use_cases.metge.crearMetge import crearMetge


# ==================================================
# ==================================================

@csrf_exempt
def crearMetgeController(request):
    #Aqui definimos el controlador que recibe el request, manda al caso de uso
    #El ENDPOINT lo configuramos en urls.py

    # Desde el front se envia en html, se convierte con javascript a json y lo recibimos en back el json.
    # y devuelve el response a front

    if request.method != 'POST':
        return JsonResponse({"status": "error", "missatge": "Mètode no permès"}, status=405)
    
    try:
        dades = json.loads(request.body)

        dataNaixement = datetime.strptime(dades['data_naixement'], "%Y-%m-%d").date()
        
        #Creamos un nuevo medico, sus nuevos valores seran lo que devuelve crearMetge tras utilizar 
        #todos los argumentos que le enviamos ahora
        nmetge =crearMetge(
            dni = dades['dni'],
            nom = dades['nom'],
            cognoms = dades['cognoms'],
            data_naixement = dataNaixement,
            telefon = dades['telefon'],
            adreca = dades['adreca'],
            correu = dades['correu'],
            num_collegiat = dades['num_collegiat']
        )
    #Si todo va bien devolvemos el response a front
        return JsonResponse({
            "status": "èxit",
            "missatge": f"Metge {nmetge.nom} creat correctament amb ID {nmetge.pk}"
        }, status=201) # 201 significa "Created" en HTTP
    
    except ValueError as e:
        return JsonResponse({
            "status": "error_negoci",
            "missatge": str(e)  # Muestra el texto exacto que se puso en el raise
        }, status=400)
    except KeyError as e:
            # Por si el usuario se olvida de enviar algún campo obligatorio en el JSON
            return JsonResponse({
                "status": "error_validacio",
                "missatge": f"Falta el camp obligatori: {str(e)}"
            }, status=400)