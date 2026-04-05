import flet as ft
import asyncio
import re
from typing import Dict, Any, List

from utils import rutas, obtener_parametro, normalizar_ruta
from consts import etiquetas, configuracion
from api_client import ClienteAPI

from models.relacion import Relacion
from models.persona import Persona

from components.caja_mensaje import caja_error, caja_cargando
from components.campo_editable import CampoEditable
from components.carta_persona import CartaPersona
from components.fila_lista import fila_lista
from components.elemento_fuente import ElementoFuente

ruta = rutas['relacion'](":id")
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

        self._archivo = None
        self._relacionados = []

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

    def _obtener_id(self):
        ruta_actual = normalizar_ruta(self.pagina.route)
        patron = rutas['relacion'](r"([A-Za-z0-9]+)")
        coincidencia = re.match(patron, ruta_actual)
        if coincidencia:
            self.relacion.id = coincidencia.group(1)
        else:
            asyncio.create_task(self._validar_ruta_inutil())

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
            await self.pagina.on_view_pop(True)
            await self.pagina.push_route(rutas['Inicio'])

    async def cargar_datos(self):
        await self._cargar_personas()
        self._agregar_personas_a_relacion()

        self._obtener_id()

        if self.relacion.id:
            try:
                self.relacion = await ClienteAPI().obtener_relacion(self.relacion.id)
                self._llenar_relacionados()
            except Exception as e: self.relacion = None

        self._actualizar_carta()
        self.pagina.update()

    def _llenar_relacionados(self):
        relacionados = []

        for persona in self.personas:
            relacionado = self.relacion.traer_relacionado(persona.id)

            if relacionado:
                relacionados.append({
                    "persona": persona,
                    "relacion": relacionado,
                })

        self._relacionados = relacionados

    async def _sincronizar_cambios(self):
        try:
            if self.relacion.id:
                await ClienteAPI().parchar_relacion(self.relacion.id, self.relacion)

                self._actualizar_carta()

            else:
                self.vista.controls = \
                    caja_cargando(
                        etiquetas["LOADING_SYNC"],
                        size=20,
                    )
                self.pagina.update()

                await asyncio.sleep(0.1)

                nueva_relacion = await ClienteAPI()\
                    .crear_relacion(self.relacion)
                
                if nueva_relacion and nueva_relacion.id:
                    ruta_nueva = rutas['relacion'](nueva_relacion.id)

                    await self.pagina.push_route(ruta_nueva)

        except Exception as e: self.relacion = None

    def _modificar_relacion(self, cambios: Dict[str, Any]):
        cambiado = self.relacion.agregar_cambios(cambios)
        if cambiado:
            if "relacionados" in cambios:
                self._llenar_relacionados()

            if self.relacion.es_cargable():
                asyncio.create_task(self._sincronizar_cambios())

            else: print(etiquetas["UNCOMPLETED_FIELDS"])

        self._actualizar_carta()
        self.pagina.update()

    def _agregar_relacionado(self, persona_id: str):
        if self.personas is None: return

        persona = self._obtener_persona_por_id(persona_id)
        if persona is None: return

        relacionado = self.relacion.agregar_relacionado(persona, modo_retorno=True)
        
        if relacionado:
            self._modificar_relacion({
                "relacionados": self.relacion.relacionados + [relacionado],
            })

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
                        lambda valor: self._modificar_relacion({
                            "nombre": valor,
                        }),
                        color_etiqueta=ft.Colors.GREY_400,
                    ),
                    ft.Container(
                        bgcolor=self.relacion.color(),
                        height=5,
                        width=(
                            500
                            if self.relacion.nombre.strip() == ""
                            else min(max(len(self.relacion.nombre) * 11.5, 500), 1000)
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
                                                al_editar=lambda valor: self._modificar_relacion({
                                                    "fecha": valor,
                                                }),
                                            ),
                                            ft.Container(width=25),
                                            CampoEditable(
                                                "Tipo",
                                                self.relacion.tipo,
                                                lambda valor: self._modificar_relacion({
                                                    "tipo": valor,
                                                }),
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
                                        lambda valor: self._modificar_relacion({
                                            "descripcion": valor,
                                        }),
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
        fila_relacionado = lambda relacionado: ft.Container(
            content=ft.Row(
                controls=[
                    CampoEditable(
                        "Relación",
                        relacionado["relacion"]["rol"],
                        lambda valor: self._modificar_relacion({
                            "relacionados": [
                                {
                                    **r,
                                    "rol": valor if r == relacionado["relacion"] else r["rol"],
                                }
                                for r in self.relacion.relacionados
                            ]
                        }),
                        color_etiqueta=ft.Colors.GREY_400,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        ft.Icons.PERSON_REMOVE_OUTLINED,
                        icon_color=ft.Colors.RED_300,
                        icon_size=15,
                        on_click=lambda e: self._eliminar_relacionado(relacionado["persona"].id),
                    )
                ],
            ),
            padding=ft.Padding(15, 0, 10, 0),
        )

        return [
            ft.Button(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ADD,
                            color=ft.Colors.WHITE,
                            size=25,
                        ),
                        ft.Container(width=10),
                        ft.Text(
                            etiquetas["ADD_PERSON"],
                            color=ft.Colors.WHITE,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(width=25),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                ),
                expand=True,
                height=50,
                bgcolor=ft.Colors.PRIMARY,
                on_click=lambda e: self._agregar_persona_evento(),
            )
        ] + [
            ft.Column(
                controls=[
                    fila_relacionado(relacionado),
                    CartaPersona(
                        persona=relacionado["persona"],
                        al_cambio=lambda cambios: None,
                        relaciones=None,
                        editable=False,
                        expand=1,
                        pagina=self.pagina,
                    )
                ],
                spacing=0,
            )
            for relacionado in self._relacionados
        ]
    
    def _fuentes_componentes(self):
        fila_eliminar_fuente = lambda fuente_id: ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(
                    ft.Icons.BOOKMARK_REMOVE_OUTLINED,
                    icon_color=ft.Colors.RED_300,
                    icon_size=15,
                    on_click=lambda e: asyncio.create_task(self._desvincular_fuente(fuente_id)),
                )
            ],
        )

        return [
            ft.Button(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ADD_LINK_ROUNDED,
                            color=ft.Colors.WHITE,
                            size=25,
                        ),
                        ft.Container(width=10),
                        ft.Text(
                            "Agregar fuente",
                            color=ft.Colors.WHITE,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                ),
                expand=True,
                height=50,
                bgcolor=ft.Colors.PRIMARY,
                on_click=lambda e: self._abrir_modal_agregar_fuente(e),
            )
        ] + [
            ft.Column(
                controls=[
                    fila_eliminar_fuente(fuente["_id"]),
                    ElementoFuente(
                        fuente=fuente,
                        al_clic=lambda f: None,
                    ).construir()
                ],
                spacing=0,
            )
            for fuente in self.relacion.fuentes
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
                ] + (
                    [
                        ft.Container(
                            content=ft.Column(
                                controls=self._fuentes_componentes(),
                                spacing=10,
                                scroll="auto",
                            ),
                            align=ft.Alignment.TOP_CENTER,
                            expand=1,
                        ),
                    ]
                    if self.relacion.id and self.relacion.id != ""
                    else []
                ),
                spacing=20,
                expand=True,
            ),
        ]
    
    # Función: Obtener render por error al cargar detalle
    def _carta_fallida(self):
        return [
            caja_error(
                'Error al cargar la relación',
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
            route=ruta_creacion if es_creacion else ruta,
            controls=[],
        )

    def _obtener_persona_por_id(self, persona_id: str) -> Persona:
        return next(
            (persona for persona in self.personas if persona.id == persona_id),
            None
        )

    def _agregar_persona_evento(self):
        modal = ft.AlertDialog(
            title=ft.Text("Agregar persona a relación"),
            content=ft.Column(
                controls=[
                    fila_lista(
                        persona=persona,
                        on_click=lambda p: (
                            self._agregar_relacionado(p.id),
                            self.pagina.pop_dialog(),
                        ),
                        compacta=True,
                    )
                    for persona in self.personas
                    if not self.relacion.es_relacionada(persona.id)
                ],
                spacing=10,
                scroll="auto",
                height=self.pagina.height * 0.5,
                width=self.pagina.width * 2 / 3,
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=lambda e: self.pagina.pop_dialog(),
                )
            ],
        )
        self.pagina.show_dialog(modal)

    def _modal_agregar_fuente_componente(self):
        return ft.Column(
            controls=[
                CampoEditable(
                    "Nombre de la fuente",
                    "",
                    lambda valor: None,
                    color_etiqueta=ft.Colors.GREY_400,
                ),
                CampoEditable(
                    "Descripción de la fuente",
                    "",
                    lambda valor: None,
                    tipo="multilinea",
                    color_etiqueta=ft.Colors.GREY_400,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.ADD_LINK_ROUNDED,
                                color=ft.Colors.WHITE,
                                size=25,
                            ),
                            ft.Container(width=10),
                            ft.Text(
                                "Agregar fuente",
                                color=ft.Colors.WHITE,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5
                    ),
                    expand=True,
                    height=40,
                    bgcolor=ft.Colors.TRANSPARENT,
                    border_radius=20,
                    border=ft.Border.all(3, ft.Colors.PRIMARY),
                    on_click=self._manejador_elegir_archivos,
                )
            ],
            spacing=10,
            expand=False,
            height=200,
        )
    
    def _abrir_modal_agregar_fuente(self, e):
        modal = ft.AlertDialog(
            title=ft.Text("Agregar una nueva fuente"),
            content=self._modal_agregar_fuente_componente(),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.pagina.pop_dialog()),
                ft.TextButton(
                    "Agregar",
                    on_click=lambda e: asyncio.create_task(self._anexar_fuente(modal))
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.pagina.show_dialog(modal)

    async def _manejador_elegir_archivos(self, e):
        seleccion = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
        )
        
        if seleccion and len(seleccion) > 0:
            self._archivo = seleccion[0]
        else:
            self._archivo = None

    async def _anexar_fuente(self, modal):
        if self._archivo is None: return

        nombre = modal.content.controls[0].valor.strip()
        descripcion = modal.content.controls[1].valor.strip()
        
        fuente = {
            "nombre": nombre if nombre != "" else self._archivo.name,
            "descripcion": descripcion,
            "archivo": self._archivo,
        }

        try:
            fuente = await ClienteAPI().anexar_fuente(self.relacion.id, fuente)
            if fuente: await self.cargar_datos()
            else: raise Exception("No se pudo anexar la fuente")
        except Exception as e: print("Error al anexar fuente:", e)
        self.pagina.pop_dialog()

    async def _desvincular_fuente(self, fuente_id):
        try:
            exito = await ClienteAPI().desvincular_fuente(self.relacion.id, fuente_id)
            if exito: await self.cargar_datos()
            else: raise Exception("No se pudo desvincular la fuente")
        except Exception as e: print("Error al desvincular fuente:", e)

    def _eliminar_relacionado(self, persona_id: str):
        relacionado = self.relacion.traer_relacionado(persona_id)
        if relacionado is None: return

        self._modificar_relacion({
            "relacionados": [
                r for r in self.relacion.relacionados
                if r != relacionado
            ]
        })
