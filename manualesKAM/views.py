from django.shortcuts import render

def manuales_view(request):
    return render(request,'manuales/manuales.html')

