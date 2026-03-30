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

from consts import etiquetas, configuracion
from api_client import ClienteAPI
from router import Enrutador
from themes import (
    tema_modo,
    tema_ekmajstro,
    estilos_config,
    recursos_config,
)

from components.BFA_principal import BotonFlotanteAccionPrincipal
from views.bienvenida import elemento_bienvenida

# Función: Configurar la página principal de la aplicación
async def configurar(pagina: ft.Page):
    pagina.title = etiquetas["LOADING"]
    pagina.theme_mode = tema_modo
    pagina.theme = tema_ekmajstro()

    # Inicializar objetos de ejemplificación única
    BotonFlotanteAccionPrincipal.instancia(pagina)
    enrutador = Enrutador.instancia(pagina)

    # Configurar eventos de navegación
    pagina.on_route_change = enrutador.enrutador
    pagina.on_view_pop = enrutador.pinchar_vista

    await cargar_configuracion(pagina)

# Función asíncrona: Cargar la configuración de la aplicación
async def cargar_configuracion(pagina: ft.Page):
    try: config = await ClienteAPI().obtener_config()
    except Exception as e:
        elemento_bienvenida.value = etiquetas["ERROR_LOADING_CONFIG"]
        config = {}
    
    if config.get('nombre'):
        pagina.title = config['nombre']
        elemento_bienvenida.value = \
            etiquetas["WELCOME_MESSAGE"](config['nombre'])

    if config.get('tipos_relacion'):
        if config['tipos_relacion'].get('estilos'):
            estilos_config.update({
                'tipos_relacion': config['tipos_relacion']['estilos'],
            })
        
        if config['tipos_relacion'].get('tipos'):
            configuracion.update({
                'tipos_relacion': config['tipos_relacion']['tipos'],
            })

    if config.get('nacionalidades'):
        nacionalidades = {}
        for nacion in config['nacionalidades'].get('opciones', []):
            nacionalidades[nacion] = {
                'nombre': nacion,
                'emoticon': config['nacionalidades']\
                    .get('emoticones', {}).get(nacion, '🌍')
            }

        configuracion.update({
            'nacionalidades': nacionalidades.keys(),
        })

        recursos_config.update({
            'nacionalidades': nacionalidades,
        })

    pagina.update()

# Función asíncrona: Vista de inicio de la aplicación
async def index(pagina: ft.Page):
    await configurar(pagina)
    await Enrutador.instancia().enrutador(None)

# Función: Ejecutar la aplicación
def main(): ft.run(index, assets_dir="assets")

if __name__ == "__main__": main()