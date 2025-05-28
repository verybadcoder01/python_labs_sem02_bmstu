import sys, pygame

pygame.init()
size = width, height = 1250, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

ball = pygame.image.load("ball.png")
bg_game = pygame.image.load("bg_game.jpg")
car = pygame.image.load("car_left1.png")
flag_pole = pygame.image.load("flag_pole.png")
trap_before = pygame.image.load("trap_before.png")
trap_after = pygame.image.load("trap_after.png")

walk_left = [pygame.image.load("car_left1.png"), pygame.image.load("car_left2.png")]
walk_right = [pygame.image.load("car_right1.png"), pygame.image.load("car_right2.png")]


FPS = 100
counter_pos = 0
x_car = width // 2
y_car = height // 2 + 80
base_y = y_car
x_ball = 100
y_ball = 100
min_x = -4
max_x = width - 285
flag = False
scene = 0
vels = [[-3, 0], [5, 0], [6, y_car]]
jmps_cnt = 0
stop = False
x_scene_2 = 0

screen.blit(bg_game, (0, 0))
screen.blit(ball, (x_ball, y_ball))
screen.blit(walk_right[0], (x_car, y_car))
pygame.display.update()

def func_parabola(x):
    return 0.005 * (x - 200) ** 2 - 200 + base_y

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if stop:
        screen.blit(flag_pole, (x_car - 110, y_car - 70))
        screen.blit(walk_right[counter_pos // 8], (x_car, y_car))
        pygame.display.update()
        continue
    if counter_pos + 1 >= 15:
        counter_pos = 0
    if y_ball != 550:
        if x_car + 100 < x_ball < x_car + 200 and y_ball == y_car:
            flag = True
            scene = 1
        if not flag:
            x_ball += 1
            y_ball += 2
        else:
            x_ball = x_car + 35
            y_ball = y_car + 7
        screen.blit(ball, (x_ball, y_ball))
    vel_x = vels[scene][0]
    vel_y = vels[scene][1]
    walk_type = walk_right
    if scene == 0:
        if x_car <= min_x:
            x_car = max_x
        walk_type = walk_left
    elif scene == 1:
        if x_car >= max_x:
            x_car = min_x
            jmps_cnt += 1
            if jmps_cnt == 1:
                scene = 2
    elif scene == 2:
        if x_car > 150:
            screen.blit(trap_after, (150, base_y + 60))
            next_y_car = func_parabola(x_scene_2)
            vel_y = next_y_car - y_car
            if abs(next_y_car - base_y) < 5 and x_scene_2 > 100:
                scene = 1
            x_scene_2 += vel_x
        else:
            screen.blit(trap_before, (150, base_y + 60))
            vel_x = 7
            vel_y = 0
    x_car += vel_x
    y_car += vel_y
    screen.blit(walk_type[counter_pos // 8], (x_car, y_car))
    counter_pos += 1
    if jmps_cnt == 3:
        if abs(x_car - width // 2) <= 10:
            stop = True

    pygame.display.update()
    screen.blit(bg_game, (0, 0))
