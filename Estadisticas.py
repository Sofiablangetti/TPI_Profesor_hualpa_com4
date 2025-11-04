"""
Cálculo de estadísticas generales sobre los colegios cargados.
"""

from Funciones import *

def mostrar_estadisticas(colegios):
    """Muestra estadísticas generales: máximos, promedios y cantidad por provincia."""
    
    if not colegios:
        print(" No hay datos disponibles para mostrar estadísticas.")
        return
    
    colegio_mayor = max(colegios, key=lambda x: x["estudiantes"])
    colegio_menor = min(colegios, key=lambda x: x["estudiantes"])

    promedio_estudiantes = sum(c["estudiantes"] for c in colegios) / len(colegios)
    promedio_anio = sum(c["anio_creacion"] for c in colegios) / len(colegios)

    colegios_por_provincia = {}
    for c in colegios:
        prov = normalizar(c["provincia"])
        colegios_por_provincia[prov] = colegios_por_provincia.get(prov, 0) + 1

    print("\n Estadísticas generales:")
    print(f"   ▫ Colegio con más estudiantes: {colegio_mayor['colegio']} ({colegio_mayor['estudiantes']:,})")
    print(f"   ▫ Colegio con menos estudiantes: {colegio_menor['colegio']} ({colegio_menor['estudiantes']:,})")
    print(f"   ▫ Promedio de estudiantes: {int(promedio_estudiantes):,}")
    print(f"   ▫ Promedio de año de creación: {int(promedio_anio)}")
    print("   ▫ Cantidad de colegios por provincia:")
    for prov, cantidad in colegios_por_provincia.items():
        print(f"      - {prov.title()}: {cantidad}")
