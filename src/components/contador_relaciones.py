import flet as ft

from themes import estilos_config
from consts import configuracion

def contador_relaciones(
    relaciones: dict[str, int],
    compacta: bool = False,
) -> ft.Control:
    if relaciones is None: return ft.Container(expand=0)

    def linea(relacion: str, cantidad: int) -> ft.Control:
        return ft.Row(
            [
                ft.Container(
                    align=ft.Alignment.CENTER,
                    width=30,
                    height=3 if not compacta else 2,
                    bgcolor=estilos_config
                        .get('tipos_relacion', {})
                        .get(relacion, {})
                        .get('color', ft.Colors.TRANSPARENT)
                ),
                ft.Container(width=5),
                ft.Text(
                    str(cantidad),
                    color=ft.Colors.GREY_400,
                    size=12 if not compacta else 10,
                    weight=ft.FontWeight.W_900,
                ),
            ],
            spacing=2 if not compacta else 0,
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
            ft.Container(expand=1),
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
        expand=True,
    )