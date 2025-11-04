"""
Programa principal de gestión de colegios.
Permite buscar, filtrar, ordenar, editar y agregar colegios desde un archivo CSV.
Incluye validaciones, estadísticas y persistencia de datos.
"""

import csv
import os
import unicodedata

# Importación de módulos propios
from Funciones import *
from Estadisticas import *
from CargaDeDatos import *
from Ordenamientos import *
from Utilidades import *

ARCHIVO_COLEGIOS = "colegios.csv"

# Verifica si el archivo existe; si no, lo crea con encabezados
if not os.path.exists(ARCHIVO_COLEGIOS):
    with open(ARCHIVO_COLEGIOS, "w", newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["provincia", "colegio", "estudiantes", "anio_creacion"])
    print(f"Archivo '{ARCHIVO_COLEGIOS}' creado automáticamente.")


def mostrar_menu():
    print("\n     - MENÚ DE OPCIONES -     ")
    print("1. Buscar colegio por nombre")
    print("2. Filtrar por provincia")
    print("3. Filtrar por rango de cantidad de estudiantes")
    print("4. Filtrar por rango de año de creación")
    print("5. Ordenar colegios")
    print("6. Mostrar estadísticas")
    print("7. Agregar un colegio")
    print("8. Editar cantidad de estudiantes o año de creación")
    print("9. Guardar cambios en el archivo CSV")
    print("10. Salir")


def guardar_colegios(colegios, ruta_csv):
    """Guarda los datos actualizados en el archivo CSV."""
    try:
        with open(ruta_csv, "w", newline='', encoding='utf-8') as archivo:
            campos = ["provincia", "colegio", "estudiantes", "anio_creacion"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for c in colegios:
                escritor.writerow(c)
        print(f"\nCambios guardados correctamente en '{ruta_csv}'.")
    except Exception as e:
        print(f"\nError al guardar el archivo: {e}")


def main():
    colegios = cargar_colegios(ARCHIVO_COLEGIOS)

    if not colegios:
        print(" No se cargó ningún colegio. Podés agregar desde el menú.")

    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()

        if not opcion.isdigit():
            print("Entrada inválida. Debés ingresar un número.")
            continue

        # Opción 1
        if opcion == "1":
            nombre = input("Ingresá el nombre (o parte del nombre) del colegio: ")
            buscar_colegio(colegios, nombre)

        # Opción 2
        elif opcion == "2":
            provincia = input("Ingresá el nombre de la provincia: ")
            filtrar_por_provincia(colegios, provincia)

        # Opción 3
        elif opcion == "3":
            min_est, max_est = pedir_rango("cantidad de estudiantes")
            if min_est is not None:
                filtrar_por_rango(colegios, "estudiantes", min_est, max_est)

        # Opción 4
        elif opcion == "4":
            min_anio, max_anio = pedir_rango("año de creación")
            if min_anio is not None:
                filtrar_por_rango(colegios, "anio_creacion", min_anio, max_anio)

        # Opción 5
        elif opcion == "5":
            campo = input("Campo para ordenar (colegio/estudiantes/anio_creacion): ").lower()
            descendente = input("¿Querés orden descendente? (s/n): ").lower() == "s"
            ordenar_colegios(colegios, campo, descendente)

        # Opción 6
        elif opcion == "6":
            mostrar_estadisticas(colegios)

        # Opción 7
        elif opcion == "7":
            agregar_colegio(colegios)

        # Opción 8
        elif opcion == "8":
            editar_colegio(colegios)

        # Opción 9
        elif opcion == "9":
            guardar_colegios(colegios, ARCHIVO_COLEGIOS)

        # Opción 10
        elif opcion == "10":
            print("\nPrograma finalizado. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intentá de nuevo.")


if __name__ == "__main__":
    main()
