import flet as ft

from consts import etiquetas
from models.persona import Persona

def fila_lista(persona: Persona, on_click: callable):
    return ft.ListTile(
        leading=ft.CircleAvatar(),
        title=ft.Text(f'{persona.apellido}, {persona.nombre}'),
        subtitle=ft.Text(etiquetas["ID_LABEL"](persona.id)),
        on_click=lambda _: on_click(persona)
    )