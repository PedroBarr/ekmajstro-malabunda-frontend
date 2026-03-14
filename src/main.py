import flet as ft

def index(pagina: ft.Page):
    pagina.title = "Malabunda"
    pagina.theme_mode = ft.ThemeMode.DARK
    
    def enrutador(e):
        pagina.views.clear()

        if pagina.route == "/":
            pagina.views.append(
                ft.View(
                    route="/",
                    controls=[ft.Text(value="Home", size=35)]
                )
            )

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