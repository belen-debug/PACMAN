#PACMAN
import pyxel
class Pacman:
    def __init__(self, x, y, velocidad, laberinto):
        self.x = x  # Posición inicial en el eje X
        self.y = y  # Posición inicial en el eje Y
        self.velocidad = velocidad  # Velocidad de movimiento
        self.laberinto = laberinto  # Referencia al laberinto (muros)
        self.tamano = 8 # Tamaño del personaje
        self.puntuacion = 0
        pyxel.load("assets/resources/assets.pyxres")  # Cargar recursos gráficos

    def recoge_punto(self):
        """Verifica si Pacman está en una posición con un punto"""
        for punto in self.laberinto.puntos:
            px, py = punto
            # Detectar colisión (distancia entre Pacman y el punto)
            if abs(self.x + self.tamano // 2 - px) < 4 and abs(self.y + self.tamano // 2 - py) < 4:
                self.laberinto.puntos.remove(punto)  # Eliminar el punto
                self.puntuacion += 10  # Aumentar el puntaje

    def puede_moverse(self, x, y):
        """Verifica si el personaje puede moverse a las coordenadas dadas"""
        tamano_celda = self.laberinto.tamano
        matriz = self.laberinto.muros

        # Calcula las celdas ocupadas por el personaje según su tamaño
        celda_izquierda = x // tamano_celda
        celda_derecha = (x + self.tamano - 1) // tamano_celda
        celda_superior = y // tamano_celda
        celda_inferior = (y + self.tamano - 1) // tamano_celda

        # Asegurarse de no salir de los límites de la matriz
        if celda_izquierda < 0 or celda_superior < 0 or celda_derecha >= len(matriz[0]) or celda_inferior >= len(matriz):
            return False

        # Verifica todas las celdas que ocupa el personaje
        for fila in range(celda_superior, celda_inferior + 1):
            for columna in range(celda_izquierda, celda_derecha + 1):
                if matriz[fila][columna] == 1:  # Si hay un muro
                    return False
                elif matriz[fila][columna] == 2: # Si es un lugar para el teletransporte
                    # Llamo a la función teletransportar
                    self.teletransportar()
                    return True


        return True

        # Creo una función teletransportar
    def teletransportar(self):
        tamano_celda = self.laberinto.tamano

        # Cuando pacman está en el borde izquierdo del mapa
        if self.x <= 0:
            # Se teletransporta al borde derecho
            # (número de celdas - 1) * tamaño de celda
            self.x = (len(self.laberinto.muros[0]) - 1) * tamano_celda
        # Si Pacman está en el borde derecho (ancho del mapa)
        elif self.x >= (len(self.laberinto.muros[0]) * tamano_celda) - self.tamano:
            # Se teletransporta al borde izquierdo
            self.x = 0


    def update(self):
        """Actualizar la posición del personaje según las teclas presionadas"""
        nuevo_x, nuevo_y = self.x, self.y

        if pyxel.btn(pyxel.KEY_LEFT):
            nuevo_x -= self.velocidad
        if pyxel.btn(pyxel.KEY_RIGHT):
            nuevo_x += self.velocidad
        if pyxel.btn(pyxel.KEY_UP):
            nuevo_y -= self.velocidad
        if pyxel.btn(pyxel.KEY_DOWN):
            nuevo_y += self.velocidad

        # Verificar colisiones antes de mover
        if self.puede_moverse(nuevo_x, self.y):  # Movimiento horizontal
            self.x = nuevo_x
        if self.puede_moverse(self.x, nuevo_y):  # Movimiento vertical
            self.y = nuevo_y

        self.recoge_punto()

    def draw(self):
        """Dibuja al personaje en pantalla"""
        pyxel.blt(self.x, self.y, 0, 16, 0, self.tamano, self.tamano, 0)
        pyxel.text(5, 5, f"Puntuacion: {self.puntuacion}", 2)


