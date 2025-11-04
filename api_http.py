"""
Cliente HTTP para trabajar con un servidor REST que expone recursos de 'colegios'.

Campos esperados por colegio:
- provincia (str)
- colegio (str)
- estudiantes (int)
- anio_creacion (int)

Endpoints asumidos:
- GET  /health           -> estado del servidor
- GET  /colegios         -> lista (acepta params q, provincia, sort_by, desc)
- POST /colegios         -> crear
- GET  /colegios/{id}    -> obtener uno
- PATCH/DELETE /colegios/{id} -> actualizar / borrar
"""

from typing import Optional, List, Dict

try:
    import requests
except ImportError:
    raise SystemExit(
        "*********************😎****************************\n"
        "* Falta el paquete 'requests'.                   *\n"
        "* Instalar con:                                  *\n"
        "*   Windows: py -3.13 -m pip install requests     *\n"
        "*   Linux/Mac: python3 -m pip install requests    *\n"
        "*********************👌***************************"
    )

BASE_URL = "http://149.50.150.15:8000".rstrip("/")


def _url(ruta: str) -> str:
    return f"{BASE_URL}{ruta}"


def establecer_base_url(url: str) -> None:
    """Permite cambiar la URL base del servidor (útil para pruebas)."""
    global BASE_URL
    BASE_URL = (url or "").rstrip("/")


def estado_servidor() -> Dict:
    """Consulta /health y devuelve el JSON de estado."""
    resp = requests.get(_url("/health"), timeout=5)
    resp.raise_for_status()
    return resp.json()


def listar_colegios(
    q: Optional[str] = None,
    provincia: Optional[str] = None,
    ordenar_por: Optional[str] = None,
    descendente: bool = False,
) -> List[Dict]:
    """Lista colegios desde el servidor con filtros parecidos a los del CSV."""
    params: Dict[str, str] = {}
    if q:
        params["q"] = q
    if provincia:
        params["provincia"] = provincia
    if ordenar_por:
        params["sort_by"] = ordenar_por
    if descendente:
        params["desc"] = "true"

    resp = requests.get(_url("/colegios"), params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def obtener_colegio(id_colegio: int) -> Dict:
    resp = requests.get(_url(f"/colegios/{id_colegio}"), timeout=10)
    resp.raise_for_status()
    return resp.json()


def crear_colegio(
    provincia: str,
    colegio: str,
    estudiantes: int,
    anio_creacion: int,
) -> Dict:
    payload = {
        "provincia": provincia,
        "colegio": colegio,
        "estudiantes": int(estudiantes),
        "anio_creacion": int(anio_creacion),
    }
    resp = requests.post(_url("/colegios"), json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def actualizar_colegio_parcial(id_colegio: int, cambios: Dict) -> Dict:
    """PATCH parcial: enviar sólo los campos a modificar."""
    resp = requests.patch(_url(f"/colegios/{id_colegio}"), json=cambios, timeout=10)
    resp.raise_for_status()
    return resp.json()


def eliminar_colegio(id_colegio: int) -> bool:
    resp = requests.delete(_url(f"/colegios/{id_colegio}"), timeout=10)
    if resp.status_code not in (200, 204):
        resp.raise_for_status()
    return True


def buscar_por_nombre(nombre: str) -> Optional[Dict]:
    """Intenta coincidencia exacta por nombre; si no, devuelve el primer candidato."""
    if not nombre:
        return None
    candidatos = listar_colegios(q=nombre, ordenar_por="colegio")
    n = nombre.strip().lower()
    for c in candidatos:
        if c.get("colegio", "").strip().lower() == n:
            return c
    return candidatos[0] if candidatos else None


def crear_desde_dict(item: Dict) -> Dict:
    """Crea un colegio a partir de un dict (útil desde el menú)."""
    return crear_colegio(
        provincia=item["provincia"],
        colegio=item["colegio"],
        estudiantes=int(item["estudiantes"]),
        anio_creacion=int(item["anio_creacion"]),
    )
