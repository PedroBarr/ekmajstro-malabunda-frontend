import flet as ft

from consts import etiquetas
from utils import rutas

ruta = rutas[etiquetas["DETAIL"]](":id")

def PersonaVista(pagina: ft.View):
    return ft.View(route=ruta, controls=[])