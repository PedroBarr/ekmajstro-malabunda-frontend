from pydantic import BaseModel
from .persona import Persona

from typing import List, Dict, Any, Optional

class ArbolRelaciones(BaseModel):
    persona: Persona
    relaciones: Dict[str, List[Dict[str, Any]]]
    fechas: List[str]

    def fechas_lista(self):
        fechas_unicas = sorted(set(self.fechas), key=lambda x: (x is not None, x))
        return [None] + fechas_unicas
    
    def tipos_lista(self):
        return [tipo for tipo in self.relaciones.keys()]
    
    def relacion_por_fecha_por_tipo(self, tipo: str, fecha: Optional[str]):
        if tipo not in self.relaciones:
            return []
        
        return [
            relacion_persona
            for relacion_persona in self.relaciones[tipo]
            if relacion_persona.get('fecha') == fecha
        ]
    
    def relaciones_por_fecha(self, fecha: Optional[str]):
        return {
            tipo: self.relacion_por_fecha_por_tipo(tipo, fecha)
            for tipo in self.relaciones.keys()
        }