import flet as ft
import asyncio

from api_client import APIClient

from views.bienvenida import Bienvenida, elemento_bienvenida
from views.lista import Lista

api = APIClient()

async def index(pagina: ft.Page):
    pagina.title = "Cargando..."
    pagina.theme_mode = ft.ThemeMode.DARK
    
    async def enrutador(e):
        pagina.views.clear()

        if pagina.route == "/": pagina.views.append(await Bienvenida(pagina))
        elif pagina.route == "/lista": pagina.views.append(await Lista(pagina, api))

        pagina.update()

    def pinchar_vista(e):
        if len(pagina.views) > 1:
            pagina.views.pop()
            pagina.go(pagina.views[-1].route)

    pagina.on_route_change = enrutador
    pagina.on_view_pop = pinchar_vista

    async def cargar_nombre():
        nombre = await api.obtener_nombre()
        if nombre:
            pagina.title = nombre
            elemento_bienvenida.value = f"Bienvenido al Sistema {nombre}"
            pagina.update()
    
    asyncio.create_task(cargar_nombre())
    await enrutador(None)

def main(): ft.app(target=index)

if __name__ == "__main__": main()