import pygame

debug_flag = True


def Game():
    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()
    jumping = 0

    pygame.display.set_caption("2D Platformer Game")


    green_button = Button()
    player = Player(100, screen_height-110)
    player.image.fill((255,255,255))
    platforms = [
        Platform(0, screen_height - 40, screen_width, 40),
        Platform(screen_width/2 - 50, screen_height*3/4, 100, 20),
        Platform(150, screen_height*2/3, 100, 20),
        Platform(screen_width - 250, screen_height*2/3, 100, 20),
    ]
    test_platforms = [
        Platform(0, screen_height - 40, 6400, 20),
        Platform(screen_width-50, screen_height*2/3, 100, 20)        
    ]
    # enemies = [
    #     Enemy((0, 0), (0, 20), (20, 0)),
    #     Enemy((100, 100), (100, 60), (60, 100))
    # ]


    player_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    # enemies_group = pygame.sprite.Group()

    player_group.add(player)
    for platform in platforms:
        platform_group.add(platform)
    # for iter in range(24):
    #     platform_group.add(Platform(screen_width + iter*screen_height*1/3, screen_height*2/3, 100, 20))
    # for enemy in enemies:
    #     enemies_group.add(enemy)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        # pygame.draw.polygon(Platform, (255,0,0), ((0,0), (0, 10), (10, 0)))

        y1 = player.rect.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player.rect.x += 5
        if keys[pygame.K_UP] and delta_y <= 0:
            player.rect.y -= 10
            jumping += 1
        elif keys[pygame.K_DOWN]:
            player.rect.y += 5
            jumping = 0
        else:
            jumping = 0

        gravity(player, screen_height, jumping)
        collision(player_group, platform_group)

        # Boundry checking
        if player.rect.x < 0:
            player.rect.x = 0
        if player.rect.x > screen_width-player.image.get_size()[0]:
            player.rect.x = screen_width-player.image.get_size()[0]
        if player.rect.y < 0:
            player.rect.y = 0
        if player.rect.y > screen_height-player.image.get_size()[1]:
            player.rect.y = screen_height-player.image.get_size()[1]

        if debug_flag:
            print("x =", player.rect.x, "y =", player.rect.y)
            print("Jumping", jumping)

        platform_group.draw(screen)
        player_group.draw(screen)
        # enemies_group(screen)
        
        # game_scrolling(platform_group)
        # game_scrolling(player_group)

        clock.tick(60)
        pygame.display.update()
        y2 = player.rect.y
        delta_y = y2-y1

    pygame.quit()


def gravity(player, screen_height, jumping):
    g = 5
    C1 = -(1/3*screen_height)/33000
    C2 = (1/3*screen_height)/60000
    
    f = g+C1*jumping+C2*jumping**2
    
    player.rect.y = player.rect.y+f


def collision(player_group, platform_group):
    for player in player_group:
        for platform in platform_group:
            platform_boundry_x = platform.rect.x < player.rect.x + player.image.get_width() and player.rect.x < platform.rect.x + platform.image.get_width()
            platform_boundry_y_high = player.rect.y + player.image.get_height() - platform.rect.y > 0 and player.rect.y - platform.rect.y + platform.image.get_height() < 0
            
            
            if platform_boundry_y_high and platform_boundry_x:
                player.rect.y = platform.rect.y - player.image.get_height()

def game_scrolling(group):
    for object in group:
        object.rect.x -= 2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, heigth):
        super().__init__()
        self.image = pygame.Surface((width, heigth))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# class Enemy(pygame.sprite.Sprite):
#     def __inti__(self, A, B, C):
#         super().__init__()
#         # self.image = pygame.draw.polygon(pygame.sprite.Sprite, (255,0,0), ((0,0), (0, 10), (10, 0)))
#         self.image = pygame.Surface((25, 25))
#         self.image.fill((255, 0, 0))
#         self.poly = self.image.get_rect()
#         self.poly.A = A
#         self.poly.B = B
#         self.poly.C = C
        



if __name__ == "__main__":
    Game()
