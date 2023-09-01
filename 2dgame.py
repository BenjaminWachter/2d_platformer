import pygame

debug_flag = True


def Game():
    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()
    jumping = 0

    pygame.display.set_caption("2D Platformer Game")

    player = Player(100, 100)
    platforms = [
        Platform(0, screen_height - 40, screen_width, 40),
        Platform(screen_width/2 - 50, screen_height*3/4, 100, 20),
        Platform(150, screen_height*2/3, 100, 20),
        Platform(screen_width - 250, screen_height*2/3, 100, 20),
    ]

    player_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()

    player_group.add(player)
    for platform in platforms:
        platform_group.add(platform)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player.rect.x += 5
        if keys[pygame.K_UP]:
            player.rect.y -= 5
            jumping += 1
        else:
            jumping = 0
        if keys[pygame.K_DOWN]:
            player.rect.y += 5

        gravity(player, screen_height, jumping)
        collision(player_group, platform_group)

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
            print("Jumping",jumping)

        platform_group.draw(screen)
        player_group.draw(screen)

        clock.tick(60)
        pygame.display.update()
    pygame.quit()


def gravity(player,screen_height,jumping):
    g = 1
    f = g+((1/3*screen_height)/3300)*jumping
    player.rect.y = player.rect.y+f


def collision(player_group, platform_group):
    for player in player_group:
        for platform in platform_group:
            if player.rect.y+player.image.get_height() - platform.rect.y > 0 and\
                    player.rect.y - platform.rect.y + platform.image.get_height() < 0 and\
                    player.rect.x+player.image.get_width() > platform.rect.x and\
                    player.rect.x < platform.rect.x + platform.image.get_width():
                player.rect.y = platform.rect.y-player.image.get_height()


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


if __name__ == "__main__":
    Game()
