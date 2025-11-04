"""
Funciones para ordenar colegios por nombre, estudiantes o año.
"""

from Funciones import *

def ordenar_colegios(colegios, campo, descendente=False):
    """Ordena los colegios según el campo elegido."""
    try:
        campo_norm = normalizar(campo)

        if "col" in campo_norm:
            campo = "colegio"
        elif "est" in campo_norm:
            campo = "estudiantes"
        elif "anio" in campo_norm or "cre" in campo_norm:
            campo = "anio_creacion"

        if campo == "colegio":
            ordenados = sorted(colegios, key=lambda x: normalizar(x["colegio"]), reverse=descendente)
        elif campo in ["estudiantes", "anio_creacion"]:
            ordenados = sorted(colegios, key=lambda x: x[campo], reverse=descendente)
        else:
            print("Campo inválido para ordenar. Usá: colegio / estudiantes / anio_creacion.")
            return

        print(f"\nColegios ordenados por {campo} ({'descendente' if descendente else 'ascendente'}):")
        mostrar_colegios(ordenados)

    except Exception as e:
        print(f"Error al ordenar: {e}")
