import pygame
import random

CELL = 20
FPS = 6
LEVEL_UP_SCORE = 5
FOODS=[
    {"color":(200,0,0),"value":1,"life":5000},
    {"color":(255,165,0),"value":2,"life":4000},
    {"color":(255,255,0),"value":3,"life":2500},
]
WHITE = (255,255,255)
GRAY = (210,210,210)
GREEN = (0,200,0)
RED = (200,0,0)
DARK = (40,40,40)
LEVELS = 1

class Wall:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self,screen):
        pygame.draw.rect(screen,DARK,(self.x*CELL,self.y*CELL,CELL,CELL))

class Food:
    def __init__(self,x,y,value,lifetime,color):
        self.x=x
        self.y=y
        self.value=value
        self.lifetime=lifetime
        self.spawn_time=pygame.time.get_ticks()
        self.color=color

    def expired(self):
        return pygame.time.get_ticks()-self.spawn_time > self.lifetime

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,
        (self.x*CELL,self.y*CELL,CELL,CELL))

class Snake:
    def __init__(self,x,y):
        self.body=[(x,y),(x-1,y),(x-2,y)]
        self.direction=(1,0)

    def next_head(self):
        x,y=self.body[0]
        dx,dy=self.direction
        return (x+dx,y+dy)

    def move(self,food):
        new_head=self.next_head()
        self.body.insert(0,new_head)
        if (food.x,food.y)==new_head:
            return True
        else:
            self.body.pop()
            return False

    def draw(self,screen):
        for part in self.body:
            pygame.draw.rect(screen,GREEN,(part[0]*CELL,part[1]*CELL,CELL,CELL))


class Level:
    def __init__(self,filename):
        self.walls=[]
        with open(filename) as f:
            y=0
            for line in f:
                x=0
                for char in line.strip():
                    if char=="#":
                        self.walls.append(Wall(x,y))
                    x+=1
                y+=1
        self.width=x
        self.height=y

def draw_ui(screen, score,level):
    text1 = font.render(f"{score}", True, (0,0,0))
    text2 = font.render(f"{level}", True, (0,0,0))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (30, 10))

def draw_background(screen,w,h):
    for y in range(h):
        for x in range(w):
            color=WHITE if (x+y)%2==0 else GRAY
            pygame.draw.rect(screen,color,(x*CELL,y*CELL,CELL,CELL))


def spawn_food(level,snake):
    while True:
        x=random.randint(1,level.width-2)
        y=random.randint(1,level.height-2)

        if (x,y) not in snake.body and all((w.x,w.y)!=(x,y) for w in level.walls):

            f=random.choice(FOODS)

            return Food(x,y,f["value"],f["life"],f["color"])


def collision(next_head,snake,walls):
    if next_head in snake.body:
        return True
    for w in walls:
        if (w.x,w.y)==next_head:
            return True
    return False


def input_control(snake):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            return False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w and snake.direction!=(0,1):
                snake.direction=(0,-1)
            if event.key==pygame.K_s and snake.direction!=(0,-1):
                snake.direction=(0,1)
            if event.key==pygame.K_a and snake.direction!=(1,0):
                snake.direction=(-1,0)
            if event.key==pygame.K_d and snake.direction!=(-1,0):
                snake.direction=(1,0)
    return True


pygame.init()
font = pygame.font.SysFont("Arial", 24)
levels=["level1.txt","level2.txt"]
level_index=0
score=0

level=Level(levels[level_index])

WIDTH=level.width*CELL
HEIGHT=level.height*CELL

screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()

snake=Snake(level.width//2,level.height//2)
food=spawn_food(level,snake)

running=True

while running:

    running=input_control(snake)

    next_head=snake.next_head()

    if collision(next_head,snake,level.walls):
        running=False

    ate = snake.move(food)

    if ate:
        score += food.value
        food = spawn_food(level,snake)

    if food.expired():
        food = spawn_food(level,snake)
    
    if score>=LEVEL_UP_SCORE:
        LEVELS+=1
        FPS+=2
        score=0
        level_index=(level_index+1)%len(levels)
        level=Level(levels[level_index])
        snake=Snake(level.width//2,level.height//2)
        food=spawn_food(level,snake)

    draw_background(screen,level.width,level.height)

    for w in level.walls:
        w.draw(screen)

    food.draw(screen)
    snake.draw(screen)
    draw_ui(screen, score,LEVELS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()