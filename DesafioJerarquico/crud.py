import os, csv
from validaciones import validar_numero, validar_texto
from recursividad import leer_todo

RUTA_BASE = "datos"

def agregar_item():
    print("\n--- AGREGAR NUEVA CIUDAD ---")
    continente = validar_texto("Continente: ")
    pais = validar_texto("País: ")
    ciudad = validar_texto("Ciudad: ")
    nombre = validar_texto("Nombre de la ciudad: ")
    poblacion = validar_numero("Población: ", int)
    superficie = validar_numero("Superficie (km²): ", float)

    ruta = os.path.join(RUTA_BASE, continente, pais, ciudad)
    os.makedirs(ruta, exist_ok=True)
    archivo_csv = os.path.join(ruta, "datos.csv")

    with open(archivo_csv, "a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=["Nombre", "Población", "Superficie"])
        if archivo.tell() == 0:
            writer.writeheader()
        writer.writerow({"Nombre": nombre, "Población": poblacion, "Superficie": superficie})

    print(" Ciudad agregada correctamente.")

def mostrar_todos():
    print("\n--- MOSTRAR TODAS LAS CIUDADES ---")
    if not os.path.exists(RUTA_BASE):
        print("No hay datos guardados aún.")
        return

    datos = leer_todo(RUTA_BASE)
    if not datos:
        print("No se encontraron ciudades.")
        return

    for d in datos:
        print(f"{d['Nombre']} - Población: {d['Población']} - Superficie: {d['Superficie']} - {d['Ubicación']}")
    print(f"\nTotal: {len(datos)} ciudades registradas.")

def modificar_item():
    print("\n--- MODIFICAR CIUDAD ---")
    if not os.path.exists(RUTA_BASE):
        print("No hay datos guardados aún.")
        return

    datos = leer_todo(RUTA_BASE)
    nombre = input("Nombre exacto de la ciudad a modificar: ").strip()
    encontrado = None
    for d in datos:
        if d["Nombre"].lower() == nombre.lower():
            encontrado = d
            break

    if not encontrado:
        print(" No se encontró la ciudad.")
        return

    nuevo_valor = validar_numero("Nueva población: ", int)
    encontrado["Población"] = nuevo_valor

    archivo_csv = encontrado["Ubicación"]
    with open(archivo_csv, newline="", encoding="utf-8") as archivo:
        lector = list(csv.DictReader(archivo))

    for fila in lector:
        if fila["Nombre"].lower() == nombre.lower():
            fila["Población"] = str(nuevo_valor)

    with open(archivo_csv, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=["Nombre", "Población", "Superficie"])
        writer.writeheader()
        writer.writerows(lector)

    print("✅ Ciudad modificada correctamente.")

def eliminar_item():
    print("\n--- ELIMINAR CIUDAD ---")
    if not os.path.exists(RUTA_BASE):
        print("No hay datos guardados aún.")
        return

    datos = leer_todo(RUTA_BASE)
    nombre = input("Nombre exacto de la ciudad a eliminar: ").strip()
    encontrado = None
    for d in datos:
        if d["Nombre"].lower() == nombre.lower():
            encontrado = d
            break

    if not encontrado:
        print(" No se encontró la ciudad.")
        return

    archivo_csv = encontrado["Ubicación"]
    with open(archivo_csv, newline="", encoding="utf-8") as archivo:
        lector = list(csv.DictReader(archivo))

    lector = [fila for fila in lector if fila["Nombre"].lower() != nombre.lower()]

    with open(archivo_csv, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=["Nombre", "Población", "Superficie"])
        writer.writeheader()
        writer.writerows(lector)

    print(" Ciudad eliminada correctamente.")
