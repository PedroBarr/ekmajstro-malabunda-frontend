import flet as ft

class CampoEditable(ft.Container):
    def __init__(
            self,
            etiqueta: str,
            valor: str,
            al_cambio: callable,
            editable: bool = True,
            **param_contenedor
        ):
        super().__init__(**param_contenedor)
        self.etiqueta = etiqueta
        self.valor = valor
        self.al_cambio = al_cambio

        self._es_editando = False
        self._es_editable = editable

        self.expand = True

        self._calc_ini()
        self._contruir()

    def _calc_ini(self):
        if self._es_editable and self._no_valor():
            self._es_editando = True

    def _conmutar_modo(self, e):
        if self._es_editable:
            self._es_editando = not self._es_editando
            self._contruir()

    def _guardar_cambio(self, e):
        valor = e.control.value
        if self.valor != valor:
            self.valor = valor
            self.al_cambio(valor)

        self._es_editando = False
        self._contruir()

    def _no_valor(self):
        return not self.valor or self.valor == ""

    def _hay_valor(self):
        return not self._no_valor()

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

    def _contruir(self):
        self.content = self._modo_edicion() \
            if self._es_editando else self._modo_lectura()
