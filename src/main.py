import flet as ft

from api_client import APIClient

from views.bienvenida import Bienvenida
from views.lista import Lista

api = APIClient()

def index(pagina: ft.Page):
    pagina.title = api.obtener_nombre() or "Cargando..."
    pagina.theme_mode = ft.ThemeMode.DARK
    
    def enrutador(e):
        pagina.views.clear()

        if pagina.route == "/": pagina.views.append(Bienvenida(pagina))
        elif pagina.route == "/lista": pagina.views.append(Lista(pagina, api))

        pagina.update()

    def pinchar_vista(e):
        if len(pagina.views) > 1:
            pagina.views.pop()
            pagina.go(pagina.views[-1].route)

    pagina.on_route_change = enrutador
    pagina.on_view_pop = pinchar_vista
    enrutador(None)

def main(): ft.app(target=index)

if __name__ == "__main__": main()