import flet as ft
from src.api_client import APIClient

def Lista(pagina: ft.Page, api: APIClient):
    vista_lista = ft.ListView(expand=True, spacing=10, padding=10)

    def obtener_personas():
        vista_lista.controls.clear()
        personas = api.obtener_personas()

        for persona in personas:
            vista_lista.controls.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(),
                    title=ft.Text(f'{persona["apellido"]}, {persona["nombre"]}'),
                    subtitle=ft.Text(f"ID: {persona['_id']}"),
                    on_click=lambda _, p=persona['_id']: pagina.go(f"/persona/{p}"),
                )
            )

        pagina.update()

    obtener_personas()

    return ft.View(
        route="/lista",
        controls=[vista_lista],
    )