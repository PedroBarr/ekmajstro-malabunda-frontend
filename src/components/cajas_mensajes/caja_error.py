import flet as ft

from consts import etiquetas
from components.caja_mensaje import caja_mensaje

def caja_error(
    mensaje: str,
    **parametros
) -> ft.Container:
    return caja_mensaje(
        mensaje=mensaje,
        **parametros
    )