import flet as ft
from typing import Optional

from models.persona import Persona
from models.relacion import Relacion

class ElementoRelacion(ft.Container):
    def __init__(
        self,
        relacion: Relacion,
        persona: Optional[Persona] = None,
        al_clic=lambda r: None,
        **parametros
    ):
        super().__init__(**parametros)
        self._relacion = relacion
        self._persona = persona
        self._al_clic = al_clic

    def _celda_relacionado(self, relacionado: Persona, es_primario=True):
        return ft.Row(
            [
                (
                    ft.Container()
                    if es_primario
                    else ft.Container(
                        margin=ft.Margin(15, 0, 20, 0),
                        content=ft.Text(
                            "/",
                            weight=ft.FontWeight.W_900,
                            size=20
                        ),
                    )
                ),
                relacionado.foto_perfil(radio=15),
                ft.Text(
                    f"{relacionado.apellido}, {relacionado.nombre}",
                    color=ft.Colors.WHITE if es_primario else ft.Colors.GREY_300,
                    weight=ft.FontWeight.BOLD if es_primario else ft.FontWeight.NORMAL,
                ),
            ],
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
        )

    def _linea_relacionados(self):
        relacionados = self._relacion.relacionados_personas()
        relacionados.sort(
            key=lambda r:\
                r.id == (self._persona.id if self._persona else r.id),
            reverse=True
        )
        
        return (
            ft.Row(
                [
                    self._celda_relacionado(
                        relacionado,
                        es_primario=(relacionado.id == self._persona.id)
                    )
                    for relacionado in relacionados
                ],
                scroll='hidden',
            )
            if len(relacionados) > 0
            else  ft.Text("Relación sin personas relacionadas", color=ft.Colors.WHITE)
        )

    def _relacion_titulo(self, **parametros):
        return ft.Column(
            [
                ft.Text(
                    self._relacion.nombre,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=24,
                ),
                ft.Container(
                    height=8,
                    width=150,
                    bgcolor=self._relacion.color(),
                    border=ft.Border.all(1, self._relacion.borde()),
                    margin=ft.Margin(0, 5),
                ),
                ft.Text(
                    self._relacion.tipo,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=14,
                    italic=True,
                ),
            ],
            spacing=2,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            **parametros
        )
    
    def _relacion_cuerpo(self, **parametros):
        return ft.Column(
            [
                ft.Text(
                    self._relacion.fecha(),
                    color=ft.Colors.GREY_300,
                    size=14,
                    italic=True,
                ),
                ft.Text(
                    self._relacion.descripcion(),
                    color=ft.Colors.WHITE,
                    size=18,
                ),
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            **parametros
        )
    
    def construir(self):
        return ft.Container(
            content=ft.Column(
                [
                    self._linea_relacionados(),
                    ft.Row(
                        [
                            self._relacion_titulo(
                                expand=1,
                                margin=ft.Margin(0, 10, 0, 10),
                            ),
                            self._relacion_cuerpo(expand=2),
                            ft.Container(expand=2),
                        ],
                        spacing=5,
                        expand=True,
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[
                    ft.Colors.with_opacity(0.3, self._relacion.color()),
                    ft.Colors.with_opacity(0.5, self._relacion.borde()),
                    ft.Colors.with_opacity(0.6, self._relacion.color()),
                ],
            ),
            border=ft.Border.all(1, ft.Colors.GREY_700),
            border_radius=20,
            on_click=lambda e: self._al_clic(self._relacion),
        )