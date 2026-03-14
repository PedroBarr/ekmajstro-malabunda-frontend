import httpx

class APIClient:
    def __init__(self):
        self.base_url = "https://ekcion-malabunda-api.up.railway.app/"
        self.timeout = 10.0

    def obtener_nombre(self):
        try:
            respuesta = httpx.get(
                self.base_url,
                timeout=self.timeout
            )
            respuesta.raise_for_status()
            return respuesta.text
        except httpx.HTTPStatusError as exc:
            print(f"Error en la solicitud: {exc.response.status_code} - {exc.response.text}")
        except Exception as exc:
            print(f"Error inesperado: {exc}")