import flet as ft
import asyncio

from consts import etiquetas
from api_client import ClienteAPI
from router import Enrutador

from components.BFA_principal import BotonFlotanteAccionPrincipal
from views.bienvenida import elemento_bienvenida

def configurar(pagina: ft.Page):
    pagina.title = etiquetas["LOADING"]
    pagina.theme_mode = ft.ThemeMode.DARK

    BotonFlotanteAccionPrincipal.instancia(pagina)
    enrutador = Enrutador.instancia(pagina)

    pagina.on_route_change = enrutador.enrutador
    pagina.on_view_pop = enrutador.pinchar_vista

    asyncio.create_task(cargar_configuracion(pagina))

async def cargar_configuracion(pagina: ft.Page):
    config = await ClienteAPI().obtener_config()
    
    if config['nombre']:
        pagina.title = config['nombre']
        elemento_bienvenida.value = \
            etiquetas["WELCOME_MESSAGE"](config['nombre'])
        
        pagina.update()

async def index(pagina: ft.Page):
    configurar(pagina)
    await Enrutador.instancia().enrutador(None)

def main(): ft.run(index)

if __name__ == "__main__": main()