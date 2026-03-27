#-------------------------------------------------------------------------------
# Nombre:      Constantes de la aplicación
# Proposito:   Contiene las constantes utilizadas en la aplicación
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import os

# Diccionario de etiquetas para la interfaz de usuario, mensajes de error,
#  notas de navegación, mensajes de aserción y excepciones.
etiquetas = {
    "LOADING": "Cargando...",

    # Indice
    "HOME": "Inicio",
    "LIST": "Lista",
    "DETAIL": "Detalle",

    # Vistas
    "ID_LABEL": lambda id: f"ID: {id}",
    "ERROR_LOADING_CONFIG": "Error. API no disponible.",

    "WELCOME_MESSAGE": lambda nombre: f"Bienvenido al Sistema {nombre}",
    "WELCOME_DESCRIPTION": "Explora una de las siguientes opciones",
    "GOTO": lambda destino: f"Ir a {destino}",

    "LIST_TITLE": "Lista de Personas",
    "ERROR_LOADING_LIST": "Error al cargar la lista.",
    "ADD_PERSON": "Agregar Persona",

    "ERROR_LOADING_DETAIL": "Error al cargar la persona.",
    "UNCOMPLETED_FIELDS": "Por favor, completa todos los campos.",
    "LOADING_SYNC": "Sincronizando cambios...",

    # Navegación
    "TOOLTIP_HOME": "Volver al Inicio",

    # Aserciones
    "ASSERT_PAGE_PARAM": "La propiedad 'pagina' debe ser una instancia de ft.Page",
    "ASSERT_API_PARAM": "La propiedad 'api' debe ser una instancia de ClienteAPI",
    "ASSERT_CAJA_PARAM": "Debe proporcionar un mensaje o un componente.",

    # Excepciones
    "EXCEPTION_API_RESPONSE":
        lambda estatus, texto: f"Error en la respuesta de la API: {estatus} - {texto}",
    "EXCEPTION_UNEXPECTED": lambda exc: f"Error inesperado: {exc}",
    "EXCEPTION_FORCED": "Excepción forzada para pruebas.",
}

# constantes de configuración de la API
api_url = os.getenv("API_URL", "https://ekcion-malabunda-api.up.railway.app")
api_tiempo_espera = 10.0

configuracion = {}