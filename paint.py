import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    points = []
    start_position = None  # Start position for shapes
    drawing_mode = 'free'  # 'square', 'right_triangle', 'equilateral_triangle', 'rhombus', or 'free'
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                # Set the color mode
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # Set the drawing mode
                if event.key == pygame.K_1:
                    drawing_mode = 'square'
                elif event.key == pygame.K_2:
                    drawing_mode = 'right_triangle'
                elif event.key == pygame.K_3:
                    drawing_mode = 'equilateral_triangle'
                elif event.key == pygame.K_4:
                    drawing_mode = 'rhombus'
                elif event.key == pygame.K_5:
                    drawing_mode = 'free'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click grows radius
                    if drawing_mode == 'free':
                        radius = min(200, radius + 1)
                    else:
                        start_position = event.pos
                elif event.button == 3: # right click shrinks radius
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if drawing_mode == 'free':
                    points = points + [position]
                    points = points[-256:]

        screen.fill((0, 0, 0))
        
        if drawing_mode != 'free' and start_position:
            if drawing_mode == 'square':
                draw_square(screen, (255, 0, 0), start_position, 50)
            elif drawing_mode == 'right_triangle':
                draw_right_triangle(screen, (0, 255, 0), start_position, 50)
            elif drawing_mode == 'equilateral_triangle':
                draw_equilateral_triangle(screen, (0, 0, 255), start_position, 50)
            elif drawing_mode == 'rhombus':
                draw_rhombus(screen, (255, 255, 0), start_position, 50)
        else:
            i = 0
            while i < len(points) - 1:
                draw_line_between(screen, i, points[i], points[i + 1], radius, mode)
                i += 1

        pygame.display.flip()
        clock.tick(60)

def draw_line_between(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    color = (0, 0, 0)
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations + 1):
        progress = i / iterations
        x = int(start[0] + dx * progress)
        y = int(start[1] + dy * progress)
        pygame.draw.circle(screen, color, (x, y), width)

def draw_square(screen, color, top_left, side_length):
    pygame.draw.rect(screen, color, (top_left[0], top_left[1], side_length, side_length))

def draw_right_triangle(screen, color, top_left, size):
    pygame.draw.polygon(screen, color, [
        top_left,
        (top_left[0], top_left[1] + size),
        (top_left[0] + size, top_left[1] + size)
    ])

def draw_equilateral_triangle(screen, color, top, size):
    height = size * (3 ** 0.5) / 2
    pygame.draw.polygon(screen, color, [
        top,
        (top[0] - size // 2, top[1] + int(height)),
        (top[0] + size // 2, top[1] + int(height))
    ])

def draw_rhombus(screen, color, center, size):
    pygame.draw.polygon(screen, color, [
        (center[0], center[1] - size),
        (center[0] - size // 2, center[1]),
        (center[0], center[1] + size),
        (center[0] + size // 2, center[1])
    ])

if __name__ == '__main__':
    main()
