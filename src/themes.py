#-------------------------------------------------------------------------------
# Nombre:      Temas de la aplicación
# Proposito:   Contiene funciones relacionadas con la configuración
#              de temas y estilos de la aplicación
#
# Autor:       Aref
#
# Creado:      23/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft

def tema_ekmajstro() -> ft.Theme:
    """ Función: Tema principal (Ekmajstro)

    Retorna la configuración de estilos y colores principal.

    Retorno:
        una instancia de ft.Theme con las configuraciones de
        estilo y color de la aplicación.
    """
    return ft.Theme(
        scaffold_bgcolor="0xFF242424",
        color_scheme=ft.ColorScheme(
            primary="0xFF545A70",
            on_primary="0xFFFFFFFF",
            secondary="0xFF545A70",
            on_secondary="0xFFDADADA",
            error="0xAAFA5A65",
            on_error="0xFF1F1D2A",
            surface="0xFF555555",
            on_surface=ft.Colors.WHITE,
        ),
        text_theme=ft.TextTheme(
            headline_medium=ft.TextStyle(
                color="0xFF1F1D2A",
                font_family="Roboto",
            ),
            headline_large=ft.TextStyle(
                color="0xFF1F1D2A",
            ),
        ),
        use_material3=True,
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.PREDICTIVE,
        ),
    )

# Configuración de modo de tema (oscuro)
tema_modo = ft.ThemeMode.DARK

estilos_config = {}