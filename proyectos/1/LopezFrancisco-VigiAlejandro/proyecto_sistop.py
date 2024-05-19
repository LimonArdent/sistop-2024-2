"""
Sistema de Archivos para la Facultad de Ingeniería, FiUnamFS
Este programa implementa un sistema de archivos FiUnamFS que permite realizar operaciones como listar, copiar y eliminar archivos. 
El programa utiliza concurrencia con semáforos para garantizar la integridad de los datos en el sistema de archivos.
Autores:
- Francisco Daniel López Campillo
- Marco Alejandro Vigi Garduño
Fecha de creación: 19 de mayo de 2024
Última modificación: 19 de mayo de 2024
Nota: Este programa es parte de un proyecto académico para las últimas dos unidades del curso.
"""

import os               #Importa el módulo 'os' que proporciona funciones para interactuar con el sistema operativo
import struct           #Importa el módulo 'struct' que permite interpretar cadenas de bytes como estructuras binarias
import threading        #Importa el módulo 'threading' que proporciona funcionalidad de subprocesos para realizar múltiples tareas de forma simultánea
from os import system   # Importa solo la función 'system' del módulo 'os'

# Variables globales
sector = 512                            #La superficie del disco se divide en sectores de 512 bytes.
cluster = sector * 4                    #Cada cluster mide cuatro sectores.
direccionSistema = "fiunamfs.img"       #Direccion de el archivo fiunamfs.img (puede ser en ruta absoluta o relativa)             

# Función para leer un entero desde el archivo en una posición específica
def leerEntero(posicion, numero):
    with open(direccionSistema, "rb") as archivo:   #Abre el archivo en modo binario de solo lectura
        archivo.seek(posicion)                      #Mueve el puntero del archivo a la posición especificada
        dato = archivo.read(numero)                 #Lee el número de bytes especificado desde la posición actual
        num = struct.unpack("<I", dato)[0]          #Desempaqueta los bytes leídos en un entero (asumiendo formato little-endian)
        return num                                  #Devuelve el entero leído

# Función para leer una cadena desde el archivo en una posición específica
def leerCadena(posicion, numero):
    with open(direccionSistema, "rb") as archivo:   #Abre el archivo en modo binario de solo lectura
        archivo.seek(posicion)                      #Mueve el puntero del archivo a la posición especificada
        cadena = archivo.read(numero)               #Lee el número de bytes especificado desde la posición actual
        string = cadena.decode("ascii").strip()     #Decodifica los bytes leídos en una cadena ASCII y elimina espacios en blanco alrededor
        return string                               #Devuelve la cadena leída

# Función que recopila la información del server ubicada en el primer cluster
def validarSistemaArchivos():
    os.system("cls")                                #Limpia la pantalla de la consola (solo en sistemas Windows)
    nombreSistema = leerCadena(0, 9)                #Lee la cadena de nombre de sistema desde la posición 0 con longitud 9 bytes
    version = leerCadena(10, 5)                     #Lee la cadena de versión desde la posición 10 con longitud 5 bytes
    etiqueta = leerCadena(20, 16)                   #Lee la cadena de etiqueta del volumen desde la posición 20 con longitud 16 bytes
    tamaio_cluster = leerEntero(40, 4)              #Lee un entero que representa el tamaño del cluster desde la posición 40 con longitud 4 bytes
    cantidadclusters = leerEntero(44, 4)            #Lee un entero que representa la cantidad de clusters que mide el directorio desde la posición 44 con longitud 4 bytes
    ccl = leerEntero(48, 4)                         #Lee un entero que representa la cantidad de clusters que mide toda la unidad desde la posición 48 con longitud 4 bytes
    
    #Imprime información recopilada del sistema de archivos en formato listado
    print(f"\nEl sistema se llama: {nombreSistema}")
    print(f"La version es: {version}")
    print(f"Etiqueta del volumen: {etiqueta}")
    print(f"Tamaño del Cluster: {tamaio_cluster} bytes")
    print(f"Numero de clusters que mide el directorio: {cantidadclusters}")
    print(f"Numero de clusters que mide toda la unidad: {ccl}")

    #Espera a que el usuario presione enter para que sea mas intuitivo el proyecto
    input ("\nPresione 'enter' para continuar...")


# Función que lista el contenido del directorio, ignorando las entradas vacías
def listado():
    os.system("cls")                                                #Limpia la pantalla de la consola (solo en sistemas Windows)
    print("Listado de archivos en el FiUNAMFS:")                    #Impresion de pantalla para una mejor visualizacion

    # Itera sobre las entradas del directorio en bloques de 64 bytes
    for i in range(0, cluster * 4, 64):
        tipo_archivo = leerCadena(cluster + i, 1)                   #Lee el tipo de archivo desde el cluster actual más el desplazamiento 'i' con longitud de 1 byte
        if tipo_archivo != "/":                                     #Verifica si el tipo de archivo es diferente de '/'
            nombre = leerCadena(cluster + i + 1, 15)                #Lee el nombre del archivo desde el cluster actual más el desplazamiento 'i' más 1 con longitud 15 bytes
            tamanio = leerEntero(cluster + i + 16, 4)               #Lee el tamaño del archivo desde el cluster actual más el desplazamiento 'i' más 16 con longitud 4 bytes
            cluster_inicial = leerEntero(cluster + i + 20, 4)       #Lee el número de cluster inicial del archivo desde el cluster actual más el desplazamiento 'i' más 20 con longitud 4 bytes
            fecha_creacion = leerCadena(cluster + i + 24, 14)       #Lee la fecha de creación del archivo desde el cluster actual más el desplazamiento 'i' más 24 con longitud 14 bytes
            fecha_modificacion = leerCadena(cluster + i + 38, 14)   #Lee la fecha de modificación del archivo desde el cluster actual más el desplazamiento 'i' más 38 con longitud 14 bytes
            
            # Muestra la información del archivo
            print(f"Archivo: {nombre}, Tamaño: {tamanio}, Cluster Inicial: {cluster_inicial}, Creado: {fecha_creacion}, Modificado: {fecha_modificacion}")
    
    # Espera que el usuario presione Enter para continuar
    input("\nIngrese 'enter' para continuar...")


# Función para mostrar el menú
def menu():
    while True:
        system("cls")                                          #Limpia la pantalla de la consola (solo en sistemas Windows)
        print("\nMenu:")
        print("1. Validar server")
        print("2. Listar archivos")
        print("3. Copiar archivo desde FiUnamFS")
        print("4. Eliminar archivo de FiUnamFS")
        print("5. Mover archivo a FiUnamFS")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")              #Solicita al usuario que seleccione una opción del menú
        
        if opcion == '1':
            validarSistemaArchivos()                           #Llama a la función para validar el sistema de archivos
        elif opcion == '2':
            listado()                                          #Llama a la función para listar los archivos
        elif opcion == '3':
            a = input(print("Ingresa el nombre a copiar desde FiUunamFS"))   #Solicita al usuario el nombre del archivo a copiar desde FiUnamFS
        elif opcion == '4':
            b = input(print("Ingresa el nombre a eliminar de FiUnamFS"))    #Solicita al usuario el nombre del archivo a eliminar de FiUnamFS
        elif opcion == '5':
            c = input(print("Ingresa el nombre a mover a FiUnamFS"))        #Solicita al usuario el nombre del archivo a mover a FiUnamFS
        elif opcion == '6':
            break                                                           #Sale del bucle while para finalizar el programa
        else:
            print("\nOpción no válida")                         # Mensaje de error para opciones no válidas
            input("\nIngrese 'enter' para continuar...")        # Espera que el usuario presione Enter para continuar

# Ejecución del programa
if __name__ == "__main__":
    menu()                                                     # Llama a la función menu para comenzar la ejecución del programa