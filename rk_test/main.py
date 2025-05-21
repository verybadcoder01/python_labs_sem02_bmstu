import pygame
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Вращающиеся спирали")
clock = pygame.time.Clock()

a = 96
k = 0.08
distance = 250

angular_speed = 0.02
center1 = (width // 2 - distance // 2, height // 2)
center2 = (width // 2 + distance // 2, height // 2)

phase_shift = math.pi * 2 + angular_speed * 25

def draw_spiral(surface, color, center, angle, reverse=False):
    points = []
    for phi in range(-300, 300, 1):
        phi_rad = phi / 50.0
        exp_term = a * math.exp(k * phi_rad)
        x = exp_term * math.cos(phi_rad + angle)
        y = exp_term * math.sin(phi_rad + angle)
        if reverse:
            x, y = -x, -y
        points.append((x + center[0], y + center[1]))
    points.append(center)
    if points:
        pygame.draw.polygon(surface, color, points, 2)


running = True
theta = 0.0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    theta += angular_speed
    angle1 = theta
    angle2 = -theta + phase_shift

    # Отрисовка спиралей
    draw_spiral(screen, (0, 0, 255), center1, angle1)
    draw_spiral(screen, (255, 0, 0), center2, angle2, reverse=True)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()