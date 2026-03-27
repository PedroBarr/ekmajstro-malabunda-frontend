#-------------------------------------------------------------------------------
# Nombre:      Componente Fila de Lista
# Proposito:   Contiene la función para crear una fila de lista con
#              información de una persona.
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft

from consts import etiquetas
from models.persona import PersonaElemento
from models import colores_tipo_relacion

# Función: Crear una fila de lista con información de una persona
def fila_lista(persona: PersonaElemento, on_click: callable):
    return ft.Container(
        content=ft.Row(
            [
                persona.foto_perfil(22),
                ft.Container(width=10),
                ft.Column(
                    [
                        ft.Text(
                            f'{persona.apellido}, {persona.nombre}',
                            size=19,
                            weight=ft.FontWeight.W_900,
                            color=ft.Colors.GREY_400,
                        ),
                        ft.Text(
                            etiquetas["ID_LABEL"](persona.id),
                            size=14,
                            color=ft.Colors.GREY,
                        ),
                    ],
                    spacing=2,
                ),
            ],
        ),
        on_click=lambda _: on_click(persona),
        padding=10,
        border_radius=25,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.BOTTOM_RIGHT,
            end=ft.Alignment.TOP_LEFT,
            colors=colores_tipo_relacion(persona),
            rotation=0.4,
        ),
        border=ft.Border.all(1, ft.Colors.GREY_700),
    )