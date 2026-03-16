import flet as ft

from consts import etiquetas

from components.BFA_principal import BotonFlotanteAccionPrincipal
from views.bienvenida import ruta as ruta_bienvenida, Bienvenida
from views.lista import ruta as ruta_lista, Lista

class Enrutador:

    _instancia = None

    def __init__(self, pagina: ft.Page): self.pagina = pagina
    
    async def enrutador(self, e):
        self.pagina.views.clear()

        if self.pagina.route == ruta_bienvenida:
            self.pagina.views.append(await Bienvenida(self.pagina))
        elif self.pagina.route == ruta_lista:
            self.pagina.views.append(await Lista(self.pagina))

        BotonFlotanteAccionPrincipal.instancia().agregar_a_pagina()

        self.pagina.update()

    async def pinchar_vista(self, e):
        if len(self.pagina.views) > 1:
            self.pagina.views.pop()
            await self.pagina.push_route(self.pagina.views[-1].route)

    @classmethod
    def instancia(cls, pagina: ft.Page = None):
        if cls._instancia is None:
            assert pagina is not None, etiquetas["ASSERT_PAGE_PARAM"]
            cls._instancia = cls(pagina)
        return cls._instancia
    


