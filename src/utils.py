import flet as ft

from consts import etiquetas

rutas = {
    etiquetas["HOME"]: "/",
    etiquetas["LIST"]: "/lista",
    etiquetas["DETAIL"]: lambda id: f"/persona/{id}",
}

async def ir_a_inicio(pagina: ft.Page):
    if pagina.route != rutas[etiquetas["HOME"]]:
        await pagina.push_route(rutas[etiquetas["HOME"]])