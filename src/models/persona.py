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

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Persona(BaseModel):
    """ Clase: Persona
        (BaseModel)

    Modelo de datos para representar a una persona para su
    serialización y deserialización en la aplicación.
    """
    id: str = Field(..., alias="_id")
    nombre: Optional[str]
    apellido: str
    metadatos: Optional[Dict[str, Any]] = \
        Field(default_factory=dict, alias="metadata")
    
    class ConfigDict: populate_by_name = True