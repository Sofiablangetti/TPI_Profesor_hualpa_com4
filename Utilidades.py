"""
Funciones auxiliares para mostrar colegios, pedir rangos y normalizar texto.
"""

import unicodedata

def mostrar_colegios(lista):
    """Muestra los colegios con todos sus datos de forma prolija."""
    for c in lista:
        print(f"{c['colegio']} | Provincia: {c['provincia']} | Estudiantes: {c['estudiantes']:,} | Año: {c['anio_creacion']}")

def pedir_rango(nombre_campo):
    """Pide al usuario un rango de valores (mínimo y máximo) para filtrar colegios."""
    try:
        minimo = int(input(f"Ingresá {nombre_campo} mínimo: "))
        maximo = int(input(f"Ingresá {nombre_campo} máximo: "))
        return minimo, maximo
    except ValueError:
        print("Entrada inválida. Debés ingresar números.")
        return None, None 

def normalizar(texto):
    """Convierte texto a minúsculas, elimina espacios y acentos."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto
