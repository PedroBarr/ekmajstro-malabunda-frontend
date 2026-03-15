import flet as ft

elemento_bienvenida = ft.Text()

async def Bienvenida(pagina: ft.Page):

    def inicializar_elementos():
        elemento_bienvenida.value = f"Cargando..."
        elemento_bienvenida.font_family = "Arial"
        elemento_bienvenida.size = 30
        elemento_bienvenida.weight = ft.FontWeight.BOLD
        elemento_bienvenida.text_align = ft.TextAlign.CENTER

    inicializar_elementos()

    return ft.View(
        route="/",
        controls=[
            ft.Row(
                [
                    ft.Column(
                        [
                            elemento_bienvenida,
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