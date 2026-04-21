import pygame
import math

# -----------------------------------
# Settings
# -----------------------------------
WIDTH, HEIGHT = 900, 650
INFO_HEIGHT = 40

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,180,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (160,32,240)
ORANGE = (255,140,0)

COLOR_OPTIONS = [
    ("WHITE", (255,255,255)),
    ("RED", (255,0,0)),
    ("GREEN", (0,180,0)),
    ("BLUE", (0,0,255)),
    ("YELLOW", (255,255,0)),
    ("PURPLE", (160,32,240)),
    ("ORANGE", (255,140,0))
]

TOOLS = [
    "brush",
    "rectangle",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
    "eraser"
]

# -----------------------------------
# Helper functions
# -----------------------------------

def draw_text(screen,text,x,y,font,color=WHITE):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))


def normalize_rect(start_pos,end_pos):
    x1,y1 = start_pos
    x2,y2 = end_pos

    left = min(x1,x2)
    top = min(y1,y2)
    width = abs(x1-x2)
    height = abs(y1-y2)

    return pygame.Rect(left,top,width,height)


def get_square_rect(start_pos,end_pos):
    x1,y1 = start_pos
    x2,y2 = end_pos

    side = min(abs(x2-x1),abs(y2-y1))

    left = x1 if x2>=x1 else x1-side
    top = y1 if y2>=y1 else y1-side

    return pygame.Rect(left,top,side,side)


def get_right_triangle_points(start_pos,end_pos):
    x1,y1 = start_pos
    x2,y2 = end_pos
    return [(x1,y1),(x1,y2),(x2,y2)]


def get_equilateral_triangle_points(start_pos,end_pos):

    x1,y1 = start_pos
    x2,y2 = end_pos

    side = abs(x2-x1)
    if side == 0:
        side = 1

    height = (math.sqrt(3)/2)*side

    if x2>=x1:
        left_x = x1
        right_x = x1+side
    else:
        left_x = x1-side
        right_x = x1

    mid_x = (left_x+right_x)/2

    if y2>=y1:
        apex_y = y1+height
        base_y = y1
    else:
        apex_y = y1-height
        base_y = y1

    return [
        (left_x,base_y),
        (right_x,base_y),
        (mid_x,apex_y)
    ]


def get_rhombus_points(start_pos,end_pos):

    x1,y1 = start_pos
    x2,y2 = end_pos

    center_x = (x1+x2)/2
    center_y = (y1+y2)/2

    left = min(x1,x2)
    right = max(x1,x2)
    top = min(y1,y2)
    bottom = max(y1,y2)

    return [
        (center_x,top),
        (right,center_y),
        (center_x,bottom),
        (left,center_y)
    ]


def draw_brush(surface,color,start,end,radius):

    dx = end[0]-start[0]
    dy = end[1]-start[1]

    steps = max(abs(dx),abs(dy))

    if steps == 0:
        pygame.draw.circle(surface,color,start,radius)
        return

    for i in range(steps+1):

        x = int(start[0]+dx*i/steps)
        y = int(start[1]+dy*i/steps)

        pygame.draw.circle(surface,color,(x,y),radius)


# -----------------------------------
# Main program
# -----------------------------------

def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Keyboard Paint")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial",18)

    canvas = pygame.Surface((WIDTH,HEIGHT))
    canvas.fill(BLACK)

    current_tool = "brush"
    color_index = 0
    current_color = COLOR_OPTIONS[color_index][1]
    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None
    preview_pos = None

    running = True

    while running:

        screen.fill(BLACK)
        screen.blit(canvas,(0,0))

        draw_text(screen,f"Tool: {current_tool}",10,10,font)
        draw_text(screen,f"Color: {COLOR_OPTIONS[color_index][0]}",180,10,font)
        draw_text(screen,f"Size: {brush_size}",350,10,font)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                if pygame.K_1 <= event.key <= pygame.K_8:
                    current_tool = TOOLS[event.key - pygame.K_1]

                elif event.key == pygame.K_9:
                    color_index = (color_index+1)%len(COLOR_OPTIONS)
                    current_color = COLOR_OPTIONS[color_index][1]

                elif event.key == pygame.K_0:
                    color_index = (color_index-1)%len(COLOR_OPTIONS)
                    current_color = COLOR_OPTIONS[color_index][1]

                elif event.key in (pygame.K_PLUS,pygame.K_EQUALS,pygame.K_KP_PLUS):
                    brush_size = min(50,brush_size+1)

                elif event.key in (pygame.K_MINUS,pygame.K_KP_MINUS):
                    brush_size = max(1,brush_size-1)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                drawing = True
                start_pos = event.pos
                preview_pos = start_pos
                last_pos = start_pos

                if current_tool == "brush":
                    pygame.draw.circle(canvas,current_color,start_pos,brush_size)

                elif current_tool == "eraser":
                    pygame.draw.circle(canvas,BLACK,start_pos,brush_size)

            elif event.type == pygame.MOUSEMOTION and drawing:

                preview_pos = event.pos

                if current_tool == "brush":
                    draw_brush(canvas,current_color,last_pos,event.pos,brush_size)
                    last_pos = event.pos

                elif current_tool == "eraser":
                    draw_brush(canvas,BLACK,last_pos,event.pos,brush_size)
                    last_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and drawing:

                end_pos = event.pos

                if current_tool == "rectangle":
                    rect = normalize_rect(start_pos,end_pos)
                    pygame.draw.rect(canvas,current_color,rect,2)

                elif current_tool == "circle":
                    rect = normalize_rect(start_pos,end_pos)
                    pygame.draw.ellipse(canvas,current_color,rect,2)

                elif current_tool == "square":
                    rect = get_square_rect(start_pos,end_pos)
                    pygame.draw.rect(canvas,current_color,rect,2)

                elif current_tool == "right_triangle":
                    pygame.draw.polygon(canvas,current_color,
                        get_right_triangle_points(start_pos,end_pos),2)

                elif current_tool == "equilateral_triangle":
                    pygame.draw.polygon(canvas,current_color,
                        get_equilateral_triangle_points(start_pos,end_pos),2)

                elif current_tool == "rhombus":
                    pygame.draw.polygon(canvas,current_color,
                        get_rhombus_points(start_pos,end_pos),2)

                drawing = False

        # PREVIEW SHAPES - вне цикла событий, но внутри основного цикла
        if drawing and current_tool in (
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ) and start_pos and preview_pos:

            temp_surface = screen.copy()

            if current_tool == "rectangle":
                rect = normalize_rect(start_pos, preview_pos)
                pygame.draw.rect(temp_surface, current_color, rect, 2)

            elif current_tool == "circle":
                rect = normalize_rect(start_pos, preview_pos)
                pygame.draw.ellipse(temp_surface, current_color, rect, 2)

            elif current_tool == "square":
                rect = get_square_rect(start_pos, preview_pos)
                pygame.draw.rect(temp_surface, current_color, rect, 2)

            elif current_tool == "right_triangle":
                pygame.draw.polygon(
                    temp_surface,
                    current_color,
                    get_right_triangle_points(start_pos, preview_pos),
                    2
                )

            elif current_tool == "equilateral_triangle":
                pygame.draw.polygon(
                    temp_surface,
                    current_color,
                    get_equilateral_triangle_points(start_pos, preview_pos),
                    2
                )

            elif current_tool == "rhombus":
                pygame.draw.polygon(
                    temp_surface,
                    current_color,
                    get_rhombus_points(start_pos, preview_pos),
                    2
                )

            screen.blit(temp_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()