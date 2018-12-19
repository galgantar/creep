import pygame

class Player(object):
    def __init__(self, width, height):
        #Constant attributes
        self.WIDTH = width
        self.HEIGHT = height
        self.velocity = 5
        self.JUMPCONST = 0.5
        self.WALK_LEFT = [pygame.image.load('textures/L1.png'), pygame.image.load('textures/L2.png'), pygame.image.load('textures/L3.png'), pygame.image.load('textures/L4.png'), pygame.image.load('textures/L5.png'), pygame.image.load('textures/L6.png'), pygame.image.load('textures/L7.png'), pygame.image.load('textures/L8.png'), pygame.image.load('textures/L9.png')]
        self.WALK_RIGHT = [pygame.transform.flip(self.WALK_LEFT[0], True, False), pygame.transform.flip(self.WALK_LEFT[1], True, False), pygame.transform.flip(self.WALK_LEFT[2], True, False), pygame.transform.flip(self.WALK_LEFT[3], True, False), pygame.transform.flip(self.WALK_LEFT[4], True, False), pygame.transform.flip(self.WALK_LEFT[5], True, False), pygame.transform.flip(self.WALK_LEFT[6], True, False), pygame.transform.flip(self.WALK_LEFT[7], True, False), pygame.transform.flip(self.WALK_LEFT[8], True, False)]

        #Variable attributes
        self.x = int(display_width/2 - self.WIDTH/2)
        self.y = display_height - self.HEIGHT
        self.jump = False
        self.standing = True
        self.left = False
        self.jump_count = 10
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
        self.check_fire()
        self.check_jump()
        self.check_move()
        return True

    def check_move(self):
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

            if self.x + self.WIDTH + self.velocity >= display_width:
                self.x = display_width - self.WIDTH
            else:
                self.x += self.velocity

        if keys[pygame.K_LEFT] == keys[pygame.K_RIGHT]:
            self.standing = True

    def check_jump(self):
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

    def check_fire(self):
        if keys[pygame.K_SPACE]:
            if len(projectiles) <= 20:
                projectiles.append(Projectile(self.x + self.WIDTH//2, int(self.y + self.HEIGHT/2), 5, self.left, (255,255,255)))

class Enemy(object):
    def __init__(self, width, height, x):
        #Constant attrubutes
        self.WALK_LEFT = [pygame.image.load('textures/L1E.png'), pygame.image.load('textures/L2E.png'), pygame.image.load('textures/L3E.png'), pygame.image.load('textures/L4E.png'), pygame.image.load('textures/L5E.png'), pygame.image.load('textures/L6E.png'), pygame.image.load('textures/L7E.png'), pygame.image.load('textures/L8E.png')]
        self.WALK_RIGHT = [pygame.transform.flip(self.WALK_LEFT[0], True, False), pygame.transform.flip(self.WALK_LEFT[1], True, False), pygame.transform.flip(self.WALK_LEFT[2], True, False), pygame.transform.flip(self.WALK_LEFT[3], True, False), pygame.transform.flip(self.WALK_LEFT[4], True, False), pygame.transform.flip(self.WALK_LEFT[5], True, False), pygame.transform.flip(self.WALK_LEFT[6], True, False), pygame.transform.flip(self.WALK_LEFT[7], True, False)]
        self.ATTACK_LEFT = [pygame.image.load('textures/L9E.png'), pygame.image.load('textures/L10E.png'), pygame.image.load('textures/L11E.png')]
        self.ATTACK_RIGHT = [pygame.transform.flip(self.ATTACK_LEFT[0], True, False), pygame.transform.flip(self.ATTACK_LEFT[1], True, False), pygame.transform.flip(self.ATTACK_LEFT[2], True, False)]
        self.WIDTH = width
        self.HEIGHT = height
        self.velocity = 3
        self.FALLCONST = 0.3

        #Variable attributes
        self.x = x
        self.y = 0
        self.fall_count = 0
        self.ze_padel = False
        self.standing = True
        self.walk_count = 0
        self.left = False
        self.closest_player_pos = None
        self.attack = True
        self.attack_count = -1

    def draw(self):
        global window
        if self.walk_count >= 16:
            self.walk_count = 0

        if self.standing:
            if self.attack:
                if self.left:
                    window.blit(self.ATTACK_LEFT[self.attack_count], (self.x, self.y))
                else:
                    window.blit(self.ATTACK_RIGHT[self.attack_count], (self.x, self.y))

            elif self.left:
                window.blit(self.WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(self.WALK_RIGHT[0], (self.x, self.y))
        elif self.left:
            window.blit(self.WALK_LEFT[self.walk_count//2], (self.x, self.y))
        else:
            window.blit(self.WALK_RIGHT[self.walk_count//2], (self.x, self.y))

    def exist(self):
        global players

        if not self.ze_padel:
            self.fall()
        else:
            self.poisci_najblizjega()

        self.check_move()

        return True

    def fall(self):
        if self.y + self.HEIGHT > display_height:
            self.y = display_height - self.HEIGHT
        elif self.y < display_height - self.HEIGHT:
            self.y += self.fall_count**2 *self.FALLCONST
            self.fall_count += 1
        else:
            self.ze_padel = True

    def check_move(self):
        if self.closest_player_pos != None and abs(self.x - self.closest_player_pos[0]) <= self.velocity:
            self.x = self.closest_player_pos[0]
            self.standing = True
            self.make_attack()

        elif self.closest_player_pos != None and self.x > self.closest_player_pos[0]:
            self.standing = False
            if self.left:
                self.walk_count += 1
                self.x -= self.velocity
            else:
                self.left = True
                self.walk_count = 0

        elif self.closest_player_pos != None and self.x < self.closest_player_pos[0]:
            self.standing = False
            if not self.left:
                self.walk_count += 1
                self.x += self.velocity
            else:
                self.left = False
                self.walk_count = 0
        else:
            self.standing = True

    def poisci_najblizjega(self):
        oddaljenosti = [abs(self.x - player.x) for player in players]
        self.closest_player_pos = (players[oddaljenosti.index(min(oddaljenosti))].x, players[oddaljenosti.index(min(oddaljenosti))].y)

    def make_attack(self):
        self.attack = True

        if self.attack_count < 2:
            self.attack_count += 1
        else:
            self.attack = False
            self.attack_count = -1

class Projectile(object):
    def __init__(self, x, y, radius, left, color):
        #Constant attributes
        self.velocity = 7
        self.color = color
        self.radius = radius
        self.y = y
        if left:
            self.direction_coefficient = -1
        else:
            self.direction_coefficient = 1

        #Variable attributes
        self.x = x

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
