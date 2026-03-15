import flet as ft

class BotonFlotanteAccionPrincipal(ft.FloatingActionButton):
    def __init__(self, pagina: ft.Page):
        super().__init__()
        self.page = pagina
        self.icon = ft.Icon(ft.Icons.HOME, color=ft.Colors.WHITE)
        self.on_click = self.ir_a_inicio

        self.bgcolor = ft.Colors.PRIMARY
        self.tooltip = "Volver al Inicio"

    async def ir_a_inicio(self, e):
        if self.page.route != "/": await self.page.push_route("/")

    @property
    def page(self): return self._page

    @page.setter
    def page(self, valor):
        assert isinstance(valor, ft.Page), \
            "La propiedad 'page' debe ser una instancia de ft.Page"
        self._page = valor

    def agregar_a_pagina(self, pagina: ft.Page):
        if (
            pagina.route != "/" and
            pagina.views
        ):
            pagina.floating_action_button = self