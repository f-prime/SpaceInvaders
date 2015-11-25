import pygame
from pygame.locals import *
import sys
import random

class SpaceInvaders:
    def __init__(self):
        self.score = 0
        self.lives = 2
        pygame.font.init()
        self.font = pygame.font.Font("assets/space_invaders.ttf", 15)
        barrierDesign = [[],[0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
                         [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                         [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                         [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                         [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
                         [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
                         [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
                         [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
                         [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1]]

        self.screen = pygame.display.set_mode((800, 600))
        self.enemySprites = {
                0:[pygame.image.load("assets/a1_0.png").convert(), pygame.image.load("assets/a1_1.png").convert()],
                1:[pygame.image.load("assets/a2_0.png").convert(), pygame.image.load("assets/a2_1.png").convert()],
                2:[pygame.image.load("assets/a3_0.png").convert(), pygame.image.load("assets/a3_1.png").convert()],
                }
        self.player = pygame.image.load("assets/shooter.png").convert()
        self.animationOn = 0
        self.direction = 1
        self.enemySpeed = 20
        self.lastEnemyMove = 0
        self.playerX = 400
        self.playerY = 550
        self.bullet = None
        self.bullets = []
        self.enemies = []
        self.barrierParticles = []
        startY = 50
        startX = 50
        for rows in range(6):
            out = []
            if rows < 2:
                enemy = 0
            elif rows < 4:
                enemy = 1
            else:
                enemy = 2
            for columns in range(10):
                out.append((enemy,pygame.Rect(startX * columns, startY * rows, 35, 35)))
            self.enemies.append(out)
        self.chance = 990

        barrierX = 50
        barrierY = 400
        space = 100

        for offset in range(1, 5):
            for b in barrierDesign:
                for b in b:
                    if b != 0:
                        self.barrierParticles.append(pygame.Rect(barrierX + space * offset, barrierY, 5,5))
                    barrierX += 5
                barrierX = 50 * offset
                barrierY += 3
            barrierY = 400

    def enemyUpdate(self):
        if not self.lastEnemyMove:
            for enemy in self.enemies:
                for enemy in enemy:
                    enemy = enemy[1]
                    if enemy.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())):
                        self.lives -= 1
                        self.resetPlayer()
                    enemy.x += self.enemySpeed * self.direction
                    self.lastEnemyMove = 25
                    if enemy.x >= 750 or enemy.x <= 0:
                        self.moveEnemiesDown()
                        self.direction *= -1
                    
                    chance = random.randint(0, 1000)
                    if chance > self.chance:
                        self.bullets.append(pygame.Rect(enemy.x, enemy.y, 5, 10))
                        self.score += 5
            if self.animationOn:
                self.animationOn -= 1                                                                                                                                                        
            else:
                self.animationOn += 1
        else:
            self.lastEnemyMove -= 1
    
        
    def moveEnemiesDown(self):
        for enemy in self.enemies:
            for enemy in enemy:
                enemy = enemy[1]
                enemy.y += 20

    def playerUpdate(self):
        key = pygame.key.get_pressed()
        if key[K_RIGHT] and self.playerX < 800 - self.player.get_width():
            self.playerX += 5
        elif key[K_LEFT] and self.playerX > 0:
            self.playerX -= 5
        if key[K_SPACE] and not self.bullet:
            self.bullet = pygame.Rect(self.playerX + self.player.get_width() / 2- 2, self.playerY - 15, 5, 10)

    def bulletUpdate(self):
        for i, enemy in enumerate(self.enemies):
            for j, enemy in enumerate(enemy):
                enemy = enemy[1]
                if self.bullet and enemy.colliderect(self.bullet):
                    self.enemies[i].pop(j)
                    self.bullet = None
                    self.chance -= 1
                    self.score += 100
                
        if self.bullet:
            self.bullet.y -= 20
            if self.bullet.y < 0:
                self.bullet = None


        for x in self.bullets:
            x.y += 20
            if x.y > 600:
                self.bullets.remove(x)
            if x.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())):
                self.lives -= 1
                self.bullets.remove(x)
                self.resetPlayer()

        for b in self.barrierParticles:
            check = b.collidelist(self.bullets)
            if check != -1:
                self.barrierParticles.remove(b)
                self.bullets.pop(check)
                self.score += 10
            elif self.bullet and b.colliderect(self.bullet):
                self.barrierParticles.remove(b)
                self.bullet = None
                self.score += 10
    def resetPlayer(self):
        self.playerX = 400

    def run(self):
        clock = pygame.time.Clock()
        for x in range(3):
            self.moveEnemiesDown()
        while True:
            
            clock.tick(60)
            self.screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            for enemy in self.enemies:
                for enemy in enemy:
                    self.screen.blit(pygame.transform.scale(self.enemySprites[enemy[0]][self.animationOn], (35,35)), (enemy[1].x, enemy[1].y))
            self.screen.blit(self.player, (self.playerX, self.playerY))
            if self.bullet:
                pygame.draw.rect(self.screen, (52, 255, 0), self.bullet)
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, (255,255,255), bullet)
            for b in self.barrierParticles:
                pygame.draw.rect(self.screen, (52, 255, 0), b)
            
            if not self.enemies:
                self.screen.blit(pygame.font.Font("assets/space_invaders.ttf", 100).render("You Win!", -1, (52,255,0)), (100, 200))
            elif self.lives > 0:
                self.bulletUpdate()
                self.enemyUpdate()
                self.playerUpdate()
            elif self.lives == 0:
                self.screen.blit(pygame.font.Font("assets/space_invaders.ttf", 100).render("You Lose!", -1, (52,255,0)), (100, 200))
            self.screen.blit(self.font.render("Lives: {}".format(self.lives), -1, (255,255,255)), (20, 10))
            self.screen.blit(self.font.render("Score: {}".format(self.score), -1, (255,255,255)), (400, 10))
            pygame.display.flip()


if __name__ == "__main__":
    SpaceInvaders().run()
