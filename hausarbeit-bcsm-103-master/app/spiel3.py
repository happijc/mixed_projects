from spiel1 import Game
import pygame

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class PingPongGame(Game):

    def __init__(self, __fps, **kwargs):
        # assign params
        self.fps = __fps #default 120
        self.screen_width = kwargs.get('__screen_width', 700)
        self.screen_height = kwargs.get('__screen_height', 500)
        self.size = (self.screen_width, self.screen_height)
        self.game_name = 'pingpong'
        self.lose = False


        # Schrift
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Consolas', 30)

        #Objekte
        self.sp = spieler(100)
        self.b = ball()


        self.colors = {
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'GREEN': (0, 255, 0),
            'RED': (255, 0, 0)
        }
        pass

    def initEventHandler(self):
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.sp.x - self.sp.speed > 0:
                self.sp.x = self.sp.x - self.sp.speed
        if keys[pygame.K_RIGHT]:
            if self.sp.x + self.sp.width + self.sp.speed < self.screen_width:
                self.sp.x = self.sp.x + self.sp.speed

    def draw(self, screen):
        screen.fill(self.colors.get('BLACK'))

        # Zeichnen
        if not self.lose:
            pygame.draw.rect(screen, self.colors.get('WHITE'), [self.sp.x, self.sp.y, self.sp.width, self.sp.height], 0)
            pygame.draw.circle(screen, self.colors.get('WHITE'), [self.b.x, self.b.y], self.b.radius)
            textsurface = self.myfont.render(" Punkte : " + str(self.score), False, self.colors.get('WHITE'))
            screen.blit(textsurface, (0, 0))
        else:
            pygame.draw.rect(screen, self.colors.get('RED'), [self.sp.x, self.sp.y, self.sp.width, self.sp.height], 0)
            pygame.draw.circle(screen, self.colors.get('RED'), [self.b.x, self.b.y], self.b.radius)
            textsurface = self.myfont.render(" Verloren " + str(self.score), False, self.colors.get('RED'))
            screen.blit(textsurface, (self.screen_width / 2 - 110, self.screen_height / 2 - 50))

    def run(self):
        # pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Ping Pong")

        # PYgame Loop
        while not self.done:
            #init events
            self.initEventHandler()

            # Logik
            self.b.x = self.b.x + self.b.xspeed
            self.b.y = self.b.y + self.b.yspeed
            # Collation detection
            # mit spieler
            if self.b.y + self.b.radius > self.sp.y and self.b.y + self.b.radius < self.sp.y + 5:
                if self.b.x + self.b.radius >= self.sp.x and self.b.x - self.b.radius <= self.sp.x + self.sp.width + 2:
                    self.score += 1
                    acc = self.score / 100
                    self.b.yspeed = -acc - self.b.yspeed
                    if self.b.x > self.sp.x + self.sp.width / 2:
                        self.b.xspeed = acc + abs(self.b.xspeed)
                    else:
                        self.b.xspeed = -acc - abs(self.b.xspeed)
                else:
                    self.b.xspeed = 0
                    self.b.yspeed = 0
                    self.sp.speed = 0
                    self.lose = True
                    # mit obererand
            if self.b.y - self.b.radius <= 0:
                self.b.yspeed = -self.b.yspeed
            # mit linke rand
            if self.b.x - self.b.radius <= 0:
                self.b.xspeed = - self.b.xspeed
            # mit rechte rand
            if self.b.x + self.b.radius >= self.screen_width:
                self.b.xspeed = - self.b.xspeed

            #draw
            self.draw(screen)

            # Framerates
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        return [self.game_name, self.score]

# Klassen
class spieler:
    x = 0
    height = 10
    y = 470
    width = 70
    speed = 1

    def __init__(self, x):
        self.x = x


class ball:
    x = 150
    y = 200
    radius = 5
    xspeed = -1
    yspeed = 1
    #speed = 5