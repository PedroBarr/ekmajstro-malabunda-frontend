import flet as ft
import asyncio

from api_client import APIClient

async def Lista(pagina: ft.Page, api: APIClient):
    vista_lista = ft.ListView(expand=True, spacing=10, padding=10)
    vista = ft.View(
        route="/lista",
        controls=[
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.ProgressRing(),
                            ft.Text(
                                "Lista de Personas",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ],
    )

    async def obtener_personas():
        vista_lista.controls.clear()
        personas = await api.obtener_personas()

        for persona in personas:
            vista_lista.controls.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(),
                    title=ft.Text(f'{persona["apellido"]}, {persona["nombre"]}'),
                    subtitle=ft.Text(f"ID: {persona['_id']}"),
                    on_click=lambda _, p=persona['_id']: pagina.go(f"/persona/{p}"),
                )
            )

        vista.controls = [vista_lista]
        pagina.update()

    asyncio.create_task(obtener_personas())

    return vista