import flet as ft
import asyncio
from typing import Dict, Any, List

from utils import rutas, obtener_parametro
from consts import etiquetas, configuracion
from api_client import ClienteAPI

from models.relacion import Relacion
from models.persona import Persona

from components.caja_mensaje import caja_error
from components.campo_editable import CampoEditable
from components.carta_persona import CartaPersona

ruta_creacion = rutas['relacion'](None)

class RelacionVista:
    def __init__(
        self,
        pagina: ft.Page,
        es_creacion=False,
    ):
        self.pagina = pagina

        self.relacion = Relacion.sintetizar()
        self.personas: List[Persona] = []

        self.contruir(es_creacion=es_creacion)

    async def _cargar_personas(self):
        try: self.personas = await ClienteAPI().obtener_personas()
        except Exception as e:
            self.personas = None

    def _agregar_personas_a_relacion(self):
        # get query parameter "personas"
        personas = obtener_parametro(self.pagina.route, "personas")
        if personas and self.personas is not None:
            personas_ids = personas.split(",")
            self.relacion.relacionados = [
                persona for persona in self.personas
                if persona.id in personas_ids
            ]

    async def cargar_datos(self):
        await self._cargar_personas()

        self._agregar_personas_a_relacion()

        self._actualizar_carta()
        self.pagina.update()

    async def _modificar_relacion(self, cambios: Dict[str, Any]):
        # calcular cambios
        self.relacion.agregar_cambios(cambios)
        self._actualizar_carta()
        self.pagina.update()

    def _fecha_editor(self, al_editar = lambda fecha: None, **parametros):
        fecha_inicio_evento_selector = ft.DatePicker(
            on_change=lambda e: (
                al_editar(e.control.value.strftime("%Y-%m-%d")),
                setattr(fecha_inicio_evento_boton.content, "value", self.relacion.fecha()),
            ),
        )

        fecha_inicio_evento_boton = ft.Button(
            content=ft.Text(self.relacion.fecha()),
            on_click=lambda e: self.pagina.show_dialog(fecha_inicio_evento_selector),
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.WHITE,
            **parametros
        )

        return fecha_inicio_evento_boton

    def _carta_relacion(self):
        return ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    CampoEditable(
                        "Nombre",
                        self.relacion.nombre,
                        lambda valor: asyncio.create_task(
                            self._modificar_relacion({
                                "nombre": valor,
                            })
                        ),
                        color_etiqueta=ft.Colors.GREY_400,
                    ),
                    ft.Container(
                        bgcolor=self.relacion.borde(),
                        height=5,
                        width=(
                            400
                            if self.relacion.nombre.strip() == ""
                            else min(len(self.relacion.nombre) * 15, 800)
                        ),
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Container(
                                            bgcolor=self.relacion.color(),
                                            border_radius=25,
                                            width=50,
                                            height=50,
                                            content=ft.Container(
                                                content=ft.Text(
                                                    self.relacion.relacionados_cantidad(),
                                                    size=25,
                                                    color=self.relacion.borde(),
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ),
                                            alignment=ft.Alignment.CENTER,
                                        ),
                                        ft.Text(
                                            "Relacionados",
                                            size=12,
                                            color=ft.Colors.ON_SURFACE,
                                        )
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.Alignment.TOP_CENTER,
                                    spacing=5,
                                ),
                                alignment=ft.Alignment.TOP_CENTER,
                                expand=False,
                                padding=ft.Padding(15, 10, 15, 0),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            self._fecha_editor(
                                                al_editar=lambda valor: asyncio.create_task(
                                                    self._modificar_relacion({
                                                        "fecha": valor,
                                                    })
                                                ),
                                            ),
                                            ft.Container(width=25),
                                            CampoEditable(
                                                "Tipo",
                                                self.relacion.tipo,
                                                lambda valor: asyncio.create_task(
                                                    self._modificar_relacion({
                                                        "tipo": valor,
                                                    })
                                                ),
                                                tipo="lista",
                                                opciones=configuracion['tipos_relacion'],
                                                color_etiqueta=ft.Colors.GREY_400,
                                                expand=False,
                                            ),
                                            ft.Container(expand=True)
                                        ],
                                        spacing=10,
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    CampoEditable(
                                        "Descripción",
                                        self.relacion.descripcion(),
                                        lambda valor: asyncio.create_task(
                                            self._modificar_relacion({
                                                "descripcion": valor,
                                            })
                                        ),
                                        tipo="multilinea",
                                        color_etiqueta=ft.Colors.GREY_400,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=10,
                                expand=True,
                            ),
                        ],
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ]
            ),
            padding=ft.Padding(20, 15, 20, 15),
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[
                    ft.Colors.with_opacity(0.3, self.relacion.color()),
                    ft.Colors.with_opacity(0.5, self.relacion.borde()),
                    ft.Colors.with_opacity(0.6, self.relacion.color()),
                ],
            ),
            border=ft.Border.all(1, ft.Colors.GREY_700),
            border_radius=20,
        )
    
    def _relacionados_componentes(self):
        return [
            CartaPersona(
                persona=persona,
                al_cambio=lambda cambios: None,
                relaciones=None,
                editable=False,
                expand=1,
                pagina=self.pagina,
            )
            for persona in self.personas
            if self.relacion.es_relacionada(persona.id)
        ]

    # Función: Obtener render por detalle (formulario de persona)    
    def _controles(self):
        return [
            self._carta_relacion(),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=self._relacionados_componentes(),
                            spacing=10,
                            scroll="auto",
                        ),
                        align=ft.Alignment.TOP_CENTER,
                        expand=1,
                    ),
                ],
                expand=True,
            ),
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
        self.vista.controls = (
            self._controles()
            if self.relacion and self.personas is not None
            else self._carta_fallida()
        )

    def contruir(self, es_creacion=False):
        self.vista = ft.View(
            route=ruta_creacion,
            controls=[],
        )