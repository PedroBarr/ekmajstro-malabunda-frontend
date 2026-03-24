#-------------------------------------------------------------------------------
# Nombre:      Vista de lista de personas
# Proposito:   Contiene la clase lista de personas
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
from utils import rutas
from api_client import ClienteAPI

from models.persona import Persona
from components.fila_lista import fila_lista
from components.caja_mensaje import caja_error

ruta = rutas[etiquetas["LIST"]]

class Lista:
    """ Clase: Lista

    Vista de lista de personas.

    Define metodos asíncronos y variables internas para la
    gestión de la vista, la navegación y la interacción con la
    API para obtener los datos de las personas y mostrarlos en
    la interfaz.
    """

    # Método dunder de inicialización
    def __init__(self, pagina: ft.Page):
        self.pagina = pagina
        self.vista_lista = ft.ListView(expand=True, spacing=10, padding=10)
        self.vista = self.construir()
    
    # Función asíncrona: Ir a la vista de detalle de una persona
    async def ir_a_detalle(self, persona_id = None):
        await self.pagina.push_route(rutas[etiquetas["DETAIL"]](persona_id))

    # Función: Agregar un botón para crear una nueva persona
    def _agregar_boton_crear(self):
        self.vista_lista.controls.insert(
            0,
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
                on_click=lambda e: \
                    asyncio.create_task(self.ir_a_detalle()),
            )
        )

    # Función asíncrona: Obtener la lista de personas
    #  y actualizar la vista con los datos obtenidos
    async def obtener_personas(self):
        self.vista_lista.controls.clear()
        try:
            personas: list[Persona] = \
                await ClienteAPI().obtener_personas()
            
        except Exception as e:
            self.vista_lista.controls.append(
                caja_error(etiquetas["ERROR_LOADING_LIST"])
            )
            
            # Para manejar excesión en que no trae datos
            personas = []
        
        for persona in personas:
            self.vista_lista.controls.append(
                fila_lista(
                    persona,
                    lambda p: asyncio.create_task(self.ir_a_detalle(p.id))
                )
            )

        self._agregar_boton_crear()
        self.vista.controls = [self.vista_lista]
        self.pagina.update()

    # Función: Construir la vista de lista de personas
    def construir(self):
        return ft.View(
            route=ruta,
            controls=[ft.Row(
                [ft.Column(
                    [
                        ft.ProgressRing(),
                        ft.Text(
                            etiquetas["LIST_TITLE"],
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=\
                        ft.CrossAxisAlignment.CENTER,
                ),],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )],
        )