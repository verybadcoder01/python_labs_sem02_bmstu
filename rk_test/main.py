import pygame
import math

pygame.init()
width, height = 1500, 1300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Это вертоооолет")
clock = pygame.time.Clock()

center_x = width // 2
center_y = height // 2
amplitude = 100
frequency = 0.02
phase = 0
speed = 0.05

helic_radius = 20
helic_leg_length = 10
helic_ski_length = 20
helic_prop_mount = 10
helic_prop_length = 60
helic_prop_phase = 0
helic_prop_speed = 10
helic_moving_speed = 1
HELIC_COLOR = (255, 0, 0)


def cas_angle_in_point(x):
    return math.atan(math.cos(x))


def draw_sine_wave(phase_offset):
    points = []
    for x in range(width):
        y = center_y + amplitude * math.sin(frequency * x + phase_offset)
        points.append((x, y))
    pygame.draw.lines(screen, (0, 0, 255), False, points, 2)


def rotate_prop():
    helic_prop_phase_rad = math.radians(helic_prop_phase)
    return [
        [
            [helic_prop_length / 2 * math.cos(helic_prop_phase_rad),
             helic_prop_length / 2 * math.sin(helic_prop_phase_rad)],
            [-helic_prop_length / 2 * math.cos(helic_prop_phase_rad),
             -helic_prop_length / 2 * math.sin(helic_prop_phase_rad)]
        ],
        [
            [helic_prop_length / 2 * math.sin(helic_prop_phase_rad),
             -helic_prop_length / 2 * math.cos(helic_prop_phase_rad)],
            [-helic_prop_length / 2 * math.sin(helic_prop_phase_rad),
             helic_prop_length / 2 * math.cos(helic_prop_phase_rad)]
        ]
    ]


def draw_helicopter(center_point):
    cas_angle = cas_angle_in_point(center_point[0])
    pygame.draw.circle(screen, HELIC_COLOR, center_point, helic_radius, 2)
    leg_bottom = (center_point[0], center_point[1] + helic_radius + helic_leg_length)
    pygame.draw.line(screen, HELIC_COLOR, center_point, leg_bottom, 2)
    pygame.draw.line(screen, HELIC_COLOR,
                     (leg_bottom[0] - helic_ski_length, leg_bottom[1]),
                     (leg_bottom[0] + helic_ski_length, leg_bottom[1]), 2)
    prop_mount_top = (center_point[0], center_point[1] - helic_radius - helic_prop_mount)
    pygame.draw.line(screen, HELIC_COLOR, center_point, prop_mount_top, 2)
    prop = rotate_prop()
    for blade in prop:
        adjusted_blade = [
            (point[0] + prop_mount_top[0], point[1] + prop_mount_top[1])
            for point in blade
        ]
        pygame.draw.line(screen, HELIC_COLOR, adjusted_blade[0], adjusted_blade[1], 2)


running = True
x_pos = 0
base_y = center_y - helic_radius - helic_leg_length
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    phase += speed
    helic_prop_phase = (helic_prop_phase + helic_prop_speed) % 360
    x_pos += helic_moving_speed
    y_pos = base_y + amplitude * math.sin(frequency * x_pos + phase)
    draw_helicopter((x_pos, y_pos))
    draw_sine_wave(phase)
    draw_helicopter([x_pos, y_pos])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
