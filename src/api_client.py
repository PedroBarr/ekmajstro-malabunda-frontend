import httpx

class APIClient:
    def __init__(self):
        self.base_url = "https://ekcion-malabunda-api.up.railway.app"
        self.timeout = 10.0

    async def obtener_nombre(self):
        async with httpx.AsyncClient(timeout=self.timeout) as cliente:
            try:
                respuesta = await cliente.get(f'{self.base_url}')
                respuesta.raise_for_status()
                return respuesta.text
            except httpx.HTTPStatusError as exc:
                print(f"Error en la solicitud: {exc.response.status_code} - {exc.response.text}")
            except Exception as exc:
                print(f"Error inesperado: {exc}")

    def obtener_personas(self):
        try:
            respuesta = httpx.get(
                f'{self.base_url}/personas',
                timeout=self.timeout
            )
            respuesta.raise_for_status()
            return respuesta.json()
        except httpx.HTTPStatusError as exc:
            print(f"Error en la solicitud: {exc.response.status_code} - {exc.response.text}")
        except Exception as exc:
            print(f"Error inesperado: {exc}")