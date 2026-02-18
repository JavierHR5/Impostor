import streamlit as st
import pandas as pd
import random

# Inicializar estado
if "step" not in st.session_state:
    st.session_state.step = "jugadores"
if "jugadores" not in st.session_state:
    st.session_state.jugadores = []
if "roles" not in st.session_state:
    st.session_state.roles = {}
if "palabra" not in st.session_state:
    st.session_state.palabra = None
if "turno" not in st.session_state:
    st.session_state.turno = 0
if "fin" not in st.session_state:
    st.session_state.fin = False

st.title("Juego del Impostor")

if st.session_state.step == "jugadores":
    st.header("Añadir jugadores")

    nuevo_jugador = st.text_input("Nombre del jugador")
    if st.button("Añadir jugador"):
        if nuevo_jugador and nuevo_jugador not in st.session_state.jugadores:
            st.session_state.jugadores.append(nuevo_jugador)
            st.rerun()

    st.write("Jugadores actuales:", st.session_state.jugadores)

    if len(st.session_state.jugadores) >= 3:
        if st.button("Continuar a categorías"):
            st.session_state.jugadores_original = st.session_state.jugadores.copy()
            st.session_state.step = "categorias"
            st.rerun()


elif st.session_state.step == "categorias":
    st.header("Elegir categorías")

    df = pd.read_excel("Categorías.xlsx")
    categorias = list(df.columns)

    seleccion = st.multiselect("Selecciona las categorías que quieres incluir", categorias)

    if st.button("Elegir palabra al azar"):
        if seleccion:
            categoria_partida = random.choice(seleccion)
            st.session_state.categoria_partida = categoria_partida
            palabras = df[categoria_partida].dropna().tolist()
            st.session_state.palabra = random.choice(palabras)
            st.session_state.step = "roles"
            st.rerun()
        else:
            st.warning("Selecciona al menos una categoría.")

elif st.session_state.step == "roles":
    st.header("Asignar impostores")

    num_jugadores = len(st.session_state.jugadores)
    num_impostores = st.number_input(
        "Número de impostores",
        min_value=1,
        max_value=num_jugadores - 1,
        value=1,
        step=1
    )

    if st.button("Asignar roles"):
        impostores = random.sample(st.session_state.jugadores, num_impostores)
        st.session_state.roles = {
            j: ("IMPOSTOR" if j in impostores else "JUGADOR")
            for j in st.session_state.jugadores
        }
        st.session_state.impostores = impostores
        st.session_state.turno = 0
        st.session_state.step = "mostrar_palabra"
        st.rerun()

elif st.session_state.step == "mostrar_palabra":
    st.header("Turno de cada jugador")

    jugadores = st.session_state.jugadores
    roles = st.session_state.roles
    palabra = st.session_state.palabra
    turno = st.session_state.turno

    if turno >= len(jugadores):
        st.success("Todos han visto su rol.")
        if st.button("Ir a votación"):
            st.session_state.step = "votacion"
            st.rerun()
    else:
        jugador_actual = jugadores[turno]
        st.subheader(f"Turno de: {jugador_actual}")

        st.info("Entrega el móvil SOLO a este jugador.")

        if st.button("Mostrar palabra / rol"):
            if roles[jugador_actual] == "IMPOSTOR":
                st.error("Eres IMPOSTOR. No tienes palabra.")
                st.error(st.session_state.categoria_partida)
            else:
                st.success(f"La palabra es: {palabra}")

        if st.button("Siguiente jugador"):
            st.session_state.turno += 1
            st.rerun()

elif st.session_state.step == "votacion":
    st.header("Votación")

    jugadores = st.session_state.jugadores
    roles = st.session_state.roles

    st.write("Votad quién creéis que es el impostor.")

    votos = {}
    for j in jugadores:
        votos[j] = st.number_input(
            f"Votos para {j}",
            min_value=0,
            max_value=len(jugadores),
            step=1,
            key=f"voto_{j}"
        )

    if st.button("Eliminar jugador"):
        eliminado = max(votos, key=votos.get)
        st.write(f"Eliminado: {eliminado}")
        st.write(f"Era: {roles[eliminado]}")

        # Eliminar del juego
        jugadores.remove(eliminado)
        roles.pop(eliminado)

        # Comprobar victoria
        impostores_vivos = sum(1 for r in roles.values() if r == "IMPOSTOR")

        if impostores_vivos == 0:
            st.session_state.resultado = "¡Los jugadores ganan!"
            st.session_state.resultado_tipo = "success"
            st.session_state.step = "fin_partida"
            st.rerun()

        elif impostores_vivos >= len(jugadores) - impostores_vivos:
            st.session_state.resultado = "¡Los impostores ganan!"
            st.session_state.resultado_tipo = "error"
            st.session_state.step = "fin_partida"
            st.rerun()

        else:
            st.info("Siguiente ronda de votación")
            st.rerun()
            
elif st.session_state.step == "fin_partida":
    if st.session_state.resultado_tipo == "success":
        st.success(st.session_state.resultado)
    else:
        st.error(st.session_state.resultado)
    st.subheader("Impostores de la partida:")
    for imp in st.session_state.impostores:
        st.write(f"• {imp}")


    if st.button("Sí, misma lista de jugadores"):
        st.session_state.jugadores = st.session_state.jugadores_original.copy()
        st.session_state.roles = {}
        st.session_state.palabra = None
        st.session_state.turno = 0
        st.session_state.step = "categorias"
        st.rerun()


    if st.button("Sí, pero cambiar jugadores"):
        # Reiniciar todo
        st.session_state.jugadores = []
        st.session_state.roles = {}
        st.session_state.palabra = None
        st.session_state.turno = 0
        st.session_state.step = "jugadores"
        st.rerun()

    if st.button("No, salir"):
        st.write("Gracias por jugar")

 