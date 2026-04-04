#-------------------------------------------------------------------------------
# Nombre:      Enrutador de la aplicación
# Proposito:   Gestionar la navegación entre vistas en la aplicación
#              Malabunda (frontal).
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
from utils import es_ruta, normalizar_ruta

from components.BFA_principal import BotonFlotanteAccionPrincipal

from views.bienvenida import ruta as ruta_bienvenida, Bienvenida
from views.lista import ruta as ruta_lista, Lista
from views.persona import (
    ruta as ruta_persona,
    ruta_creacion as ruta_persona_creacion,
    PersonaVista,
)
from views.relacion import (
    ruta as ruta_relacion,
    ruta_creacion as ruta_relacion_creacion,
    RelacionVista,
)

class Enrutador:
    """ Clase: Enrutador

    Presenta un enrutador de ejemplificación única para
    gestionar la navegación entre vistas.
    """

    _instancia = None # Variable para la ejemplificación única

    # Método dunder de inicialización
    def __init__(self, pagina: ft.Page): self.pagina = pagina
    
    # Función asíncrona: Enrutador de la aplicación
    async def enrutador(self, e):
        if self.pagina.route == ruta_bienvenida:
            self.pagina.views.append(await Bienvenida(self.pagina))
        elif self.pagina.route == ruta_lista:
            lista = Lista(self.pagina)
            self.pagina.views.append(lista.vista)
            self.pagina.update()
            asyncio.create_task(lista.obtener_personas())
        elif (
            es_ruta(ruta_persona, self.pagina.route) or
            self.pagina.route == ruta_persona_creacion
        ):
            persona = PersonaVista(
                self.pagina,
                es_creacion=self.pagina.route == ruta_persona_creacion
            )
            
            self.pagina.views.append(persona.vista)
            asyncio.create_task(persona.cargar_datos())

        elif (
            es_ruta(ruta_relacion, self.pagina.route) or
            normalizar_ruta(self.pagina.route) == ruta_relacion_creacion
        ):
            relacion = RelacionVista(
                self.pagina,
                es_creacion=(
                    normalizar_ruta(self.pagina.route) ==
                        ruta_relacion_creacion
                ),
            )

            self.pagina.views.append(relacion.vista)
            asyncio.create_task(relacion.cargar_datos())

        # Agregar botón flotante de acción principal
        BotonFlotanteAccionPrincipal.instancia().agregar_a_pagina()

        self.pagina.update()

    # Función asíncrona: Pinchar la vista actual para volver a la vista
    #  anterior
    async def pinchar_vista(self, e):
        if len(self.pagina.views) > 1:
            self.pagina.views.pop()

            # Para evitar el enrutamiento
            if e not in [True]:
                await self.pagina.push_route(self.pagina.views[-1].route)

    # Método de clase: obtener la ejemplificación única del botón
    @classmethod
    def instancia(cls, pagina: ft.Page = None):
        if cls._instancia is None:
            assert pagina is not None, etiquetas["ASSERT_PAGE_PARAM"]
            cls._instancia = cls(pagina)

        return cls._instancia
