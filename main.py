# MAIN
import pyxel
from pacman1 import Pacman
from muros import Muros
from fantasma import Fantasma

def crear_fantasmas():
    # Coordenadas del centro del laberinto (ajustar según tamaño del laberinto)
    centro_x = 120  # Coordenada X en el centro
    centro_y = 120  # Coordenada Y en el centro
    # Lista de fantasmas con diferentes sprites
    fantasmas = [
        Fantasma(centro_x, centro_y, 0,),  # Primer fantasma (sprite 0)
    ]
    return fantasmas


def main():
    pyxel.init(256, 256)  # Inicializa la pantalla
    pyxel.load("assets/resources/assets.pyxres")  # Cargar recursos gráficos
    laberinto = Muros(16)  # Crea el laberinto
    personaje = Pacman(16, 16, 1, laberinto)  # Crea al personaje Pacman
    fantasmas = [
       Fantasma(110, 110, 2.5, laberinto),  # Fantasma rojo
       Fantasma(120, 120, 3, laberinto),  # Fantasma rosado
       Fantasma(130, 130, 2, laberinto),  # Fantasma marrón
       Fantasma(140, 140, 1.5, laberinto),  # Fantasma azul
    ]
    vidas = 3 

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
                return True
        return False

    def update():
        nonlocal vidas

        personaje.automovimiento() #Hace que pacman se mueva solo
        personaje.update()  # Actualiza a Pacman
        for fantasma in fantasmas:
            fantasma.update()

        # Detectar colisión entre Pacman y fantasmas
        if detectar_colision():
            vidas -= 1  # Reduce las vidas en 1
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

        pyxel.text(210, 5, f"Vidas: {vidas}",5)


    pyxel.run(update, draw)  # Corre el bucle principal

if __name__ == "__main__":
    main()

