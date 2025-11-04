"""
Funciones que usan api_client.py y adaptan la interfaz a la lógica del menú
(compatibles con las funciones de vista/ordenamiento/estadísticas).
"""

from function.tools import normalizar                       # si usás Funciones.py renombralo o crea wrapper
from function.view import mostrar_colegios, ordenar_colegios  # view debe tener mostrar_colegios/ordenar_colegios
from function.statistics import mostrar_estadisticas         # statistics debe aceptar la lista de colegios
from function.shearch import buscar_colegio, filtrar_por_provincia, filtrar_por_rango
from function import api_client


def _coerce(items: list[dict]) -> list[dict]:
    """Convierte/asegura tipos que el resto del programa espera."""
    for p in items:
        p["provincia"] = str(p.get("provincia", ""))
        p["colegio"] = str(p.get("colegio", ""))
        # Aseguramos int en estudiantes y anio_creacion (si vienen como strings)
        try:
            p["estudiantes"] = int(p.get("estudiantes", 0))
        except Exception:
            p["estudiantes"] = 0
        try:
            p["anio_creacion"] = int(p.get("anio_creacion", 0))
        except Exception:
            p["anio_creacion"] = 0
    return items


def obtener_colegios_api(q=None, provincia=None, sort_by=None, desc=False):
    items = api_client.listar_colegios(q=q, provincia=provincia, ordenar_por=sort_by, descendente=desc)
    return _coerce(items)


def buscar_colegio_api(nombre: str):
    """Busca por nombre usando la API y delega a la función de búsqueda local para mostrar."""
    colegios = obtener_colegios_api(q=nombre)
    # reutilizamos la función de búsqueda de tu proyecto
    buscar_colegio(colegios, nombre)


def filtrar_provincia_api(provincia: str):
    colegios = obtener_colegios_api()
    filtrar_por_provincia(colegios, provincia)


def filtrar_rango_api(campo: str):
    """Pide rango desde la UI (main.py) y filtra con la función local (filtrar_por_rango)."""
    colegios = obtener_colegios_api()
    filtrar_por_rango(colegios, campo)   # se espera que filtrar_por_rango lea los límites por input


def ordenar_colegios_api(campo: str, descendente: bool = False):
    colegios = obtener_colegios_api()
    ordenar_colegios(colegios, campo, descendente)


def estadisticas_api():
    colegios = obtener_colegios_api()
    mostrar_estadisticas(colegios)


def agregar_colegio_api():
    print("\n--- Agregar nuevo colegio (API) ---")
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

    creado = api_client.crear_desde_dict({
        "provincia": provincia,
        "colegio": colegio,
        "estudiantes": estudiantes,
        "anio_creacion": anio
    })
    print(f"✅ Colegio '{creado.get('colegio', colegio)}' creado correctamente en el servidor.")


def editar_colegio_api():
    print("\n--- Editar colegio (API) ---")
    nombre = input("Ingresá el nombre del colegio que querés editar: ")
    nombre_normalizado = normalizar(nombre)

    colegios = obtener_colegios_api()
    resultados = [c for c in colegios if nombre_normalizado in normalizar(c["colegio"])]

    if not resultados:
        print(f"No se encontró ningún colegio que contenga '{nombre}'.")
        return

    print(f"\nSe encontraron {len(resultados)} colegio(s):")
    for i, c in enumerate(resultados):
        print(f"{i + 1}. {c['colegio']} | Estudiantes: {c['estudiantes']:,} | Año creación: {c['anio_creacion']}")

    try:
        indice = int(input("Elegí el número del colegio que querés editar: ")) - 1
        if indice < 0 or indice >= len(resultados):
            print("Número inválido.")
            return

        colegio = resultados[indice]
        nueva_poblacion = int(input(f"Nueva cantidad de estudiantes para {colegio['colegio']}: "))
        nuevo_anio = int(input(f"Nuevo año de creación para {colegio['colegio']}: "))

        if "id" not in colegio:
            exacto = api_client.buscar_por_nombre(colegio["colegio"])
            if not exacto or "id" not in exacto:
                print("No se pudo determinar el ID en el servidor.")
                return
            colegio["id"] = exacto["id"]

        actualizado = api_client.actualizar_colegio_parcial(colegio["id"], {
            "estudiantes": int(nueva_poblacion),
            "anio_creacion": int(nuevo_anio)
        })
        print(f"✅ Datos actualizados para {actualizado.get('colegio', colegio['colegio'])}.")

    except ValueError:
        print("Entrada inválida.")


def borrar_colegio_api():
    print("\n--- Borrar colegio (API) ---")
    modo = input("¿Buscar por (1) nombre o (2) id? : ").strip() or "1"

    if modo == "2":
        try:
            cid = int(input("ID: ").strip())
        except ValueError:
            print("ID inválido.")
            return
        if input(f"¿Confirmás borrar id={cid}? (s/n): ").strip().lower() == "s":
            api_client.eliminar_colegio(cid)
            print(f"✅ Colegio con id={cid} borrado correctamente.")
        else:
            print("Cancelado.")
        return

    nombre = input("Ingresá el nombre (o parte): ").strip()
    if not nombre:
        print("Nombre vacío, cancelado.")
        return

    cand = api_client.listar_colegios(q=nombre, ordenar_por="colegio")
    if not cand:
        print(f"No se encontró ningún colegio que contenga '{nombre}'.")
        return

    mostrar_colegios(cand)

    try:
        idx = int(input("Elegí el número del colegio a borrar (1..n): ").strip()) - 1
        if idx < 0 or idx >= len(cand):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    elegido = cand[idx]
    if "id" not in elegido:
        exacto = api_client.buscar_por_nombre(elegido.get("colegio", ""))
        if not exacto or "id" not in exacto:
            print("No se pudo determinar el ID en el servidor.")
            return
        elegido = exacto

    if input(f"¿Confirmás borrar '{elegido['colegio']}' (id={elegido['id']})? (s/n): ").strip().lower() == "s":
        api_client.eliminar_colegio(elegido["id"])
        print(f"✅ '{elegido['colegio']}' borrado correctamente.")
    else:
        print("Cancelado.")
