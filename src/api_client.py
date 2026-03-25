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

from consts import api_url, api_tiempo_espera, etiquetas

from models.persona import Persona

# Enlaces de la API para diferentes recursos
enlaces = {
    'nombre': lambda api: f'{api}',
    'personas': lambda api: f'{api}/personas',
    'persona': lambda api: f'{api}/personas/{{id}}',
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
        
        return {
            'nombre': nombre
        }

    # Función asíncrona envuelta: Obtener la lista de personas
    #  desde la API y devolverla como una lista de objetos Persona
    @envolver_peticion
    async def obtener_personas(self, cliente: httpx.AsyncClient):
        respuesta = await cliente.get(self._enlace('personas'))
        respuesta.raise_for_status()
        return [Persona(**persona) for persona in respuesta.json()]
    
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