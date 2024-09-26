from app.spiel1 import SnakeGame
from app.spiel3 import PingPongGame
from app.spiel2 import Tetris
import json
import pygame


class GameHelper:

    def __init__(self):
        self.__sortedValues = []

    def saveScore(self, score):
        scoreDictBoilerPlate = {
            'snake': {

            },
            'tetris': {

            },
            'pingpong': {

            }
        }
        f = open('./app/scores', 'r')
        savedScores = f.read()
        # scores are empty
        if (savedScores == ''):
            # save first score into boilerplate
            scoreDictBoilerPlate[score[0]][0] = score[1]
            self.writeScoresToFile(scoreDictBoilerPlate)
            return
        else:
            # scores are not empty
            savedScores = json.loads(savedScores)
            # check length
            if (len(savedScores[score[0]]) == 0):
                savedScores[score[0]][0] = score[1]
                self.writeScoresToFile(savedScores)
                return
            else:
                # save score in game dict
                savedScores[score[0]][len(savedScores[score[0]])] = score[1]
                self.writeScoresToFile(savedScores)

    def writeScoresToFile(self, scores):
        f = open('./app/scores', 'w')
        f.write(json.dumps(scores))
        f.close()

    @staticmethod
    def takeSecond(item):
        return item[1]

    def getSortedScores(self):
        f = open('./app/scores', 'r')
        savedScoresData = f.read()
        returnDict = {}

        if (savedScoresData != ''):
            #load with json lib
            savedScoresDict = json.loads(savedScoresData)
            for game in savedScoresDict:
                #convert to list to use native sort functions
                savedScoresList = savedScoresDict[game].items()
                savedScoresList.sort(key=GameHelper.takeSecond, reverse=True)

                topGameScores = []
                #get top 3 entries
                i = 0
                for savedScore in savedScoresList:
                    if i >= 3:
                        break
                    topGameScores.append(savedScore[1])
                    i += 1


                returnDict[game] = topGameScores
            return returnDict
        return {}


def initGameMenuScreen():

    gameHelper = GameHelper()

    pygame.init()

    homeScreen = pygame.display.set_mode((400, 500))
    test_font = pygame.font.SysFont('Consolas', 50)
    surface = pygame.Surface((400, 500))
    clock = pygame.time.Clock()
    # background = pygame.image.load('digital-art-fantasy-art-Godzilla-King-Kong-Godzilla-Vs-Kong-ramen-2039311-wallhere.com.jpg')

    # ______________________________________________________
    jeu1 = test_font.render('Snake', False, 'white')
    jeu1_rect = jeu1.get_rect(center=(190, 240))

    # ______________________________________________________
    jeu2 = test_font.render('Tetris', False, ('White'))
    jeu2_rect = jeu2.get_rect(center=(190, 340))

    # ______________________________________________________
    jeu3 = test_font.render('Ping Pong', False, ('white'))
    jeu3_rect = jeu3.get_rect(center=(190, 420))

    surface.fill('grey')
    myText = test_font.render('Gruppe_5.1:  Isabel F.  Martin G.  Nadim A.  Jean H.', False, 'blue')
    myText_pos = 100

    gameStarted = False
    run = True

    while run:
        # mon ecran et mon arriere plan
        homeScreen.blit(surface, (0, 0))
        pygame.draw.rect(surface, 'white', jeu1_rect, 1)
        pygame.draw.rect(surface, 'black', jeu2_rect, 1)
        pygame.draw.rect(surface, 'black', jeu3_rect, 1)
        homeScreen.blit(jeu1, jeu1_rect)
        homeScreen.blit(jeu2, jeu2_rect)
        homeScreen.blit(jeu3, jeu3_rect)

        # _______________________________________________________
        mouse_press = pygame.mouse.get_pressed()

        if mouse_press[0]:
            mouse_pos = pygame.mouse.get_pos()
            if jeu1_rect.collidepoint(mouse_pos):
                if gameStarted == False:
                    print('execute game 1')
                    gameStarted = True
                    # Snake
                    game = SnakeGame(5, __screen_width=500, __screen_height=500)  #
                    score = game.run()
                    gameHelper.saveScore(score)
                    gameStarted = False
            elif jeu2_rect.collidepoint(mouse_pos):
                if gameStarted == False:
                    print('execute game 2')
                    gameStarted = True
                    # Tetris
                    game = te = Tetris(20, 10)
                    score = game.run()
                    gameHelper.saveScore(score)
                    gameStarted = False
            elif jeu3_rect.collidepoint(mouse_pos):
                if gameStarted == False:
                    print('execute game 3')
                    gameStarted = True
                    # Ping Pong
                    game = PingPongGame(120, __screen_width=700, __screen_height=500)
                    score = game.run()
                    gameHelper.saveScore(score)
                    gameStarted = False
            else:
                None

        try:
            # _______________________________________________________
            # homeScreen.blit(background,(-150,-100))

            # defilement de mon texte
            myText_pos -= 1
            if myText_pos < -700:
                myText_pos = 400
            homeScreen.blit(myText, (myText_pos, 30))

            # Block pour le choix du jeu
            # pygame.draw.rect(homeScreen, 'green', [90, 220, 200, 60], 1)
            # pygame.draw.rect(homeScreen, 'red', [90, 300, 200, 60], 1)
            # pygame.draw.rect(homeScreen, 'yellow', [90, 380, 200, 60], 1)

            pygame.display.update()
            clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # if event.type == pygame.pygame.Rect.collidepoint(x, y):
                # if jeu1_rect.collidepoint(event.pos):print('action')
        except pygame.error:
            #catch pygame error, that pygame session dont exists anymore and create new pygame session
            initGameMenuScreen()

initGameMenuScreen()