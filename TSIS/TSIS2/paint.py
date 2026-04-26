import pygame
import math
from datetime import datetime
from collections import deque

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
    "brush",           # A
    "pencil",          # B
    "line",            # C
    "rectangle",       # D
    "circle",          # E
    "square",          # F
    "right_triangle",  # G
    "equilateral_triangle", # H
    "rhombus",         # I
    "fill",            # J
    "text",            # K
    "eraser"           # L
]

BRUSH_SIZES = {
    "small": 2,
    "medium": 5,
    "large": 10
}

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


def flood_fill(surface, pos, target_color, fill_color):
    """Flood fill algorithm using BFS"""
    if not (0 <= pos[0] < surface.get_width() and 0 <= pos[1] < surface.get_height()):
        return
    
    if target_color == fill_color:
        return
    
    queue = deque([pos])
    visited = set()
    visited.add(pos)
    
    while queue:
        x, y = queue.popleft()
        
        if not (0 <= x < surface.get_width() and 0 <= y < surface.get_height()):
            continue
        
        if surface.get_at((x, y))[:3] != target_color[:3]:
            continue
        
        surface.set_at((x, y), fill_color)
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and 0 <= nx < surface.get_width() and 0 <= ny < surface.get_height():
                visited.add((nx, ny))
                queue.append((nx, ny))


def save_canvas(surface, filename=None):
    """Save canvas with timestamp"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drawing_{timestamp}.png"
    
    pygame.image.save(surface, filename)
    return filename


# -----------------------------------
# Main program
# -----------------------------------

def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Keyboard Paint - Extended")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial",18)
    text_font = pygame.font.SysFont("Arial", 24)

    canvas = pygame.Surface((WIDTH,HEIGHT))
    canvas.fill(BLACK)

    current_tool = "brush"
    color_index = 0
    current_color = COLOR_OPTIONS[color_index][1]
    brush_size_name = "medium"
    brush_size = BRUSH_SIZES[brush_size_name]

    drawing = False
    start_pos = None
    last_pos = None
    preview_pos = None
    
    # Text tool variables
    text_mode = False
    text_pos = None
    text_input = ""

    running = True

    while running:

        screen.fill(BLACK)
        screen.blit(canvas,(0,0))

        # Draw info bar
        draw_text(screen,f"Tool: {current_tool} | Color: {COLOR_OPTIONS[color_index][0]} | Size: {brush_size_name}({brush_size}px)",10,10,font)
        draw_text(screen,"1-3:Size | A-L:Tool | 9/0:Color | Ctrl+S:Save | ESC:Quit",10,HEIGHT-25,font,YELLOW)

        # Text input display
        if text_mode:
            draw_text(screen,f"Text: {text_input}_ (ENTER to confirm, ESC to cancel)",10,HEIGHT-50,font,YELLOW)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # ALWAYS allow ESC and Ctrl+S
                if event.key == pygame.K_ESCAPE:
                    if text_mode:
                        text_mode = False
                        text_input = ""
                        text_pos = None
                    else:
                        running = False
                    continue

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = save_canvas(canvas)
                    print(f"Canvas saved as: {filename}")
                    continue

                # IF IN TEXT MODE - ONLY handle text input
                if text_mode:
                    if event.key == pygame.K_RETURN:
                        if text_input and text_pos:
                            text_surface = text_font.render(text_input, True, current_color)
                            canvas.blit(text_surface, text_pos)
                        text_mode = False
                        text_input = ""
                        text_pos = None
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    elif event.unicode.isprintable():
                        text_input += event.unicode
                    continue

                # NOT IN TEXT MODE - handle tool/brush/color changes
                # Brush sizes: 1=small, 2=medium, 3=large
                if event.key == pygame.K_1:
                    brush_size_name = "small"
                    brush_size = BRUSH_SIZES["small"]

                elif event.key == pygame.K_2:
                    brush_size_name = "medium"
                    brush_size = BRUSH_SIZES["medium"]

                elif event.key == pygame.K_3:
                    brush_size_name = "large"
                    brush_size = BRUSH_SIZES["large"]

                # Tools: A-L (12 tools total)
                elif pygame.K_a <= event.key <= pygame.K_l:
                    tool_idx = event.key - pygame.K_a
                    if tool_idx < len(TOOLS):
                        current_tool = TOOLS[tool_idx]

                # Color: 9=next, 0=previous
                elif event.key == pygame.K_9:
                    color_index = (color_index+1)%len(COLOR_OPTIONS)
                    current_color = COLOR_OPTIONS[color_index][1]

                elif event.key == pygame.K_0:
                    color_index = (color_index-1)%len(COLOR_OPTIONS)
                    current_color = COLOR_OPTIONS[color_index][1]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # Skip mouse if in text mode
                if text_mode:
                    continue

                drawing = True
                start_pos = event.pos
                preview_pos = start_pos
                last_pos = start_pos

                if current_tool == "brush":
                    pygame.draw.circle(canvas,current_color,start_pos,brush_size)

                elif current_tool == "eraser":
                    pygame.draw.circle(canvas,BLACK,start_pos,brush_size)

                elif current_tool == "fill":
                    target_color = canvas.get_at(event.pos)[:3]
                    flood_fill(canvas, event.pos, target_color, current_color)
                    drawing = False

                elif current_tool == "text":
                    text_mode = True
                    text_pos = event.pos
                    text_input = ""
                    drawing = False

            elif event.type == pygame.MOUSEMOTION and drawing:

                preview_pos = event.pos

                if current_tool == "brush":
                    draw_brush(canvas,current_color,last_pos,event.pos,brush_size)
                    last_pos = event.pos

                elif current_tool == "pencil":
                    pygame.draw.line(canvas,current_color,last_pos,event.pos,brush_size)
                    last_pos = event.pos

                elif current_tool == "eraser":
                    draw_brush(canvas,BLACK,last_pos,event.pos,brush_size)
                    last_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and drawing:

                end_pos = event.pos

                if current_tool == "line":
                    pygame.draw.line(canvas,current_color,start_pos,end_pos,brush_size)

                elif current_tool == "rectangle":
                    rect = normalize_rect(start_pos,end_pos)
                    pygame.draw.rect(canvas,current_color,rect,brush_size)

                elif current_tool == "circle":
                    rect = normalize_rect(start_pos,end_pos)
                    pygame.draw.ellipse(canvas,current_color,rect,brush_size)

                elif current_tool == "square":
                    rect = get_square_rect(start_pos,end_pos)
                    pygame.draw.rect(canvas,current_color,rect,brush_size)

                elif current_tool == "right_triangle":
                    pygame.draw.polygon(canvas,current_color,
                        get_right_triangle_points(start_pos,end_pos),brush_size)

                elif current_tool == "equilateral_triangle":
                    pygame.draw.polygon(canvas,current_color,
                        get_equilateral_triangle_points(start_pos,end_pos),brush_size)

                elif current_tool == "rhombus":
                    pygame.draw.polygon(canvas,current_color,
                        get_rhombus_points(start_pos,end_pos),brush_size)

                drawing = False

        # Live preview for shapes
        if drawing and current_tool in (
            "line",
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ) and start_pos and preview_pos:

            temp_surface = screen.copy()

            if current_tool == "line":
                pygame.draw.line(temp_surface,current_color,start_pos,preview_pos,brush_size)

            elif current_tool == "rectangle":
                rect = normalize_rect(start_pos, preview_pos)
                pygame.draw.rect(temp_surface, current_color, rect, brush_size)

            elif current_tool == "circle":
                rect = normalize_rect(start_pos, preview_pos)
                pygame.draw.ellipse(temp_surface, current_color, rect, brush_size)

            elif current_tool == "square":
                rect = get_square_rect(start_pos, preview_pos)
                pygame.draw.rect(temp_surface, current_color, rect, brush_size)

            elif current_tool == "right_triangle":
                pygame.draw.polygon(
                    temp_surface,
                    current_color,
                    get_right_triangle_points(start_pos, preview_pos),
                    brush_size
                )

            elif current_tool == "equilateral_triangle":
                pygame.draw.polygon(
                    temp_surface,
                    current_color,
                    get_equilateral_triangle_points(start_pos, preview_pos),
                    brush_size
                )

            elif current_tool == "rhombus":
                pygame.draw.polygon(
                    temp_surface,
                    current_color,
                    get_rhombus_points(start_pos, preview_pos),
                    brush_size
                )

            screen.blit(temp_surface, (0, 0))

        # Text cursor preview
        if text_mode and text_pos:
            pygame.draw.line(screen, YELLOW, text_pos, (text_pos[0], text_pos[1] + 20), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()