import pygame
import random

width = 800
height = 600

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.prev_rect = self.rect.copy()
        self.rect.center = (width // 2, height // 2)
        self.speed = 5  # 플레이어 이동 속도
        self.dx = 0
        self.dy = 0

    def update(self):
        self.prev_rect = self.rect.copy()  # 현재 위치를 이전 위치로 저장
        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy
        if 0 <= new_x <= width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= height - self.rect.height:
            self.rect.y = new_y

    def check_collision(self, sprite):
        return pygame.sprite.collide_rect(self, sprite)

    def whatisthis(self, target):
        return f"Name: {target.name}, ID: {target.id}, Mine Time: {target.mine_time}"

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.block_info = None  # 마우스가 위치한 블록 정보

    def update(self, pos):
        self.rect.center = pos
    
    def checkblock(self):
        for block in block_sprites:
            if self.rect.colliderect(block.rect):
                self.block_info = block  # 마우스가 위치한 블록 정보 갱신
                return
        # 블록 위에 마우스가 없는 경우 블록 정보 초기화
        self.block_info = None

def show_info(text, x, y):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, green)
    text_rect = text_surface.get_rect(center=(x, y))
    pygame.draw.rect(screen, black, (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
    screen.blit(text_surface, text_rect)

class Block(pygame.sprite.Sprite):
    def __init__(self, image_path, name, id, mine_time):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()  # 이미지 불러오기
        self.image.set_colorkey(white)  # 흰색을 투명으로 설정
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.name = name
        self.id = id
        self.mine_time = mine_time
        self.elapsed_time = 0  # 경과 시간

    def update(self):
        self.elapsed_time += 1  # 경과 시간 업데이트
        if self.elapsed_time >= self.mine_time * 60:  # mine_time을 초로 환산하여 비교
            self.kill()  # 블록 제거

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Game")

# 블럭 이미지 파일 경로
block_image_paths = ["./python/블럭깨기/block1.png", "./python/블럭깨기/block2.png", "./python/블럭깨기/block3.png"]

# 블럭 스프라이트 그룹
block_sprites = pygame.sprite.Group()
block1 = Block(block_image_paths[0], "몰라",  1, 3)
block2 = Block(block_image_paths[1], "asdf",  2, 54)
block3 = Block(block_image_paths[2], "tsetsaet",  3, 34)
block_sprites.add(block1)
block_sprites.add(block2)
block_sprites.add(block3)

blocks = [
    {
        "name": "몰라",
        "id": 1,
        "mine_time": 3
    },
    {
        "name": "asdf",
        "id": 2,
        "mine_time": 54
    },
    {
        "name": "tsetsaet",
        "id": 3,
        "mine_time": 34
    }
]

# 플레이어 생성
player = Player()

# 마우스 생성
mouse = Mouse()

# 게임 루프
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.dy -= player.speed
            elif event.key == pygame.K_DOWN:
                player.dy += player.speed
            elif event.key == pygame.K_LEFT:
                player.dx -= player.speed
            elif event.key == pygame.K_RIGHT:
                player.dx += player.speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.dy += player.speed
            elif event.key == pygame.K_DOWN:
                player.dy -= player.speed
            elif event.key == pygame.K_LEFT:
                player.dx += player.speed
            elif event.key == pygame.K_RIGHT:
                player.dx -= player.speed
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트 처리
            if event.button == 3:  # 마우스 우클릭인 경우
                mouse.checkblock()
            if event.button == 1:  # 마우스 좌클릭인 경우
                for block in block_sprites:
                    if player.check_collision(block):
                        # 플레이어가 블록과 충돌하면 경과 시간 초기화
                        block.elapsed_time = 0

    # 플레이어 업데이트
    player.update()
    
    for block in block_sprites:
        if player.check_collision(block):
            # 충돌이 감지되면 플레이어의 위치를 이전 위치로 되돌림
            player.rect = player.prev_rect
    
    # 마우스 업데이트
    mouse_pos = pygame.mouse.get_pos()
    mouse.update(mouse_pos)
    
    # 마우스가 블록 위에 있는 경우에만 정보 표시
    if mouse.block_info:
        info_text = player.whatisthis(mouse.block_info)
        show_info(info_text, mouse.rect.centerx, mouse.rect.centery + 30)
    
    # 스프라이트 그룹 그리기
    block_sprites.draw(screen)
    screen.blit(player.image, player.rect)
    screen.blit(mouse.image, mouse.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
