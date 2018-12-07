import pygame

class Player():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.x = int(display_width/2 - self.width/2)
        self.y = display_height - self.height
        self.velocity = 5
        self.jump = False
        self.standing = True
        self.left = False
        self.right = True
        self.jump_count = 10
        self.JUMPCONST = 0.5
        self.walk_count = 0

    def draw(self):
        global window
        if self.walk_count >= 18:
            self.walk_count = 0

        if self.standing:
            if self.left:
                window.blit(WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(WALK_RIGHT[0], (self.x, self.y))

        elif self.left:
            window.blit(WALK_LEFT[self.walk_count//2], (self.x, self.y))
        elif self.right:
            window.blit(WALK_RIGHT[self. walk_count//2], (self.x, self.y))

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
            if self.right:
                self.walk_count = 0
                self.right = False
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
            self.right = True
            self.walk_count += 1

            if self.x + self.width + self.velocity >= display_width:
                self.x = display_width - self.width
            else:
                self.x += self.velocity

        if keys[pygame.K_LEFT] == keys[pygame.K_RIGHT]:
            self.standing = True

        return True

class Projectile():
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

    for projectile in projectiles:
        projectile.draw()

    pygame.display.update()

pygame.init()

display_width = 800
display_height = 500

window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Python game")

clock = pygame.time.Clock()

WALK_RIGHT = [pygame.image.load('textures/R1.png'), pygame.image.load('textures/R2.png'), pygame.image.load('textures/R3.png'), pygame.image.load('textures/R4.png'), pygame.image.load('textures/R5.png'), pygame.image.load('textures/R6.png'), pygame.image.load('textures/R7.png'), pygame.image.load('textures/R8.png'), pygame.image.load('textures/R9.png')]
WALK_LEFT = [pygame.image.load('textures/L1.png'), pygame.image.load('textures/L2.png'), pygame.image.load('textures/L3.png'), pygame.image.load('textures/L4.png'), pygame.image.load('textures/L5.png'), pygame.image.load('textures/L6.png'), pygame.image.load('textures/L7.png'), pygame.image.load('textures/L8.png'), pygame.image.load('textures/L9.png')]
bg = pygame.image.load('textures/luna.png')
standing = pygame.image.load('textures/standing.png')

game_run = True

players = []
players.append(Player(64, 64))
projectiles = []

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    clock.tick(27)
    keys = pygame.key.get_pressed()

    for projectile in projectiles:
        if not projectile.exist():
            projectiles.remove(projectile)

    for player in players:
        if not player.exist():
            players.remove(player)

    draw_window()

pygame.quit()
