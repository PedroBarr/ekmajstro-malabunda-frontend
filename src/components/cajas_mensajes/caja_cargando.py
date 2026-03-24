#-------------------------------------------------------------------------------
# Nombre:      Componente Caja Cargando
# Proposito:   Contiene la clase caja cargando que muestra un
#               indicador de carga junto con un mensaje opcional.
#
# Autor:       Aref
#
# Creado:      23/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft

from consts import etiquetas
from components.caja_mensaje import caja_mensaje

def caja_cargando(
    mensaje: str = None,
    **parametros
) -> ft.Container:
    """ Función: Componente Caja Cargando

    Muestra un indicador de carga junto con un mensaje opcional.

    Parámetros:
        mensaje (str, opcional): Mensaje a mostrar junto al
            indicador de carga. Si no se proporciona, se usa el
            mensaje predeterminado de la aplicación.

    Retorno:
        una instancia de ft.Container con aspecto adaptable a
        diferentes jerarquías de la aplicación.
    """
    if parametros.get("size") is None:
        parametros["size"] = 16

    texto = mensaje if mensaje else etiquetas["LOADING"]

    return caja_mensaje(componente=[
        ft.ProgressRing(
            color=ft.Colors.PRIMARY,
            stroke_width=5,
            width=50,
            height=50
        ),
        ft.Container(height=20),
        ft.Text(
            texto,
            **parametros
        )
    ])