import pygame

import sys
import random

# Inicializar Pygame
pygame.init()

#Iniciar juego
start = False

# Configuración de la ventana
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Autoajuste de Parámetros")

#------------------------------------------------------------------------
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Añadir Sprite PNG")
# Cargar la imagen del sprite (asegúrate de que tenga fondo transparente)
sprite_image = pygame.image.load("sprite.png").convert_alpha()
# Crear un rectángulo para posicionar el sprite
sprite_rect = sprite_image.get_rect()
sprite_rect.center = (400, 300)  # Posición inicial del sprite
#------------------------------------------------------------------------


#texto
fuente = pygame.font.Font(None, 45)  # Fuente predeterminada, tamaño 36
COLOR_TEXTO = (0, 0, 0)
# Variables de tiempo
minutos = 0
segundos = 0

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Reloj para controlar FPS
reloj = pygame.time.Clock()
FPS = 60

# Propiedades del personaje
x, y = ANCHO // 2, ALTO // 2
velocidad = 8
player_size = 25

# Propiedades del enemigo
instanciasEnemigos = 3
LimiteEnemigo = 10  # Limita la velocidad de los enemigos
canMove = False  # Controla si el jugador se está moviendo

# decremento = True  # Controla si se decrementa el límite de enemigos
# aumentoInstancias = True  # Controla si se aumenta el número de instancias de enemigos

# Bucle principal
def mover_personaje(x, y, velocidad, teclas, ancho, alto):
    if teclas[pygame.K_LEFT]:
        x -= velocidad
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    if teclas[pygame.K_UP]:
        y -= velocidad
    if teclas[pygame.K_DOWN]:
        y += velocidad
    # Teletransporte si sale de los bordes
    if ((x > ancho or x < 0) and x != 0):
        x -= (x/abs(x)) * ancho
    if ((y > alto or y < 0) and y != 0):
        y -= (y/abs(y)) * alto
    return x, y

def actualizar_personaje_y_colisiones(x, y, enemigos, player_size):
    # Mover personaje y detectar colisiones con enemigos
    teclas = pygame.key.get_pressed()
    x, y = mover_personaje(x, y, velocidad, teclas, ANCHO, ALTO)
    dibujar_personaje(pantalla, x, y)

    # Colisión con enemigos
    for ex, ey, _, _ in enemigos:
        distancia = ((x - ex) ** 2 + (y - ey) ** 2) ** 0.5
        if distancia < player_size + (player_size - 5):
            game_over()
            break
    return x, y

# def actualizar_enemigo_y_colisiones(x, y, enemigos, enemy_size):
#     # Mover penemigo y detectar colisiones con enemigos
#     mover_enemigos(enemigos, x, y, ANCHO, ALTO, player_size)
    

#     # Colisión con enemigos
#     for ex, ey, _, _ in enemigos:
#         distancia = ((x - ex) ** 2 + (y - ey) ** 2) ** 0.5
#         if distancia < player_size + (player_size - 5):
#             game_over()
#             break
#     return x, y

def game_over():
    global x, y, enemigos, segundos, start, LimiteEnemigo
    x, y = ANCHO // 2, ALTO // 2
    # if instanciasEnemigos > 3:
    #     instanciasEnemigos -= 2
    # if LimiteEnemigo < 5:
    #     LimiteEnemigo += 2
    enemigos = instanciar_enemigos(instanciasEnemigos, ANCHO, ALTO, player_size)
    segundos = 0
    start = False

#Rend.Jugador
def dibujar_personaje(pantalla, x, y):
    # Actualiza la posición del rect del sprite antes de hacer blit
    sprite_rect.center = (x, y)
    pantalla.blit(sprite_image, sprite_rect)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill(BLANCO)

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_SPACE]:
        start = True
    canMove = any(teclas[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])
        
    #Lógica de enemigos
    def instanciar_enemigos(cantidad, ancho, alto, radio):
        enemigos = []
        for _ in range(cantidad):
            ex = random.randint(radio, ancho - radio)
            ey = random.randint(radio, alto - radio)
            # Cada enemigo tiene posición y velocidad independientes
            vx = velocidad/LimiteEnemigo
            vy = velocidad/LimiteEnemigo
            enemigos.append([ex, ey, vx, vy])
        return enemigos
    
     # Instanciar enemigos solo una vez fuera del bucle principal
    if 'enemigos' not in locals():
        enemigos = instanciar_enemigos(instanciasEnemigos, ANCHO, ALTO, player_size)

    # Dibujar enemigos
    for ex, ey, vx, vy in enemigos:
        pygame.draw.circle(pantalla, (0, 0, 255), (ex, ey), player_size-5)
    

    if start:
        x, y = mover_personaje(x, y, velocidad, teclas, ANCHO, ALTO)
        actualizar_personaje_y_colisiones(x, y, enemigos, player_size)
        dibujar_personaje(pantalla, x, y)
        

        def mover_enemigos(enemigos, px, py, ancho, alto, radio):
            for enemigo in enemigos:
                ex, ey, vx, vy = enemigo
                # Añadir un pequeño factor aleatorio para cada enemigo
                dx = px - ex + random.uniform(-20, 20)
                dy = py - ey + random.uniform(-20, 20)
                dist = (dx**2 + dy**2) ** 0.5
                if dist != 0:
                    enemigo[2] = (dx / dist) * (velocidad / LimiteEnemigo)
                    enemigo[3] = (dy / dist) * (velocidad / LimiteEnemigo)
                enemigo[0] += enemigo[2]
                enemigo[1] += enemigo[3]
            # Función anónima para colisiones entre enemigos
            # colisionar_enemigos = lambda enemigos, radio: [
            #     (
            #         enemigo.__setitem__(0, enemigo[0] + (radio if enemigo[0] < otro[0] and abs(enemigo[0] - otro[0]) < 2*radio else -radio if enemigo[0] > otro[0] and abs(enemigo[0] - otro[0]) < 2*radio else 0)),
            #         enemigo.__setitem__(1, enemigo[1] + (radio if enemigo[1] < otro[1] and abs(enemigo[1] - otro[1]) < 2*radio else -radio if enemigo[1] > otro[1] and abs(enemigo[1] - otro[1]) < 2*radio else 0))
            #     )
            #     for i, enemigo in enumerate(enemigos)
            #     for j, otro in enumerate(enemigos)
            #     if i != j and ((enemigo[0] - otro[0])**2 + (enemigo[1] - otro[1])**2) < (2*radio)**2
            # ]

            # colisionar_enemigos(enemigos, radio)

        # Mover enemigos
        mover_enemigos(enemigos, x, y, ANCHO, ALTO, player_size)

        

        #timer de actualización
        segundos += 1 / FPS
        minutos_mostrar= int(segundos // 60)  # Convertir segundos a minutos
        segundos_mostrar = int(segundos % 60)  # Obtener el resto de los segundos

        LimiteEnemigo = 4 if canMove else 1.5 # Ajusta la velocidad de los enemigos según si el jugador se mueve o no

        #Texto de tiempo
        texto_posicion_raton = f"{minutos_mostrar:02d}:{segundos_mostrar:02d}"
        #Dibujar el texto en la pantalla
        superficie_texto = fuente.render(texto_posicion_raton, True, COLOR_TEXTO)
        texto_rect = superficie_texto.get_rect(center=(ANCHO // 2, 30))  # Centrado horizontal, 30 px desde arriba
        pantalla.blit(superficie_texto, texto_rect)

    else:
        texto_inicio = "Presiona Espacio para iniciar"
        superficie_inicio = fuente.render(texto_inicio, True, COLOR_TEXTO)
        rect_inicio = superficie_inicio.get_rect(center=(ANCHO // 2, ALTO // 2 + 45))
        pantalla.blit(superficie_inicio, rect_inicio)
        # Actualiza la posición del rect del sprite antes de hacer blit
        sprite_rect.center = (x, y)

        dibujar_personaje(pantalla, x, y)

        #Texto de tiempo
        texto_posicion_raton = "00:00"
        #Dibujar el texto en la pantalla
        superficie_texto = fuente.render(texto_posicion_raton, True, COLOR_TEXTO)
        texto_rect = superficie_texto.get_rect(center=(ANCHO // 2, 30))  # Centrado horizontal, 30 px desde arriba
        pantalla.blit(superficie_texto, texto_rect)

    pygame.display.flip()
    reloj.tick(FPS)

