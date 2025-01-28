# config.py

# Configuración general
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
CELL_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // CELL_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (80, 70, 60)
BORDER_COLOR = (200, 200, 200)
BACKGROUND_COLOR = (0, 10, 10)  # Color de fondo del tablero (gris oscuro)

# Velocidades de movimiento
SPEED_ROTATE = 110
SPEED_LEFT = 100
SPEED_RIGHT = 100
SPEED_DOWN = 100

# Formas de las piezas de Tetris
SHAPES = [
    [[1, 1, 1, 1]],  # Línea
    [[1, 1], [1, 1]],  # Cuadrado
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]
