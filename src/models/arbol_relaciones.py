from pydantic import BaseModel
from .persona import Persona

from typing import List, Dict, Any, Optional

class ArbolRelaciones(BaseModel):
    persona: Persona
    relaciones: Dict[str, List[Dict[str, Any]]]
    fechas: List[str]