import tkinter as tk
import os
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import ttk
import threading
import requests
import zipfile
import mysql.connector
import shutil
from tqdm import tqdm
import mysql.connector
import webbrowser

def DescargarWordpress(ruta):
    titulo["text"] = "Descargando Wordpress"
    url = 'https://wordpress.org/latest.zip'  # URL del archivo de WordPress para descargar
    destino = f'{ruta}/wordpress_latest.zip'

    barra_progreso = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
    barra_progreso.pack(padx=20, pady=20)

    response = requests.get(url, stream=True)
    content_length = int(response.headers.get("content-length"))

    chunk_size = 1024
    total = 0

    with open(destino, "wb") as f:
        for data in response.iter_content(chunk_size=chunk_size):
            total += len(data)
            f.write(data)
            porcentaje = int(total * 100 / content_length)  # Calcular el progreso actual
            barra_progreso["value"] = porcentaje  # Actualizar la barra de progreso
            app.update_idletasks()


    titulo["text"] = "Descarga completada"
    barra_progreso["value"] = 100
    barra_progreso.destroy()
    Descomprimir_Wordpress(ruta, destino)

def Descomprimir_Wordpress(ruta, destino):
    titulo["text"] = "Descomprimiendo Wordpress"

    ruta_zip = destino
    ruta_destino = ruta

    barra_progreso = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
    barra_progreso.pack(padx=20, pady=20)
    

    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        total_files = len(zip_ref.infolist())
        extracted_files = 0

        for file_info in zip_ref.infolist():
            extracted_files += 1
            extract_path = os.path.join(ruta_destino, file_info.filename)
            zip_ref.extract(file_info.filename, ruta_destino)
            porcentaje = int(extracted_files * 100 / total_files)
            barra_progreso["value"] = porcentaje
            app.update_idletasks()

    titulo["text"] = "Extracción completada"
    barra_progreso["value"] = 100
    barra_progreso.destroy()
    Base_Datos(ruta)

def Base_Datos(ruta):
    def valorar(ruta):
        if not entrada_baseDatos.get() and not entrada_carpeta.get() and not entrada_contraseña.get() and not entrada_usuario.get():
            titulo["text"] = "Todas las entradas están vacias"
        elif not entrada_baseDatos.get():
            titulo["text"] = "La entrada de base de datos está vacía."
        elif not entrada_carpeta.get():
            titulo["text"] = "La entrada de carpeta está vacía."
        elif not entrada_contraseña.get():
            titulo["text"] ="La entrada de contraseña está vacía."
        elif not entrada_usuario.get():
            titulo["text"] = "La entrada de usuario está vacía."
        else:
            EjecutarMySQL(ruta)

    def EjecutarMySQL(ruta):
        titulo["text"] = "CREANDO BASE DE DATOS"

        user = entrada_usuario.get()
        password = entrada_contraseña.get()
        host = 'localhost'
        carpeta = entrada_carpeta.get()
        nombre_BD = entrada_baseDatos.get()

        text_BaseDatos.destroy()
        text_carpeta.destroy()
        text_contraseña.destroy()
        text_usuario.destroy()
        entrada_baseDatos.destroy()
        entrada_carpeta.destroy()
        entrada_contraseña.destroy()
        entrada_usuario.destroy()
        boton_enviarBD.destroy()

        ruta_original = os.path.join(ruta, 'wordpress')
        nuevo_nombre = os.path.join(ruta, carpeta)
        os.rename(ruta_original, nuevo_nombre)

        conexion = mysql.connector.connect(
        host='localhost',
        user=user,
        password= password
        )

        if conexion:
            titulo["text"] = "Se ha conectado a la base de datos con éxito"
            cursor = conexion.cursor()

            cursor.execute(f"CREATE DATABASE {nombre_BD}")

            cursor.close()
            conexion.close()
        
            with open(f'{ruta}\{carpeta}\wp-config-sample.php', 'r') as archivo_origen:
                contenido = archivo_origen.read()
                contenido_modificado = contenido.replace('database_name_here', nombre_BD)
                contenido_modificado = contenido_modificado.replace('username_here', user)
                contenido_modificado = contenido_modificado.replace('password_here', password)
                contenido_modificado = contenido_modificado.replace('wp_', 'hkp_')

            with open(f'{ruta}\{carpeta}\wp-config.php', 'w') as archivo_destino:
                archivo_destino.write(contenido_modificado)
            
            titulo["text"] = "LA INSTALACIÓN DE WORDPRESS HA SIDO UN ÉXITO, ESPERO QUE DISFRUTE DE SU SITIO WEB"
            webbrowser.open(f"localhost/{carpeta}")
            messagebox.showinfo("INSTALACIÓN COMPLETADA", "Ya está todo listo. Gracias por instalar Wordpress")
            app.destroy()
        else:
            titulo["text"] = "Alguno de los datos introducidos no era correcto"



    titulo["text"] = "Introduce tus datos de la BD"
    text_usuario = tk.Label(app, text="Introduce tu usuario: ", font=("Helvetica", 16))
    entrada_usuario = tk.Entry(app, font=("Helvetica", 16))
    text_contraseña = tk.Label(app, text="Introduce tu contraseña: ", font=("Helvetica", 16))
    entrada_contraseña = tk.Entry(app, font=("Helvetica", 16))
    text_BaseDatos = tk.Label(app, text="Introduce aquí nombre de la BD ", font=("Helvetica", 16))
    entrada_baseDatos = tk.Entry(app, font=("Helvetica", 16))
    text_carpeta = tk.Label(app, text="Introduce el nombre de la carpeta de Wordpress: ", font=("Helvetica", 16))
    entrada_carpeta = tk.Entry(app, font=("Helvetica", 16))
    boton_enviarBD = tk.Button(app, text="Enviar", font=("Helvetica", 16), command=lambda: valorar(ruta))
    boton_enviarBD.pack()
    text_usuario.pack()
    entrada_usuario.pack()
    text_contraseña.pack()
    entrada_contraseña.pack()
    text_BaseDatos.pack()
    entrada_baseDatos.pack()
    text_carpeta.pack()
    entrada_carpeta.pack()
    text_usuario.place(x=580, y=120)
    entrada_usuario.place(x=800, y=120)
    text_contraseña.place(x=550, y=160)
    entrada_contraseña.place(x=800, y=160)
    text_BaseDatos.place(x=480, y=200)
    entrada_baseDatos.place(x=800, y=200)
    text_carpeta.place(x=300, y=240)
    entrada_carpeta.place(x=800, y=240)
    boton_enviarBD.place(x=700, y=300)




def Instalar_Wordpress():

    def Si():
        
        def EnviarRuta():


            ruta = entrada_datos.get()
            
            if not(os.path.exists(ruta) and os.path.isdir(ruta) and os.path.basename(ruta) == 'htdocs'):
                
                titulo["text"] = "La ruta no es correcta, por favor, introduce una correcta"
            else:
                entrada_datos.destroy()
                mensaje_ad.destroy()
                boton_enviar.destroy()
                DescargarWordpress(ruta)
                


        titulo["text"] = "Introduce la dirección htdocs de tu servidor XAMPP"
        boton_si.destroy()
        boton_no.destroy()
        entrada_datos = tk.Entry(app, font=("Helvetica", 16))
        entrada_datos.pack(padx=20, pady=20)
        mensaje_ad = tk.Label(app, text="Introduce aquí la ruta -->", font=("Helvetica", 16))
        mensaje_ad.pack()
        mensaje_ad.place(x=500, y=120)
        entrada_datos.place(x=800, y=120)
        boton_enviar = tk.Button(app, text="Enviar Ruta", command=EnviarRuta, font=("Helvetica", 16))
        boton_enviar.pack(padx=20, pady=20)
        boton_enviar.place(x=700, y=170)
    
    def No():
        messagebox.showinfo("¡¡AVISO!!", "Necesitas tener XAMPP instalado para proceder con la instalación")
        app.destroy()

    # Aquí podrías poner la lógica para instalar WordPress
    print("Instalando WordPress...")
    boton_info.destroy()
    boton_instalar.destroy()
    titulo["text"] = "¿TIENES INSTALADO UN SERVIDOR XAMPP EN TU EQUIPO?"
    boton_si = tk.Button(app, text="SI", command=Si, font=("Helvetica", 18))
    boton_si.pack(pady=20)
    boton_no = tk.Button(app, text="NO", command=No, font=("Helvetica", 18))
    boton_no.pack(pady=20)
    boton_si.place(x=700, y=120)
    boton_no.place(x=800, y=120)


def Mas_Informacion():
    # Aquí podrías mostrar más información sobre WordPress
    print("Mostrando más información...")


app = tk.Tk()
app.title("INSTALADOR DE WORDPRESS ---> by HackPress <----")

# Configura el tamaño de la ventana
app.geometry("1920x1080")

# Cargar la imagen de fondo
fondo_pantalla = PhotoImage(file="background.png")  # Cambia la ruta a la ubicación de tu imagen

# Crear etiqueta para el fondo de pantalla
fondo_label = tk.Label(app, image=fondo_pantalla)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear título
titulo = tk.Label(app, text="BIENVENIDO AL INSTALADOR DE WORDPRESS", font=("Helvetica", 24, "bold"), bg="white")
titulo.pack(pady=30)

# Crear botones
boton_instalar = tk.Button(app, text="Instalar Wordpress", command=Instalar_Wordpress, font=("Helvetica", 18))
boton_instalar.pack(pady=20)
boton_instalar.place(x=1300, y=750)

boton_info = tk.Button(app, text="Más Info", command=Mas_Informacion, font=("Helvetica", 18))
boton_info.pack(pady=20)
boton_info.place(x=1160, y=750)

# Crear etiqueta para la versión
texto_version = tk.Label(app, text="Ver 1.1", font=("Helvetica", 16), bg="white")
texto_version.place(x=10, y=800, anchor="sw")

app.mainloop()