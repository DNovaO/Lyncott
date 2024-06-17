from django.shortcuts import render

def directorios_view(request):
    return render(request, 'directorio/directorio.html')