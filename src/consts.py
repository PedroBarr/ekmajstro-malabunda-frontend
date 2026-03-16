import os

etiquetas = {
    "LOADING": "Cargando...",

    # Indice
    "HOME": "Inicio",
    "LIST": "Lista",
    "DETAIL": "Detalle",

    # Vistas
    "ID_LABEL": lambda id: f"ID: {id}",

    "WELCOME_MESSAGE": lambda nombre: f"Bienvenido al Sistema {nombre}",
    "WELCOME_DESCRIPTION": "Explora una de las siguientes opciones",
    "GOTO": lambda destino: f"Ir a {destino}",

    "LIST_TITLE": "Lista de Personas",

    # Tooltips
    "TOOLTIP_HOME": "Volver al Inicio",

    # Aserciones
    "ASSERT_PAGE_PARAM": "La propiedad 'pagina' debe ser una instancia de ft.Page",
    "ASSERT_API_PARAM": "La propiedad 'api' debe ser una instancia de ClienteAPI",

    # Excepciones
    "EXCEPTION_API_RESPONSE":
        lambda estatus, texto: f"Error en la respuesta de la API: {estatus} - {texto}",
    "EXCEPTION_UNEXPECTED": lambda exc: f"Error inesperado: {exc}",
}

api_url = os.getenv("API_URL", "https://ekcion-malabunda-api.up.railway.app")
api_tiempo_espera = 10.0