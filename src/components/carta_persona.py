import flet as ft

from models.persona import Persona

from components.campo_editable import CampoEditable

class CartaPersona(ft.Card):
    def __init__(
        self,
        persona: Persona,
        al_cambio: callable,
        editable: bool = True,
        **param_contenedor
    ):
        super().__init__(**param_contenedor)
        self.persona = persona
        self.al_cambio = al_cambio

        self._es_editable = editable

        self._construir()

    def _foto_perfil(self):
        return ft.CircleAvatar(
            radius=30,
            content=self.persona.imagen(),
            bgcolor=ft.Colors.BLUE_GREY_700,
        )
    
    def _modificar_persona(self, cambios: dict):
        self.persona.modificar(cambios)
        self.al_cambio(self.persona)
    
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
                                lambda valor: self._modificar_persona({
                                    "apellido": valor
                                }),
                                editable=self._es_editable,
                            ),
                            ft.Text("/", weight=ft.FontWeight.W_900, size=20),
                            ft.Container(width=25),
                            CampoEditable(
                                "Nombre",
                                self.persona.nombre,
                                lambda valor: self._modificar_persona({
                                    "nombre": valor
                                }),
                                editable=self._es_editable,
                            ),
                        ],
                    ),
                ],
            ),
        )
    
    def _cabecera(self):
        return ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self._foto_perfil(),
                    self._info_cabecera(),
                ]
            ),
        )
    
    def _divisor(self):
        divisor = ft.Divider(height=10, thickness=1, expand=1)

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
    
    def _marca_tiempo(self):
        return ft.Container(
            alignment=ft.Alignment.BOTTOM_RIGHT,
            content=ft.Text(
                f"Última modificación: {self.persona.marca_tiempo_modificacion()}",
                size=10,
                color=ft.Colors.OUTLINE,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ),
        )

    def _construir(self):
        self.content = ft.Container(
            padding=ft.Padding(20, 25, 20, 15),
            expand=True,
            content=ft.Column(
                spacing=10,
                controls=[
                    self._cabecera(),
                    self._divisor(),
                    self._marca_tiempo(),
                ]
            ),
        )