import pygame

class Player(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.WALK_LEFT = [pygame.image.load('textures/L1.png'), pygame.image.load('textures/L2.png'), pygame.image.load('textures/L3.png'), pygame.image.load('textures/L4.png'), pygame.image.load('textures/L5.png'), pygame.image.load('textures/L6.png'), pygame.image.load('textures/L7.png'), pygame.image.load('textures/L8.png'), pygame.image.load('textures/L9.png')]
        self.WALK_RIGHT = [pygame.transform.flip(self.WALK_LEFT[0], True, False), pygame.transform.flip(self.WALK_LEFT[1], True, False), pygame.transform.flip(self.WALK_LEFT[2], True, False), pygame.transform.flip(self.WALK_LEFT[3], True, False), pygame.transform.flip(self.WALK_LEFT[4], True, False), pygame.transform.flip(self.WALK_LEFT[5], True, False), pygame.transform.flip(self.WALK_LEFT[6], True, False), pygame.transform.flip(self.WALK_LEFT[7], True, False), pygame.transform.flip(self.WALK_LEFT[8], True, False)]

        self.x = int(display_width/2 - self.width/2)
        self.y = display_height - self.height
        self.velocity = 5
        self.jump = False
        self.standing = True
        self.left = False
        self.jump_count = 10
        self.JUMPCONST = 0.5
        self.walk_count = 0

    def draw(self):
        global window
        if self.walk_count >= 18:
            self.walk_count = 0

        if self.standing:
            if self.left:
                window.blit(self.WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(self.WALK_RIGHT[0], (self.x, self.y))

        elif self.left:
            window.blit(self.WALK_LEFT[self.walk_count//2], (self.x, self.y))
        else:
            window.blit(self.WALK_RIGHT[self. walk_count//2], (self.x, self.y))

    def exist(self):
        if keys[pygame.K_SPACE]:
            if len(projectiles) <= 20:
                projectiles.append(Projectile(self.x + self.width//2, int(self.y + self.height/2), 5, self.left, (255,255,255)))

        if not self.jump:
            if keys[pygame.K_UP]:
                self.jump = True
        else:
            if self.jump_count >= -10:
                predznak = 1
                if self.jump_count < 0:
                    predznak = -1

                self.y -= self.jump_count**2 * predznak * self.JUMPCONST
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 10

        if keys[pygame.K_LEFT]:
            if not self.left:
                self.walk_count = 0
            self.standing = False
            self.left = True
            self.walk_count += 1

            if self.x - self.velocity <= 0:
                self.x = 0
            else:
                self.x -= self.velocity

        if keys[pygame.K_RIGHT]:
            if self.left:
                self.walk_count = 0
                self.left = False
            self.standing = False
            self.walk_count += 1

            if self.x + self.width + self.velocity >= display_width:
                self.x = display_width - self.width
            else:
                self.x += self.velocity

        if keys[pygame.K_LEFT] == keys[pygame.K_RIGHT]:
            self.standing = True

        return True

class Enemy(object):
    def __init__(self, width, height, x):
        self.WALK_LEFT = [pygame.image.load('textures/L1E.png'), pygame.image.load('textures/L2E.png'), pygame.image.load('textures/L3E.png'), pygame.image.load('textures/L4E.png'), pygame.image.load('textures/L5E.png'), pygame.image.load('textures/L6E.png'), pygame.image.load('textures/L7E.png'), pygame.image.load('textures/L8E.png'), pygame.image.load('textures/L9E.png')]
        self.WALK_RIGHT = [pygame.transform.flip(self.WALK_LEFT[0], True, False), pygame.transform.flip(self.WALK_LEFT[1], True, False), pygame.transform.flip(self.WALK_LEFT[2], True, False), pygame.transform.flip(self.WALK_LEFT[3], True, False), pygame.transform.flip(self.WALK_LEFT[4], True, False), pygame.transform.flip(self.WALK_LEFT[5], True, False), pygame.transform.flip(self.WALK_LEFT[6], True, False), pygame.transform.flip(self.WALK_LEFT[7], True, False), pygame.transform.flip(self.WALK_LEFT[8], True, False)]

        self.x = x
        self.y = 0
        self.width = width
        self.height = height
        self.standing = True

        self.walk_count = 0
        self.velocity = 3
        self.left = False
        self.fall_count = 0
        self.FALLCONST = 0.3
        self.ze_padel = False

    def draw(self):
        global window
        if self.walk_count >= 18:
            self.walk_count = 0
        if self.standing:
            if self.left:
                window.blit(self.WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(self.WALK_RIGHT[0], (self.x, self.y))
        elif self.left:
            window.blit(self.WALK_LEFT[self.walk_count//2], (self.x, self.y))
        else:
            window.blit(self.WALK_RIGHT[self.walk_count//2], (self.x, self.y))

    def exist(self):
        if not self.ze_padel:
            self.fall()
        return True

    def fall(self):
        if self.y + self.height >= display_height:
            self.y = display_height - self.height
        elif self.y <= display_height - self.height:
            self.y += self.fall_count**2 *self.FALLCONST
            self.fall_count += 1
        else:
            self.ze_padel = True

class Projectile(object):
    def __init__(self, x, y, radius, is_left, color):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.velocity = 5
        if is_left:
            self.direction_coefficient = -1
        else:
            self.direction_coefficient = 1

    def exist(self):
        if self.x + self.radius*2 < display_width and self.x >= 0:
            self.x += self.velocity * self.direction_coefficient
            return True
        else:
            return False

    def draw(self):
        global window
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

def draw_window():
    window.blit(bg, (0,0))

    for player in players:
        player.draw()

    for enemy in enemies:
        enemy.draw()

    for projectile in projectiles:
        projectile.draw()

    pygame.display.update()

pygame.init()

display_width = 800
display_height = 500

window = pygame.display.set_mode((display_width, display_height))
#window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Creep")

clock = pygame.time.Clock()

bg = pygame.image.load('textures/luna.png')

game_run = True

players = []
projectiles = []
enemies = []
players.append(Player(64, 64))
enemies.append(Enemy(64, 64, 400))

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    clock.tick(27)
    keys = pygame.key.get_pressed()

    for player in players:
        if not player.exist():
            players.remove(player)

    for enemy in enemies:
        if not enemy.exist():
            enemies.remove(enemy)

    for projectile in projectiles:
        if not projectile.exist():
            projectiles.remove(projectile)

    draw_window()

pygame.quit()
