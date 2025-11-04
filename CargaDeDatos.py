"""
Carga de datos desde archivo CSV.
Lee colegios, valida campos y convierte tipos.
"""

import csv

def cargar_colegios(ruta_csv):
    """Carga los colegios desde un archivo CSV y valida los datos."""
    
    colegios = []

    try:
        with open(ruta_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    provincia = fila.get("provincia")
                    colegio = fila.get("colegio")
                    estudiantes = fila.get("estudiantes")
                    anio_creacion = fila.get("anio_creacion")

                    if not (provincia and colegio and estudiantes and anio_creacion):
                        raise ValueError("Faltan datos en la fila")

                    colegio_dict = {
                        "provincia": provincia.strip(),
                        "colegio": colegio.strip(),
                        "estudiantes": int(estudiantes),
                        "anio_creacion": int(anio_creacion)
                    }
                    
                    colegios.append(colegio_dict)

                except Exception:
                    print(f"Fila con formato incorrecto y se omitió: {fila}")

        if colegios:
            print(f"\nSe cargaron correctamente {len(colegios)} colegios.\n")
        else:
            print("\nNo se cargó ningún colegio válido. Verificá el formato del CSV.\n")

    except FileNotFoundError:
        print("\nError: No se encontró el archivo especificado.")
    except Exception as e:
        print(f"\nError al leer el archivo: {e}")
        
    return colegios
