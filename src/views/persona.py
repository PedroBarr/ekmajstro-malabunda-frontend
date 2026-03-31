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
from datetime import datetime

from consts import etiquetas, configuracion
from utils import rutas
from api_client import ClienteAPI

from models.persona import Persona, PersonaElemento
from models.arbol_relaciones import ArbolRelaciones

from components.carta_persona import CartaPersona
from components.fila_lista import fila_lista
from components.resumen_evento import resumen_evento
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
        self._eventos = []
        
        self._personas: list[PersonaElemento] = []
        self._arbol: ArbolRelaciones = None
        self._grafo3d: Dict[str, List] = None

        self._altura_conmutador_principal = 230

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
            altura_forzada=self._altura_conmutador_principal,
            al_cambio=lambda _: self._actualizar_conmutador_principal(),
            inicio=1,
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
                    ClienteAPI().eventos_persona(self.persona.id)
                ).add_done_callback(
                    lambda fut: self._actualizar_eventos(fut.result())
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
                self.vista.controls = \
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

    async def _preprocesar_evento_a_agregar(self, evento: dict):
        if self.persona and self.persona.id:
            evento["personaId"] = self.persona.id
            
            if evento.get("fecha_fin") is None:
                del evento["fecha_fin"]
            
            try:
                await ClienteAPI().crear_evento_persona(evento=evento)
            except Exception as e:
                print(f"Error al crear el evento: {e}")
            finally:
                await self.cargar_datos()

        return True
    
    def _abrir_modal_agregar_evento(self):
        nombre_evento = ft.TextField(
            label="Nombre del evento",
            autofocus=True,
            expand=True,
        )

        hoy = datetime.now()
        fechas_evento = [hoy.strftime("%Y-%m-%d"), hoy.strftime("%Y-%m-%d")]

        fecha_inicio_evento_selector = ft.DatePicker(
            last_date=datetime(hoy.year + 1, 12, 31),
            on_change=lambda e: (
                fechas_evento.__setitem__(0, e.control.value.strftime("%Y-%m-%d")),
                setattr(fecha_inicio_evento_boton.content, "value", fechas_evento[0]),
            ),
        )

        fecha_inicio_evento_boton = ft.Button(
            content=ft.Text(fechas_evento[0]),
            on_click=lambda e: self.pagina.show_dialog(fecha_inicio_evento_selector),
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.WHITE,
            expand=True,
        )

        fecha_fin_evento_selector = ft.DatePicker(
            last_date=datetime(hoy.year + 1, 12, 31),
            on_change=lambda e: (
                fechas_evento.__setitem__(1, e.control.value.strftime("%Y-%m-%d")),
                setattr(fecha_fin_evento_boton.content, "value", fechas_evento[1]),
            ),
        )

        fecha_fin_evento_boton = ft.Button(
            content=ft.Text(fechas_evento[1]),
            on_click=lambda e: self.pagina.show_dialog(fecha_fin_evento_selector),
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.WHITE,
            expand=True,
        )

        incluir_fecha_fin = ft.Checkbox(
            label="Incluir fecha de fin",
            on_change=lambda _: setattr(fecha_fin_evento_boton, "visible", incluir_fecha_fin.value),
        )

        incluir_fecha_fin.value = False
        incluir_fecha_fin.on_change(None)

        nacionalidad_evento = ft.Dropdown(
            options=[
                ft.DropdownOption(key=nac, text=nac)
                for nac in configuracion["nacionalidades"]
            ],
            expand=True,
        )

        descripcion_evento = ft.TextField(
            label="Descripción del evento",
            multiline=True,
            expand=True,
            min_lines=2,
            max_lines=5,
        )

        confirmar_evento = lambda _: (
            asyncio.create_task(self._preprocesar_evento_a_agregar({
                "nombre": nombre_evento.value,
                "fecha_inicio": fechas_evento[0],
                "fecha_fin": fechas_evento[1] if incluir_fecha_fin.value else None,
                "nacionalidad": nacionalidad_evento.value,
                "descripcion": descripcion_evento.value,
            })).add_done_callback(
                lambda fut: self.pagina.pop_dialog() if fut.result() else None
            )
        )

        modal = ft.AlertDialog(
            title=ft.Text("Agregar un nuevo evento"),
            content=ft.Container(
                content=ft.Column(
                    [
                        nombre_evento,
                        ft.Row(
                            [
                                fecha_inicio_evento_boton,
                                fecha_fin_evento_boton,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [
                                incluir_fecha_fin,
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        nacionalidad_evento,
                        descripcion_evento,
                    ],
                    spacing=10,
                ),
                height=250,
            ),
            actions=[
                ft.Button(
                    "Cancelar",
                    on_click=lambda e: self.pagina.pop_dialog(),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.GREY_600,
                        padding=ft.Padding(25, 10, 25, 10),
                    ),
                ),
                ft.Button(
                    "Confirmar",
                    on_click=confirmar_evento,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.PRIMARY,
                        padding=ft.Padding(25, 10, 25, 10),
                    ),
                ),
            ],
        )

        self.pagina.show_dialog(modal)

    def _ir_a_relacionar_persona(self):
        modal = ft.AlertDialog(
            title=ft.Text("Relacionar con otra persona"),
            content=ft.Text("Funcionalidad en desarrollo."),
            actions=[
                ft.Button(
                    "Cerrar",
                    on_click=lambda e: self.pagina.pop_dialog(),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.PRIMARY,
                        padding=ft.Padding(25, 10, 25, 10),
                    ),
                )
            ],
        )

        self.pagina.show_dialog(modal)

    def _ver_articulo_relacionado(self):
        modal = ft.AlertDialog(
            title=ft.Text("Ver artículo relacionado"),
            content=ft.Text("Funcionalidad en desarrollo."),
            actions=[
                ft.Button(
                    "Cerrar",
                    on_click=lambda e: self.pagina.pop_dialog(),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.PRIMARY,
                        padding=ft.Padding(25, 10, 25, 10),
                    ),
                )
            ],
        )

        self.pagina.show_dialog(modal)

    def _reportar_error(self):
        modal = ft.AlertDialog(
            title=ft.Text("Reportar un error"),
            content=ft.Text("Se necesita iniciar sesión."),
            actions=[
                ft.Button(
                    "Cerrar",
                    on_click=lambda e: self.pagina.pop_dialog(),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.PRIMARY,
                        padding=ft.Padding(25, 10, 25, 10),
                    ),
                )
            ],
        )

        self.pagina.show_dialog(modal)
    
    async def _al_evento(self, evento: ft.Event, tipo: str):
        opciones = {
            'agregar_evento': self._abrir_modal_agregar_evento,
            'agregar_relacion': self._ir_a_relacionar_persona,
            'ver_articulo': self._ver_articulo_relacionado,
            'reportar_error': self._reportar_error,
        }

        if tipo in opciones:
            opciones[tipo]()
        else:
            dialogo = self.alerta_componente(
                contenido=ft.Text(
                    f"Incapaz de manejar evento '{tipo}'.",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                )
            )
            self.pagina.show_dialog(dialogo)
        
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
                            al_evento=self._al_evento,
                            editable=True,
                            expand=1,
                            elevation=5,
                            pagina=self.pagina,
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
                        lambda p: asyncio.create_task(self.pagina.push_route(rutas[etiquetas["DETAIL"]](p.id))),
                        compacta=True,
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
                    self.pagina.height - self._altura_conmutador_principal - 50
                ),
                angulo_elevacion_inicial=75,
                al_repintar=lambda: self.pagina.update(),
                al_ver_detalles=lambda id: \
                    asyncio.create_task(self.pagina.push_route(rutas[etiquetas["DETAIL"]](id))),
            )\
                .construir()
        )

    def _actualizar_personas(self, personas: list[PersonaElemento]):
        self._personas = personas
        self._actualizar_conmutador_principal()

    def _actualizar_eventos(self, eventos: list[Dict[str, str]]):
        self._eventos = eventos
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
        return (
            caja_mensaje(
                mensaje="No hay contexto disponible.",
            )
            if not self._eventos or self._eventos == []
            else ft.Column(
                [
                    resumen_evento(
                        evento,
                    )
                    for evento in self._eventos
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
            )
        )
    
    def _actualizar_conmutador_relaciones(self):
        self._envoltura_conmutador_relaciones.content = \
            self.conmutador_relaciones.construir()
        
    def alerta_componente(
        self,
        contenido: str,
    ):
        return ft.AlertDialog(
            content=contenido,
            alignment=ft.Alignment.CENTER,
            actions=[
                ft.Button(
                    ft.Text(
                        "Cerrar",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                    ),
                    on_click=lambda e: self.pagina.pop_dialog(),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.PRIMARY,
                        padding=ft.Padding(25, 10, 25, 10),
                    ),
                )
            ],
        )