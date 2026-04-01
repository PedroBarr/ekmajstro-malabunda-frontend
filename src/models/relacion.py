import flet as ft

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from themes import estilos_config

from .persona import PersonaElemento

class Relacion(BaseModel):

    id: Optional[str] = Field(..., alias="_id")
    nombre: str
    tipo: str
    
    relacionados: Optional[List[PersonaElemento | Dict]] = Field(
        default_factory=list,
        exclude=True,
    )
    contexto: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        exclude=True,
    )

    fuentes: Optional[List[Any]] = Field(
        default_factory=list,
        exclude=True,
    )
    
    metadatos: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        exclude=True,
    )

    model_config = {"populate_by_name": True,}

    def color(self) -> ft.Colors:
        return estilos_config['tipos_relacion'].get(self.tipo, {}).get('color', ft.Colors.GREY)

    def borde(self) -> ft.Colors:
        return estilos_config['tipos_relacion'].get(self.tipo, {}).get('borde', ft.Colors.GREY)
    
    def descripcion(self) -> str:
        return self.contexto.get('descripcion', '')
    
    def fecha(self) -> str:
        return self.contexto.get('fecha', '')
    
    def relacionados_personas(self) -> List[PersonaElemento]:
        return [
            (
                relacionado
                if isinstance(relacionado, PersonaElemento)
                else PersonaElemento(**relacionado.get("personaId", {}))
            )
            for relacionado in self.relacionados
        ]