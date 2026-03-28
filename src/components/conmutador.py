import flet as ft

from typing import Callable, List

class Conmutador(ft.Container):
    def __init__(
        self,
        iconos: list[ft.Control],
        componentes: List[ft.Control | Callable],
        etiquetas: list[str] = None,
        inicio: int = 0,
        al_cambio: callable = None,
        altura_forzada: int = None,
    ) -> None:
        super().__init__()

        self.iconos = iconos
        self.componentes = componentes

        assert len(iconos) == len(componentes), \
            "La cantidad de iconos y componentes debe ser la misma."
        
        assert len(iconos) > 0, \
            "Debe haber al menos un icono y componente para el conmutador."

        if etiquetas:
            assert len(etiquetas) == len(iconos), \
                "La cantidad de etiquetas debe coincidir con la de iconos y componentes."
            
        else:
            etiquetas = [f"Opción {i+1}" for i in range(len(iconos))]

        self.etiquetas = etiquetas

        assert type(inicio) == int and 0 <= inicio < len(iconos), \
            "El índice de inicio debe ser un entero válido."

        self.indice_actual = inicio
        self.al_cambio = al_cambio

        self.altura_forzada = altura_forzada

        self.construir()

    def _cambiar_opcion(self, indice: int):
        if indice != self.indice_actual:
            self.indice_actual = indice
            self.construir()

            if self.al_cambio:
                self.al_cambio(indice)

    def _lista_opciones(self):
        return [
            (
                icono if isinstance(icono, ft.Control) else
                icono(etiqueta=etiqueta) if callable(icono) else
                (
                    ft.Container(
                        width=30,
                        height=30,
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=10,
                        content=ft.IconButton(
                            icon=ft.Icon(
                                icono if type(icono).__name__ in ['str', 'Icons'] else ft.Icons.CIRCLE,
                                color=ft.Colors.GREY_300,
                                size=12,
                            ),
                            on_click=lambda _, i=i: self._cambiar_opcion(i)
                        ),
                        border=ft.Border.all(1, ft.Colors.GREY_500),
                        tooltip=(
                            ft.Tooltip(
                                etiqueta,
                                bgcolor=ft.Colors.GREY_700,
                            ) if etiqueta else None
                        ),
                    )
                )
            )
            for i, (icono, etiqueta) in enumerate(zip(self.iconos, self.etiquetas))
        ]
    
    def _obtener_componente_actual(self):
        componente = self.componentes[self.indice_actual]
        return componente() if callable(componente) else componente

    def construir(self) -> ft.Control:
        return ft.Column(
            [
                ft.Row(
                    controls=self._lista_opciones(),
                    spacing=10,
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=self._obtener_componente_actual(),
                            expand=1,
                            height=self.altura_forzada,
                        ),
                    ],
                    expand=1
                ),
            ],
            spacing=20,
        )