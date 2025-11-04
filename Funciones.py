"""
Funciones de búsqueda, filtrado, edición y agregado de colegios.
"""

from Utilidades import *

def buscar_colegio(colegios, nombre):
    """Busca colegios que contengan el texto ingresado."""
    nombre_normalizado = normalizar(nombre)
    resultados = [c for c in colegios if nombre_normalizado in normalizar(c["colegio"])]
    if resultados:
        print(f"\n Se encontraron {len(resultados)} colegio(s) con el nombre '{nombre}':")
        mostrar_colegios(resultados)
    else:
        print(f"\n No se encontró ningún colegio que contenga '{nombre}'.")

def filtrar_por_provincia(colegios, provincia):
    """Filtra colegios por provincia."""
    provincia_normalizada = normalizar(provincia)
    resultados = [c for c in colegios if provincia_normalizada in normalizar(c["provincia"])]
    if resultados:
        print(f"\n Colegios en la provincia '{provincia}':")
        mostrar_colegios(resultados)
    else:
        print(f"\n No se encontraron colegios en la provincia '{provincia}'.")

def filtrar_por_rango(colegios, campo, minimo, maximo):
    """Filtra colegios por un rango numérico."""
    resultados = [c for c in colegios if minimo <= c[campo] <= maximo]
    if resultados:
        print(f"\n Colegios con {campo} entre {minimo} y {maximo}:")
        mostrar_colegios(resultados)
    else:
        print(f"\n No hay colegios con {campo} en ese rango.")

def editar_colegio(colegios):
    """Permite editar cantidad de estudiantes o año de creación."""
    print("\n Editar colegio ")
    nombre = input("Ingresá el nombre del colegio que querés editar: ")
    nombre_normalizado = normalizar(nombre)

    resultados = [c for c in colegios if nombre_normalizado in normalizar(c["colegio"])]

    if not resultados:
        print(f" No se encontró ningún colegio que contenga '{nombre}'.")
        return

    print(f"\nSe encontraron {len(resultados)} colegio(s):")
    for i, c in enumerate(resultados):
        print(f"{i + 1}. {c['colegio']} | Estudiantes: {c['estudiantes']:,} | Año creación: {c['anio_creacion']}")

    try:
        indice = int(input("Elegí el número del colegio que querés editar: ")) - 1
        if indice < 0 or indice >= len(resultados):
            print(" Número inválido.")
            return

        colegio = resultados[indice]
        nuevo_est = int(input(f"Nueva cantidad de estudiantes para {colegio['colegio']}: "))
        nuevo_anio = int(input(f"Nuevo año de creación para {colegio['colegio']}: "))

        colegio["estudiantes"] = nuevo_est
        colegio["anio_creacion"] = nuevo_anio

        print(f"Datos actualizados para {colegio['colegio']}.")

    except ValueError:
        print("Entrada inválida.")

def agregar_colegio(colegios):
    """Agrega un nuevo colegio al listado."""
    print("\n--- Agregar nuevo colegio ---")

    provincia = input("Provincia: ").strip()
    while provincia == "":
        provincia = input("La provincia no puede estar vacía. Ingresá nuevamente: ").strip()

    colegio = input("Nombre del colegio: ").strip()
    while colegio == "":
        colegio = input("El nombre no puede estar vacío. Ingresá nuevamente: ").strip()

    try:
        estudiantes = int(input("Cantidad de estudiantes: "))
        anio = int(input("Año de creación: "))
    except ValueError:
        print("Error: los campos deben ser numéricos.")
        return

    nuevo = {
        "provincia": provincia,
        "colegio": colegio,
        "estudiantes": estudiantes,
        "anio_creacion": anio
    }

    colegios.append(nuevo)
    print(f"Colegio '{colegio}' agregado correctamente.")
