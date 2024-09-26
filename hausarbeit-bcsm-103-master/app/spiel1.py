import pygame
import random

class Game:
    screen_width = 0
    screen_height = 0
    fps = 0
    clock = 0
    score = 0
    done = False
    game_name = None

    def initEventHandler(self):
        pass

    def draw(self, screen):
        pass

    def run(self):
        pass

class SnakeGame(Game):

    screen_width = 0
    screen_height = 0
    grid_height = 25
    grid_width = 25
    zoom = 15
    snake = None
    apple = None
    colors = []
    grid = []
    offset_left = 0
    offset_top = 0

    def __init__(self, __fps, **kwargs):
        #assign params
        self.fps = __fps
        self.screen_width = kwargs.get('__screen_width', 500)
        self.screen_height = kwargs.get('__screen_height', 500)
        self.game_name = 'snake'

        #define offset to center grid
        self.offset_left = ((self.screen_width - self.grid_width * self.zoom) / 2)
        self.offset_top = ((self.screen_height - self.grid_height * self.zoom) / 2)

        #set snake centered at first
        self.snake = Snake(self.grid_width / 2, self.grid_height / 2)
        #create start apple
        self.apple = Apple(self.grid_width, self.grid_height, self.snake.size)
        #set colors for game objects
        self.colors = {
            'lightGreen': (190, 252, 3),
            'darkGreen': (6, 207, 43),
            'darkRed': (240, 61, 41),
            'white': (255, 255, 255)
        }
        #init coordinate field
        self.grid = []
        for i in range(self.grid_height):
            line = []
            for j in range(self.grid_width):
                line.append(0)
            self.grid.append(line)


    def initEventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.snake.down()

                if event.key == pygame.K_DOWN:
                    self.snake.up()

                if event.key == pygame.K_RIGHT:
                    self.snake.right()

                if event.key == pygame.K_LEFT:
                    self.snake.left()
                pass
            if event.type == pygame.QUIT:
                self.done = True


    def draw(self, screen):

        screen.fill(color=self.colors.get('white'))

        #draw grid
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                pygame.draw.rect(screen, self.colors.get('lightGreen'), [self.calcXCoord(i), self.calcYCoord(j), 1*self.zoom, 1*self.zoom])

        #draw score
        font = pygame.font.SysFont("monospace", 16)
        scoretext = font.render("Score = " + str(self.score), 1, (0, 0, 0))
        screen.blit(scoretext, (5, 10))

        #draw snake
        for field in self.snake.size:
            pygame.draw.rect(screen, self.colors.get('darkGreen'),
                             [self.calcXCoord(field[0]), self.calcYCoord(field[1]), 1 * self.zoom, 1 * self.zoom])

        # draw apple
        pygame.draw.rect(screen, self.colors.get('darkRed'),
                         [self.calcXCoord(self.apple.size[0]), self.calcYCoord(self.apple.size[1]), 1 * self.zoom,
                          1 * self.zoom])

        #move snake
        self.snake.move()

        #check if eat an apple
        if(self.snake.eatApple(self.apple.x_coord, self.apple.y_coord)):
            self.score += self.apple.points
            self.apple = Apple(self.grid_width, self.grid_height, self.snake.size)

        #check intersection
        if(self.snake.collide(self.grid_width, self.grid_height) == True):
            self.done = True


    def calcYCoord(self, __coord):
        return __coord * self.zoom + self.offset_top

    def calcXCoord(self, __coord):
        return __coord * self.zoom + self.offset_left

    def run(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        while not self.done:
            screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
            pygame.display.set_caption('Snake')
            #init event handler
            self.initEventHandler()

            #draw screen
            self.draw(screen)

            # check difficulty level
            if (self.score > 150 and self.score < 250):
                # difficulty level hard as calcit
                self.fps = 15
            elif (self.score > 250 and self.score < 400):
                # difficulty level hard as fluorit
                self.fps = 20
            elif (self.score > 400 and self.score < 500):
                # difficulty level hard as quarz
                self.fps = 25
            elif (self.score > 500 and self.score < 600):
                # difficulty level hard as topas
                self.fps = 30
            elif (self.score > 600):
                # difficulty level hard as a diamond
                self.fps = 45

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        return [self.game_name, self.score]

class Snake:
    x_coord = 0
    y_coord = 0
    size = []
    direction = None

    def __init__(self, __x_coord, __y_coord):
        self.x_coord = __x_coord
        self.y_coord = __y_coord
        self.size = []
        #0 = x, 1 = y
        self.size.append([self.x_coord, self.y_coord])
        self.direction = 'up'

    def collide(self, __grid_width, __grid_height):
        #check grid collision
        x_coord = self.size[0][0]
        y_coord = self.size[0][1]
        #minimal and maximal grid positions
        if(x_coord <= -1 or y_coord <= -1 or x_coord >= __grid_width or y_coord >= __grid_height):
            return True

        #check snake collision | skip first iteration
        for element in self.size[1:]:
            if(self.size[0][0] == element[0] and self.size[0][1] == element[1]):
                return True

        return False

    def eatApple(self, __apple_x_coord, __apple_y_coord):
        #if first element of snake x = x apple and snake y = y apple
        if(self.size[0][0] == __apple_x_coord and self.size[0][1] == __apple_y_coord):
            if (self.direction == 'up'):
                self.size.append([self.size[0][0], self.size[0][1] - 1])
            if (self.direction == 'down'):
                self.size.append([self.size[0][0], self.size[0][1] + 1])
            if (self.direction == 'right'):
                self.size.append([self.size[0][0] - 1, self.size[0][1]])
            if (self.direction == 'left'):
                self.size.append([self.size[0][0] + 1, self.size[0][1]])
            return True
        return False


    def up(self):
        if self.direction == 'down':
            return
        self.direction = 'up'

    def down(self):
        if self.direction == 'up':
            return
        self.direction = 'down'

    def left(self):
        if self.direction == 'right':
            return
        self.direction = 'left'

    def right(self):
        if self.direction == 'left':
            return
        self.direction = 'right'

    def move(self):
        more_than_one_bodyparts = False
        if(len(self.size) > 1):
            more_than_one_bodyparts = True
            list_element = [self.size[0][0], self.size[0][1]]
        else:
            list_element = self.size[0]

        if(self.direction == 'up'):
            list_element[1] += 1
        if (self.direction == 'down'):
            list_element[1] -= 1
        if (self.direction == 'right'):
            list_element[0] += 1
        if (self.direction == 'left'):
            list_element[0] -= 1

        if(more_than_one_bodyparts == True):
            self.size.pop()
            self.size.insert(0, list_element)

class Apple:
    x_coord = 0
    y_coord = 0
    size = []
    points = 50

    def __init__(self, __grid_width, __grid_height, __snake_size):
        self.x_coord = random.randint(1, __grid_width - 1)
        self.y_coord = random.randint(1, __grid_width - 1)

        #prevent apple spawning in body of snake
        correctCoordinates = True
        while correctCoordinates:
            if(self.checkCoordinates(__grid_width, __grid_height, __snake_size) == True):
                correctCoordinates = False

        self.size = [self.x_coord, self.y_coord]

    def checkCoordinates(self, __grid_width, __grid_height, __snake_size):
        for elem in __snake_size:
            if (self.x_coord == elem[0] and self.y_coord == elem[1]):
                self.x_coord = random.randint(1, __grid_width - 1)
                self.y_coord = random.randint(1, __grid_width - 1)
                self.checkCoordinates(__grid_width, __grid_height, __snake_size)
        return True