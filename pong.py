import pygame as py
import random
import time
from tkinter import *



# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Variables
W, H = 1600, 900
W2, H2 = W//2, H//2
HW, HH = W / 2, H / 2
FPS = 60
secs = 0

# Initialize PyGame
py.init()
py.mixer.init()
display = py.display.set_mode((W, H))
py.display.set_caption('Pong')
clock = py.time.Clock()

# Clase usada para iniciar el juego con determinados ajustes
# Instancias: cantidad de jugadores(1 o 2), cantidad de paletas(1 o 2), difficultad(0, 1 o 2)
class Game:
    def __init__(self, player, pallets, difficulty, style):
        self.players = player
        self.pallets = pallets
        self.difficulty = difficulty
        self.style = style
        self.images = self.load_images()
        self.sound_effects = self.load_sounds()
        self.matrix = []
        self.make_matrix()
        self.score1 = 0
        self.score2 = 0

    def make_matrix(self):  # Metodo para generar matriz
        n, m = 25, 40
        i, j = 0, 0
        x, y = W // m, H // n
        while W >= i:
            while H >= j:
                self.matrix.append([i, j])
                j += y
            i += x
            j = 0

    def get_matrix(self):
        return self.matrix

    def start_game(self):  # Metodo para iniciar el juego
        images = self.images[0]
        poss1 = 38
        poss2 = 1026
        poss3 = poss1 + 5
        poss4 = poss2 + 5
        if self.players == 1:
            if self.pallets == 2:
                poss1 -= 4
                poss2 -= 4
                humane2 = Player(('py.K_w', 'py.K_s'), self.difficulty, poss3, self.matrix, [True, 'HUMANE'], images[1], self.pallets)
                cpu2 = Player('', self.difficulty, poss4, self.matrix, [True, 'CPU'], images[3], self.pallets)
                sprites.add(humane2)
                sprites.add(cpu2)
                players.add(humane2)
                players.add(cpu2)
            humane = Player(('py.K_w', 'py.K_s'), self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
            cpu = Player('', self.difficulty, poss2, self.matrix, [True, 'CPU'], images[2], self.pallets)
            sprites.add(humane)
            sprites.add(cpu)
            players.add(humane)
            players.add(cpu)

        if self.players == 2:
            if self.pallets == 2:
                poss1 -= 4
                poss2 -= 4
                humane1 = Player(('py.K_w', 'py.K_s'), self.difficulty, poss3, self.matrix, [True, 'HUMANE'], images[1], self.pallets)
                humane2 = Player(('py.K_UP', 'py.K_DOWN'), self.difficulty, poss4, self.matrix, [True, 'HUMANE'], images[3], self.pallets)
                sprites.add(humane1)
                sprites.add(humane2)
                players.add(humane1)
                players.add(humane2)
            humane1 = Player(('py.K_w', 'py.K_s'), self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
            humane2 = Player(('py.K_UP', 'py.K_DOWN'), self.difficulty, poss2, self.matrix, [True, 'HUMANE'], images[2], self.pallets)
            sprites.add(humane1)
            sprites.add(humane2)
            players.add(humane1)
            players.add(humane2)
        ball = Ball(self.difficulty, self.images[1])
        sprites.add(ball)
        balls.add(ball)

    def load_images(self):  # Metodo para cargar imagenes del juego
        pallet_images = None
        ball = None
        bg = None
        wall_image = None
        if self.style == 0:
            white_pallet = py.image.load('img/default_pallet.png').convert_alpha()
            ball = py.Surface((10, 10))
            ball.fill(white)
            bg = py.image.load('img/default_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [white_pallet, white_pallet, white_pallet, white_pallet]
            wall_image = white_pallet
        if self.style == 1:
            wall_image = py.image.load('img/neon_wall.png').convert_alpha()
            player_red = py.image.load('img/neon_red.png').convert_alpha()
            player_green = py.image.load('img/neon_green.png').convert_alpha()
            player_pink = py.image.load('img/neon_pink.png').convert_alpha()
            player_blue = py.image.load('img/neon_blue.png').convert_alpha()
            ball = py.image.load('img/neon_ball.png').convert_alpha()
            bg = py.image.load('img/neon_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [player_red, player_green, player_pink, player_blue]
        if self.style == 2:
            wall_image = py.image.load('img/baseball_wall.png').convert_alpha()
            player_bat = py.image.load('img/baseball_bat.png').convert_alpha()
            ball = py.image.load('img/baseball_ball.png').convert_alpha()
            pallet_images = [player_bat, player_bat, player_bat, player_bat]
            bg = py.image.load('img/baseball_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
        return pallet_images, ball, bg, wall_image

    def load_sounds(self):  # Metodo para cargar la musica del juego
        bounce = None
        score = None
        music = None
        if self.style == 0:
            bounce = py.mixer.Sound('sound/default_bounce.wav')
            score = py.mixer.Sound('sound/default_score.wav')
            music = py.mixer.Sound('sound/default_music.ogg')
        if self.style == 1:
            bounce = py.mixer.Sound('sound/neon_bounce.wav')
            score = py.mixer.Sound('sound/neon_score.wav')
            music = py.mixer.Sound('sound/neon_music.ogg')
        if self.style == 2:
            bounce = py.mixer.Sound('sound/baseball_bounce.wav')
            score = py.mixer.Sound('sound/baseball_score.wav')
            music = py.mixer.Sound('sound/baseball_music.ogg')
        return bounce, score, music

    def get_sound_effects(self):  # Metodo para obtener los sonidos del juego
        return self.sound_effects

    def add_score1(self):  # Metodo que ajusta el puntaje del jugador 1
        self.score1 += 1
        for pallets in players:
            pallets.reset_speed()

    def add_score2(self):  # Metodo que ajusta el puntaje del jugador 2
        self.score2 += 1
        for pallets in players:
            pallets.reset_speed()

    def get_scores(self):
        return self.score1, self.score2

    def get_wall_spawn_rate(self):
        spawn_rate = 0
        if self.difficulty == 0:
            spawn_rate = 0.7
        elif self.difficulty == 1:
            spawn_rate = 0.5
        elif self.difficulty == 2:
            spawn_rate = 0.25
        return spawn_rate


def draw_text(surf, text, poss, font):
    font_type = py.font.match_font(font[0])
    make_font = py.font.Font(font_type, font[1])
    text_surface = make_font.render(text, True, font[2])
    rect = text_surface.get_rect()
    rect.center = poss
    surf.blit(text_surface, rect)


# Clase que crea las paletas de los jugadores
# Instancias: controles del jugador, difficultad, posicion de las paletas, la matrix, el estado(vivo, humano/computador)
class Player(py.sprite.Sprite):
    def __init__(self, keys, difficulty, poss, matrix, status, image, pallets):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.pallets = pallets
        size = self.set_pallets_size()
        self.pallet_size = matrix[12][1] - matrix[12-size][1]
        self.status = status
        self.keys = keys
        self.matrix = matrix
        self.speed = self.set_speed()
        self.default_speed = self.speed
        self.image = py.transform.scale(image, (25, self.pallet_size))
        self.rect = self.image.get_rect()
        self.rect.center = self.matrix[poss]
        self.speed_limit = 40

    def pallet_segments(self):  # Metodo que retorna una lista con los segmentos de la paleta
        segment = self.pallet_size / 3
        return [self.rect.top] + [self.rect.top+segment] + [self.rect.bottom-segment] + [self.rect.bottom]

    def set_pallets_size(self):  # Metodo que ajusta el largo de la paleta segun dificultad
        large = 0
        if self.difficulty == 0:
            large = 9
        if self.difficulty == 1:
            large = 6
        if self.difficulty == 2:
            large = 3
        return large

    def set_speed(self):  # Metodo que ajusta la velocidad de la paleta segun dificultad
        speed = 0
        if self.difficulty == 0:
            speed = 7
        if self.difficulty == 1:
            speed = 10
        if self.difficulty == 2:
            speed = 15
        return speed

    def increase_xSpeed(self):  # Metodo para aumentar la velocidad progresivamente
        if self.speed_limit > self.speed > 0:
            self.speed += 1
        if -self.speed_limit < self.speed < 0:
            self.speed -= 1

    def reset_speed(self):
        self.speed = self.default_speed

    def set_status(self, boolean):
        self.status[0] = boolean

    def update(self):  # Metodo que actualiza la posicion de la paleta en la pantalla
        k = py.key.get_pressed()
        if self.pallets == 2:
            if self.status[0] and self.status[1] == 'HUMANE':
                if k[eval(self.keys[0])]:
                    self.rect.y -= self.speed
                if k[eval(self.keys[1])]:
                    self.rect.y += self.speed
            if self.status[0] and self.status[1] == 'CPU':
                for ball in balls:
                    y = ball.get_ball_yPoss()
                    if self.difficulty == 2:
                        self.rect.y = y
                    if self.difficulty == 1:
                        if secs % 2 == 0:
                            self.rect.y = y
                    if self.difficulty == 0:
                        if secs % 3 == 0:
                            self.rect.y = y
            if self.rect.bottom < 0:
                self.rect.top = H
            if self.rect.top > H:
                self.rect.bottom = 0
        else:
            if self.status[0] and self.status[1] == 'HUMANE':
                if k[eval(self.keys[0])] and self.rect.top > 0:
                    self.rect.y -= self.speed
                if k[eval(self.keys[1])] and self.rect.bottom < H:
                    self.rect.y += self.speed
            if self.status[0] and self.status[1] == 'CPU':
                for ball in balls:
                    y = ball.get_ball_yPoss()
                    if self.difficulty == 2:
                        self.rect.y = y
                    if self.difficulty == 1:
                        if secs % 2 == 0:
                            self.rect.y = y
                    if self.difficulty == 0:
                        if secs % 3 == 0:
                            self.rect.y = y


# Clase que crea la pelota
# Instancias: la difficultad
class Ball(py.sprite.Sprite):
    def __init__(self, difficulty, image):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.poss = (HW, HH)
        self.size = self.set_size()
        self.original_image = py.transform.scale(image, (self.size, self.size))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.poss
        self.speed = self.set_speed()
        self.xSpeed = random.choice(self.speed)
        self.ySpeed = random.choice(self.speed)
        self.sound_effects = game.get_sound_effects()
        self.speed_limit = 55
        self.rotation_speed = 7
        self.last_rotation = 0

    def rotate(self):  # Metodo para rotar la imagen de la bola
        self.last_rotation += self.rotation_speed
        self.image = py.transform.rotate(self.original_image, self.last_rotation)

    def get_ball_poss(self):  # Metodo para obtener la posicion de la bola
        return self.rect.center

    def get_ball_yPoss(self):
        return self.rect.y

    def set_ySpeed(self, collision):  # Metodo que hace a la pelota cambiar de direccion en caso de colisionar con la paleta
        if collision == 'top':
            self.ySpeed = self.speed[0]
        if collision == 'center':
            self.ySpeed = 0
        if collision == 'bottom':
            self.ySpeed = self.speed[1]

    def set_xSpeed(self):  # Metodo para invertir la direccion de la bola al rebotar
        if self.xSpeed < 0:
            self.xSpeed = abs(self.xSpeed)
        else:
            self.xSpeed = -self.xSpeed

    def top_xSpeed(self):  # Metodo para cambiar la velocidad de la bola
        if self.xSpeed < 0:
            self.xSpeed = -50
        else:
            self.xSpeed = 50

    def increase_xSpeed(self):  # Metodo para aumentar la velocidad progresivamente
        if self.speed_limit > self.xSpeed > 0:
            self.xSpeed += 2
        if -self.speed_limit < self.xSpeed < 0:
            self.xSpeed -= 2

    def set_speed(self):  # Metodo que ajusta la velocidad de la pelota segun dificultads
        speed_range = [0, 0]
        if self.difficulty == 0:
            speed_range = [-6, 6]
        if self.difficulty == 1:
            speed_range = [-8, 8]
        if self.difficulty == 2:
            speed_range = [-10, 10]
        return speed_range

    def set_size(self):  # Metodo que ajusta el radio de la bola segun dificultad
        ball_size = 0
        if self.difficulty == 0:
            ball_size = 55
        if self.difficulty == 1:
            ball_size = 40
        if self.difficulty == 2:
            ball_size = 25
        return ball_size

    def new_ball(self):  # Metodo que crea una bola cada vez que se anota un punto
        newBall = Ball(self.difficulty, self.original_image)
        sprites.add(newBall)
        balls.add(newBall)

    def update(self):  # Metodo que actualiza la posicion de la pelota en la pantalla
        self.rotate()
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        if self.rect.top <= 0:
            self.ySpeed = -self.ySpeed
            self.rect.top = 1
            self.sound_effects[0].play()
        if self.rect.bottom >= H:
            self.ySpeed = -self.ySpeed
            self.rect.bottom = H-1
            self.sound_effects[0].play()
        if self.rect.left < 0:
            self.sound_effects[1].play()
            game.add_score2()
            time.sleep(1)
            self.kill()
            self.new_ball()
        if self.rect.right > W:
            self.sound_effects[1].play()
            game.add_score1()
            time.sleep(1)
            self.kill()
            self.new_ball()


# Clase que crea la muros
# Instancias:
class Wall(py.sprite.Sprite):
    def __init__(self, matrix, image):
        py.sprite.Sprite.__init__(self)
        self.matrix = matrix
        self.width = random.randrange(20, 100, W//40)
        self.height = random.randrange(20, 100, H//25)
        self.image = py.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = random.choice(self.matrix[400:800])

#Parte del menu interfaz

# Variables
W2, H2 = 800, 600
game = Game([1,1,1,0])
def player1():
    game = Game(1,1,1,0)
def player2():
    global game
    game = Game(2,1,1,0)
    main.destroy()
def paletas1():
    game = Game(1,1,1,0)
def paletas2():
    game = Game(1,2,1,0)
def facil():
    game = Game(1,1,0,0)
def medio():
    game = Game(1,1,1,0)
def dificil():
    game = Game(1,1,2,0)
main = Tk()
main.minsize(W2, H2)
main.resizable(NO, NO)
main.title('Pong')
Fondo_pong = PhotoImage(file="img/Imagen de menu de pong.gif")


# Interface
def load_interface(xPoss, yPoss, xWidth, fgColor, bgColor, fonts):
    # Ventana de ajustes
    def ajustes():
        def cerrar_ajustes():
            ventana2.destroy()
            main.deiconify()

        main.withdraw()

        ventana2 = Toplevel()
        ventana2.title("Ajustes")

        ventana2.minsize(W2, H2)
        ventana2.resizable(width=NO, height=NO)

        canvas2 = Canvas(ventana2, width=W2, height=H2, bg="black")
        canvas2.place(x=-1, y=0)

        settings = Label(canvas2, text="Ajustes", font=fonts + str(40), fg=fgColor, bg=bgColor)
        settings.place(x=290, y=10)

        dificultad = Label(canvas2, text="Seleccione dificultad", font=fonts + str(20), fg=fgColor, bg=bgColor)
        dificultad.place(x=230, y=420)

        facil = Button(canvas2, text="Facil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        facil.place(x=180, y=470)

        medio = Button(canvas2, text="Medio", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        medio.place(x=330, y=470)

        dificil = Button(canvas2, text="Dificil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        dificil.place(x=480, y=470)

        musica = Label(canvas2, text="Musica:", font=fonts + str(20), fg=fgColor, bg=bgColor)
        musica.place(x=500, y=120)

        musica_on = Button(canvas2, text="On", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        musica_on.place(x=630, y=115)

        musica_off = Button(canvas2, text="Off", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        musica_off.place(x=690, y=115)

        sonido = Label(canvas2, text="Sonido:", font=fonts + str(20), fg=fgColor, bg=bgColor)
        sonido.place(x=500, y=200)

        sonido_on = Button(canvas2, text="On", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        sonido_on.place(x=630, y=195)

        sonido_off = Button(canvas2, text="Off", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        sonido_off.place(x=690, y=195)

        escenario = Label(canvas2, text="Escoja escenario:", font=fonts + str(20), fg=fgColor, bg=bgColor)
        escenario.place(x=40, y=120)

        clasico = Button(canvas2, text="Clasico", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        clasico.place(x=50, y=160)

        neon = Button(canvas2, text="Neon", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        neon.place(x=50, y=210)

        futbol = Button(canvas2, text="Futbol", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        futbol.place(x=50, y=260)

        aceptar_ajustes = Button(canvas2, text="LISTO!", font=fonts + str(20), fg="black", bg="White", borderwidth=0)
        aceptar_ajustes.place(x=670, y=10)

        volver = Button(canvas2, text="VOLVER", font=fonts + str(20), fg="black", bg="White", borderwidth=0,
                        command=cerrar_ajustes)
        volver.place(x=10, y=10)

    def puntuaciones():
        def cerrar_puntuciones():
            main.deiconify()
            ventana_scores.destroy()

        main.withdraw()

        ventana_scores = Toplevel()
        ventana_scores.title("Ingreso de Jugador")

        ventana_scores.minsize(W2, H2)
        ventana_scores.resizable(width=NO, height=NO)

        canvas_scores = Canvas(ventana_scores, width=W2, height=H2, bg="black")
        canvas_scores.place(x=-1, y=0)

        label_scores = Label(canvas_scores, text="Digite nombre de jugador:", font=fonts + str(20), fg=fgColor,
                             bg=bgColor)
        label_scores.place(x=40, y=120)

        escribir_jugadores = Entry(canvas_scores, width=30)
        escribir_jugadores.place(x=200, y=300)

        def agregar_scores():
            agregar_puntuaciones = open('Scores.txt', 'a')
            agregar_puntuaciones.write = (escribir_jugadores.get())

    def mostrar_puntuaciones():
        def cerrar_mostrar_puntuciones():
            main.deiconify()
            ventana__mostrar_scores.destroy()

        main.withdraw()

        ventana__mostrar_scores = Toplevel()
        ventana__mostrar_scores.title("Puntuaciones")

        ventana__mostrar_scores.minsize(W2, H2)
        ventana__mostrar_scores.resizable(width=NO, height=NO)

        canvas_mostrar_scores = Canvas(ventana__mostrar_scores, width=W2, height=H2, bg="black")
        canvas_mostrar_scores.place(x=-1, y=0)

        label_mejores = Label(canvas_mostrar_scores, text="Mejores Puntuaciones:", font=fonts + str(20), fg=fgColor,
                              bg=bgColor)
        label_mejores.place(x=200, y=120)

        canvas_tabla = Canvas(canvas_mostrar_scores, width=W2 // 2, height=H2 // 2)
        canvas_tabla.place(x=200, y=200)

        cerrar_scores = Button(canvas_mostrar_scores, text="BACK!", font=fonts + str(20), fg="black", bg="White",
                               borderwidth=0, command=cerrar_mostrar_puntuciones)
        cerrar_scores.place(x=5, y=0)

        def separarPuntuaciones(i):
            if i == len(listaScores):
                return
            listaScores[i] = listaScores[i].replace("\n", "").split(";")
            separarPuntuaciones(i + 1)

        file = open("Scores.txt", 'r')
        listaScores = file.readlines()
        separarPuntuaciones(0)
        file.close()

        def crearTabla(x, y, columns):
            global tabla
            if x == len(listaScores):
                return ''
            elif y == 2:
                tabla += [columns]
                return crearTabla(x + 1, 0, [])
            else:
                if y == 0:
                    seccion = Entry(canvas_tabla, text='', width=3, justify=CENTER)
                    seccion.grid(row=x, column=y)
                    return crearTabla(x, y + 1, columns + [seccion])
                seccion = Entry(canvas_tabla, text='', width=30)
                seccion.grid(row=x, column=y)
                return crearTabla(x, y + 1, columns + [seccion])

        # Llena la tabla anteriormente creada
        def llenarTabla(x, y):  # funcion que llena la tabla para vendedores con el vendedores.txt
            global tabla
            if x == len(listaScores):
                return
            elif y != 2:
                print(listaScores[x][y])
                tabla[x][y].insert(0, listaScores[x][y])
                return llenarTabla(x, y + 1)
            else:
                return llenarTabla(x + 1, 0)

        crearTabla(0, 0, [])
        llenarTabla(0, 0)
        tabla = []

    mainCanvas = Canvas(main, width=W2, height=H2, bg=bgColor)
    mainCanvas.place(x=xPoss, y=yPoss)

    tittleLabel = Label(mainCanvas, image=Fondo_pong, borderwidth=0)
    tittleLabel.place(x=xPoss+5, y=yPoss-50)

    playersButton1 = Button(mainCanvas, text='1 Player', font=fonts +str(30), fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT, borderwidth=0, command=player1)
    playersButton1.place(x=xPoss + 290, y=yPoss + 250)

    playersButton2 = Button(mainCanvas, text='2 Player', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,justify=RIGHT, borderwidth=0, command=player2)
    playersButton2.place(x=xPoss + 290, y=yPoss + 310)

    playersOption = Button(mainCanvas, text='Options', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,justify=RIGHT, borderwidth=0, command=ajustes)
    playersOption.place(x=xPoss + 290, y=yPoss + 370)

    playersHightscore = Button(mainCanvas, text='Scores', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,justify=RIGHT, borderwidth=0)
    playersHightscore.place(x=xPoss + 290, y=yPoss + 430)


load_interface(0, 0, 10, 'white', 'black', 'Fixedsys ')

main.mainloop()





# Sprite Groups
sprites = py.sprite.Group()
players = py.sprite.Group()
balls = py.sprite.Group()
walls = py.sprite.Group()

# Inicia la Clase Game
game.start_game()

# Cargar fondo, sonidos y otros
back_grounds = game.load_images()[2]
sound_effects = game.get_sound_effects()
sound_effects[2].play(loops=-1)
M = game.get_matrix()
walls_images = game.load_images()[3]
walls_spawn = game.get_wall_spawn_rate()


def show_pause():
    pause = True
    while pause:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                py.quit()
            if event.type == py.KEYUP:
                pause = False
        draw_text(display, "PAUSA", (W / 2, H / 2), ("Arial", 64, white))
        draw_text(display, "Presione cualquiere tecla para continuar", (W / 2, H * 3 / 4), ("Arial", 22, white))

        py.display.update()


# Game loop
loop = True
while loop:
    clock.tick(FPS)
    for event in py.event.get():
        if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
            loop = False
        if event.type == py.KEYUP and event.key == py.K_p:
            show_pause()

    # Time
    start_time = py.time.get_ticks()//1000
    if secs == start_time:
        secs += 1

    # Colisiones paleta con bola
    hits = py.sprite.groupcollide(players, balls, False, False)
    if hits:
        sound_effects[0].play()
        if random.random() > walls_spawn:
            wall = Wall(M, walls_images)
            sprites.add(wall)
            walls.add(wall)
        for element in balls:
            element.set_xSpeed()
            for pallet in hits:
                ball_poss = element.get_ball_poss()[1]
                pallet_segment = pallet.pallet_segments()
                if pallet_segment[0] <= ball_poss < pallet_segment[1]:  # Revisa si la bola choca en la parte superior
                    element.set_ySpeed('top')
                if pallet_segment[1] <= ball_poss <= pallet_segment[2]:  # Revisa si la bola choca en la parte central
                    element.set_ySpeed('center')
                if pallet_segment[2] < ball_poss <= pallet_segment[3]:  # Revisa si la bola choca en la parte inferior
                    element.set_ySpeed('bottom')
                element.increase_xSpeed()
                pallet.increase_xSpeed()

    if py.sprite.groupcollide(balls, walls, False, True):
        sound_effects[0].play()
        for element in balls:
            element.set_xSpeed()

    # Update
    sprites.update()

    # Draw
    display.blit(back_grounds, (0, 0))
    sprites.draw(display)
    draw_text(display, str(game.get_scores()[0]), M[366], ('arial', 80, white))
    draw_text(display, str(game.get_scores()[1]), M[652], ('arial', 80, white))

    py.display.update()



py.quit()