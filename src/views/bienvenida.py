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
        controls=[ft.Row(
            [ft.Column(
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
                        color=ft.Colors.ON_PRIMARY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )],
    )