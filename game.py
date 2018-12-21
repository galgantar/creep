import pygame

class Player(object):
    def __init__(self, width, height):
        #Constant attributes
        self.WIDTH = width
        self.HEIGHT = height
        self.velocity = 5
        self.JUMPCONST = 0.5
        self.WALK_LEFT = [pygame.image.load('textures/L1.png'), pygame.image.load('textures/L2.png'), pygame.image.load('textures/L3.png'), pygame.image.load('textures/L4.png'), pygame.image.load('textures/L5.png'), pygame.image.load('textures/L6.png'), pygame.image.load('textures/L7.png'), pygame.image.load('textures/L8.png'), pygame.image.load('textures/L9.png')]
        self.WALK_RIGHT = [flip_picture(self.WALK_LEFT[0]), flip_picture(self.WALK_LEFT[1]), flip_picture(self.WALK_LEFT[2]), flip_picture(self.WALK_LEFT[3]), flip_picture(self.WALK_LEFT[4]), flip_picture(self.WALK_LEFT[5]), flip_picture(self.WALK_LEFT[6]), flip_picture(self.WALK_LEFT[7]), flip_picture(self.WALK_LEFT[8])]
        self.HITBOXCONST = (17, 13, -33, -13)

        #Variable attributes
        self.x = int(display_width/2 - self.WIDTH/2)
        self.y = display_height - self.HEIGHT
        self.isJump = False
        self.standing = True
        self.isLeft = False
        self.jump_count = 10
        self.walk_count = 0
        self.hitbox = None

    def draw(self):
        global window
        if self.walk_count >= 18:
            self.walk_count = 0

        if self.standing:
            if self.isLeft:
                window.blit(self.WALK_LEFT[0], (self.x, self.y))
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
            else:
                window.blit(self.WALK_RIGHT[0], (self.x, self.y))
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

        elif self.isLeft:
            window.blit(self.WALK_LEFT[self.walk_count//2], (self.x, self.y))
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        else:
            window.blit(self.WALK_RIGHT[self. walk_count//2], (self.x, self.y))
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def exist(self):
        self.check_fire()
        self.check_jump()
        self.check_move()
        self.hitbox = tuple(first + last for first, last in zip((self.x, self.y, self.WIDTH, self.HEIGHT), self.HITBOXCONST))
        return True

    def check_move(self):
        if keys[pygame.K_LEFT]:
            if not self.isLeft:
                self.walk_count = 0
            self.standing = False
            self.isLeft = True
            self.walk_count += 1

            if self.x - self.velocity <= 0:
                self.x = 0
            else:
                self.x -= self.velocity

        if keys[pygame.K_RIGHT]:
            if self.isLeft:
                self.walk_count = 0
                self.isLeft = False
            self.standing = False
            self.walk_count += 1

            if self.x + self.WIDTH + self.velocity >= display_width:
                self.x = display_width - self.WIDTH
            else:
                self.x += self.velocity

        if keys[pygame.K_LEFT] == keys[pygame.K_RIGHT]:
            self.standing = True

    def check_jump(self):
        if not self.isJump:
            if keys[pygame.K_UP]:
                self.isJump = True
        else:
            if self.jump_count >= -10:
                predznak = 1
                if self.jump_count < 0:
                    predznak = -1

                self.y -= self.jump_count**2 * predznak * self.JUMPCONST
                self.jump_count -= 1
            else:
                self.isJump = False
                self.jump_count = 10

    def check_fire(self):
        if keys[pygame.K_SPACE]:
            if len(projectiles) <= 20:
                projectiles.append(Projectile(self.x + self.WIDTH//2, int(self.y + self.HEIGHT/2), 5, self.isLeft, (255,255,255)))

class Enemy(object):
    def __init__(self, width, height, x):
        #Constant attrubutes
        self.WALK_LEFT = [pygame.image.load('textures/L1E.png'), pygame.image.load('textures/L2E.png'), pygame.image.load('textures/L3E.png'), pygame.image.load('textures/L4E.png'), pygame.image.load('textures/L5E.png'), pygame.image.load('textures/L6E.png'), pygame.image.load('textures/L7E.png'), pygame.image.load('textures/L8E.png')]
        self.WALK_RIGHT = [flip_picture(self.WALK_LEFT[0]), flip_picture(self.WALK_LEFT[1]), flip_picture(self.WALK_LEFT[2]), flip_picture(self.WALK_LEFT[3]), flip_picture(self.WALK_LEFT[4]), flip_picture(self.WALK_LEFT[5]), flip_picture(self.WALK_LEFT[6]), flip_picture(self.WALK_LEFT[7])]
        self.ATTACK_LEFT = [pygame.image.load('textures/L9E.png'), pygame.image.load('textures/L10E.png'), pygame.image.load('textures/L11E.png')]
        self.ATTACK_RIGHT = [flip_picture(self.ATTACK_LEFT[0]), flip_picture(self.ATTACK_LEFT[1]), flip_picture(self.ATTACK_LEFT[2])]
        self.WIDTH = width
        self.HEIGHT = height
        self.velocity = 2
        self.FALLCONST = 0.3
        self.LEFT_HITBOXCONST = (27, 8, -37, -10)
        self.RIGHT_HITBOXCONST = (10, 8, -37, -10)

        #Variable attributes
        self.x = x
        self.y = 0
        self.fall_count = 0
        self.ze_padel = False
        self.standing = True
        self.walk_count = 0
        self.isLeft = False
        self.closest_player_pos = None
        self.attack = False
        self.attack_count = -1
        self.hitbox = None

    def draw(self):
        global window
        if self.walk_count >= 16:
            self.walk_count = 0

        if self.attack:
            if self.isLeft:
                window.blit(self.ATTACK_LEFT[self.attack_count], (self.x, self.y))
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
            else:
                window.blit(self.ATTACK_RIGHT[self.attack_count], (self.x, self.y))
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

        elif self.isLeft:
            window.blit(self.WALK_LEFT[self.walk_count//2], (self.x, self.y))
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        else:
            window.blit(self.WALK_RIGHT[self.walk_count//2], (self.x, self.y))
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def exist(self):
        global players

        if not self.ze_padel:
            self.fall()
        else:
            self.poisci_najblizjega()
            self.check_move()

        if self.isLeft:
            self.hitbox = tuple(first + last for first, last in zip((self.x, self.y, self.WIDTH, self.HEIGHT), self.LEFT_HITBOXCONST))
        else:
            self.hitbox = tuple(first + last for first, last in zip((self.x, self.y, self.WIDTH, self.HEIGHT), self.RIGHT_HITBOXCONST))
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
        if abs(self.x - self.closest_player_pos[0]) <= self.velocity:
            self.x = self.closest_player_pos[0]
            self.make_attack()

        elif self.x > self.closest_player_pos[0]:
            self.attack = False
            if self.isLeft:
                self.walk_count += 1
                self.x -= self.velocity
            else:
                self.isLeft = True
                self.walk_count = 0

        elif self.x < self.closest_player_pos[0]:
            self.attack = False
            if not self.isLeft:
                self.walk_count += 1
                self.x += self.velocity
            else:
                self.isLeft = False
                self.walk_count = 0
        else:
            pass

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

    def hit(self):
        print("Enemy hit")

class Projectile(object):
    def __init__(self, x, y, radius, left, color):
        #Constant attributes
        self.velocity = 7
        self.color = color
        self.RADIUS = radius
        self.y = y
        self.isLeft = left
        self.HITBOXCONST = (-self.RADIUS, -self.RADIUS, 0, 0)
        if left:
            self.direction_coefficient = -1
        else:
            self.direction_coefficient = 1

        #Variable attributes
        self.x = x
        self.hitbox = None

    def exist(self):
        if self.x + self.RADIUS*2 < display_width and self.x >= 0:
            self.x += self.velocity * self.direction_coefficient
            if self.isLeft:
                self.hitbox = tuple(first+last for first, last in zip((self.x, self.y, self.RADIUS*2, self.RADIUS*2), self.HITBOXCONST))
            else:
                self.hitbox = tuple(first+last for first, last in zip((self.x, self.y, self.RADIUS*2, self.RADIUS*2), self.HITBOXCONST))
            return True
        else:
            return False

    def draw(self):
        global window
        pygame.draw.circle(window, self.color, (self.x, self.y), self.RADIUS)
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

def draw_window():
    window.blit(bg, (0,0))

    for player in players:
        player.draw()

    for enemy in enemies:
        enemy.draw()

    for projectile in projectiles:
        projectile.draw()

    pygame.display.update()

def flip_picture(picture):
    return pygame.transform.flip(picture, True, False)

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
enemies = []
projectiles = []
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
