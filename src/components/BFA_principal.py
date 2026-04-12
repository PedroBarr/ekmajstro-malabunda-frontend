#-------------------------------------------------------------------------------
# Nombre:      Componente Botón Flotante de Acción Principal
# Proposito:   Contiene el botón flotante principal
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft
import asyncio

from consts import etiquetas
from utils import ir_a_inicio, rutas

from views.bienvenida import ruta as ruta_bienvenida

class BotonFlotanteAccionPrincipal(ft.FloatingActionButton):
    """ Clase: Boton Flotante Principal
        (FloatingActionButton)

    Componente de botón flotante que presenta las acciones
    principales de la aplicación.
    """
    _instancia = None # Variable para la ejemplificación única

    # Método dunder de inicialización
    def __init__(self, pagina: ft.Page):
        super().__init__(
            shape=ft.CircleBorder(),
        )
        self.pagina = pagina

        self.content=ft.GestureDetector(
            content=ft.Image(
                src="favicon.svg",
                width=30,
                height=30,
                color=ft.Colors.with_opacity(0.75, ft.Colors.WHITE),
            ),
            on_secondary_tap=self._al_clic_derecho,
            on_secondary_tap_down=self._pre_clic_derecho,
            on_secondary_tap_up=self._pos_clic_derecho,
        )

        self.on_click = lambda _: \
            asyncio.create_task(ir_a_inicio(self.pagina))

        self.bgcolor = ft.Colors.PRIMARY
        self.tooltip = etiquetas["TOOLTIP_HOME"]

    # Método propiedad: página
    @property
    def pagina(self): return self._page

    @pagina.setter
    def pagina(self, valor):
        assert isinstance(valor, ft.Page), etiquetas["ASSERT_PAGE_PARAM"]
        self._page = valor

    # Método: es necesario agregar el botón a la página    
    def debe_agregarse(self):
        return (
            self.pagina.route != ruta_bienvenida and
            self.pagina.views
        )

    # Método: agregar el botón a la vista actual
    def agregar_a_pagina(self):
        if self.debe_agregarse():
            self.pagina.views[-1].floating_action_button = self

    @property
    def floating_action_button(self):
        return None

    # Método de clase: obtener la ejemplificación única del botón
    @classmethod
    def instancia(cls, pagina: ft.Page = None):        
        if cls._instancia is None:
            assert pagina is not None, etiquetas["ASSERT_PAGE_PARAM"]
            cls._instancia = cls(pagina)

        return cls._instancia
    
    async def _pre_clic_derecho(self, evento: ft.TapEvent):
        await ft.BrowserContextMenu().disable()

    def _lista_menu_contextual(self):
        return ft.Column(
            controls=[
                ft.TextButton(
                    content="Crear persona",
                    on_click=lambda _: (
                        asyncio.create_task(
                            self.pagina.push_route(rutas[etiquetas["DETAIL"]](None))
                        ),
                        self.pagina.pop_dialog(),
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.ON_PRIMARY,
                        overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.ON_PRIMARY),
                    ),
                ),
            ],
            tight=True,
        )
    
    async def _al_clic_derecho(self, evento: ft.ControlEventHandler):
        self.pagina.show_dialog(ft.SnackBar(
            content=self._lista_menu_contextual(),
            show_close_icon=True,
            close_icon_color=ft.Colors.ON_PRIMARY,
            persist=True,
            behavior=ft.SnackBarBehavior.FLOATING,
            bgcolor=ft.Colors.ON_ERROR,
        ))

    async def _pos_clic_derecho(self, evento: ft.ControlEventHandler):
        await ft.BrowserContextMenu().enable()
