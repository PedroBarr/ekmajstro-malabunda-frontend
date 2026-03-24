#-------------------------------------------------------------------------------
# Nombre:      Componente Campo Editable
# Proposito:   Contiene la clase campo editable que sirve para mostrar
#               una interfaz de edición de un campo de texto
#
# Autor:       Aref
#
# Creado:      23/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft

class CampoEditable(ft.Container):
    """ Clase: Campo Editable

    Componente para mostrar una interfaz conmutable entre modo
    de lectura y modo de edición, con el propósito de permitir
    la edición de valores de texto.
    """

    # Método dunder de inicialización
    def __init__(
            self,
            etiqueta: str,
            valor: str,
            al_cambio: callable,
            editable: bool = True,
            **param_contenedor
        ):
        super().__init__(**param_contenedor)
        # Variables expuestas
        self.etiqueta = etiqueta
        self.valor = valor
        self.al_cambio = al_cambio

        # Variables internas
        self._es_editando = False
        self._es_editable = editable

        # Inicialización
        self.expand = True

        self._calc_ini()
        self._contruir()

    # Función: Calcular estado inicial de edición
    def _calc_ini(self):
        if self._es_editable and self._no_valor():
            self._es_editando = True

    # Función: Conmutar entre modo de lectura y edición
    def _conmutar_modo(self, e):
        if self._es_editable:
            self._es_editando = not self._es_editando
            self._contruir()

    # Función: Guardar cambio y disparar el callback de cambio
    def _guardar_cambio(self, e):
        valor = e.control.value
        if self.valor != valor:
            self.valor = valor
            self.al_cambio(valor)

        self._es_editando = False
        self._contruir()

    # Función: Validador de valor
    def _no_valor(self):
        return not self.valor or self.valor == ""

    # Función: Validador de campo
    def _hay_valor(self):
        return not self._no_valor()

    # Función: Obtener render de modo lectura
    def _modo_lectura(self):
        return ft.Container(
            content=ft.Text(
                self.valor if self._hay_valor() else self.etiqueta,
                size=20,
                color=ft.Colors.ON_SURFACE
                    if self._hay_valor()
                    else ft.Colors.OUTLINE_VARIANT,
            ),
            expand=True,
            align=ft.Alignment.CENTER_LEFT,
            on_click=self._conmutar_modo,
        )
    
    # Función: Obtener render de modo edición
    def _modo_edicion(self):
        return ft.TextField(
            label=self.etiqueta,
            value=self.valor,
            on_submit=self._guardar_cambio,
            on_blur=self._guardar_cambio,
            autofocus=True,
            expand=True,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(
                size=16,
                color=ft.Colors.ON_SURFACE,
            ),
            label_style=ft.TextStyle(
                size=12,
                color=ft.Colors.OUTLINE,
            ),
            dense=True,
        )

    # Función: Construir render
    def _contruir(self):
        self.content = self._modo_edicion() \
            if self._es_editando else self._modo_lectura()
