import pygame
import random

width = 800
height = 800

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

    def update(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        if 0 <= new_x <= width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= height - self.rect.height:
            self.rect.y = new_y

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

    def update(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("게임 화면")

player = Player()
apple = Apple()
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.update(0, -5)
    if keys[pygame.K_DOWN]:
        player.update(0, 5)
    if keys[pygame.K_LEFT]:
        player.update(-5, 0)
    if keys[pygame.K_RIGHT]:
        player.update(5, 0)
    if keys[pygame.K_ESCAPE]:
        running = False

    # 충돌 검사
    if player.rect.colliderect(apple.rect):
        apple.update()

    screen.blit(player.image, player.rect)
    screen.blit(apple.image, apple.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
