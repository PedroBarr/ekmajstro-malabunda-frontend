import flet as ft
from typing import Dict
from datetime import datetime

from themes import recursos_config

def resumen_evento(
    evento: Dict[str, str],
    on_click: callable = lambda evento: None,
) -> ft.Container:
    tiene_fecha_fin = 'fecha_fin' in evento and evento['fecha_fin'] is not None
    linea_fecha = datetime.fromisoformat(evento['fecha_inicio'].replace("Z", "+00:00")).strftime("%Y-%m-%d")
    
    if tiene_fecha_fin:
        linea_fecha += " / " + datetime.fromisoformat(evento['fecha_fin'].replace("Z", "+00:00")).strftime("%Y-%m-%d")

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text(
                            (recursos_config['nacionalidades'].get(evento.get('nacionalidad', 'desconocida'), {})).get('emoticon', recursos_config['nacionalidades']['desconocida']['emoticon']),
                            size=30,
                        ),
                        ft.Container(width=10),
                        ft.Column(
                            [
                                ft.Text(
                                    evento.get("nombre", "Evento sin nombre"),
                                    size=19,
                                    weight=ft.FontWeight.W_900,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    linea_fecha,
                                    size=14,
                                    color=ft.Colors.GREY,
                                ),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                    ],
                ),
                ft.Text(
                    evento.get("descripcion", ""),
                    size=16,
                    color=ft.Colors.GREY_400,
                ),
            ],
            spacing=10,
        ),
        on_click=lambda _: on_click(evento),
        padding=ft.Padding(25, 10, 15, 25),
        border_radius=15,
        border=ft.Border.all(1, ft.Colors.GREY_700),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.BOTTOM_RIGHT,
            end=ft.Alignment.TOP_LEFT,
            colors=[
                ft.Colors.with_opacity(0.5, ft.Colors.PRIMARY),
                ft.Colors.with_opacity(0.8, ft.Colors.PRIMARY_FIXED_DIM),
                ft.Colors.TRANSPARENT,
                ft.Colors.BLUE_GREY_800,
            ],
            rotation=0.4,
        ),
    )