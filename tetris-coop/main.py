import pygame
import random

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
BACKGROUND_COLOR = (0 , 10, 10)  # Color de fondo del tablero (gris oscuro)

# SPEEED 
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

class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, screen, offset_x, offset_y):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (
                            offset_x + (self.x + col_idx) * CELL_SIZE,
                            offset_y + (self.y + row_idx) * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        )
                    )

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.background_color = BACKGROUND_COLOR  # Color de fondo del tablero (gris oscuro)
        self.lines_cleared_count = 0  # Contador de líneas eliminadas

    def draw(self, screen, offset_x, offset_y):

        # Dibujar el fondo del tablero
        pygame.draw.rect(
            screen,
            self.background_color,  # Usar el color definido
            (
                offset_x,
                offset_y,
                BOARD_WIDTH * CELL_SIZE,
                BOARD_HEIGHT * CELL_SIZE,
            )
        )

        # Dibujar el borde del tablero
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            (
                offset_x, offset_y,
                BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE
            ),
            3
        )
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.grid[row][col]:
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        (
                            offset_x + col * CELL_SIZE,
                            offset_y + row * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        )
                    )

    def check_collision(self, tetromino):
        for row_idx, row in enumerate(tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = tetromino.x + col_idx
                    y = tetromino.y + row_idx
                    # Verificar límites del tablero
                    if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                        print(f"Colisión detectada fuera de límites en ({x}, {y}).")
                        return True
                    # Verificar celdas ocupadas
                    if y >= 0 and self.grid[y][x] != 0:
                        print(f"Colisión detectada en celda ocupada ({x}, {y}).")
                        return True
        return False



    def place_tetromino(self, tetromino):
        print("Intentando colocar la pieza en el tablero...")
        for row_idx, row in enumerate(tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = tetromino.x + col_idx
                    y = tetromino.y + row_idx
                    if y < 0 or self.grid[y][x] != 0:  # Ignorar si la celda está ocupada o fuera del tablero
                        print(f"Advertencia: Celda ocupada en ({x}, {y}). Ignorando este bloque.")
                        continue
                    print(f"Colocando bloque en ({x}, {y}).")
                    self.grid[y][x] = 1




    def clear_lines(self):
        print("Comprobando si hay líneas para limpiar...")
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = BOARD_HEIGHT - len(new_grid)
        self.lines_cleared_count += lines_cleared  # Incrementar el contador
        print(f"Líneas eliminadas: {lines_cleared}.")
        self.grid = [[0] * BOARD_WIDTH for _ in range(lines_cleared)] + new_grid



    def is_game_over(self):
        #print("Comprobando si el juego ha terminado...")
        game_over = any(self.grid[1][col] for col in range(BOARD_WIDTH))
        if game_over:
            print("Game over detectado: hay bloques en la segunda fila.")
        return game_over


class Player:
    def __init__(self, board, x_start, color, controls):
        self.board = board
        self.initial_x = x_start  # Guardar la posición inicial
        self.tetromino = self.spawn_tetromino(x_start, color)
        self.controls = controls
        self.last_action_time = pygame.time.get_ticks()
        # Crear temporizadores independientes para cada acción
        self.last_action_times = {
            'left': 0,
            'right': 0,
            'down': 0,
            'rotate': 0
        }

    def spawn_tetromino(self, x_start, color):
        print(f"Generando nueva pieza para el jugador en la posición inicial {x_start}.")
        tetromino = Tetromino(x_start, 0, random.choice(SHAPES), color)
        if self.board.check_collision(tetromino):
            print("No hay espacio para generar una nueva pieza. El jugador debe esperar.")
            return None  # Devuelve None si no se puede generar una pieza
        print(f"Nueva pieza generada en posición válida: ({tetromino.x}, {tetromino.y})")
        return tetromino

    def update(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Movimiento a la izquierda
        if keys[self.controls['left']] and current_time - self.last_action_times['left'] > SPEED_LEFT:
            self.tetromino.x -= 1
            if self.board.check_collision(self.tetromino):
                self.tetromino.x += 1  # Revertir si colisiona
            self.last_action_times['left'] = current_time

        # Movimiento a la derecha
        if keys[self.controls['right']] and current_time - self.last_action_times['right'] > SPEED_RIGHT:
            self.tetromino.x += 1
            if self.board.check_collision(self.tetromino):
                self.tetromino.x -= 1  # Revertir si colisiona
            self.last_action_times['right'] = current_time

        # Movimiento hacia abajo
        if keys[self.controls['down']] and current_time - self.last_action_times['down'] > SPEED_DOWN:
            self.tetromino.y += 1
            if self.board.check_collision(self.tetromino):
                self.tetromino.y -= 1  # Revertir si colisiona
            self.last_action_times['down'] = current_time

        # Rotación
        if keys[self.controls['rotate']] and current_time - self.last_action_times['rotate'] > SPEED_ROTATE:
            self.tetromino.rotate()
            if self.board.check_collision(self.tetromino):
                for _ in range(3):  # Revertir rotación (rotar 3 veces más para restaurar)
                    self.tetromino.rotate()
            self.last_action_times['rotate'] = current_time





    def drop(self):
        print(f"Intentando mover hacia abajo la pieza del jugador en posición: ({self.tetromino.x}, {self.tetromino.y})")
        self.tetromino.y += 1
        if self.board.check_collision(self.tetromino):
            print(f"Colisión detectada al mover hacia abajo. Fijando pieza en el tablero.")
            self.tetromino.y -= 1  # Revertir movimiento
            self.board.place_tetromino(self.tetromino)  # Colocar la pieza en el tablero
            self.board.clear_lines()  # Limpiar líneas completas
            print("Líneas despejadas si es necesario. Generando nueva pieza.")
            self.tetromino = self.spawn_tetromino(self.initial_x, self.tetromino.color)  # Generar nueva pieza
        else:
            print(f"La pieza se movió hacia abajo a la posición ({self.tetromino.x}, {self.tetromino.y}).")



    def draw(self, screen, offset_x, offset_y):
        self.tetromino.draw(screen, offset_x, offset_y)

def game_over_menu(screen):
    print("Entrando al menú de game over...")
    font = pygame.font.Font(None, 74)
    screen.fill(BLACK)

    # Variables de espaciado dinámico
    line_spacing = 60  # Espaciado entre las líneas
    start_y = SCREEN_HEIGHT // 5  # Punto inicial vertical

    # Renderizar los textos
    message = font.render("Perdierooon :S", True, WHITE)
    separator = font.render(".:*~*:._.:*~*:._.:*~*:._.:*~*:.", True, WHITE)
    retry = font.render("R para reintentar", True, WHITE)
    menu = font.render("ESC para menú", True, WHITE)

    # Mostrar textos con espaciado
    screen.blit(message, (SCREEN_WIDTH // 5, start_y))
    screen.blit(separator, (SCREEN_WIDTH // 5, start_y + line_spacing))
    screen.blit(retry, (SCREEN_WIDTH // 5, start_y + 2 * line_spacing))
    screen.blit(menu, (SCREEN_WIDTH // 5, start_y + 3 * line_spacing))

    pygame.display.flip()

    # Manejo de eventos
    while True:
        print("Esperando entrada en el menú de game over...")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("El jugador cerró la ventana desde el menú de game over.")
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("El jugador seleccionó reintentar.")
                    return "retry"
                if event.key == pygame.K_ESCAPE:
                    print("El jugador seleccionó volver al menú principal.")
                    return "menu"
        pygame.time.wait(100)



def main_menu(screen):
    # Cargar la imagen de fondo desde la carpeta assets
    background = pygame.image.load("./assets/tetris_background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Escalar al tamaño de la ventana

    # Fuente para los textos
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    
    while True:
        # Dibujar la imagen de fondo
        screen.blit(background, (0, 0))

        # Dibujar los textos del menú en la esquina inferior izquierda
        title = font.render("Tetris Cooperativo", True, WHITE)
        start = small_font.render("Enter para jugar", True, WHITE)
        quit_msg = small_font.render("Esc para salir", True, WHITE)
        
        # Posiciones del menú
        margin = 50  # Margen desde el borde de la pantalla
        screen.blit(title, (margin, SCREEN_HEIGHT - 200))  # Título del juego
        screen.blit(start, (margin, SCREEN_HEIGHT - 150))  # Opción "Enter para jugar"
        screen.blit(quit_msg, (margin, SCREEN_HEIGHT - 100))  # Opción "Esc para salir"

        pygame.display.flip()
        pygame.time.wait(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
def main():
    pygame.init()
    # Ajustar el tamaño de la ventana al tamaño inicial del tablero
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE + 100  # Agregar márgenes
    SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE + 100
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Tetris Cooperativo")
    clock = pygame.time.Clock()

    # Variables para la caída automática
    fall_time = 0  # Tiempo acumulado para controlar la caída
    fall_speed = 500  # Tiempo en milisegundos entre cada caída automática

    while True:
        print("Juego iniciado, inicializando tablero y jugadores.")
        # Inicializar el tablero y los jugadores
        board = Board()
        player1 = Player(board, 3, BLUE, {'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w})
        player2 = Player(board, BOARD_WIDTH - 6, RED, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP})

        print("Mostrando menú principal.")
        main_menu(screen)  # Mostrar el menú principal

        running = True
        while running:
            try:
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Saliendo del juego.")
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Detectar tecla ESC
                            print("ESC presionado. Volviendo al menú principal.")
                            running = False  # Salir del juego y volver al menú principal

                # Obtener tamaño actual de la ventana
                screen_width, screen_height = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()

                # Calcular el offset dinámico para centrar el tablero
                offset_x = (screen_width - BOARD_WIDTH * CELL_SIZE) // 2
                offset_y = (screen_height - BOARD_HEIGHT * CELL_SIZE) // 2

                # Actualizar las piezas automáticamente después de un intervalo
                if current_time - fall_time > fall_speed:
                    print("Actualizando caída automática de piezas.")
                    player1.drop()
                    player2.drop()
                    fall_time = current_time

                # Limpiar pantalla y dibujar el tablero y las piezas
                screen.fill(BLACK)

                # Dibujar el texto "ESC : Menú"
                font = pygame.font.Font(None, 36)
                menu_text = font.render("ESC : Menú", True, WHITE)
                screen.blit(menu_text, (offset_x, 10))  # Alinear con el inicio del tablero

                # Dibujar el contador de líneas eliminadas
                tablero_derecha = offset_x + BOARD_WIDTH * CELL_SIZE
                lines_text = font.render(f"Líneas: {board.lines_cleared_count}", True, WHITE)
                text_width, _ = font.size(f"Líneas: {board.lines_cleared_count}")  # Obtener ancho del texto
                screen.blit(lines_text, (tablero_derecha - text_width, 10))  # Alinear con el borde derecho del tablero

                # Dibujar el tablero y las piezas
                board.draw(screen, offset_x, offset_y)
                player1.update()
                player2.update()
                player1.draw(screen, offset_x, offset_y)
                player2.draw(screen, offset_x, offset_y)

                # Comprobar si el juego ha terminado
                if board.is_game_over():
                    print("¡Game Over detectado! Mostrando menú de game over.")
                    choice = game_over_menu(screen)
                    if choice == "retry":
                        print("El jugador eligió reintentar.")
                        board = Board()
                        player1 = Player(board, 3, BLUE, {'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w})
                        player2 = Player(board, BOARD_WIDTH - 6, RED, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP})
                        fall_time = current_time  # Reiniciar el temporizador
                        continue
                    elif choice == "menu":
                        print("El jugador eligió volver al menú principal.")
                        running = False

                pygame.display.flip()
                clock.tick(FPS)

            except Exception as e:
                print(f"Excepción detectada: {str(e)}")
                choice = game_over_menu(screen)
                if choice == "retry":
                    print("El jugador eligió reintentar después de Game Over.")
                    board = Board()
                    player1 = Player(board, 3, BLUE, {'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w})
                    player2 = Player(board, BOARD_WIDTH - 6, RED, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP})
                    fall_time = current_time  # Reiniciar el temporizador
                    continue
                elif choice == "menu":
                    print("El jugador eligió volver al menú principal después de Game Over.")
                    running = False

if __name__ == "__main__":
    main()
