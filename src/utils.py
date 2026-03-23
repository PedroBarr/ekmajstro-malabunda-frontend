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
    etiquetas["DETAIL"]: lambda id: f"/persona/{id}" if id else "/persona",
}

# Función asíncrona: Ir a la vista de inicio
async def ir_a_inicio(pagina: ft.Page):
    if pagina.route != rutas[etiquetas["HOME"]]:
        await pagina.push_route(rutas[etiquetas["HOME"]])

def es_ruta(ruta_objetivo: str, ruta_actual: str) -> bool:
    ruta_regex = re.sub(r":\w+", r"[^/]+", ruta_objetivo)
    ruta_regex = f"^{ruta_regex}$"
    return re.match(ruta_regex, ruta_actual) is not None