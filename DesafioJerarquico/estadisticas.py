from recursividad import leer_todo
import os

def mostrar_estadisticas():
    print("\n--- ESTADÍSTICAS GENERALES ---")
    if not os.path.exists("datos"):
        print("No hay datos guardados aún.")
        return

    datos = leer_todo("datos")
    if not datos:
        print("No hay datos.")
        return

    total = len(datos)
    suma_poblacion = sum(float(d["Población"]) for d in datos)
    promedio = suma_poblacion / total

    print(f"Total de ciudades: {total}")
    print(f"Población total: {suma_poblacion}")
    print(f"Población promedio: {promedio:.2f}")
