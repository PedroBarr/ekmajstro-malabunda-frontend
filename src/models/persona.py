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
    modificado: Optional[datetime] = \
        Field(default_factory=datetime.now, alias="updatedAt")
    
    model_config = {"populate_by_name": True,}

    def imagen(self) -> ft.Control:
        imagen = self.metadatos.get("imagen")
        iniciales = (
            (self.nombre[0] if self.nombre else "") +
            (self.apellido[0] if self.apellido else "")
        )

        guardaespacio = "?" if not iniciales else iniciales.upper()

        if imagen:
            return ft.Image(src=imagen, width=50, height=50, fit=ft.ImageFit.COVER)
        else:
            return ft.Text(
                guardaespacio,
                size=25,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            )
        
    def marca_tiempo_modificacion(self) -> str:
        if not self.modificado: return ""
        return self.modificado.strftime("%Y-%m-%d %H:%M:%S")
        
    def modificar(self, dicc: Dict[str, Any]):
        for clave, valor in dicc.items():
            if hasattr(self, clave): setattr(self, clave, valor)

    @classmethod
    def sintetizar(
        cls,
        id: Optional[str] = None,
        nombre: Optional[str] = "",
        apellido: str = "",
        metadatos: Optional[Dict[str, Any]] = None,
        modificado: Optional[datetime] = None,
        dicc: Optional[Dict[str, Any]] = None,
    ):
        _id = id or (dicc.get("id") if dicc else None)
        _nombre = nombre or (dicc.get("nombre") if dicc else "")
        _apellido = apellido or (dicc.get("apellido") if dicc else "")
        _metadatos = metadatos or (dicc.get("metadata") if dicc else None) or {}
        _modificado = modificado or (dicc.get("updatedAt") if dicc else None) or datetime.now()
        return cls(
            id=_id,
            nombre=_nombre,
            apellido=_apellido,
            metadatos=_metadatos,
            modificado=_modificado,
        )