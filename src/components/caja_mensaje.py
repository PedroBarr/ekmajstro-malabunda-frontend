#-------------------------------------------------------------------------------
# Nombre:      Componente Caja Mensaje
# Proposito:   Contiene la clase caja mensaje que sirve de base para
#               la jerarquía de cajas de mensajes
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

def caja_mensaje(
    mensaje: str = None,
    componente: ft.Control = None,
    **parametros
) -> ft.Container: 
    assert mensaje or componente, etiquetas["ASSERT_CAJA_PARAM"]

    if mensaje and parametros.get("size") is None:
        parametros["size"] = 16
    
    contenido = (
        [ft.Text(mensaje, **parametros)]
        if mensaje
        else componente
    )

    return ft.Container(
        expand=True,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=contenido
                ),
            ]
        )
    )

from components.cajas_mensajes.caja_cargando import caja_cargando
from components.cajas_mensajes.caja_error import caja_error