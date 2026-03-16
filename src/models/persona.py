from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Persona(BaseModel):
    id: str = Field(..., alias="_id")
    nombre: Optional[str]
    apellido: str
    metadatos: Optional[Dict[str, Any]] = \
        Field(default_factory=dict, alias="metadata")
    
    class ConfigDict: populate_by_name = True