from .models import *
from .views import *

def printAllSelectedItems(parametrosSeleccionados):
    print("All Selected Items:")
    for key, value in parametrosSeleccionados.items():
        print(f"{key}: {value}")