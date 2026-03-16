import flet as ft
import asyncio

from consts import etiquetas
from utils import rutas
from api_client import ClienteAPI

ruta = rutas[etiquetas["LIST"]]

class Lista:
    def __init__(self, pagina: ft.Page):
        self.pagina = pagina
        self.vista_lista = ft.ListView(expand=True, spacing=10, padding=10)
        self.vista = self.vista(pagina)
        
    async def ir_a_detalle(self, persona_id):
        await self.pagina.push_route(rutas[etiquetas["DETAIL"]](persona_id))

    async def obtener_personas(self):
        self.vista_lista.controls.clear()
        personas = await ClienteAPI().obtener_personas()
        
        for persona in personas:
            self.vista_lista.controls.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(),
                    title=ft.Text(f'{persona["apellido"]}, {persona["nombre"]}'),
                    subtitle=ft.Text(f"ID: {persona['_id']}"),
                    on_click=lambda _, p = \
                        persona['_id']: asyncio.create_task(self.ir_a_detalle(p))
                )
            )

        self.vista.controls = [self.vista_lista]
        self.pagina.update()

    def vista(self, pagina: ft.Page):
        vista = ft.View(
            route=ruta,
            controls=[ft.Row(
                [ft.Column(
                    [
                        ft.ProgressRing(),
                        ft.Text(
                            etiquetas["LIST_TITLE"],
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )],
        )        

        return vista