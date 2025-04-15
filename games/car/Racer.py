import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game with Road and Coins")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player_img = pygame.image.load("C:/Users/asylb/OneDrive/Рабочий стол/pp2/lab-8/car/assets/player_car.png")
enemy_img = pygame.image.load("C:/Users/asylb/OneDrive/Рабочий стол/pp2/lab-8/car/assets/enemy_car.png")
coin_img = pygame.image.load("C:/Users/asylb/OneDrive/Рабочий стол/pp2/lab-8/car/assets/coin.png")
road_img = pygame.image.load("C:/Users/asylb/OneDrive/Рабочий стол/pp2/lab-8/car/assets/road.png")

player_img = pygame.transform.scale(player_img, (60, 100))
enemy_img = pygame.transform.scale(enemy_img, (60, 100))
coin_img = pygame.transform.scale(coin_img, (60, 60))
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

SPEED_INCREASE_INTERVAL = 5  
SPEED_INCREASE_AMOUNT = 1   
INITIAL_ENEMY_SPEED = 6
coin_speed = 4

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 120))
        self.speed = 10

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 150:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    base_speed = INITIAL_ENEMY_SPEED  

    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(180, WIDTH - 180), -100))
        self.speed = Enemy.base_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

    @classmethod
    def increase_speed(cls):
        cls.base_speed += SPEED_INCREASE_AMOUNT

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect(center=(random.randint(180, WIDTH - 180), -30))
        self.speed = coin_speed
        self.weight = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

player = Player()
player_group = pygame.sprite.GroupSingle(player)
enemy_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

ADD_ENEMY = pygame.USEREVENT + 1
ADD_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_ENEMY, 1500)
pygame.time.set_timer(ADD_COIN, 2000)

coin_count = 0
win_score = 60
  
game_over = False
win = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:
            if event.type == ADD_ENEMY:
                enemy = Enemy()
                enemy_group.add(enemy)
                all_sprites.add(enemy)
            if event.type == ADD_COIN:
                coin = Coin()
                coin_group.add(coin)
                all_sprites.add(coin)

    if not game_over:
        keys = pygame.key.get_pressed()
        player_group.update(keys)
        enemy_group.update()
        coin_group.update()

        if pygame.sprite.spritecollideany(player, enemy_group):
            game_over = True
            win = False

        for coin in pygame.sprite.spritecollide(player, coin_group, True):
            coin_count += coin.weight  

            if coin_count % SPEED_INCREASE_INTERVAL == 0:
                Enemy.increase_speed()
                for enemy in enemy_group:
                    enemy.speed = Enemy.base_speed

            if coin_count >= win_score:
                game_over = True
                win = True

    screen.blit(road_img, (0, 0))
    all_sprites.draw(screen)

    coin_text = font.render(f"Coins: {coin_count}", True, (255, 255, 255))
    screen.blit(coin_text, (WIDTH - 150, 10))

    if game_over:
        if win:
            msg = font.render("YOU WIN!", True, (0, 255, 0))
        else:
            msg = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(msg, (WIDTH // 2 - 90, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)