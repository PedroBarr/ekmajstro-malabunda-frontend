import flet as ft

def tema_ekmajstro() -> ft.Theme:
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


tema_modo = ft.ThemeMode.DARK