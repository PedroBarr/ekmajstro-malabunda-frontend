#-------------------------------------------------------------------------------
# Nombre:      Componente Caja Error
# Proposito:   Contiene la clase caja error que muestra un mensaje
#               necesario para informar al usuario que ha ocurrido un
#               funcionamiento indeseado
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

def caja_error(
    mensaje: str,
    **parametros
) -> ft.Container:
    """ Función: Componente Caja Error

    Muestra un indicador de error con un mensaje de un estado
    indeseado.

    Parámetros:
        mensaje (str): Mensaje a mostrar.

    Retorno:
        una instancia de ft.Container con aspecto adaptable a
        diferentes jerarquías de la aplicación.
    """
    return caja_mensaje(
        mensaje=mensaje,
        **parametros
    )