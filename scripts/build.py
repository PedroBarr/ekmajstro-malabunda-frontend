import os
import subprocess

def build():

    # Construir la aplicación con Flet
    subprocess.run(["flet", "publish", "src/main.py", "--base-url", "/ekmajstro-malabunda-frontend/"], check=True)

    # Duplicar el archivo index.html a 404.html para manejar rutas no encontradas
    dist_path = os.path.join("src", "dist")
    index_path = os.path.join(dist_path, "index.html")
    not_found_path = os.path.join(dist_path, "404.html")
    
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as index_file:
            content = index_file.read()
        with open(not_found_path, "w", encoding="utf-8") as not_found_file:
            not_found_file.write(content)
        print("Archivo 404.html creado exitosamente.")
    else:
        print("Error: index.html no encontrado en la carpeta dist.")