import pygame
import math

COLORS = [
    (255, 50, 50),    # красный
    (50, 255, 50),    # зелёный
    (50, 50, 255),    # синий
    (255, 255, 50),   # жёлтый
    (255, 50, 255),   # магента
    (50, 255, 255),   # голубой
    (255, 150, 50),   # оранжевый
    (200, 200, 200),  # серый
]

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'brush'  # brush, eraser, color_picker
    color_idx = 2  # индекс синего
    color = COLORS[color_idx]
    drawing = False
    start_point = None
    points = []
    shapes = []  # сохраняем нарисованные фигуры
    
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
                
                # Инструменты на цифры
                if event.key == pygame.K_1:
                    mode = 'brush'
                elif event.key == pygame.K_2:
                    mode = 'eraser'
                elif event.key == pygame.K_3:
                    mode = 'color_picker'
                elif event.key == pygame.K_4:
                    mode = 'line'
                elif event.key == pygame.K_5:
                    mode = 'rectangle'
                elif event.key == pygame.K_6:
                    mode = 'circle'
                elif event.key == pygame.K_7:
                    mode = 'triangle'
                elif event.key == pygame.K_8:
                    mode = 'polygon'
                
                # Смена цветов на 9 и 0
                if event.key == pygame.K_9:
                    color_idx = (color_idx - 1) % len(COLORS)
                    color = COLORS[color_idx]
                elif event.key == pygame.K_0:
                    color_idx = (color_idx + 1) % len(COLORS)
                    color = COLORS[color_idx]
                
                # Цвета на буквы (старая система)
                if event.key == pygame.K_r:
                    color = (255, 50, 50)
                elif event.key == pygame.K_g:
                    color = (50, 255, 50)
                elif event.key == pygame.K_b:
                    color = (50, 50, 255)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левый клик - больше
                    if mode == 'brush':
                        drawing = not drawing  # toggle рисования
                    elif mode == 'eraser':
                        drawing = not drawing
                    elif mode in ['line', 'rectangle', 'circle', 'triangle', 'polygon']:
                        if not drawing:
                            start_point = event.pos
                            drawing = True
                        else:
                            # Вторый клик - рисуем фигуру
                            end_point = event.pos
                            shapes.append((mode, start_point, end_point, color, radius))
                            drawing = False
                            start_point = None
                    else:
                        radius = min(200, radius + 1)
                elif event.button == 3:  # правый клик - меньше
                    radius = max(1, radius - 1)
                elif event.button == 4:  # скролл вверх
                    radius = min(200, radius + 1)
                elif event.button == 5:  # скролл вниз
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and mode == 'brush':
                    if drawing:
                        points.append(None)  # разделитель штрихов
            
            if event.type == pygame.MOUSEMOTION:
                if drawing and mode == 'brush':
                    points.append(event.pos)
                    points = points[-256:]
                elif drawing and mode == 'eraser':
                    # Стираем в радиусе
                    points = erase_point(points, event.pos, radius * 2)
        
        # Левый клик + shift = увеличение размера
        if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
            if pressed[pygame.K_UP]:
                radius = min(200, radius + 1)
            if pressed[pygame.K_DOWN]:
                radius = max(1, radius - 1)
        
        screen.fill((0, 0, 0))
        
        # Рисуем все сохранённые фигуры
        for shape_data in shapes:
            shape_type, start, end, shape_color, shape_radius = shape_data
            draw_shape(screen, shape_type, start, end, shape_color, shape_radius)
        
        # Рисуем накопленные точки (для brush)
        i = 0
        while i < len(points) - 1:
            if points[i] is None or points[i + 1] is None:
                i += 1
                continue
            draw_line_between(screen, i, points[i], points[i + 1], radius, color)
            i += 1
        
        # Превью текущей фигуры при рисовании
        if drawing and mode in ['line', 'rectangle', 'circle', 'triangle', 'polygon']:
            mouse_pos = pygame.mouse.get_pos()
            draw_shape_preview(screen, mode, start_point, mouse_pos, color, radius)
        
        # Инфо панель
        font = pygame.font.Font(None, 24)
        mode_text = f"Mode: {mode} | Size: {radius} | Color: {color_idx + 1}/8"
        text_surf = font.render(mode_text, True, (255, 255, 255))
        screen.blit(text_surf, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

def draw_line_between(screen, index, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def draw_shape(screen, shape_type, start, end, color, radius):
    if shape_type == 'line':
        pygame.draw.line(screen, color, start, end, radius)
    elif shape_type == 'rectangle':
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        pygame.draw.rect(screen, color, rect, radius)
    elif shape_type == 'circle':
        dist = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        pygame.draw.circle(screen, color, start, int(dist), radius)
    elif shape_type == 'triangle':
        # Треугольник: start вверху, end вниз справа, третья точка влево
        p1 = start
        p2 = end
        p3 = (start[0] - (end[0] - start[0]), end[1])
        pygame.draw.polygon(screen, color, [p1, p2, p3], radius)
    elif shape_type == 'polygon':
        # Пятиугольник
        center = start
        radius_dist = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        points = []
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi / 2
            x = int(center[0] + radius_dist * math.cos(angle))
            y = int(center[1] + radius_dist * math.sin(angle))
            points.append((x, y))
        pygame.draw.polygon(screen, color, points, radius)

def draw_shape_preview(screen, shape_type, start, end, color, radius):
    if shape_type == 'line':
        pygame.draw.line(screen, color, start, end, max(1, radius // 2))
    elif shape_type == 'rectangle':
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        pygame.draw.rect(screen, color, rect, max(1, radius // 2))
    elif shape_type == 'circle':
        dist = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        pygame.draw.circle(screen, color, start, int(dist), max(1, radius // 2))
    elif shape_type == 'triangle':
        p1 = start
        p2 = end
        p3 = (start[0] - (end[0] - start[0]), end[1])
        pygame.draw.polygon(screen, color, [p1, p2, p3], max(1, radius // 2))
    elif shape_type == 'polygon':
        center = start
        radius_dist = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        points = []
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi / 2
            x = int(center[0] + radius_dist * math.cos(angle))
            y = int(center[1] + radius_dist * math.sin(angle))
            points.append((x, y))
        pygame.draw.polygon(screen, color, points, max(1, radius // 2))

def erase_point(points, pos, size):
    # Удаляем точки в радиусе
    new_points = []
    for p in points:
        if p is None:
            new_points.append(None)
            continue
        dist = math.sqrt((p[0] - pos[0])**2 + (p[1] - pos[1])**2)
        if dist > size:
            new_points.append(p)
    return new_points

main()