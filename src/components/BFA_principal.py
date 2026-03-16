import flet as ft
import asyncio

from consts import etiquetas
from utils import ir_a_inicio

from views.bienvenida import ruta as ruta_bienvenida

class BotonFlotanteAccionPrincipal(ft.FloatingActionButton):
    
    _instancia = None

    def __init__(self, pagina: ft.Page):
        super().__init__()
        self.pagina = pagina
        self.icon = ft.Icon(ft.Icons.HOME, color=ft.Colors.WHITE)
        self.on_click = lambda _: asyncio.create_task(ir_a_inicio(self.pagina))

        self.bgcolor = ft.Colors.PRIMARY
        self.tooltip = etiquetas["TOOLTIP_HOME"]

    @property
    def pagina(self): return self._page

    @pagina.setter
    def pagina(self, valor):
        assert isinstance(valor, ft.Page), etiquetas["ASSERT_PAGE_PARAM"]
        self._page = valor
    
    def debe_agregarse(self):
        return (
            self.pagina.route != ruta_bienvenida and
            self.pagina.views
        )

    def agregar_a_pagina(self):
        if self.debe_agregarse():
            self.pagina.floating_action_button = self

    @classmethod
    def instancia(cls, pagina: ft.Page = None):        
        if cls._instancia is None:
            assert pagina is not None, etiquetas["ASSERT_PAGE_PARAM"]
            cls._instancia = cls(pagina)
        return cls._instancia