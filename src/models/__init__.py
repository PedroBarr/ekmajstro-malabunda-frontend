#-------------------------------------------------------------------------------
# Nombre:      Modelos de datos de la aplicación
# Proposito:   Empaquetar los modelos de datos de la aplicación
#              Malabunda (frontal).
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Modelos de datos de la aplicación

Empaquetar los modelos de datos de la aplicación Malabunda
(frontal). Empaqueta modelos para la representación,
transformación, serialización y deserialización de datos en
la aplicación.
"""

import flet as ft

from .persona import PersonaElemento
from themes import estilos_config

def colores_tipo_relacion(persona: PersonaElemento) -> list[ft.Colors]:
    colores: list[ft.Colors] = []

    if estilos_config.get('tipos_relacion'):
        colores = [
            (
                ft.Colors.with_opacity(
                    int(estilo.get('opacidad'), 16) / (255 * 2),
                    estilo.get('color')
                ) or
                ft.Colors.TRANSPARENT
            )
            for tipo, estilo in estilos_config['tipos_relacion'].items()
            if tipo in persona.relaciones.keys()
        ]
    
    colores.extend([ft.Colors.TRANSPARENT] * (len(colores) or 1))
    
    return colores