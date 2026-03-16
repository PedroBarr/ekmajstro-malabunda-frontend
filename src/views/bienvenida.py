import flet as ft
import asyncio

from consts import etiquetas
from utils import rutas

ruta = rutas[etiquetas["HOME"]]

elemento_bienvenida = ft.Text()

async def Bienvenida(pagina: ft.Page):

    def inicializar_elementos():
        elemento_bienvenida.value = etiquetas["LOADING"]
        elemento_bienvenida.font_family = "Arial"
        elemento_bienvenida.size = 30
        elemento_bienvenida.weight = ft.FontWeight.BOLD
        elemento_bienvenida.text_align = ft.TextAlign.CENTER

        if pagina.title != elemento_bienvenida.value:
            elemento_bienvenida.value = \
                etiquetas["WELCOME_MESSAGE"](pagina.title)

    async def ir_a_lista(e):
        await pagina.push_route(rutas[etiquetas["LIST"]])
    
    inicializar_elementos()

    return ft.View(
        route=ruta,
        controls=[
            ft.Row(
                [
                    ft.Column(
                        [
                            elemento_bienvenida,
                            ft.Text(
                                etiquetas["WELCOME_DESCRIPTION"],
                                size=16,
                            ),
                            ft.Button(
                                etiquetas["GOTO"](etiquetas["LIST_TITLE"]),
                                icon=ft.Icons.LIST,
                                on_click=ir_a_lista,
                                height=50,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ],
    )