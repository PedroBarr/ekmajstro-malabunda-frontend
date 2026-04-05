import flet as ft
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from themes import estilos_config
from consts import configuracion

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
    
    def relacionados_cantidad(self) -> int:
        return len(self.relacionados)
    
    def relacionados_personas(self) -> List[PersonaElemento]:
        return [
            (
                relacionado
                if isinstance(relacionado, PersonaElemento)
                else PersonaElemento(**relacionado.get("personaId", {}))
            )
            for relacionado in self.relacionados
        ]
    
    def es_relacionada(self, persona_id: str): 
        return any(
            persona_id == (
                relacionado.id
                if isinstance(relacionado, PersonaElemento)
                else relacionado.get("personaId", {}).get("_id", "")
            )
            for relacionado in self.relacionados
        )
    
    def agregar_cambios(self, cambios: Dict[str, Any]):
        hay_cambios = False
        
        for clave, valor in cambios.items():
            if clave in self.contexto and self.contexto[clave] != valor:
                self.contexto[clave] = valor
                hay_cambios = True
            elif hasattr(self, clave) and getattr(self, clave) != valor:
                setattr(self, clave, valor)
                hay_cambios = True

        return hay_cambios
    
    def es_cargable(self) -> bool:
        descripcion = self.descripcion()
        fecha = self.fecha()

        return (
            self.nombre and self.nombre != "" and
            self.tipo and self.tipo in configuracion.get('tipos_relacion', ["relación_falsa"]) and
            descripcion and descripcion != "" and
            fecha and fecha != "" and
            self.relacionados_cantidad() >= 2 and
            all(relacionado.id and relacionado.id != "" for relacionado in self.relacionados_personas())
        )
    
    def model_dump(self, **parametros):
        incluir_id = parametros.get("include_id", True)
        
        if "include_id" in parametros: del parametros["include_id"]

        dicc = super().model_dump(**parametros)

        if not incluir_id and "_id" in dicc: del dicc["_id"]

        dicc['contexto'] = self.contexto
        
        dicc['relacionados'] = [
            {
                "rol": "Relacionado",
                "personaId": persona.id,
            }
            for persona in self.relacionados_personas()
        ]

        return dicc

    @classmethod
    def sintetizar(
        cls,
        id: Optional[str] = None,
        nombre: Optional[str] = "",
        tipo: Optional[str] = "",
        descripcion: Optional[str] = "",
        fecha: Optional[str] = "",
        dicc: Optional[Dict[str, Any]] = None,
        relacion: Optional["Relacion"] = None,
    ):
        _id = (
            id or
            (dicc.get("id") if dicc else None) or
            (relacion.id if relacion else None)
        )

        _nombre = (
            nombre or
            (dicc.get("nombre") if dicc else "") or
            (relacion.nombre if relacion else "")
        )

        _tipo = (
            tipo or
            (dicc.get("tipo") if dicc else "") or
            (relacion.tipo if relacion else "") or
            (
                configuracion['tipos_relacion'][0]
                if configuracion['tipos_relacion']
                else ""
            )
        )

        _descripcion = (
            descripcion or
            (dicc.get("contexto", {}).get("descripcion") if dicc else "") or
            (relacion.descripcion() if relacion else "")
        )
        
        _fecha = (
            fecha or
            (dicc.get("contexto", {}).get("fecha") if dicc else "") or
            (relacion.fecha() if relacion else "") or
            datetime.now().strftime("%Y-%m-%d")
        )

        _contexto = (
            (dicc.get("contexto", {}) if dicc else None) or
            (relacion.contexto if relacion else None) or
            {}
        )

        _contexto.update({
            "descripcion": _descripcion,
            "fecha": _fecha,
        })

        return cls(
            id=_id,
            nombre=_nombre,
            tipo=_tipo,
            contexto=_contexto,
        )
    
    def traer_relacionado(self, personaId: str) -> PersonaElemento | Dict | None:
        for relacionado in self.relacionados:
            persona = (
                relacionado
                if isinstance(relacionado, PersonaElemento)
                else PersonaElemento(**relacionado.get("personaId", {}))
            )
            if persona.id == personaId: return relacionado
        
        return None
    
    def agregar_relacionado(
        self,
        persona: PersonaElemento,
        rol: str = "Relacionado",
        modo_retorno: bool = False,
    ):
        personaJson = persona.model_dump(by_alias=True, exclude={"metadatos",})
        if modo_retorno:
            return {
                "personaId": personaJson,
                "rol": rol,
            }
        
        if not self.traer_relacionado(persona.id):
            self.relacionados.append({
                "personaId": personaJson,
                "rol": rol,
            })