import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import tabulate
import random
import os

# Definir los jugadores que van a participar 
def Jugadores():
    x='N'
    Nombres=[]
    while (x!='Y'):
        nombre=input("Introduce tu nombre: ")
        Nombres.append(nombre)
        x=input("Quieres comenzar la partida? Responde Y/N")
        
    return tuple(Nombres)


# Definir las categorías que quiero que entren 
def Palabra():
    # Cargar categorías desde la primera fila del Excel
    Categorias_df=openpyxl.load_workbook("Categorías.xlsx")
    dataframe=Categorias_df.active
    
    Categorias = [cell.value for cell in dataframe[1]] 
    print("Categorías disponibles:", Categorias)

    # El programa pregunta que categorías quieres incluir
    Categorias_seleccionadas=[]
    for categoria  in Categorias:
        x = input(f"¿Quieres añadir la categoría '{categoria}'? Y/N: ").upper()
        if x=='Y':
            Categorias_seleccionadas.append(categoria ) 
    print ("Categorías disponibles:",Categorias_seleccionadas)
    
    # Selecciona una categoría entre las seleccionadas de manera aleatoria
    Categoria_Partida=random.choice(Categorias_seleccionadas)
    print ("La categoría será:",Categoria_Partida)

    # Cargar todas las palabras de esa categoría 
    df = pd.read_excel("Categorías.xlsx") 
    Palabras = df[Categoria_Partida].dropna().tolist()

    # Selecciona una palabra de manera aleatoria
    Palabra_Juego=random.choice(Palabras)
    
    return Palabra_Juego

# Seleccionar los impostores
def Impostores(Jugadores):
    #El programa pide el número de impostores
    x=int(input("El número de impostores es: "))
    while x>len(Jugadores) or x<1:
        print("Número inválido. Debe ser entre 1 y", len(Jugadores)) 
        x = int(input("Introduce otro número: "))
    
    # Se asignan los roles a cada jugador
    Impostores_Asignados=random.sample(Jugadores,x)
    # Se crea un diccionario
    roles={}
    for jugador in Jugadores:
        if jugador in Impostores_Asignados:
            roles[jugador]="IMPOSTOR"
        else:
            roles[jugador]="Jugador"
    return roles

# Muestra el rol de impostor o la palabra de cada jugador
def Mostrar_rol(Dict,Palabra):
    
    for Nombre in Dict:
        # Limpiar pantalla antes de mostrar el turno 
        os.system("cls" if os.name == "nt" else "clear")

        print("Es el turno de", Nombre)

        Ready = input("Listo? Y/N ").upper()
        while Ready != 'Y':
            Ready = input("Avisa cuando estés listo (Y): ").upper()

        if Dict[Nombre]=="IMPOSTOR":
            print("La palabra es:", Dict[Nombre])
        else:
            print("La palabra es:", Palabra)
        input("\nPulsa ENTER para pasar al siguiente jugador...")

    # El return va fuera del for
    return

# Hay que hacer ronda de votaciones y comprobar si hay otro impostor entre los jugadores que quedan
def Votacion(Dict,Palabra):
    num_impostores = sum(1 for rol in Dict.values() if rol == "IMPOSTOR")

    while num_impostores>0 and num_impostores<len(Dict):
        Votos = {}
        print("Ronda de votos")
        for Nombre in Dict:
            Votos[Nombre] = int(input(f"Votos a {Nombre}? "))
            while Votos[Nombre]>len(Dict):
                print("Te has equivocado, los votos no pueden ser mayor que el número de jugadores")
                Votos[Nombre] = int(input(f"Votos a {Nombre}? "))
        # Jugador con más votos
        Eliminado = max(Votos, key=Votos.get)

        print(f"El jugador eliminado es: {Eliminado}")
        print(f"El jugador eliminado era {Dict[Eliminado]}")

        if Dict[Eliminado]=="IMPOSTOR":
            
            num_impostores-=1
            guess=input("Sabes cual es la palabra?")
            if guess==Palabra:
                print(f"Gana {Dict[Eliminado]}")
                break
        Dict.pop(Eliminado)
        print(f"Quedan {num_impostores} impostores")
        print(f"Quedan {len(Dict)} jugadores vivos\n")
    # Condición de victoria
    if num_impostores == 0:
        print("Los impostores han sido descubiertos. Ganan los jugadores normales.")
    else:
        print("Los impostores igualan o superan a los jugadores. Ganan los impostores.")
    return

        