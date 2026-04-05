#-------------------------------------------------------------------------------
# Nombre:      Cliente API de la aplicación
# Proposito:   Contiene el cliente API para interactuar con el
#              dorsal
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import httpx
import mimetypes

from consts import api_url, api_tiempo_espera, etiquetas

from models.persona import Persona, PersonaElemento
from models.relacion import Relacion
from models.arbol_relaciones import ArbolRelaciones

# Enlaces de la API para diferentes recursos
enlaces = {
    'nombre': lambda api: f'{api}',
    'personas': lambda api: f'{api}/personas',
    'persona': lambda api: f'{api}/personas/{{id}}',
    'config_tipos_relacion': lambda api: f'{api}/tipos_relacion/config',
    'config_eventos': lambda api: f'{api}/eventos/config',
    'relacion': lambda api: f'{api}/relaciones/{{id}}',
    'relaciones_conteo_persona': lambda api: f'{api}/relaciones/persona/{{id}}/conteo',
    'relaciones_persona': lambda api: f'{api}/relaciones/persona/{{id}}',
    'relaciones_personas_persona': lambda api: f'{api}/relaciones/personas/{{id}}',
    'relaciones_arbol_persona': lambda api: f'{api}/relaciones/persona/{{id}}/arbol',
    'relaciones_grafo_persona': lambda api: f'{api}/relaciones/persona/{{id}}/grafico3d',
    'crear_relacion': lambda api: f'{api}/relaciones',
    'eventos_persona': lambda api: f'{api}/eventos/persona/{{id}}',
    'crear_evento_persona': lambda api: f'{api}/eventos',
    'anexar_fuente': lambda api: f'{api}/fuentes/anexar/{{id}}',
}

class ClienteAPI:
    """ Clase: Cliente API

    Cliente para interactuar con la API del dorsal.

    Define metodos asíncronos y decoradores para la gestión
    de las peticiones a la API, el manejo de errores y la
    obtención de datos para su uso en la aplicación.
    """

    # Método dunder de inicialización
    def __init__(self):
        self.url_base = api_url
        self.tiempo_espera = api_tiempo_espera

    # Función privada: Obtener el enlace para el endpoint de la API
    def _enlace(self, clave: str): return enlaces[clave](self.url_base)

    # Decorador: Envolver las funciones de petición a la API para
    #  manejar errores y gestionar el cliente HTTP
    def envolver_peticion(funcion: callable):
        # Envoltura asíncrona para manejar la petición a la API
        async def envoltorio(self, *args, **kwargs):
            async with httpx.AsyncClient(timeout=self.tiempo_espera) as cliente:
                try:
                    # parámetro para forzar excepciones en pruebas
                    if kwargs.get("forzar_exc"):
                        raise Exception(etiquetas["EXCEPTION_FORCED"])
                    
                    return await funcion(self, cliente, *args, **kwargs)
                except httpx.HTTPStatusError as exc:
                    print(
                        etiquetas["EXCEPTION_API_RESPONSE"](
                            exc.response.status_code,
                            exc.response.text
                        )
                    )

                    if not kwargs.get("omitir_exc"): raise exc
                    
                except Exception as exc:
                    print(etiquetas["EXCEPTION_UNEXPECTED"](exc))

                    # parámetro para omitir excepciones
                    if not kwargs.get("omitir_exc"): raise exc

        return envoltorio

    # Función asíncrona envuelta: Obtener la configuración
    #  inicializada en la API
    @envolver_peticion
    async def obtener_config(self, cliente: httpx.AsyncClient):
        # Nombre
        respuesta = await cliente.get(self._enlace('nombre'))
        respuesta.raise_for_status()
        nombre = respuesta.text.strip() if respuesta.text.strip() else None

        # Tipos relacion
        respuesta = await cliente.get(self._enlace('config_tipos_relacion'))
        respuesta.raise_for_status()
        config_tipos_relacion = respuesta.json()
        estilos_tipos_relacion = config_tipos_relacion.get('estilo', {})
        tipos_relacion = config_tipos_relacion.get('tipos', [])
        cantidad_tipos_relacion = config_tipos_relacion.get('cantidad', len(tipos_relacion))

        # Eventos
        respuesta = await cliente.get(self._enlace('config_eventos'))
        respuesta.raise_for_status()
        config_eventos = respuesta.json()
        nacionalidades = config_eventos.get('nacionalidades', [])
        cantidad_nacionalidades = config_eventos.get('cantidad', len(nacionalidades))
        emoticones_nacionalidades = config_eventos.get('emoticones', {})

        return {
            'nombre': nombre,
            'tipos_relacion': {
                'estilos': estilos_tipos_relacion,
                'tipos': tipos_relacion,
                'cantidad': cantidad_tipos_relacion,
            },
            'nacionalidades': {
                'opciones': nacionalidades,
                'cantidad': cantidad_nacionalidades,
                'emoticones': emoticones_nacionalidades
            }
        }

    # Función asíncrona envuelta: Obtener la lista de personas
    #  desde la API y devolverla como una lista de objetos Persona
    @envolver_peticion
    async def obtener_personas(self, cliente: httpx.AsyncClient):
        respuesta = await cliente.get(self._enlace('personas'))
        respuesta.raise_for_status()
        return [PersonaElemento(**persona) for persona in respuesta.json()]
    
    # Función asíncrona envuelta: Obtener una persona específica por su ID
    #  desde la API y devolverla como un objeto Persona
    @envolver_peticion
    async def obtener_persona(self, cliente: httpx.AsyncClient, id: str):
        respuesta = await cliente.get(f"{self._enlace('persona')}".format(id=id))
        respuesta.raise_for_status()
        return Persona(**respuesta.json())
    
    # Función asíncrona envuelta: Parchar (actualizar parcialmente) una persona
    #  en la API con los cambios proporcionados y devolver la persona actualizada
    #  como un objeto Persona
    @envolver_peticion
    async def parchar_persona(self, cliente: httpx.AsyncClient, id: str, cambios: dict):
        respuesta = await cliente.patch(
            f"{self._enlace('persona')}".format(id=id),
            json=cambios
        )
        respuesta.raise_for_status()
        return Persona(**respuesta.json())
    
    # Función asíncrona envuelta: Crear una nueva persona en la API con los datos
    #  proporcionados y devolver la persona creada como un objeto Persona
    @envolver_peticion
    async def crear_persona(self, cliente: httpx.AsyncClient, persona: Persona):
        brutos = persona.model_dump(by_alias=True)
        if "_id" in brutos: del brutos["_id"]
        respuesta = await cliente.post(
            self._enlace('personas'),
            json=brutos
        )
        respuesta.raise_for_status()
        return Persona(**respuesta.json())
    
    @envolver_peticion
    async def obtener_relacion(self, cliente: httpx.AsyncClient, id: str):
        respuesta = await cliente.get(f"{self._enlace('relacion')}".format(id=id))
        respuesta.raise_for_status()
        return Relacion(**respuesta.json())
    
    @envolver_peticion
    async def parchar_relacion(
        self,
        cliente: httpx.AsyncClient,
        id: str,
        relacion: dict
    ):
        respuesta = await cliente.patch(
            f"{self._enlace('relacion')}".format(id=id),
            json=relacion.model_dump(by_alias=True)
        )
        respuesta.raise_for_status()
        return Relacion(**respuesta.json())

    @envolver_peticion
    async def relaciones_conteo_persona(self, cliente: httpx.AsyncClient, id: str):
        respuesta = await cliente.get(f"{self._enlace('relaciones_conteo_persona')}".format(id=id))
        respuesta.raise_for_status()
        return respuesta.json()
    
    @envolver_peticion
    async def relaciones_persona(self, cliente: httpx.AsyncClient, id: str):
        respuesta = await cliente.get(f"{self._enlace('relaciones_persona')}".format(id=id))
        respuesta.raise_for_status()
        return [Relacion(**relacion) for relacion in respuesta.json()]

    @envolver_peticion
    async def relaciones_personas_persona(self, cliente: httpx.AsyncClient, id: str):
        respuesta = await cliente.get(f"{self._enlace('relaciones_personas_persona')}".format(id=id))
        respuesta.raise_for_status()
        return [
            PersonaElemento(
                _id=persona.get('personaId').get('_id'),
                nombre=persona.get('personaId').get('nombre'),
                apellido=persona.get('personaId').get('apellido'),
                relaciones=persona.get('relaciones', {})
            )
            for persona in respuesta.json()
        ]

    @envolver_peticion
    async def relaciones_arbol_persona(self, cliente: httpx.AsyncClient, persona: Persona):
        respuesta = await cliente.get(f"{self._enlace('relaciones_arbol_persona')}".format(id=persona.id))
        respuesta.raise_for_status()
        relaciones = {}

        for relacion in respuesta.json():
            if relacion == "fechas": continue
            
            relaciones[relacion] = [
                {
                    'persona': Persona(
                        _id=relacion_persona.get('personaId').get('_id'),
                        nombre=relacion_persona.get('personaId').get('nombre'),
                        apellido=relacion_persona.get('personaId').get('apellido'),
                        metadatos=relacion_persona.get('personaId').get('metadata', {}),
                    ),
                    'fecha': relacion_persona.get('fecha', None),
                    'nombre': relacion_persona.get('nombreRelacion', ""),
                }
                for relacion_persona in respuesta.json()[relacion]
            ]
        
        return ArbolRelaciones(
            persona=persona,
            relaciones=relaciones,
            fechas=respuesta.json().get('fechas', [])
        )
    
    @envolver_peticion
    async def relaciones_grafo_persona(self, cliente: httpx.AsyncClient, persona: Persona):
        respuesta = await cliente.get(f"{self._enlace('relaciones_grafo_persona')}".format(id=persona.id))
        respuesta.raise_for_status()
        return respuesta.json()
    
    @envolver_peticion
    async def crear_relacion(self, cliente: httpx.AsyncClient, relacion: Relacion):
        respuesta = await cliente.post(
            self._enlace('crear_relacion'),
            json=relacion.model_dump(by_alias=True, include_id=False)
        )
        
        respuesta.raise_for_status()
        return Relacion(**respuesta.json())
    
    @envolver_peticion
    async def eventos_persona(self, cliente: httpx.AsyncClient, id: str):
        respuesta = await cliente.get(f"{self._enlace('eventos_persona')}".format(id=id))
        respuesta.raise_for_status()
        return respuesta.json()
    
    @envolver_peticion
    async def crear_evento_persona(self, cliente: httpx.AsyncClient, evento: dict):
        respuesta = await cliente.post(self._enlace('crear_evento_persona'),json=evento)
        respuesta.raise_for_status()
        return respuesta.json()
    
    @envolver_peticion
    async def anexar_fuente(
        self,
        cliente: httpx.AsyncClient,
        id: str,
        fuente: dict # debe contener 'nombre', 'descripcion' y 'archivo' (ft.FilePickerFile with bytes)
    ):
        # hacer un patch form-data con las llaves 'nombre' y 'descripcion' (de tipo texto), y 'archivo' (de tipo file)
        assert (
            'nombre' in fuente and
            'descripcion' in fuente and
            'archivo' in fuente and
            hasattr(fuente['archivo'], 'name') and
            hasattr(fuente['archivo'], 'bytes')
        ), "La fuente no pudo ser anexada por datos faltantes o mal formateados."
        tipo = mimetypes.guess_type(fuente['archivo'].name)[0] or 'application/octet-stream'
        archivos = {
            'archivo': (fuente['archivo'].name, fuente['archivo'].bytes, tipo)
        }
        datos = {
            'nombre': fuente['nombre'],
            'descripcion': fuente['descripcion']
        }
        respuesta = await cliente.patch(
            f"{self._enlace('anexar_fuente')}".format(id=id),
            data=datos,
            files=archivos
        )
        respuesta.raise_for_status()
        return respuesta.json()

