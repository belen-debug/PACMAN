# MAIN
#Importamos al programa tanto la libreria de pyxel como las clases del juego
import time
import pyxel
from pacman1 import Pacman
from muros import Muros
from fantasma import Fantasma
import constants


def main():
    pyxel.init(256, 256)  # Inicializa la pantalla con dimensiones 256x256 píxeles
    laberinto = Muros(16)  # Crea el laberinto, representado por la clase Muros con tamalo de celda 16
    personaje = Pacman(16, 16, 1, laberinto)  # Crea al personaje Pacman, con coordenadas iniciales 16 y 16,referencia al laberinto

    """ En esta lista se recogen los 4 fantasmas, con sus posiciones iniciales, asociacion al laberinto y  tamaño de
    sprite (indice para imagen vertical)"""
    fantasmas = [
       Fantasma(110, 110, 2.5, laberinto, personaje),
       Fantasma(120, 120, 3, laberinto, personaje),
       Fantasma(130, 130, 2, laberinto, personaje),
       Fantasma(140, 140, 1.5, laberinto, personaje),
    ]
    vidas = 3


    fantasmas_muertos = []

    def reiniciar_posiciones():
        """Reinicia las posiciones de Pacman y los fantasmas"""
        personaje.x, personaje.y = 16, 16
        fantasmas[0].x, fantasmas[0].y = 110, 110
        fantasmas[1].x, fantasmas[1].y = 120, 120
        fantasmas[2].x, fantasmas[2].y = 130, 130
        fantasmas[3].x, fantasmas[3].y = 140, 140


    def detectar_colision():
        """Verifica si Pacman colisiona con algún fantasma"""
        for fantasma in fantasmas:
            if (
                abs(personaje.x - fantasma.x) < personaje.tamano
                and abs(personaje.y - fantasma.y) < personaje.tamano
            ):
                return fantasma
        return None

    """ Este es el modo en el que si pacman ha comido una pildora entonces, se activa este modo en 
    el que pacman puede a los fantasmas mientras estos escapan de él. Los fantasmas cambian de color
    y cuando se los come reinicia su posición a una (jaula) y vuelven a ser fantasmas normales.
    El modo dura 5s """


    def update():
        nonlocal vidas
        personaje.automovimiento() #Hace que pacman se mueva solo
        personaje.update()  # Actualiza a Pacman

        # Detecta si Pacman ha comido una nueva pildora
        if personaje.nueva_pildora:
            personaje.pildora_comida = True
            # Reinicia el temporizador de la pildora
            personaje.inicio_pildora = time.time()
            # Reactiva el modo escape de los fantasmas
            reactivar_fantasmas()
            # Reinicia el indicador
            personaje.nueva_pildora = False

        for fantasma in fantasmas:
            """ Si es verdad que el pacman ha comido una pildora y el fantasma no se ha muerto aún,
             entonces el fantasma escapa del personaje"""
            if personaje.pildora_comida and fantasma not in fantasmas_muertos:
                fantasma.escapar(personaje.x,personaje.y)
                fantasma.modo_escape = True

            else:
                fantasma.update()  # Movimiento normal

        if personaje.pildora_comida:

            if time.time() - personaje.inicio_pildora > constants.DURACION_PILDORA:
                personaje.pildora_comida = False
                fantasmas_muertos.clear()
                quitar_modo_escape()

        fantasma_colisionado = detectar_colision() # Para detectar con qué fantasma ha colisionado

        # Detectar colisión entre Pacman y fantasmas
        if fantasma_colisionado:

            """ Si pacman ha comido una pildora y sigue habiendo tiempo en el modo pildora
             reinicia la posición del fantasma con el que ha colisionado"""

            if personaje.pildora_comida and fantasma_colisionado not in fantasmas_muertos:
                fantasma_colisionado.x, fantasma_colisionado.y = 110, 110
                fantasmas_muertos.append(fantasma_colisionado)
                fantasma_colisionado.modo_escape = False

            else:
                vidas -= 1  # Reduce las vidas en 1
                quitar_modo_escape()
                fantasmas_muertos.clear()

                personaje.pildora_comida = False
                if vidas > 0:
                    reiniciar_posiciones()  # Reinicia las posiciones de los personajes
                else:
                    pyxel.quit()  # Cierra el juego si las vidas llegan a 0

    def quitar_modo_escape():
        for fantasma in fantasmas:
            fantasma.modo_escape = False

    def reactivar_fantasmas():
        """Reactivamos a los fantasmas muertos para que vuelvan al modo escapar."""
        fantasmas_muertos.clear()  # Limpiar la lista de fantasmas muertos
        # Pone a todos los fantasmas en modo escapar
        for fantasma in fantasmas:
            fantasma.modo_escape = True


    def draw():
        pyxel.cls(0)  # Limpia la pantalla antes de redibujar
        laberinto.draw()  # Dibuja el laberinto
        personaje.draw()  # Dibuja al personaje
        for fantasma in fantasmas:  # Dibuja cada fantasma
            fantasma.draw()

        pyxel.rect (20, 240, 64, 16, 10)
        pyxel.text(25, 244, f"Vidas: {vidas}",1)




    pyxel.run(update, draw)  # Corre el bucle principal

if __name__ == "__main__":
    main()
