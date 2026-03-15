import flet as ft

elemento_bienvenida = ft.Text()

async def Bienvenida(pagina: ft.Page):

    def inicializar_elementos():
        elemento_bienvenida.value = f"Cargando..."
        elemento_bienvenida.font_family = "Arial"
        elemento_bienvenida.size = 30
        elemento_bienvenida.weight = ft.FontWeight.BOLD
        elemento_bienvenida.text_align = ft.TextAlign.CENTER

        if pagina.title != elemento_bienvenida.value:
            elemento_bienvenida.value = f"Bienvenido al Sistema {pagina.title}"

    async def ir_a_lista(e): await pagina.push_route("/lista")
    
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
                            ft.Button(
                                "Ver Lista de Personas",
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