#-------------------------------------------------------------------------------
# Nombre:      Utilidades de la aplicación
# Proposito:   Contiene funciones auxiliares para el funcionamiento
#              de la aplicación
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft
import re

from consts import etiquetas

# Diccionario de rutas para la navegación de la aplicación
rutas = {
    etiquetas["HOME"]: "/",
    etiquetas["LIST"]: "/lista",
    etiquetas["DETAIL"]: lambda id: \
        f"/persona/{id}" if id else "/persona",
}

# Función asíncrona: Ir a la vista de inicio
async def ir_a_inicio(pagina: ft.Page):
    if pagina.route != rutas[etiquetas["HOME"]]:
        await pagina.push_route(rutas[etiquetas["HOME"]])

# Función: Identificar si ruta argumentada coincide con ruta
#  parametrizada
def es_ruta(ruta_objetivo: str, ruta_actual: str) -> bool:
    ruta_regex = re.sub(r":\w+", r"[^/]+", ruta_objetivo)
    ruta_regex = f"^{ruta_regex}$"
    return re.match(ruta_regex, ruta_actual) is not None

def normalizar_ruta(ruta_actual: str) -> str:
    ruta = ruta_actual.split("?")[0]
    if ruta.endswith("/") and ruta != "/":
        ruta = ruta[:-1]
    return ruta

def obtener_parametros(ruta_actual: str) -> dict:
    parametros = {}
    if "?" in ruta_actual:
        query_string = ruta_actual.split("?")[1]
        for param in query_string.split("&"):
            key, value = param.split("=")
            parametros[key] = value
    return parametros

def obtener_parametro(ruta_actual: str, clave: str) -> str:
    parametros = obtener_parametros(ruta_actual)
    return parametros.get(clave, None)