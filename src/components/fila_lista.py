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

# Función: Crear una fila de lista con información de una persona
def fila_lista(persona: PersonaElemento, on_click: callable):
    return ft.ListTile(
        leading=ft.CircleAvatar(),
        title=ft.Text(f'{persona.apellido}, {persona.nombre}'),
        subtitle=ft.Text(etiquetas["ID_LABEL"](persona.id)),
        on_click=lambda _: on_click(persona)
    )