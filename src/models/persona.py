#-------------------------------------------------------------------------------
# Nombre:      Modelo Persona
# Proposito:   Contiene el modelo de datos para representar a una persona
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import flet as ft

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class Persona(BaseModel):
    """ Clase: Persona
        (BaseModel)

    Modelo de datos para representar a una persona para su
    serialización y deserialización en la aplicación.
    """
    id: Optional[str] = Field(..., alias="_id")
    nombre: Optional[str] = ""
    apellido: str
    metadatos: Optional[Dict[str, Any]] = \
        Field(default_factory=dict, alias="metadata")
    
    # Campo para controlar la fecha de modificación, sin sintezación
    modificado: Optional[datetime] = Field(
        default_factory=datetime.now,
        alias="updatedAt",
        exclude=True
    )
    
    model_config = {"populate_by_name": True,}

    # Función: obtener imagen dinámica
    def imagen(
        self,
        medida: int = 50,
        medida_fuente: int = 25,
    ) -> ft.Control:
        # Opción: Existe imagen en metadatos
        imagen = self.metadatos.get("imagen")

        # Opción: Usar iniciales del nombre y apellido
        iniciales = (
            (self.nombre[0] if self.nombre else "") +
            (self.apellido[0] if self.apellido else "")
        )

        # Opción: No existen datos
        guardaespacio = "?" if not iniciales else iniciales.upper()

        # Retornar imagen si existe
        if imagen:
            return ft.Image(
                src=imagen,
                width=medida,
                height=medida,
                fit=ft.ImageFit.COVER,
            )
        
        # Retornar cadena si no existe imagen
        else:
            return ft.Text(
                guardaespacio,
                size=medida_fuente,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
                style=ft.TextStyle(
                    letter_spacing=3,
                ),
            )
        
    # Función: Obtener render de foto de perfil
    def foto_perfil(self, radio: int = 30) -> ft.Control:
        return ft.CircleAvatar(
            radius=radio,
            content=self.imagen(radio, radio // 1.5),
            bgcolor=ft.Colors.PRIMARY,
        )

    # Función: obtener marca de tiempo de modificación
    def marca_tiempo_modificacion(self) -> str:
        if not self.modificado: return ""
        return self.modificado.strftime("%Y-%m-%d %H:%M:%S")

    # Función: modificar campos de la persona a partir de un diccionario
    def modificar(self, dicc: Dict[str, Any]):
        for clave, valor in dicc.items():
            if hasattr(self, clave): setattr(self, clave, valor)

    # Función: calcular cambios con respecto a otra persona
    def cambios(self, persona: "Persona") -> Dict[str, Any]:
        cambios = {}

        # Comparar campos directos
        for campo in self.__class__.model_fields:
            valor_actual = getattr(self, campo)
            valor_nuevo = getattr(persona, campo)
            if campo == "metadatos": continue
            
            if valor_actual != valor_nuevo:
                cambios[campo] = valor_nuevo
        
        claves_metadatos = (
            set(self.metadatos.keys()) |
            set(persona.metadatos.keys())
        )
        
        # Comparar campos de metadatos
        for clave in claves_metadatos:
            valor_actual = self.metadatos.get(clave) or None
            valor_nuevo = persona.metadatos.get(clave) or None
            
            if valor_actual != valor_nuevo:
                cambios[f"metadata.{clave}"] = valor_nuevo

        return cambios

    # Función: Validar si se puede cargar la persona a la API
    def es_cargable(self) -> bool:
        return (
            self.apellido and self.apellido != ""
        )

    # Método de clase: sintetizar (parse) persona
    @classmethod
    def sintetizar(
        cls,
        id: Optional[str] = None,
        nombre: Optional[str] = "",
        apellido: str = "",
        metadatos: Optional[Dict[str, Any]] = None,
        modificado: Optional[datetime] = None,
        dicc: Optional[Dict[str, Any]] = None,
        persona: Optional["Persona"] = None,
    ):
        _id = (
            id or
            (dicc.get("id") if dicc else None) or
            (persona.id if persona else None)
        )

        _nombre = (
            nombre or
            (dicc.get("nombre") if dicc else "") or
            (persona.nombre if persona else "")
        )

        _apellido = (
            apellido or
            (dicc.get("apellido") if dicc else "") or
            (persona.apellido if persona else "")
        )

        _metadatos = (
            metadatos or
            (dicc.get("metadata") if dicc else None) or
            (persona.metadatos if persona else {}) or
            {}
        )

        _modificado = (
            modificado or
            (dicc.get("updatedAt") if dicc else None) or
            (persona.modificado if persona else datetime.now()) or
            datetime.now()
        )

        return cls(
            id=_id,
            nombre=_nombre,
            apellido=_apellido,
            metadatos=_metadatos,
            modificado=_modificado,
        )