import httpx

from consts import api_url, api_tiempo_espera, etiquetas

from models.persona import Persona

enlaces = {
    'nombre': lambda api: f'{api}',
    'personas': lambda api: f'{api}/personas',
}

class ClienteAPI:
    def __init__(self):
        self.url_base = api_url
        self.tiempo_espera = api_tiempo_espera

    def enlace(self, clave):
        return enlaces[clave](self.url_base)

    def envolver_peticion(funcion):
        async def envoltorio(self, *args, **kwargs):
            async with httpx.AsyncClient(timeout=self.tiempo_espera) as cliente:
                try: return await funcion(self, cliente, *args, **kwargs)
                except httpx.HTTPStatusError as exc:
                    print(
                        etiquetas["EXCEPTION_API_RESPONSE"](
                            exc.response.status_code,
                            exc.response.text
                        )
                    )
                except Exception as exc:
                    print(etiquetas["EXCEPTION_UNEXPECTED"](exc))
        return envoltorio

    @envolver_peticion
    async def obtener_config(self, cliente: httpx.AsyncClient):
        respuesta = await cliente.get(self.enlace('nombre'))
        respuesta.raise_for_status()
        nombre = respuesta.text.strip() if respuesta.text.strip() else None
        
        return {
            'nombre': nombre
        }

    @envolver_peticion
    async def obtener_personas(self, cliente: httpx.AsyncClient):
        respuesta = await cliente.get(self.enlace('personas'))
        respuesta.raise_for_status()
        return [Persona(**persona) for persona in respuesta.json()]