import flet as ft

from consts import etiquetas
from components.caja_mensaje import caja_mensaje

def caja_cargando(
    mensaje: str = None,
    **parametros
) -> ft.Container:
    if parametros.get("size") is None:
        parametros["size"] = 16

    texto = mensaje if mensaje else etiquetas["LOADING"]

    return caja_mensaje(componente=[
        ft.ProgressRing(
            color=ft.Colors.PRIMARY,
            stroke_width=5,
            width=50,
            height=50
        ),
        ft.Container(height=20),
        ft.Text(
            texto,
            **parametros
        )
    ])