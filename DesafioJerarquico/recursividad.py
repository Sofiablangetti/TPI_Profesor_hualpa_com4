import os, csv

def leer_todo(ruta_base):
    """
    Recorre todas las carpetas y lee todos los CSV.
    Retorna una lista de diccionarios.
    """
    datos = []

    for elemento in os.listdir(ruta_base):
        ruta_completa = os.path.join(ruta_base, elemento)

        if os.path.isdir(ruta_completa):
            datos.extend(leer_todo(ruta_completa))  
        elif elemento.endswith(".csv"):
            with open(ruta_completa, encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    fila["Ubicación"] = ruta_completa.replace("\\", "/")
                    datos.append(fila)
    return datos
