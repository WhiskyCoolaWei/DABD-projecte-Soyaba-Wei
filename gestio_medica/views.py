from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("<h1>¡Bienvenido al panel de Gestión Médica!</h1> <p>El flujo de datos funciona perfectamente.</p>")