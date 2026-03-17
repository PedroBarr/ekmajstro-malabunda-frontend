#-------------------------------------------------------------------------------
# Nombre:      Aplicativo principal de Malabunda
# Proposito:   Contiene el aplicativo principal de Malabunda
#              (frontal) y su configuración.
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft
import asyncio

from consts import etiquetas
from api_client import ClienteAPI
from router import Enrutador

from components.BFA_principal import BotonFlotanteAccionPrincipal
from views.bienvenida import elemento_bienvenida

# Función: Configurar la página principal de la aplicación
def configurar(pagina: ft.Page):
    pagina.title = etiquetas["LOADING"]
    pagina.theme_mode = ft.ThemeMode.DARK

    # Inicializar objetos de ejemplificación única
    BotonFlotanteAccionPrincipal.instancia(pagina)
    enrutador = Enrutador.instancia(pagina)

    # Configurar eventos de navegación
    pagina.on_route_change = enrutador.enrutador
    pagina.on_view_pop = enrutador.pinchar_vista

    asyncio.create_task(cargar_configuracion(pagina))

# Función asíncrona: Cargar la configuración de la aplicación
async def cargar_configuracion(pagina: ft.Page):
    config = await ClienteAPI().obtener_config()
    
    if config['nombre']:
        pagina.title = config['nombre']
        elemento_bienvenida.value = \
            etiquetas["WELCOME_MESSAGE"](config['nombre'])
        
        pagina.update()

# Función asíncrona: Vista de inicio de la aplicación
async def index(pagina: ft.Page):
    configurar(pagina)
    await Enrutador.instancia().enrutador(None)

# Función: Ejecutar la aplicación
def main(): ft.run(index)

if __name__ == "__main__": main()