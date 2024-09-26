from spiel1 import Game
import pygame
import random



# Define colors tetris figures
figure_colors = [
    (0, 0, 0),
    (0, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
]


class TetrisFigure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # random tetris figure
        self.type = random.randint(0, len(self.figures) - 1)

        # Define different colors for different figues
        if self.type == 0 or self.type == 3 or self.type == 6:
            self.color = 1
        elif self.type == 1 or self.type == 4:
            self.color = 2
        elif self.type == 2 or self.type == 5:
            self.color = 3

        self.rotation = 0

    # returns tetris figure
    def image(self):
        return self.figures[self.type][self.rotation]

    # rotation of tetris figure
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

class Tetris(Game):
    # start with level 1
    level = 1
    # level up every 20 points
    level_up_at = 15
    last_level_up = 0
    count_lines = 0
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.size = (400, 500)
        self.screen = pygame.display.set_mode(self.size)
        self.game_name = "tetris"

        self.figure_colors = [
            (0, 0, 0),
            (0, 255, 255),
            (255, 0, 0),
            (0, 255, 0),
        ]

        self.colors = {
            # Define colors for background
            'BLACK':  (0, 0, 0),
            'WHITE': (255, 255, 255),
            'GRAY': (128, 128, 128)
        }

        pygame.display.set_caption("Tetris")
        pygame.font.init()

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = 25
        self.tetris = self
        self.counter = 0
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.level = 1
        self.last_level_up = 0
        self.count_lines = 0

        # possible states: "start", "break" and "gameover"
        self.state = "start"

        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.font_small = pygame.font.SysFont('Calibri', 15, True, False)
        self.font_tall = pygame.font.SysFont('Calibri', 65, True, False)
        self.text_game_over = self.font_tall.render("Game Over", True, (0, 0, 255))
        self.text_press_esc = self.font.render("Press ESC to start again", True, (0, 0, 0))
        self.text_break = self.font_tall.render("Break", True, (0, 0, 255))
        self.text_press_return = self.font.render("Press ENTER to Continue", True, (0, 0, 0))

        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    # create new tetris figure at x = 3 and y = 0
    def new_tetris_figure(self):
        self.figure = TetrisFigure(3, 0)

    # check if tetris figure intersects while moving left, right, down or rotating
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    # finished lines
    def break_lines(self):
        lines = 0

        # check for full horizontal lines
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            # destroy lines from bottom to top if full
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]

        # points = finished lines^2
        self.score += lines ** 2
        self.count_lines += lines
        self.level_up()

    # one level up for 15 full lines
    def level_up(self):
        if self.score > 0 and self.count_lines >= self.last_level_up + self.level_up_at:
            self.level += 1
            self.last_level_up += self.level_up_at

    # freeze tetris figure directly at the bottom
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    # move down
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    # freeze tetris figure
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_tetris_figure()

        # check for game over
        if self.intersects():
            self.state = "gameover"

    # go to left or right
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    # rotating
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    # run game
    def run(self):
        pygame.init()
        while not self.done:
            if self.tetris.figure is None:
                self.tetris.new_tetris_figure()
            self.counter += 1
            if self.counter > 100000:
                self.counter = 0

            if self.counter % (self.fps // self.tetris.level // 2) == 0:
                if self.tetris.state == "start":
                    self.tetris.go_down()

            # initialize event handling
            self.initEventhandler()
            self.screen.fill(self.colors.get('WHITE'))

            # draw on screen
            self.draw(self.screen)

            # show changes
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
        return [self.game_name, self.score]

    def draw(self, screen):
        for i in range(self.tetris.height):
            for j in range(self.tetris.width):
                pygame.draw.rect(screen, self.colors.get('GRAY'),
                                 [self.tetris.x + self.tetris.zoom * j, self.tetris.y + self.tetris.zoom * i,
                                  self.tetris.zoom, self.tetris.zoom], 1)
                if self.tetris.field[i][j] > 0:
                    pygame.draw.rect(screen, self.figure_colors[self.tetris.field[i][j]],
                                     [self.tetris.x + self.tetris.zoom * j + 1,
                                      self.tetris.y + self.tetris.zoom * i + 1,
                                      self.tetris.zoom - 2,
                                      self.tetris.zoom - 1])

        if self.tetris.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.tetris.figure.image():
                        pygame.draw.rect(screen, self.figure_colors[self.tetris.figure.color],
                                         [self.tetris.x + self.tetris.zoom * (j + self.tetris.figure.x) + 1,
                                          self.tetris.y + self.tetris.zoom * (i + self.tetris.figure.y) + 1,
                                          self.tetris.zoom - 2, self.tetris.zoom - 2])

        # gui
        text_score = self.font.render("Score: " + str(self.tetris.score), True, self.colors.get('BLACK'))
        text_level = self.font.render("Level: " + str(self.tetris.level), True, self.colors.get('BLACK'))
        text_help_esc = self.font_small.render("Break: press enter", True, self.colors.get('BLACK'))
        text_help_return = self.font_small.render("Game over: press esc", True, self.colors.get('BLACK'))
        screen.blit(text_score, [0, 0])
        screen.blit(text_level, [0, 25])
        screen.blit(text_help_esc, [10, 470])
        screen.blit(text_help_return, [230, 470])

        # check for new state
        if self.tetris.state == "gameover":
            self.done = True
        if self.tetris.state == "break":
            screen.blit(self.text_break, [110, 200])
            screen.blit(self.text_press_return, [50, 265])


    def initEventhandler(self):
        key_delay = 300
        key_internal = 50
        pygame.key.set_repeat(key_delay, key_internal)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.tetris.rotate()
                if event.key == pygame.K_DOWN:
                    self.go_down()
                if event.key == pygame.K_LEFT:
                    self.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    self.go_side(1)
                if event.key == pygame.K_SPACE:
                    self.tetris.go_space()
                if event.key == pygame.K_RETURN:
                    if self.state == "start":
                        self.state = "break"
                    else:
                        if self.state != "gameover":
                            self.state = "start"
                if event.key == pygame.K_ESCAPE:
                    if self.tetris.state == "gameover":
                        self.tetris.__init__(20, 10)
                        self.screen.fill(self.colors.get('WHITE'))
                        self.figure = None
                    else:
                        self.state = "gameover"
