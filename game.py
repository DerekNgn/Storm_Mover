import random
import pygame
from pygame.event import event_name
from settings import *
from sprites import *


class ToughMoverGame:
    def __init__(self):
        self.background = pygame.image.load('src/images/background.png')
        self.gamebackground = pygame.image.load(
            'src/images/game-background.png')
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.last = 0
        self.font = pygame.font.match_font(FONT_NAME)
        self.jumpSound = pygame.mixer.Sound('src/sound/jump.wav')
        self.jumpSound.set_volume(0.05)
        self.pointSound = pygame.mixer.Sound('src/sound/dropoff.wav')
        self.pointSound.set_volume(0.05)
        self.punchSound = pygame.mixer.Sound('src/sound/punch.wav')
        self.punchSound.set_volume(0.05)
        pygame.mixer.music.load('src/sound/theme.mp3')
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.1)

    def run_game(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.jumpSound.play()
                    self.player.jump()

    def update(self):
        self.all_sprites.update()
        self.platformInteractions()
        self.packageInteractions()
        self.hailInteractions()

    def draw(self):
        self.screen.blit(self.gamebackground, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text('Score: ' + str(self.score),
                       24, WHITE, WIDTH/2, HEIGHT-550)
        pygame.display.flip()

    def start_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text('Press any key to play', 24,
                       WHITE, WIDTH/2, HEIGHT * 2/3)
        pygame.display.flip()
        self.waitForAKey()

    def play_game(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.hails = pygame.sprite.Group()
        self.ground = Platform(0, HEIGHT - 40, WIDTH, 40)
        self.ground.spritesheet = SpriteSheet('src/images/ground.png')
        self.ground.image = self.ground.spritesheet.get_image(0, 0, WIDTH, 40)
        self.ground.image.set_colorkey(BLACK)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)
        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            p.spritesheet = SpriteSheet('src/images/porch.png')
            p.image = p.spritesheet.get_image(0, 0, 40, 20)
            p.image.set_colorkey(BLACK)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.newPackage()
        self.car = Car(120, 60)
        self.car.spritesheet = SpriteSheet('src/images/truck.png')
        self.car.image = self.car.spritesheet.get_image(0, 0, 120, 60)
        self.car.image.set_colorkey(BLACK)
        self.all_sprites.add(self.car)
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.run_game()

    def game_over(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text('Game Over', 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text('Score: ' + str(self.score), 24,
                       WHITE, WIDTH/2, HEIGHT * 2/4)
        self.draw_text('Press any key to play again', 24,
                       WHITE, WIDTH/2, HEIGHT * 3/4)
        pygame.display.flip()
        self.waitForAKey()

    def waitForAKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def newPackage(self):
        new_package = random.randint(0, 4)
        self.package = Package(*PLATFORM_LIST[new_package])
        self.all_sprites.add(self.package)

    def newHail(self):
        hail = Hail(random.randint(0, WIDTH), 0)
        self.hails.add(hail)
        self.all_sprites.add(hail)

    def platformInteractions(self):
        if self.player.vel.y > 0:
            collides = pygame.sprite.spritecollide(
                self.player, self.platforms, False)
            if collides:
                if self.player.pos.y < collides[0].rect.bottom:
                    self.player.pos.y = collides[0].rect.top + 1
                    self.player.vel.y = 0

    def packageInteractions(self):
        pickupPackage = pygame.sprite.collide_rect(
            self.player, self.package)
        if pickupPackage:
            self.player.isCarrying = True
            self.all_sprites.remove(self.package)
        dropOffPackage = pygame.sprite.collide_rect(self.player, self.car)
        if dropOffPackage:
            if self.player.isCarrying:
                self.player.isCarrying = False
                self.pointSound.play()
                self.score += 1
                self.newPackage()

    def hailInteractions(self):
        for hail in self.hails:
            if hail.rect.y >= HEIGHT - 40:
                hail.kill()
            hailHits = pygame.sprite.collide_rect(self.player, hail)
            if hailHits:
                self.punchSound.play()
                self.player.gotHit = True
                self.playing = False
                self.game_over()
        now = pygame.time.get_ticks()
        if now - self.last > 400:
            self.newHail()
            self.last = pygame.time.get_ticks()


game = ToughMoverGame()
game.start_screen()
while game.running:
    game.play_game()
    game.game_over()
