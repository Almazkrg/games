import pygame
import sys
import math


pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing App")
clock = pygame.time.Clock()

drawing = False
last_pos = None
current_color = BLACK
current_tool = "pen"  
start_pos = None


colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
color_rects = []
for i, color in enumerate(colors):
    color_rects.append(pygame.Rect(10 + i * 40, 10, 30, 30))

tools = ["pen", "rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus", "eraser"]
tool_rects = []
for i, tool in enumerate(tools):
    tool_rects.append(pygame.Rect(10 + i * 100, 50, 80, 30))

drawing_surface = pygame.Surface((WIDTH, HEIGHT))
drawing_surface.fill(WHITE)

def draw_tool_buttons():
    for i, tool in enumerate(tools):
        color = (200, 200, 200) if current_tool == tool else (150, 150, 150)
        pygame.draw.rect(screen, color, tool_rects[i])
        font = pygame.font.SysFont(None, 24)
        display_name = tool.replace("_", " ").title()
        if len(display_name) > 8:
            display_name = display_name[:8] + "..."
        text = font.render(display_name, True, BLACK)
        screen.blit(text, (tool_rects[i].x + 5, tool_rects[i].y + 5))

def draw_color_palette():
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, color_rects[i])
        if color == current_color:
            pygame.draw.rect(screen, WHITE, color_rects[i], 2)

def draw_square(surface, start, end, color):
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])
    size = min(width, height)
    rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), size, size)
    pygame.draw.rect(surface, color, rect, 2)

def draw_right_triangle(surface, start, end, color):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surface, color, points, 2)

def draw_equilateral_triangle(surface, start, end, color):
    width = abs(end[0] - start[0])
    height = width * math.sqrt(3) / 2
    points = [
        start,
        end,
        ((start[0] + end[0]) // 2, min(start[1], end[1]) - height)
    ]
    pygame.draw.polygon(surface, color, points, 2)

def draw_rhombus(surface, start, end, color):
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])
    points = [
        (center_x, start[1]),
        (end[0], center_y),
        (center_x, end[1]),
        (start[0], center_y)
    ]
    pygame.draw.polygon(surface, color, points, 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            for i, rect in enumerate(color_rects):
                if rect.collidepoint(pos):
                    current_color = colors[i]
            
            for i, rect in enumerate(tool_rects):
                if rect.collidepoint(pos):
                    current_tool = tools[i]
            
            if pos[1] > 90: 
                drawing = True
                start_pos = pos
                last_pos = pos
        
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            if current_tool in ["rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"] and start_pos:
                end_pos = pygame.mouse.get_pos()
                if current_tool == "rectangle":
                    rect = pygame.Rect(min(start_pos[0], end_pos[0]), 
                                     min(start_pos[1], end_pos[1]),
                                     abs(end_pos[0] - start_pos[0]),
                                     abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(drawing_surface, current_color, rect, 2)
                elif current_tool == "circle":
                    center = ((start_pos[0] + end_pos[0]) // 2,
                             (start_pos[1] + end_pos[1]) // 2)
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + 
                                (end_pos[1] - start_pos[1]) ** 2) ** 0.5 / 2)
                    pygame.draw.circle(drawing_surface, current_color, center, radius, 2)
                elif current_tool == "square":
                    draw_square(drawing_surface, start_pos, end_pos, current_color)
                elif current_tool == "right_triangle":
                    draw_right_triangle(drawing_surface, start_pos, end_pos, current_color)
                elif current_tool == "equilateral_triangle":
                    draw_equilateral_triangle(drawing_surface, start_pos, end_pos, current_color)
                elif current_tool == "rhombus":
                    draw_rhombus(drawing_surface, start_pos, end_pos, current_color)
        
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = pygame.mouse.get_pos()
            if current_tool == "pen":
                if last_pos:
                    pygame.draw.line(drawing_surface, current_color, last_pos, current_pos, 2)
                last_pos = current_pos
            elif current_tool == "eraser":
                if last_pos:
                    pygame.draw.line(drawing_surface, WHITE, last_pos, current_pos, 20)
                last_pos = current_pos
    
    screen.fill(WHITE)
    screen.blit(drawing_surface, (0, 0))
    
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, 90))
    draw_color_palette()
    draw_tool_buttons()
    
    if drawing and current_tool in ["rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"] and start_pos:
        current_pos = pygame.mouse.get_pos()
        if current_tool == "rectangle":
            rect = pygame.Rect(min(start_pos[0], current_pos[0]), 
                             min(start_pos[1], current_pos[1]),
                             abs(current_pos[0] - start_pos[0]),
                             abs(current_pos[1] - start_pos[1]))
            pygame.draw.rect(screen, current_color, rect, 2)
        elif current_tool == "circle":
            center = ((start_pos[0] + current_pos[0]) // 2,
                     (start_pos[1] + current_pos[1]) // 2)
            radius = int(((current_pos[0] - start_pos[0]) ** 2 + 
                         (current_pos[1] - start_pos[1]) ** 2) ** 0.5 / 2)
            pygame.draw.circle(screen, current_color, center, radius, 2)
        elif current_tool == "square":
            draw_square(screen, start_pos, current_pos, current_color)
        elif current_tool == "right_triangle":
            draw_right_triangle(screen, start_pos, current_pos, current_color)
        elif current_tool == "equilateral_triangle":
            draw_equilateral_triangle(screen, start_pos, current_pos, current_color)
        elif current_tool == "rhombus":
            draw_rhombus(screen, start_pos, current_pos, current_color)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 