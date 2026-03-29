#-------------------------------------------------------------------------------
# Nombre:      Vista de detalle de persona
# Proposito:   Contiene la clase detalle de persona
#
# Autor:       Aref
#
# Creado:      23/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft
import asyncio
import re
from typing import Dict, List

from consts import etiquetas
from utils import rutas
from api_client import ClienteAPI

from models.persona import Persona, PersonaElemento
from models.arbol_relaciones import ArbolRelaciones

from components.carta_persona import CartaPersona
from components.fila_lista import fila_lista
from components.arbol_persona import ArbolPersona
from components.grafo3d import Grafo3D
from components.caja_mensaje import caja_cargando, caja_error, caja_mensaje
from components.conmutador import Conmutador

ruta = rutas[etiquetas["DETAIL"]](":id")
ruta_creacion = rutas[etiquetas["DETAIL"]](None)

class PersonaVista:
    """ Clase: PersonaVista

    Vista de detalle de persona.

    Define metodos asíncronos y variables internas para la
    gestión de la vista, la navegación y la interacción con la
    API para obtener los datos de la persona o crear una nueva,
    además de renderizar una interfaz con capacidad de edición.
    """

    # Método dunder de inicialización
    def __init__(self, pagina: ft.Page, es_creacion: bool = False):
        self.pagina = pagina

        self.persona: Persona = Persona.sintetizar()
        self.relaciones_contadores = {}
        self._personas: list[PersonaElemento] = []
        self._arbol: ArbolRelaciones = None
        self._grafo3d: Dict[str, List] = None

        self.conmutador_principal = Conmutador(
            [
                ft.Icons.PERSON_4_ROUNDED,
                ft.Icons.STYLE_ROUNDED,
            ],
            [
                self._personas_componente,
                self._contexto_componente,
            ],
            etiquetas=[
                "Personas",
                "Contexto",
            ],
            altura_forzada=180,
            al_cambio=lambda _: self._actualizar_conmutador_principal(),
        )

        self._envoltura_conmutador_principal = ft.Container(
            expand=1,
            content=self.conmutador_principal.construir(),
        )

        self.conmutador_relaciones = Conmutador(
            [
                ft.Icons.TRANSFORM,
                ft.Icons.KEYBOARD_OPTION_KEY_ROUNDED,
                ft.Icons.CONTROL_CAMERA,
            ],
            [
                lambda: caja_mensaje(
                    mensaje="No hay relaciones para mostrar (Lista).",
                ),
                self._arbol_componente,
                self._grafo3d_componente,
            ],
            etiquetas=[
                "Lista",
                "Árbol",
                "Red",
            ],
            inicio=1,
            al_cambio=lambda _: self._actualizar_conmutador_relaciones(),
        )

        self._envoltura_conmutador_relaciones = ft.Container(
            expand=1,
            content=self.conmutador_relaciones.construir(),
        )
        
        self._actualizar_persona()
        self.construir(es_creacion=es_creacion)

    # Función: Actualizar estado interno de la persona
    def _actualizar_persona(self):
        self._persona = Persona.sintetizar(persona=self.persona)

    def _actualizar_relaciones_conteo(self, conteo: dict[str, int]):
        self.relaciones_contadores = conteo
        self._actualizar_carta()

    # Función: Obtener ID desde la ruta y procesarla
    def _obtener_id(self):
        ruta_actual = self.pagina.route
        patron = rutas[etiquetas["DETAIL"]](r"([A-Za-z0-9]+)")
        coincidencia = re.match(patron, ruta_actual)
        if coincidencia:
            self.persona.id = coincidencia.group(1)
        else:
            asyncio.create_task(self._validar_ruta_inutil())

    # Función asíncrona: Validar ruta inútil y manejarla
    async def _validar_ruta_inutil(self):
        terna_vistas = (
            self.pagina.views[-3:]
            if len(self.pagina.views) >= 3
            else self.pagina.views
        )

        if (
            all(
                terna_vistas[i].route == ruta_creacion
                for i in [0, -1]
            ) and
            terna_vistas[1].route == ruta
        ):
            await self.pagina.on_view_pop(True)
            await self.pagina.on_view_pop(True)
            await self.pagina.on_view_pop(None)

    # Función asíncrona: Cargar datos de la persona desde la API
    async def cargar_datos(self):
        self._obtener_id()

        if self.persona.id:
            try:
                self.persona = await ClienteAPI().obtener_persona(
                    self.persona.id
                )
                self._actualizar_persona()

                asyncio.create_task(
                    ClienteAPI().relaciones_conteo_persona(self.persona.id)
                ).add_done_callback(
                    lambda fut: self._actualizar_relaciones_conteo(fut.result())
                )

                asyncio.create_task(
                    ClienteAPI().relaciones_personas_persona(self.persona.id)
                ).add_done_callback(
                    lambda fut: self._actualizar_personas(fut.result())
                )

                asyncio.create_task(
                    ClienteAPI().relaciones_arbol_persona(self.persona)
                ).add_done_callback(
                    lambda fut: self._actualizar_arbol(fut.result())
                )

                asyncio.create_task(
                    ClienteAPI().relaciones_grafo_persona(self.persona)
                ).add_done_callback(
                    lambda fut: self._actualizar_grafo(fut.result())
                )

            except Exception as e: self.persona = None

        self._actualizar_carta()
        self.pagina.update()
        
    # Función asíncrona: Sincronizar cambios con la API
    async def _sincronizar_cambios(self, cambios: dict):
        try:
            # Si la persona tiene ID, es una actualización
            if self.persona.id:
                # Parchar la persona por API
                await ClienteAPI().parchar_persona(
                    self.persona.id,
                    cambios
                )

                self._actualizar_persona()

            # Si no tiene ID, es una creación
            else:
                self.vista.controls[0] = \
                    caja_cargando(
                        etiquetas["LOADING_SYNC"],
                        size=20,
                    )
                self.pagina.update()

                # Simular espera para que se renderize el cargador
                await asyncio.sleep(0.1)

                # Crear la persona por API
                nueva_persona = await ClienteAPI()\
                    .crear_persona(self.persona)
                
                if nueva_persona and nueva_persona.id:
                    ruta_nueva = \
                        rutas[etiquetas["DETAIL"]](nueva_persona.id)
                    
                    await self.pagina.push_route(ruta_nueva)

        except Exception as e: self.persona = None
        
    # Función asíncrona: Modificar la persona y sincronizar cambios
    async def _modificar_persona(self, persona: Persona):
        # calcular cambios
        cambios = self._persona.cambios(persona)
        
        if cambios:
            if persona.es_cargable():
                # sincronizar solo si hay cambios y tiene el mínimo de
                #  campos necesarios
                asyncio.create_task(self._sincronizar_cambios(cambios))

            else: print(etiquetas["UNCOMPLETED_FIELDS"])
    
        self.persona = persona
        self._actualizar_carta()
        self.pagina.update()

    # Función: Obtener render por detalle (formulario de persona)    
    def _controles(self):
        return [
            ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        CartaPersona(
                            persona=self.persona,
                            relaciones=self.relaciones_contadores,
                            al_cambio=lambda p: \
                                asyncio.create_task(self._modificar_persona(p)),
                            editable=True,
                            expand=1,
                            elevation=5,
                        ),
                        self._envoltura_conmutador_principal,
                    ],
                ),
            ),
            self._envoltura_conmutador_relaciones,
        ]
    
    # Función: Obtener render por error al cargar detalle
    def _carta_fallida(self):
        return [
            caja_error(
                etiquetas["ERROR_LOADING_DETAIL"],
                size=20,
            )
        ]
    
    # Función: Actualizar render
    def _actualizar_carta(self):
        self.vista.controls = \
            self._controles() if self.persona else self._carta_fallida()

    # Función: Construir la vista con ruta dinámica
    def construir(self, es_creacion=False):
        self.vista = ft.View(
            route=ruta if not es_creacion else ruta_creacion,
            controls=self._controles(),
        )

    def _personas_componente(self):
        return (
            caja_mensaje(
                mensaje="No hay personas relacionadas.",
            )
            if not self._personas or self._personas == []
            else ft.Column(
                [
                    fila_lista(
                        persona,
                        lambda p: asyncio.create_task(self.pagina.push_route(rutas[etiquetas["DETAIL"]](p.id)))
                    )
                    for persona in self._personas
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
            )
        )
    
    def _arbol_componente(self):
        return (
            caja_mensaje(
                mensaje="No hay relaciones para mostrar.",
            )
            if not self._arbol
            else ArbolPersona(arbol=self._arbol).construir()
        )
    
    def _grafo3d_componente(self):
        return (
            caja_mensaje(
                mensaje="No hay relaciones para mostrar.",
            )
            if not self._grafo3d else
            Grafo3D(
                grafo=self._grafo3d,
                dimensiones_iniciales=(
                    self.pagina.width,
                    self.pagina.height - self._altura_conmutador_principal
                ),
                angulo_elevacion_inicial=75,
                al_repintar=lambda: self.pagina.update()
            )\
                .construir()
        )

    def _actualizar_personas(self, personas: list[PersonaElemento]):
        self._personas = personas
        self._actualizar_conmutador_principal()

    def _actualizar_arbol(self, arbol: ArbolRelaciones):
        self._arbol = arbol
        self._actualizar_conmutador_relaciones()

    def _actualizar_grafo(self, grafo: Dict[str, List]):
        self._grafo3d = grafo
        self._actualizar_conmutador_relaciones()
    
    def _actualizar_conmutador_principal(self):
        self._envoltura_conmutador_principal.content = \
            self.conmutador_principal.construir()
    
    def _contexto_componente(self):
        return caja_mensaje(
            mensaje="No hay contexto disponible.",
        )
    
    def _actualizar_conmutador_relaciones(self):
        self._envoltura_conmutador_relaciones.content = \
            self.conmutador_relaciones.construir()