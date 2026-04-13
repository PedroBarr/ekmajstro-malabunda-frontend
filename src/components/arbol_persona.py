import flet as ft

from models.persona import Persona
from models.arbol_relaciones import ArbolRelaciones

from themes import estilos_config

def nodo_persona(
    persona: Persona,
    rol: str = "Relacionado",
    **parametros
) -> ft.Container:
    """ Función: NodoPersona

    Componente para construir un nodo de persona en el árbol de
    relaciones. Trayendo la foto de perfil de la persona en un
    círculo, y el nombre completo debajo de la foto.
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                persona.foto_perfil(25),
                ft.Text(
                    rol,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
            ],
             spacing=5,
             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
         ),
         **parametros
    )

def nodo_relacion(texto: str, tipo: str = "", **parametros) -> ft.Container:
    """ Función: NodoRelacion

    Componente para construir un nodo cabezera de tipo de
    relación en el árbol de relaciones. Mostrando el nombre del
    tipo de relación en un circulo, con el fondo según el tema.
    """
    return ft.Container(
        content=ft.Text(
            texto,
            size=12,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
        padding=10,
        bgcolor=estilos_config['tipos_relacion'].get(tipo, {}).get('borde', ft.Colors.GREY_500),
        border_radius=10,
        **parametros
    )

class ArbolPersona(ft.Container):
    """ Clase: ArbolPersona
        (Container)

    Componente para construir la visualización de un árbol de
    relaciones.

    Construye una grilla donde:
     - La primera columna muestra los tipos de relaciones (primera
        columna es la persona/raíz, las siguientes columnas son los
        tipos de relaciones).
     - Cada fila es una fecha que muestra las personas relacionadas
        en esa fecha por cada tipo de relación con la persona/raíz.
     - Entre cada nodo de persona se muestran una línea (por lo que
        no se usa una tabla)
    """
    def __init__(self, arbol: ArbolRelaciones):
        super().__init__()
        self._arbol: ArbolRelaciones = arbol
        self._persona: Persona = arbol.persona

        self._tipos = arbol.tipos_lista()
        self._fechas = arbol.fechas_lista()
    
    def _n_columnas(self):
        return len(self._tipos) + 1  # +1 para la columna de la persona/raíz

    def _n_filas(self):
        return len(self._fechas) + 1  # +1 para la fila de los tipos de relación
    
    def _cabecera(self):
        return ft.Row(
            controls=[
                nodo_persona(
                    self._persona,
                    expand=1,
                ),
                *[
                    nodo_relacion(
                        tipo,
                        tipo,
                        expand=3,
                    )
                    for tipo in self._tipos
                ]
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )
    
    def _fila_fecha(self, fecha):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        fecha or "",
                        expand=1,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    *[
                        ft.Column(
                            controls=[
                                ft.Container(
                                    width=20,
                                    height=(
                                        20 +
                                        119 * len(max(self._arbol.relaciones_por_fecha(fecha).values(), key=lambda x: len(x), default=[])) -
                                        119 * len(self._arbol.relaciones_por_fecha(fecha).get(tipo, []))
                                    ),
                                    bgcolor=estilos_config['tipos_relacion'].get(tipo, {}).get('borde', ft.Colors.GREY_500),
                                ),
                                *[
                                    ft.Column(
                                        [
                                            nodo_relacion(relacion_persona.get('nombre', 'Desconocido'), tipo),
                                            nodo_persona(relacion_persona.get('persona'), relacion_persona.get('rol', 'Relacionado')),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    )
                                    for relacion_persona in self._arbol.relaciones_por_fecha(fecha).get(tipo, [])
                                ],
                            ],
                            spacing=0,
                            expand=3,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                        for tipo in self._tipos
                    ]
                ],
                spacing=10,
            ),
            border=(
                None if fecha is None else
                ft.Border.only(top=ft.BorderSide(1, ft.Colors.with_opacity(0.15, ft.Colors.GREY_300), ft.BorderSideStrokeAlign.INSIDE, ft.BorderStyle.SOLID))
            ),
        )

    def construir(self):
        if not self._arbol or not self._arbol.persona:
            return ft.Container()
        
        return ft.Column(
            controls=[
                self._cabecera(),
                *[self._fila_fecha(fecha) for fecha in self._fechas]
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )