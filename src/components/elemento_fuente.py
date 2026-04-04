import flet as ft
from typing import Dict

class ElementoFuente(ft.Container):
    def __init__(
        self,
        fuente: Dict,
        al_clic=lambda f: None,
        **parametros
    ):
        super().__init__(**parametros)
        self._fuente = fuente
        self._al_clic = al_clic

    def _icono_tipo(self):
        tipo = self._fuente["tipoArchivo"]
        if tipo == "application/pdf":
            icono = ft.Icons.PICTURE_AS_PDF_ROUNDED
        elif tipo.startswith("image/"):
            icono = ft.Icons.TERRAIN_SHARP
        elif tipo.startswith("video/"):
            icono = ft.Icons.SLOW_MOTION_VIDEO_OUTLINED
        elif tipo.startswith("audio/"):
            icono = ft.Icons.MULTITRACK_AUDIO_ROUNDED
        elif tipo == "text/plain":
            icono = ft.Icons.SEGMENT_ROUNDED
        elif tipo == "text/html":
            icono = ft.Icons.HTML_ROUNDED
        elif tipo == "application/json":
            icono = ft.Icons.JAVASCRIPT_ROUNDED
        elif tipo == "text/uri-list":
            icono = ft.Icons.SEND_ROUNDED
        else:
            icono = ft.Icons.INSERT_DRIVE_FILE_ROUNDED

        return ft.CircleAvatar(
            content=ft.Icon(icono, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREY_700,
            radius=20,
        )

    def construir(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self._icono_tipo(),
                            ft.Text(
                                self._fuente["nombre"],
                                weight=ft.FontWeight.BOLD,
                                size=18,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Text(
                        self._fuente["descripcion"],
                        size=14,
                    ),
                ],
                spacing=10,
            ),
            padding=ft.Padding(15, 20, 15, 20),
            border=ft.Border.all(1, ft.Colors.GREY_700),
            border_radius=20,
            on_click=lambda e: self._al_clic(self._fuente),
        )