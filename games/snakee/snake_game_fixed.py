import pygame
import random
import os
import sys
import math
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FOOD_SIZE = BLOCK_SIZE * 2  
HEAD_SIZE = BLOCK_SIZE * 2
FOOD_LIFETIME = 10 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
game_over_font = pygame.font.SysFont(None, 48)

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GRAY = (64, 64, 64) 
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

FOOD_TYPES = [
    {"weight": 1, "color": RED, "points": 1}, 
    {"weight": 0.3, "color": BLUE, "points": 3},
    {"weight": 0.1, "color": YELLOW, "points": 5} 
]

ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets")

try:
    food_img = pygame.image.load(os.path.join(ASSET_PATH, "food.png"))
    snake_head_img = pygame.image.load(os.path.join(ASSET_PATH, "snake_head.png"))
    obstacle_img = pygame.image.load(os.path.join(ASSET_PATH, "obstacle.png"))
    
    food_img = pygame.transform.scale(food_img, (FOOD_SIZE, FOOD_SIZE)) 
    snake_head_img = pygame.transform.scale(snake_head_img, (HEAD_SIZE, HEAD_SIZE))
    obstacle_img = pygame.transform.scale(obstacle_img, (BLOCK_SIZE, BLOCK_SIZE))
    
    pygame.mixer.music.load(os.path.join(ASSET_PATH, "snake_music.wav"))
    pygame.mixer.music.play(-1)
except (pygame.error, FileNotFoundError) as e:
    print(f"Қате: Суреттер немесе музыка файлдары табылмады: {e}")
    print("Пожалуйста, assets папкасындағы файлдардың бар екенін тексеріңіз")
    sys.exit(1)

obstacles = []
for x in range(100, 500, BLOCK_SIZE):
    obstacles.append((x, 100))

for x in range(100, 500, BLOCK_SIZE):
    obstacles.append((x, 300))

obstacles.extend([(300, 200), (320, 200), (340, 200)])

def draw_snake(snake):
    
    for i, pos in enumerate(snake):
        if i == 0:  
            if len(snake) > 1:
                next_pos = snake[1]
                angle = math.degrees(math.atan2(next_pos[1] - pos[1], next_pos[0] - pos[0]))
                rotated_head = pygame.transform.rotate(snake_head_img, angle)
                head_rect = rotated_head.get_rect(center=(pos[0] + HEAD_SIZE//2, pos[1] + HEAD_SIZE//2))
                screen.blit(rotated_head, head_rect.topleft)
            else:
                screen.blit(snake_head_img, pos)
        else:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_obstacles():
    
    for obs in obstacles:
        shadow_rect = pygame.Rect(obs[0] + 2, obs[1] + 2, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect)
        obs_rect = pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE)
        screen.blit(obstacle_img, obs_rect)
        pygame.draw.rect(screen, BLACK, obs_rect, 2)

def generate_food(snake):
    
    while True:
        x = random.randint(0, (WIDTH - FOOD_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - FOOD_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_rect = pygame.Rect(x, y, FOOD_SIZE, FOOD_SIZE)
        
        snake_rects = [pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE) for pos in snake]
        obstacle_rects = [pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE) for obs in obstacles]
        
        if not any(food_rect.colliderect(snake_rect) for snake_rect in snake_rects) and \
           not any(food_rect.colliderect(obs_rect) for obs_rect in obstacle_rects):
            total_weight = sum(food["weight"] for food in FOOD_TYPES)
            rand = random.uniform(0, total_weight)
            current_weight = 0
            for food_type in FOOD_TYPES:
                current_weight += food_type["weight"]
                if rand <= current_weight:
                    return {
                        "position": (x, y),
                        "type": food_type,
                        "spawn_time": time.time()
                    }
            return {
                "position": (x, y),
                "type": FOOD_TYPES[0],  
                "spawn_time": time.time()
            }

def draw_food(food):
    current_time = time.time()
    time_left = max(0, FOOD_LIFETIME - (current_time - food["spawn_time"]))
    
    pygame.draw.rect(screen, food["type"]["color"], 
                    (*food["position"], FOOD_SIZE, FOOD_SIZE))
    
    if time_left < 3:  
        if int(time_left * 2) % 2 == 0:
            pygame.draw.rect(screen, WHITE, 
                           (*food["position"], FOOD_SIZE, FOOD_SIZE), 2)

def display_score_level(score, level):
    text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))

def show_game_over(score, level):
    game_over_text = game_over_font.render("Ойын бітті!", True, RED)
    score_text = font.render(f"Ұпай: {score}  Деңгей: {level}", True, BLACK)
    restart_text = font.render("Қайта бастау үшін SPACE басыңыз", True, BLACK)
    quit_text = font.render("Шығу үшін ESC басыңыз", True, BLACK)
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 80))
    pygame.display.flip()

def check_collision(head, food):
    head_rect = pygame.Rect(head[0], head[1], HEAD_SIZE, HEAD_SIZE)
    food_rect = pygame.Rect(food["position"][0], food["position"][1], FOOD_SIZE, FOOD_SIZE)
    return head_rect.colliderect(food_rect)

def check_boundary_collision(head):
    return (head[0] < 0 or 
            head[0] > WIDTH - BLOCK_SIZE or 
            head[1] < 0 or 
            head[1] > HEIGHT - BLOCK_SIZE)

def check_obstacle_collision(head, obstacles):
    head_rect = pygame.Rect(head[0], head[1], HEAD_SIZE, HEAD_SIZE)
    for obs in obstacles:
        obs_rect = pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE)
        if head_rect.colliderect(obs_rect):
            return True
    return False

def check_self_collision(head, snake):
    return head in snake[1:]

def is_valid_start_position(pos, obstacles):
    start_rect = pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)
    for obs in obstacles:
        obs_rect = pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE)
        if start_rect.colliderect(obs_rect):
            return False
    return True

def get_safe_start_position(obstacles):
    margin = BLOCK_SIZE * 2
    attempts = 0
    while attempts < 100: 
        x = random.randint(margin, WIDTH - margin)
        y = random.randint(margin, HEIGHT - margin)
        pos = (x - x % BLOCK_SIZE, y - y % BLOCK_SIZE)  
        if is_valid_start_position(pos, obstacles):
            return pos
        attempts += 1
    return (BLOCK_SIZE * 3, HEIGHT // 2)

def main():
    while True:  
        start_pos = get_safe_start_position(obstacles)
        running = True
        snake = [start_pos]
        dx, dy = BLOCK_SIZE, 0
        food = generate_food(snake)
        score = 0
        level = 1
        speed = 10

        while running:
            clock.tick(speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            new_dx, new_dy = dx, dy
            if keys[pygame.K_LEFT] and dx == 0:
                new_dx, new_dy = -BLOCK_SIZE, 0
            elif keys[pygame.K_RIGHT] and dx == 0:
                new_dx, new_dy = BLOCK_SIZE, 0
            elif keys[pygame.K_UP] and dy == 0:
                new_dx, new_dy = 0, -BLOCK_SIZE
            elif keys[pygame.K_DOWN] and dy == 0:
                new_dx, new_dy = 0, BLOCK_SIZE

            next_head = (snake[0][0] + new_dx, snake[0][1] + new_dy)
            if not (check_boundary_collision(next_head) or 
                   check_obstacle_collision(next_head, obstacles) or 
                   next_head in snake[1:]):
                dx, dy = new_dx, new_dy
                head = next_head
            else:
                head = (snake[0][0] + dx, snake[0][1] + dy)

            if (check_boundary_collision(head) or 
                check_obstacle_collision(head, obstacles) or 
                head in snake[1:]):
                running = False
                continue

            snake.insert(0, head)

            current_time = time.time()
            if current_time - food["spawn_time"] > FOOD_LIFETIME:
                food = generate_food(snake)

            if check_collision(head, food):
                score += food["type"]["points"]
                food = generate_food(snake)
                if score % 3 == 0:
                    level += 1
                    speed += 2
            else:
                snake.pop()

            screen.fill(WHITE)
            draw_snake(snake)
            draw_obstacles()
            draw_food(food)
            display_score_level(score, level)
            pygame.display.flip()

        show_game_over(score, level)
        waiting_for_key = True
        
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_key = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
