import flet as ft

from themes import estilos_config
from consts import configuracion

def contador_relaciones(relaciones: dict[str, int]) -> ft.Control:

    def linea(relacion: str, cantidad: int) -> ft.Control:
        return ft.Row(
            [
                ft.Container(
                    align=ft.Alignment.CENTER,
                    width=30,
                    height=3,
                    bgcolor=estilos_config
                        .get('tipos_relacion', {})
                        .get(relacion, {})
                        .get('color', ft.Colors.TRANSPARENT)
                ),
                ft.Container(width=5),
                ft.Text(
                    str(cantidad),
                    color=ft.Colors.GREY_400,
                    size=12,
                    weight=ft.FontWeight.W_900,
                ),
            ],
             spacing=2,
        )

    return ft.Row(
        [
            ft.Column(
                [
                    linea(tipo, relaciones.get(tipo, 0))
                    for tipo in configuracion.get('tipos_relacion', [])
                ],
                spacing=0,
            ),
            ft.Container(width=15),
            ft.Text(
                str(sum(relaciones.values())),
                size=40,
                weight=ft.FontWeight.W_900,
                color=ft.Colors.GREY_100,
                text_align=ft.TextAlign.CENTER,
                align=ft.Alignment.CENTER,
            ),
        ],
        spacing=5,
    )