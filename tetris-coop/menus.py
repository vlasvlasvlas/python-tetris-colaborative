# menus.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE


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