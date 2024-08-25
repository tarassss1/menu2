import pygame
import pygame_menu
import random

pygame.init()

# Налаштування основного вікна
window_size = (800, 500)
window = pygame.display.set_mode(window_size)

# Ініціалізація змінних для фону та стін
background_image = pygame.image.load('background.png')  
background_image = pygame.transform.scale(background_image, window_size)

class Player:
    def __init__(self, x, y, width, height, image):
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.gravity = 0.5
        self.jump_power = -10
        self.vel_y = 0
        self.can_jump = False
        self.jumps = 2

    def move(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for w in walls:
            if self.rect.colliderect(w.rect):
                self.jumps = 2
                if self.vel_y > 0:
                    self.rect.bottom = w.rect.top
                    self.vel_y = 0
                    self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power
            if self.jumps <= 1:
                self.can_jump = False
            self.jumps -= 1 

    def move_horizontal(self, dx):
        self.jumps = 2
        self.rect.x += dx

class Wall:
    def __init__(self, x, y, width, height, color=(22, 26, 31)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

def start_game():
    global walls
    player = Player(100, 100, 50, 50, 'player.png')
    walls = [
        Wall(20, 100, 200, 1000),
        Wall(350, 100, 150, 400),
        Wall(100, 450, 500, 400),
    ]

    white = (255, 255, 255)
    clock = pygame.time.Clock()
    game = True
    move_left = False
    move_right = False

    pygame.mixer.music.load('background_music.wav')
    pygame.mixer.music.play(-1)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                return  # Повернення до меню

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    move_right = True
                    player.original_image = pygame.image.load("player-reverse.png")
                    player.image = pygame.transform.scale(player.original_image, (50, 50))
                if event.key == pygame.K_a:
                    move_left = True
                    player.original_image = pygame.image.load("player.png")
                    player.image = pygame.transform.scale(player.original_image, (50, 50))
                if event.key == pygame.K_w:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_a:
                    move_left = False

        window.blit(background_image, (0, 0))
        player.move()

        if move_right:
            player.move_horizontal(3)
        if move_left:
            player.move_horizontal(-3)

        for wall in walls:
            wall.draw(window)
            wall.rect.y += 1

        window.blit(player.image, (player.rect.x, player.rect.y))

        if random.randint(1,1500) % 147 == 0:
            walls.append(Wall(random.randint(0,400),0,70,10))
        if random.randint(1,1200) % 147 == 0:
            walls.append(Wall(random.randint(0,400),0,100,10))
        if random.randint(1,1500) % 147 == 0:
            walls.append(Wall(random.randint(0,400),0,70,10))
        if random.randint(1,1200) % 147 == 0:
            walls.append(Wall(random.randint(0,400),0,130,10))

        clock.tick(60)
        pygame.display.update()

    pygame.quit()
    pygame.mixer.music.stop()

def set_skin(value, skin):
    global selected_skin
    selected_skin = skin

def skin_menu():
    menu = pygame_menu.Menu('Choose Your Skin', *window_size, theme=pygame_menu.themes.THEME_DARK)
    menu.add.selector('Select Skin: ', [('Default', 'player.png'), ('Reverse', 'player-reverse.png')], onchange=set_skin)
    menu.add.button('Back', main_menu)
    menu.mainloop(window)

def main_menu():
    menu = pygame_menu.Menu('Main Menu', *window_size, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Start Game', start_game)
    menu.add.button('Choose Skin', skin_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        menu.update(events)
        menu.draw(window)
        pygame.display.update()

if __name__ == "__main__":
    main_menu()