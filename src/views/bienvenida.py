import flet as ft

def Bienvenida(pagina: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Bienvenido al Sistema " + pagina.title,
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Explora una de las siguientes opciones",
                                size=16,
                            ),
                            ft.ElevatedButton(
                                "Ver Lista de Personas",
                                icon=ft.Icons.LIST,
                                on_click=lambda _: pagina.go("/lista"),
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