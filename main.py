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
    tiempo_modo_pildora = 0 # Este es el tiempo restante en el modo pildora medido en FPS

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

    """ Este es el modo en el que si pacman ha comido una pildora entonces, se activa este modo en el que pacman puede
    a los fantasmas mientras estos escapan de él. Los fantasmas cambian de color y cuando se los come reinicia su posición a una (jaula) y vuelven a ser fantasmas normales.
    El modo dura 5s """


    def update():
        nonlocal vidas, tiempo_modo_pildora

        personaje.automovimiento() #Hace que pacman se mueva solo
        personaje.update()  # Actualiza a Pacman
        for fantasma in fantasmas:
            """ Si es verdad que el fantasma ha comido una pildora, entonces el fantasma escape del personaje"""
            if personaje.pildora_comida:
                fantasma.escapar(personaje.x,personaje.y)
            else:
                fantasma.update()  # Movimiento normal

        if personaje.pildora_comida:
            constants.inicio_pildora = time.time()
            if time.time() - constants.inicio_pildora > constants.duracion_pildora:
                personaje.pildora_comida = False

        fantasma_colisionado = detectar_colision() # Para detectar con qué fantasma ha colisionado

        # Detectar colisión entre Pacman y fantasmas
        if fantasma_colisionado:

            """ Si pacman ha comido una pildora y sigue habiendo tiempo en el modo pildora
             reinicia la posición del fantasma con el que ha colisionado"""


            if personaje.pildora_comida:
                fantasma_colisionado.x, fantasma_colisionado.y = 110, 110
                fantasma_colisionado = False

            #elif not pildora_comida:
            else:
                vidas -= 1  # Reduce las vidas en 1
                fantasma_colisionado.modo_escape = False


                if vidas > 0:
                    reiniciar_posiciones()  # Reinicia las posiciones de los personajes
                else:
                    pyxel.quit()  # Cierra el juego si las vidas llegan a 0





    def draw():
        pyxel.cls(0)  # Limpia la pantalla antes de redibujar
        laberinto.draw()  # Dibuja el laberinto
        personaje.draw()  # Dibuja al personaje
        for fantasma in fantasmas:  # Dibuja cada fantasma
            fantasma.draw()

        pyxel.rect (20, 240, 64, 16, 10)
        pyxel.text(25, 244, f"Vidas: {vidas}",1)

        # Enseña el tiempo que queda
        if tiempo_modo_pildora > 0:
            tiempo_restante = tiempo_modo_pildora // 30  # Convertir fotogramas a segundos
            pyxel.text(170, 5, f"Modo Pildora: {tiempo_restante}s", 8)


    pyxel.run(update, draw)  # Corre el bucle principal

if __name__ == "__main__":
    main()