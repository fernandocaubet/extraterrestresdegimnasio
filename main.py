import pygame
import random
import math
from pygame import mixer

# inicializar game
pygame.init()


# crear pantalla
pantalla = pygame.display.set_mode((800,600) )
se_ejecuta = True


# Titulo y icono
pygame.display.set_caption('Invasion Pastelera')
icono = pygame.image.load("extraterrestre.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo.jpg')


# Variables Jugador
img_jugador = pygame.image.load('nave.png')
jugador_x = 368
jugador_y = 520
jugador_x_cambio = 0


# Variables enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantinda_enemigos = 8
for r in range(cantinda_enemigos):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.1)
    enemigo_y_cambio.append(50)

# Variables de la bala
img_bala = pygame.image.load('bala.png')
balas = []
bala_x = 0
bala_y = 520
bala_x_cambio = 0
bala_y_cambio = 0.3
bala_visible = False
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

fuente_final = pygame.font.Font('freesansbold.ttf', 40)


#
def texto_final():
    mi_fuente_final = fuente_final.render('JUEGO TERMINADO', True,(255,255,255))
    pantalla.blit(mi_fuente_final, (60,200))



#Funcion Mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje:{puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x,y))



# Funcion JuGADOR
def jugador(x,y):
    pantalla.blit(img_jugador,(x, y))

# Funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x, y))

# Funcuion de bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x+16, y+10))

# Funcion detectar colision
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt((math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2)))
    if distancia < 27:
        return True
    else:
        return False


# Loop de Juego
while se_ejecuta:

    # fondo de la pantalla
    pantalla.blit(fondo, (0,0))

    # iterar eventos
    for evento in pygame.event.get():

        # Evento Cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # Evanto presionar tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.2
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.2
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.set_volume(0.3)
                sonido_bala.play()
                nueva_bala = {"x":jugador_x, "y":jugador_y, "velocidad": -5}
                balas.append(nueva_bala)


        # Evento soltar Flecha
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)



    #m Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio


    # Mantener detro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicacion del enemigo
    for e in range(cantinda_enemigos):
        enemigo_x[e] += enemigo_x_cambio[e]

        # FIn del JUEGO
        if enemigo_y[e] > 500:
            for k in range(cantinda_enemigos):
                enemigo_x[k] = 1000
            texto_final()
            break


        #  Mantener detro de bordes al enemigo

        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3              #cambia la direccion
            enemigo_y[e] += enemigo_y_cambio[e]     #baja 50 px
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]

        for bala in balas:
            colision = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision:
                sonido_colicion = mixer.Sound('colicion.mp3')
                sonido_colicion.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)
                break
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento Bala
    if bala_y <= 30:
        bala_y = 500
        bala_visible = False


    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio



    jugador(jugador_x,jugador_y)

    mostrar_puntaje(texto_x,texto_y)
    pygame.display.update()
