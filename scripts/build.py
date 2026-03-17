#-------------------------------------------------------------------------------
# Nombre:      Guión de construcción
# Proposito:   Construir la aplicación web para despliegue.
#
# Autor:       Aref
#
# Creado:      19-3/3/1999+19+9-1
# Derechos
# de autor:    (k) Alta Lengua 2026
# Licencia:    <GPLv3>
#-------------------------------------------------------------------------------

import os
import subprocess

def construir():
    """ Funcion: Construir

    Funcion que construye la aplicación web para despliegue.
    Y ajusta el archivo 404.html para manejar rutas no
    encontradas.
    """

    # Construir la aplicación con Flet
    subprocess.run(
        [
            "flet",
            "publish",
            "src/main.py",
            "--base-url",
            "/ekmajstro-malabunda-frontend/"
        ],
        check=True
    )

    # Duplicar el archivo index.html a 404.html para manejar rutas no encontradas
    ruta_dist = os.path.join("src", "dist")
    ruta_index = os.path.join(ruta_dist, "index.html")
    ruta_404 = os.path.join(ruta_dist, "404.html")

    if os.path.exists(ruta_index):
        with open(ruta_index, "r", encoding="utf-8") as arch_index:
            contenido = arch_index.read()
        with open(ruta_404, "w", encoding="utf-8") as arch_404:
            arch_404.write(contenido)

        print("Archivo 404.html creado exitosamente.")
        
    else:
        print("Error: index.html no encontrado en la carpeta dist.")