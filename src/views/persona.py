import flet as ft
import asyncio
import re

from consts import etiquetas
from utils import rutas
from api_client import ClienteAPI

from models.persona import Persona

from components.carta_persona import CartaPersona

ruta = rutas[etiquetas["DETAIL"]](":id")

class PersonaVista:
    def __init__(self, pagina: ft.Page, es_creacion: bool = False):
        self.pagina = pagina
        self.persona: Persona = Persona.sintetizar()
        self._actualizar_persona()
        self.construir(es_creacion=es_creacion)

    def _actualizar_persona(self):
        self._persona = Persona.sintetizar(persona=self.persona)

    def _obtener_id(self):
        ruta_actual = self.pagina.route
        patron = rutas[etiquetas["DETAIL"]](r"([A-Za-z0-9]+)")
        coincidencia = re.match(patron, ruta_actual)
        if coincidencia: self.persona.id = coincidencia.group(1)

    async def cargar_datos(self):
        self._obtener_id()
        
        try:
            self.persona = await ClienteAPI().obtener_persona(
                self.persona.id
            )
            self._actualizar_persona()
        except Exception as e: self.persona = None

        self._actualizar_carta()
        self.pagina.update()

    async def _sincronizar_cambios(self, cambios: dict):
        try:
            await ClienteAPI().parchar_persona(
                self.persona.id,
                cambios
            )
            self._actualizar_persona()
        except Exception as e: self.persona = None
        

    async def _modificar_persona(self, persona: Persona):
        cambios = self._persona.cambios(persona)
        if cambios:
            asyncio.create_task(self._sincronizar_cambios(cambios))
                    
        self.persona = persona
        self._actualizar_carta()
        self.pagina.update()
    
    def _controles(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                CartaPersona(
                    persona=self.persona,
                    al_cambio=lambda p: \
                        asyncio.create_task(
                            self._modificar_persona(p)
                        ),
                    editable=True,
                    expand=1,
                    elevation=5,
                ),
                ft.Container(expand=1),
            ]
        )
    
    def _carta_fallida(self):
        return ft.Container(
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Error al cargar los datos de la persona.",
                                size=20
                            )
                        ]
                    ),
                ]
            )
        )
    
    def _actualizar_carta(self):
        self.vista.controls = [
            self._controles() if self.persona else self._carta_fallida()
        ]

    def construir(self, es_creacion=False):
        self.vista = ft.View(
            route=ruta if not es_creacion else "/persona",
            controls=[self._controles()],
        )