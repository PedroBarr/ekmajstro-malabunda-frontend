#-------------------------------------------------------------------------------
# Nombre:      Vista de bienvenida
# Proposito:   Contiene la vista asíncrona de bienvenida y sus
#              elementos relacionados
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft

from consts import etiquetas
from utils import rutas

ruta = rutas[etiquetas["HOME"]]

# elemento para la pancarta de bienvenida, se define a
#  nivel de módulo para su actualización dinámica
elemento_bienvenida = ft.Text()

async def Bienvenida(pagina: ft.Page):
    """ Función: Vista de bienvenida

    Funcion que retorna la vista de bienvenida con su
    configuración inicial.

    Parametros:
        pagina (ft.Page) -- página de Flet en la que
            se renderizará la vista de bienvenida

    Retorno:
        una instancia de ft.View que representa la
        vista de bienvenida
    """

    # Función: Inicializar los elementos de la vista
    def inicializar_elementos():
        elemento_bienvenida.value = etiquetas["LOADING"]
        elemento_bienvenida.font_family = "Arial"
        elemento_bienvenida.size = 30
        elemento_bienvenida.weight = ft.FontWeight.BOLD
        elemento_bienvenida.text_align = ft.TextAlign.CENTER

        # Actualizar el mensaje si el título cambia
        if pagina.title != elemento_bienvenida.value:
            elemento_bienvenida.value = \
                etiquetas["WELCOME_MESSAGE"](pagina.title)

    # Función asíncrona: Ir a la vista de lista
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
                            ft.Image(
                                src="favicon.png",
                                width=300,
                                height=300,
                                color=ft.Colors.with_opacity(0.75, ft.Colors.WHITE),
                            ),
                            elemento_bienvenida,
                            ft.Text(
                                etiquetas["WELCOME_DESCRIPTION"],
                                size=16,
                                text_align=ft.TextAlign.JUSTIFY,
                                width=pagina.width * 0.8,
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.CircleAvatar(
                                                    content=ft.Icon(
                                                        ft.Icons.PERSON_2_ROUNDED,
                                                        color=ft.Colors.ON_PRIMARY
                                                    ),
                                                    bgcolor=ft.Colors.PRIMARY,
                                                ), ft.Text(
                                                    etiquetas["GOTO"](etiquetas["LIST_TITLE"]),
                                                    color=ft.Colors.ON_PRIMARY,
                                                ),
                                                ft.Container(height=10),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=20,
                                            tight=True,
                                        ),
                                        on_click=ir_a_lista,
                                        padding=ft.Padding.symmetric(horizontal=15, vertical=20),
                                        bgcolor=ft.Colors.ON_ERROR,
                                        border_radius=15,
                                        border=ft.Border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.ON_PRIMARY)),
                                        shadow=ft.BoxShadow(
                                            color=ft.Colors.with_opacity(
                                                0.1, ft.Colors.BLACK
                                            ),
                                            blur_radius=9,
                                            spread_radius=9,
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
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
        bottom_appbar=ft.BottomAppBar(
            content=ft.Row(
                controls=[
                    ft.Text("Desarrollado por Alta Lengua"),
                    ft.Text("·", size=30, width=20, text_align=ft.TextAlign.CENTER),
                    ft.Text("2026"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.TRANSPARENT,
            notch_margin=0,
            padding=0,
            margin=0,
            height=50,
        ),
    )