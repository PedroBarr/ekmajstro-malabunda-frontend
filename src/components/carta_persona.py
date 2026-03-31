#-------------------------------------------------------------------------------
# Nombre:      Componente Carta Persona
# Proposito:   Contiene la clase carta persona que sirve para mostrar
#               una interfaz de formulario para el modelo persona
#
# Autor:       Aref
#
# Creado:      23/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft
from typing import Dict
from datetime import datetime
import asyncio

from models.persona import Persona
from consts import configuracion
from themes import recursos_config

from components.campo_editable import CampoEditable
from components.contador_relaciones import contador_relaciones

class CartaPersona(ft.Card):
    """ Clase: Carta Persona

    Componente para mostrar una interfaz de formulario que
    presente las funcionalidades de visualización y edición de
    un objeto del modelo persona.
    """

    # Método dunder de inicialización
    def __init__(
        self,
        persona: Persona,
        al_cambio: callable,
        relaciones: Dict[str, int] = {},
        editable: bool = True,
        al_evento=lambda e, tipo: None,
        pagina:ft.Page = None,
        **param_contenedor
    ):
        super().__init__(**param_contenedor)
        self.persona = persona
        self.relaciones = relaciones
        self._pagina = pagina

        self.al_cambio = al_cambio
        self._al_evento = al_evento

        self._es_editable = editable

        self._construir()

    # Función: Modificar persona y disparar callback de cambio
    def _modificar_persona(self, cambios: dict):
        self.persona.modificar(cambios)
        self.al_cambio(self.persona)

    def _linea_nacionalidades(self):
        texto_base = lambda texto: ft.Text(
            texto,
            size=20,
            opacity=0.7,
        )

        return ft.Row(
            spacing=5,
            expand=1,
            controls=(
                [
                    texto_base(
                        recursos_config['nacionalidades']['desconocida']['emoticon'],
                    )
                ] if not self.persona.nacionalidades
                else [
                    (
                        texto_base(
                            (recursos_config['nacionalidades'].get(nacion) or {}).get('emoticon', '❓'),
                        )
                        if nacion in configuracion.get('nacionalidades', [])
                        else texto_base(
                            recursos_config['nacionalidades']['desconocida']['otro'],
                        )
                    )
                    for nacion in self.persona.nacionalidades
                ]
            ),
        )
    
    # Función: Obtener render de información de cabecera
    def _info_cabecera(self):
        return ft.Container(
            expand=True,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        spacing=5,
                        controls=[
                            CampoEditable(
                                "Apellido",
                                self.persona.apellido,
                                lambda valor: \
                                    self._modificar_persona({
                                        "apellido": valor
                                    }),
                                editable=self._es_editable,
                            ),
                            ft.Text(
                                "/",
                                weight=ft.FontWeight.W_900,
                                size=20
                            ),
                            ft.Container(width=25),
                            CampoEditable(
                                "Nombre",
                                self.persona.nombre,
                                lambda valor: \
                                    self._modificar_persona({
                                        "nombre": valor
                                    }),
                                editable=self._es_editable,
                            ),
                        ],
                    ),
                    self._linea_nacionalidades(),
                ],
            ),
        )
    
    # Función: Obtener render de cabecera
    def _cabecera(self):
        return ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.persona.foto_perfil(),
                    self._info_cabecera(),
                ]
            ),
        )
    
    # Función: Obtener render de división entre cabecera y cuerpo
    def _divisor(self):
        divisor = ft.Divider(height=10, thickness=1, expand=1)

        # se calcula dinámicamente el uso del divisor
        return ft.Row(
            controls=(
                [divisor] if not self.persona.id
                else [
                    divisor,
                    ft.Text(
                        self.persona.id,
                        size=10,
                        color=ft.Colors.OUTLINE,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                    ),
                    divisor,
                ]
            ),
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    # Función: Obtener render de marca de tiempo de última modificación
    def _marca_tiempo(self):
        if not self.persona.id: return ft.Container()
        return ft.Container(
            alignment=ft.Alignment.BOTTOM_RIGHT,
            content=ft.Text(
                "Última modificación: " + \
                    self.persona.marca_tiempo_modificacion(),
                size=10,
                color=ft.Colors.OUTLINE,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ),
        )
    
    def _agregar_alias(self, alias_o_evento: str | ft.ControlEventHandler):
        alias = (
            alias_o_evento.value
            if type(alias_o_evento) is ft.TextField
            else alias_o_evento
        )
        
        if type(alias) is str:
            alias = alias.strip()
            if alias and alias not in self.persona.alias:
                self._modificar_persona({
                    "alias": self.persona.alias + [alias]
                })
    
    def _abrir_modal_agregar_alias(self):
        alias_nuevo = ft.TextField(
            label="Alias",
            autofocus=True,
            expand=True,
        )
        confirmar_evento = lambda _: (self._agregar_alias(alias_nuevo), self._pagina.pop_dialog())

        modal = ft.AlertDialog(
            title=ft.Text("Agregar un nuevo alias"),
            content=alias_nuevo,
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: self._pagina.pop_dialog(),
                ),
                ft.TextButton(
                    "Agregar",
                    on_click=confirmar_evento,
                ),
            ],
        )

        alias_nuevo.on_submit = confirmar_evento

        self._pagina.show_dialog(modal)
    
    def _linea_alias(self, **parametros):
        alias_base = lambda alias: ft.Container(
            content=ft.Text(
                alias,
                size=12,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=ft.Colors.PRIMARY,
            padding=ft.Padding.symmetric(horizontal=12, vertical=3),
            height=25,
            border_radius=ft.BorderRadius.all(15),
        )

        boton_agregar_alias = ft.Button(
            "+",
            on_click=lambda e: self._abrir_modal_agregar_alias(),
            bgcolor=ft.Colors.PRIMARY if self.persona and self.persona.id and self._es_editable else ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            disabled=not self.persona.id or not self._es_editable,
            width=60,
            height=25,
            align=ft.Alignment.CENTER,
        )

        return ft.Row(
            spacing=5,
            controls=[
                ft.Text(
                    "Alias: ",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Row(
                    spacing=5,
                    controls=[
                        alias_base(alias=alias)
                        for alias in self.persona.alias
                    ],
                ),
                boton_agregar_alias,
            ],
            scroll="hidden",
            **parametros,
        )
    
    def _cuerpo(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        controls=[
                            self._linea_alias(expand=2),
                            ft.Button(
                                "Agregar evento",
                                on_click=lambda e: asyncio.create_task(self._al_evento(e, "agregar_evento")),
                                bgcolor=ft.Colors.PRIMARY if self.persona and self.persona.id else ft.Colors.GREY_600,
                                color=ft.Colors.WHITE,
                                disabled=not self.persona or not self.persona.id,
                                expand=1,
                            ),
                            ft.Button(
                                "Agregar relación",
                                on_click=lambda e: asyncio.create_task(self._al_evento(e, "agregar_relacion")),
                                bgcolor=ft.Colors.PRIMARY if self.persona and self.persona.id else ft.Colors.GREY_600,
                                color=ft.Colors.WHITE,
                                disabled=not self.persona or not self.persona.id,
                                expand=1,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
                                [
                                    ft.Row(
                                        controls=[
                                            ft.Button(
                                                "Ver artículo",
                                                on_click=lambda e: asyncio.create_task(self._al_evento(e, "ver_articulo")),
                                                bgcolor=ft.Colors.GREY_600,
                                                color=ft.Colors.WHITE,
                                                disabled=True,
                                                expand=1,
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Button(
                                                "Reportar error",
                                                on_click=lambda e: asyncio.create_task(self._al_evento(e, "reportar_error")),
                                                bgcolor=ft.Colors.DEEP_PURPLE_200 if self.persona and self.persona.id else ft.Colors.GREY_600,
                                                color=ft.Colors.WHITE,
                                                disabled=not self.persona or not self.persona.id,
                                                expand=1,
                                            ),
                                        ],
                                    ),
                                ],
                                spacing=10,
                                horizontal_alignment=ft.MainAxisAlignment.CENTER,
                                expand=2,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        (
                                            datetime.fromisoformat(self.persona.ultimo_periodo['fecha_inicio'].replace("Z", "+00:00")).strftime("%Y-%m-%d")
                                            if 'fecha_inicio' in self.persona.ultimo_periodo and type(self.persona.ultimo_periodo['fecha_inicio']) is str
                                            else ""
                                        ) + " / " +
                                        (
                                            datetime.fromisoformat(self.persona.ultimo_periodo['fecha_fin'].replace("Z", "+00:00")).strftime("%Y-%m-%d")
                                            if 'fecha_fin' in self.persona.ultimo_periodo and type(self.persona.ultimo_periodo['fecha_fin']) is str
                                            else "Actualidad"
                                        ),
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Text(
                                        (
                                            self.persona.ultimo_periodo['estado']
                                            if 'estado' in self.persona.ultimo_periodo
                                            else "Sin información de periodo"
                                        ),
                                        size=12,
                                        color=ft.Colors.GREY_400,
                                    ),
                                ],
                                spacing=0,
                                expand=1,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            contador_relaciones(
                                self.relaciones
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=10,
            ),
            expand=True,
        )

    # Función: Construir componente
    def _construir(self):
        self.content = ft.Container(
            padding=ft.Padding(20, 25, 20, 15),
            expand=True,
            content=ft.Column(
                spacing=10,
                controls=[
                    self._cabecera(),
                    self._divisor(),
                    self._cuerpo(),
                    self._marca_tiempo(),
                ]
            ),
        )