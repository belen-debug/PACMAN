#FANTASMA"
import pyxel
import random

class Fantasma:
    def __init__(self, x, y, sprite, laberinto):
        self.x = x  # Posición X
        self.y = y  # Posición Y
        self.sprite = sprite  # Sprite del fantasma (índice para la imagen vertical)
        self.tamano = 8  # Tamaño del fantasma (en píxeles)
        self.laberinto = laberinto  # Referencia al laberinto
        self.direccion = random.choice(['left', 'right', 'up', 'down'])  # Dirección inicial aleatoria
        self.velocidad = 2  # Velocidad de movimiento del fantasma (puedes ajustar esto)

    def puede_moverse(self, x, y):
        """Verifica si el fantasma puede moverse a las coordenadas dadas"""
        tamano_celda = self.laberinto.tamano
        matriz = self.laberinto.muros

        # Calcula las celdas ocupadas por el fantasma según su tamaño
        celda_izquierda = x // tamano_celda
        celda_derecha = (x + self.tamano - 1) // tamano_celda
        celda_superior = y // tamano_celda
        celda_inferior = (y + self.tamano - 1) // tamano_celda

        # Asegurarse de no salir de los límites de la matriz
        if celda_izquierda < 0 or celda_superior < 0 or celda_derecha >= len(matriz[0]) or celda_inferior >= len(matriz):
            return False

        # Verifica todas las celdas que ocupa el fantasma
        for fila in range(celda_superior, celda_inferior + 1):
            for columna in range(celda_izquierda, celda_derecha + 1):
                if matriz[fila][columna] == 1:  # Si hay un muro
                    return False

        return True

    def update(self):
        """Actualizar la posición del fantasma con movimiento aleatorio y evitando paredes"""
        nuevo_x, nuevo_y = self.x, self.y

        # Movimiento según la dirección actual
        if self.direccion == 'left':
            nuevo_x -= self.velocidad
        elif self.direccion == 'right':
            nuevo_x += self.velocidad
        elif self.direccion == 'up':
            nuevo_y -= self.velocidad
        elif self.direccion == 'down':
            nuevo_y += self.velocidad

        # Verificar si puede moverse a la nueva posición, si no puede, cambiar de dirección aleatoria
        if not self.puede_moverse(nuevo_x, nuevo_y):
            self.direccion = random.choice(['left', 'right', 'up', 'down'])

        # Si puede moverse, actualizamos la posición
        if self.puede_moverse(nuevo_x, nuevo_y):
            self.x, self.y = nuevo_x, nuevo_y

    def draw(self):
        """Dibuja el fantasma en pantalla usando su sprite (suponiendo que están en una fila vertical)"""
        pyxel.blt(self.x, self.y, 0, 0, self.sprite * 16, self.tamano, self.tamano, 0)



