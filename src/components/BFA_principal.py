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
from utils import ir_a_inicio

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
        super().__init__()
        self.pagina = pagina
        self.icon = ft.Icon(ft.Icons.HOME, color=ft.Colors.WHITE)
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

    # Método: agregar el botón a la página
    def agregar_a_pagina(self):
        if self.debe_agregarse():
            self.pagina.floating_action_button = self

    # Método de clase: obtener la ejemplificación única del botón
    @classmethod
    def instancia(cls, pagina: ft.Page = None):        
        if cls._instancia is None:
            assert pagina is not None, etiquetas["ASSERT_PAGE_PARAM"]
            cls._instancia = cls(pagina)

        return cls._instancia
