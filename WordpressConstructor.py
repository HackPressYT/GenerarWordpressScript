import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import urllib.request
import requests
import zipfile
import shutil
import threading

# VARIABLES GLOBALES
path_entry = None

# FUNCIONES DE LA INTERFAZ GRÁFICA

def on_button_click():
    # Eliminar contenido anterior
    for widget in root.winfo_children():
        widget.destroy()

    # Mostrar la imagen de fondo
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Mostrar el nuevo contenido en la misma ventana
    title_label = tk.Label(root, text="¿Tienes XAMPP instalado?", font=("Helvetica", 20))
    title_label.pack(pady=20)

    # Opciones "Sí" y "No" en el centro de la ventana (orientación vertical)
    option_frame = tk.Frame(root)
    option_frame.pack()

    option_yes = tk.Button(option_frame, text="Sí", command=on_yes_click, font=("Helvetica", 16))
    option_yes.pack(side=tk.LEFT, padx=10)

    option_no = tk.Button(option_frame, text="No", command=on_no_click, font=("Helvetica", 16))
    option_no.pack(side=tk.LEFT, padx=10)

def on_yes_click():
    global path_entry  # Accede a la variable global

    # Eliminar contenido anterior
    for widget in root.winfo_children():
        widget.destroy()

    # Mostrar la imagen de fondo
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Título principal centrado
    main_title_label = tk.Label(root, text="Indica la ruta donde se encuentra la carpeta htdocs", font=("Helvetica", 20))
    main_title_label.pack(pady=20)

    # Texto "Ruta:" y campo de entrada
    path_label = tk.Label(root, text="Ruta: ", font=("Helvetica", 16))
    path_label.pack()

    path_entry = tk.Entry(root, font=("Helvetica", 16))
    path_entry.pack()

    # Botón "Enviar" centrado
    send_button = tk.Button(root, text="Enviar", command=on_send_click, font=("Helvetica", 16))
    send_button.pack(pady=20)

def on_send_click():
    global path_entry  # Accede a la variable global

    ruta = path_entry.get()  # Obtén el valor del campo de entrada

    if os.path.isdir(ruta) and 'htdocs' in ruta:
        # Eliminar contenido anterior
        for widget in root.winfo_children():
            widget.destroy()

        # Mostrar la imagen de fondo
        background_label = tk.Label(root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Mostrar texto "Iniciando Descarga de Wordpress"
        installing_label = tk.Label(root, text="Iniciando Descarga de Wordpress", font=("Helvetica", 20))
        installing_label.pack(pady=50)

        # Barra de progreso de descarga
        download_progress_label = tk.Label(root, text="", relief=tk.SUNKEN, anchor=tk.W, width=1, font=("Helvetica", 16), bg="blue")
        download_progress_label.place(x=0, y=550, relwidth=0, relheight=0.1)

        # Porcentaje de descarga
        download_percentage_label = tk.Label(root, text="0%", font=("Helvetica", 16))
        download_percentage_label.place(x=400, y=570)

        # Función para descargar Wordpress y actualizar la barra de progreso de descarga
        def download_wordpress():
            url = "https://es.wordpress.org/latest-es_ES.zip"
            archivo = "wordpress.zip"

            response = requests.get(url, stream=True)
            total_size = int(response.headers.get("content-length", 0))
            block_size = 1024
            progress = 0

            with open(archivo, "wb") as f:
                for data in response.iter_content(block_size):
                    progress += len(data)
                    f.write(data)
                    percentage = int(progress * 100 / total_size)
                    download_progress_label.place(relwidth=percentage / 100)
                    download_percentage_label.config(text=f"{percentage}%")
                    root.update()

            installing_label.config(text="¡Wordpress Descargado!")
            # Llamar a extract_wordpress con installing_label como argumento
            extract_wordpress(archivo, installing_label)

        # Iniciar la descarga de Wordpress utilizando un hilo
        download_thread = threading.Thread(target=download_wordpress)
        download_thread.start()

    else:
        # Mostrar mensaje de error
        error_label = tk.Label(root, text="No has introducido la ruta correcta, vuelve a intentarlo",
                               font=("Helvetica", 16, "bold"), fg="red", wraplength=400)
        error_label.pack(pady=20)

        # Limpiar el campo de entrada
        path_entry.delete(0, tk.END)

def extract_wordpress(archivo, installing_label):
    for widget in root.winfo_children():
        widget.destroy()
    # Mostrar texto "Descomprimiendo archivo"
    extracting_label = tk.Label(root, text="Descomprimiendo archivo", font=("Helvetica", 20))
    extracting_label.pack(pady=50)

    # Barra de progreso de extracción
    extract_progress_label = tk.Label(root, text="", relief=tk.SUNKEN, anchor=tk.W, width=1, font=("Helvetica", 16), bg="green")
    extract_progress_label.place(x=0, y=550, relwidth=0, relheight=0.1)

    # Porcentaje de extracción
    extract_percentage_label = tk.Label(root, text="0%", font=("Helvetica", 16))
    extract_percentage_label.place(x=400, y=570)

    # Función para descomprimir Wordpress y actualizar la barra de progreso de extracción
    def extract_zip():
        with zipfile.ZipFile(archivo, 'r') as archivo_zip:
            total_files = len(archivo_zip.infolist())
            extracted_files = 0

            for file in archivo_zip.infolist():
                extracted_files += 1
                percentage = int(extracted_files * 100 / total_files)
                extract_progress_label.place(relwidth=percentage / 100)
                extract_percentage_label.config(text=f"{percentage}%")
                root.update()

                archivo_zip.extract(file)
        
        # Eliminar el archivo ZIP descargado
        os.remove(archivo)

        # Reiniciar el proceso
        for widget in root.winfo_children():
            widget.destroy()
        installing_label.config(text="¡Wordpress instalado!")
        root.after(2000, move_folder_and_ask_mysql_data)

    # Iniciar la extracción del archivo ZIP utilizando un hilo
    extract_thread = threading.Thread(target=extract_zip)
    extract_thread.start()

def on_no_click():
    messagebox.showinfo("Respuesta", "Primero instala XAMPP y luego vuelve a ejecutar este asistente.")

def move_folder_and_ask_mysql_data():
    # Mostrar mensaje de inicio de proceso de instalación
    for widget in root.winfo_children():
        widget.destroy()
    install_process_label = tk.Label(root, text="Comenzando proceso de instalación", font=("Helvetica", 20))
    install_process_label.pack(pady=50)

    # Barra de progreso de instalación
    install_progress_label = tk.Label(root, text="", relief=tk.SUNKEN, anchor=tk.W, width=1, font=("Helvetica", 16), bg="yellow")
    install_progress_label.place(x=0, y=550, relwidth=0, relheight=0.1)

    # Porcentaje de instalación
    install_percentage_label = tk.Label(root, text="0%", font=("Helvetica", 16))
    install_percentage_label.place(x=400, y=570)

    # ... (código para pedir datos de MySQL)

# Crear ventana
root = tk.Tk()
root.title("Asistente de Instalación de WordPress")
root.geometry("1920x1200")  # Tamaño de la ventana

# Cambiar el icono de la ventana
icon_image = Image.open("icon.ico")  # Reemplaza "icon.ico" con el nombre de tu archivo de icono
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_photo)

# Cargar imagen de fondo
background_image = Image.open("background.png")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Texto centrado
welcome_label = tk.Label(root, text="Bienvenido al Asistente de Instalación de WordPress", font=("Helvetica", 24))
welcome_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Botón "Iniciar Instalación"
button = tk.Button(root, text="Iniciar Instalación", image=icon_photo, compound=tk.LEFT, command=on_button_click, font=("Helvetica", 16))
button.pack()
button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

root.mainloop()