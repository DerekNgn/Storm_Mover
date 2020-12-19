import pygame
from pygame import image
from settings import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.isCarrying = False
        self.gotHit = False
        self.image = pygame.Surface((30, 30))
        self.readySpritesheet = SpriteSheet('src/images/ready.png')
        self.carryingSpritesheet = SpriteSheet('src/images/carrying.png')
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH - 180, HEIGHT - 40)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH - 20
        if self.pos.x < 0:
            self.pos.x = 0 + 20

        self.rect.midbottom = self.pos

        if self.isCarrying:
            self.image = self.carryingSpritesheet.get_image(0, 0, 30, 30)
            self.image.set_colorkey(BLACK)
        # elif self.gotHit:
            # self.image.fill(RED)
        else:
            self.image = self.readySpritesheet.get_image(0, 0, 30, 30)
            self.image.set_colorkey(BLACK)

    def jump(self):
        self.rect.x += 1
        collides = pygame.sprite.spritecollide(
            self, self.game.platforms, False)
        self.rect.x -= 1
        if collides:
            self.vel.y = PLAYER_JUMP


class Car(pygame.sprite.Sprite):
    def __init__(self, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - w - 20
        self.rect.y = HEIGHT - 40 - h


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.hasPackage = False
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Package(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w - 10, h + 10))
        self.spritesheet = SpriteSheet('src/images/package.png')
        self.image = self.spritesheet.get_image(0, 0, 30, 20)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x + 5
        self.rect.y = y - 22


class Hail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.spritesheet = SpriteSheet('src/images/hail.png')
        self.image = self.spritesheet.get_image(0, 0, 10, 10)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if x < WIDTH/2:
            velX = 4
        else:
            velX = -4
        self.vel = vec(velX, 4)

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y


class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, w, h):
        image = pygame.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        return image
