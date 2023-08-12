#LIBRERÍAS

import os
import urllib.request
import time
import rarfile
import zipfile
import mysql.connector
import shutil
import requests
from tqdm import tqdm
import mysql.connector


#FUNCIONES

# ------------------> Limpiar Consola <---------------------#

def limpiar_consola():
    # Comando para limpiar la consola según el sistema operativo
    comando_limpiar = "cls" if os.name == "nt" else "clear"

    # Ejecutar el comando para limpiar la consola
    os.system(comando_limpiar)

# -----------------> Descargar Wordpress <-------------------#

def Descarga_Wordpress(ruta):
    
    url = 'https://wordpress.org/latest.zip'
    destino = f'{ruta}/wordpress_latest.zip'

    respuesta = requests.get(url, stream=True) #Si se puede acceder al enlace

    tamaño_total = int(respuesta.headers.get('content-length', 0)) #Tamaño Total del Wordpress

    #La barra de progreso
    barra_progreso = tqdm(total=tamaño_total, unit='B', unit_scale=True, desc=destino, ncols=100)

    with open(destino, 'wb') as archivo:
        for datos in respuesta.iter_content(chunk_size=1024):
            archivo.write(datos)
            barra_progreso.update(len(datos))
            time.sleep(0.01)
        barra_progreso.close()
    
    if Descarga_Wordpress:
        limpiar_consola()
        print("La descarga de Wordpress fue un éxito")
        print("Descomprimiendo los archivos: ")
        descomprimir_archivo(destino, ruta)
        
    else:
        limpiar_consola()
        print("Parece que algo ha fallado, vuelvelo a intentar más tarde")

# ----------------> Descomprimir Archivo ZIP <------------------#

def descomprimir_archivo(ruta_archivo_zip, htdocsDIR):
    
    archivo_zip = ruta_archivo_zip
    directorio_destino = htdocsDIR

    # Obtener el tamaño total del archivo ZIP
    tamaño_total = os.path.getsize(archivo_zip)

    # Inicializar el objeto tqdm para mostrar la barra de progreso
    barra_progreso = tqdm(total=tamaño_total, unit='B', unit_scale=True, desc="Extrayendo", ncols=100)

    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        for archivo in zip_ref.namelist():
            zip_ref.extract(archivo, directorio_destino)
            barra_progreso.update(len(archivo.encode('utf-8')))  # Simulación de progreso
            time.sleep(0.01)  # Simulación de extracción más lenta

    barra_progreso.close()
    nombre = input("Indica el nombre que le quieres poner a tu carpeta de wordpress --> SI QUIERES QUE SEA EL NOMBRE PREDETERMINADO, DEJA ESTE CAMPO VACIO: ")
    if nombre:
        ruta_original = os.path.join(ruta, 'wordpress')
        nuevo_nombre = os.path.join(ruta, nombre)
        os.rename(ruta_original, nuevo_nombre)
    else:
        nombre = "wordpress"
    base_datos(htdocsDIR, nombre)

# -----------------> Entrar a BD, crear y aplicar a WP config <------------------------------------

def base_datos(ruta, nombre):
    print("Ahora necesitaré que me proporciones los datos de MySQL")
    user = input("Introduce tu usuario: ")
    password = input("Introduce tu contraseña: ")
    host = 'localhost'
    conexion = mysql.connector.connect(
        host='localhost',
        user=user,
        password= password
    )

    if conexion:
        print("Se ha conectado a la base de datos con éxito")
        cursor = conexion.cursor()

        nombre_BD = input("Introduce un nombre para la base de datos: ")
        cursor.execute(f"CREATE DATABASE {nombre_BD}")

        cursor.close()
        conexion.close()
        
        with open(f'{ruta}\{nombre}\wp-config-sample.php', 'r') as archivo_origen:
            contenido = archivo_origen.read()
            contenido_modificado = contenido.replace('database_name_here', nombre_BD)
            contenido_modificado = contenido_modificado.replace('username_here', user)
            contenido_modificado = contenido_modificado.replace('password_here', password)
            contenido_modificado = contenido_modificado.replace('wp_', 'hkp_')

        with open(f'{ruta}\{nombre}\wp-config.php', 'w') as archivo_destino:
            archivo_destino.write(contenido_modificado)


    else:
        print("Error, alguno de los datos proporcionados no eran correctos")
        conexion.close()
        
    


#PROGRAMA
limpiar_consola()
print("Bienvenido al Sistema de Instalación de Wordpress")
print("¿Tienes un Servidor XAMPP instalado?. Escriba Si o No")

text = input().upper()

if text == "SI":
    limpiar_consola()
    ruta = input("Ahora indicame la carpeta htdocs de tu servidor XAMPP: ")
    intentos = 3
    while not (os.path.exists(ruta) and os.path.isdir(ruta) and os.path.basename(ruta) == 'htdocs'):
        limpiar_consola()
        
        if not (os.path.exists(ruta) and os.path.isdir(ruta) and os.path.basename(ruta) == 'htdocs'):
            intentos -= 1
            if intentos == 0:
                print("Lo siento, ya no te quedan intentos")
                break
            print("La ruta que nos proporcionas no es correcta")
            ruta = input(f"Por favor, vuelve a escribir una ruta correcta. Te quedan {intentos} intentos: ")
    
    limpiar_consola()
    print("Perfecto, la ruta que nos proporcionas es la correcta")
    print("Descargando Wordpress: ")
    Descarga_Wordpress(ruta)
    

    
    

else:
    limpiar_consola()
    print("Deberías instalar el software XAMPP antes de proceder con esta instalación")


