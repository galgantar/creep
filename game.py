import pygame
import random
import enum

class bulletType(enum.Enum):
    RED = enum.auto()
    GREEN = enum.auto()
    BLUE = enum.auto()

class inputType(enum.Enum):
    KEYBOARD = enum.auto()


class Player(object):
    def __init__(self, inputForm):
        #Constant attributes
        self.INPUTTYPE = inputForm
        self.velocity = 5
        self.JUMPCONST = 0.5
        self.FALLCONST = 0.5
        self.WALK_LEFT = [pygame.image.load(texture_location+'L1.png'), pygame.image.load(texture_location+'L2.png'), pygame.image.load(texture_location+'L3.png'), pygame.image.load(texture_location+'L4.png'), pygame.image.load(texture_location+'L5.png'), pygame.image.load(texture_location+'L6.png'), pygame.image.load(texture_location+'L7.png'), pygame.image.load(texture_location+'L8.png'), pygame.image.load(texture_location+'L9.png')]
        self.WALK_RIGHT = [flip_picture(self.WALK_LEFT[0]), flip_picture(self.WALK_LEFT[1]), flip_picture(self.WALK_LEFT[2]), flip_picture(self.WALK_LEFT[3]), flip_picture(self.WALK_LEFT[4]), flip_picture(self.WALK_LEFT[5]), flip_picture(self.WALK_LEFT[6]), flip_picture(self.WALK_LEFT[7]), flip_picture(self.WALK_LEFT[8])]
        self.WIDTH = self.WALK_LEFT[0].get_width()
        self.HEIGHT = self.WALK_LEFT[0].get_height()
        self.HITBOXCONST = (17, 15, -33, -16)
        self.MAXSHOOTCOUNT = 15

        #Variable attributes
        self.health = 100
        self.x = random.randint(0, display_width-self.WIDTH)
        self.y = -self.HEIGHT
        self.isJump = False
        self.standing = True
        self.isLeft = False
        self.jump_count = 10
        self.walk_count = 0
        self.fall_count = 0
        self.hitbox = None
        self.shoot_count = self.MAXSHOOTCOUNT
        self.current_platform = None

        #Command attrubutes
        self.inputLEFT = None
        self.inputRIGHT = None
        self.inputUP = None
        self.inputFIRE = None

    def draw(self):
        global window
        display_health("My health: " + str(self.health))

        if self.walk_count >= 18:
            self.walk_count = 0

        if self.standing:
            if self.isLeft:
                window.blit(self.WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(self.WALK_RIGHT[0], (self.x, self.y))

        elif self.isLeft:
            window.blit(self.WALK_LEFT[self.walk_count//2], (self.x, self.y))
        else:
            window.blit(self.WALK_RIGHT[self. walk_count//2], (self.x, self.y))

    def exist(self):
        self.get_input_vaues()
        self.check_fire()
        check_fall(self)
        self.check_jump()
        self.check_move()
        self.generate_hitbox()

        if self.health > 0:
            return True
        else:
            return False

    def get_input_vaues(self):
        if self.INPUTTYPE == inputType.KEYBOARD:
            keys = pygame.key.get_pressed()
            self.inputLEFT = keys[pygame.K_LEFT]
            self.inputRIGHT = keys[pygame.K_RIGHT]
            self.inputUP = keys[pygame.K_UP]
            self.inputFIRE = keys[pygame.K_SPACE]

    def check_fire(self):
        if self.shoot_count < self.MAXSHOOTCOUNT:
            self.shoot_count += 1
        if self.inputFIRE and self.shoot_count == self.MAXSHOOTCOUNT:
            if len(projectiles) <= 10:
                self.shoot_count = 0
                projectile = Projectile(self.x + self.WIDTH//2, int(self.y + self.HEIGHT/2), self.isLeft)
                projectiles.append(projectile)
                projectile.SOUND.play()

    def check_jump(self):
        if not self.isJump:
            if self.inputUP and self.current_platform != None:
                self.isJump = True
        else:
            speed = round(self.jump_count**2 * self.JUMPCONST + 0.5) #0.5 must be added in order to correctly round floats smaller than 1
            if self.jump_count >= 0:
                self.y -= speed
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.isJump = False

    def check_move(self):
        if self.inputLEFT:
            if not self.isLeft:
                self.walk_count = 0
            self.standing = False
            self.isLeft = True
            self.walk_count += 1

            if self.x - self.velocity <= 0:
                self.x = 0
            else:
                self.x -= self.velocity

        if self.inputRIGHT:
            if self.isLeft:
                self.walk_count = 0
                self.isLeft = False
            self.standing = False
            self.walk_count += 1

            if self.x + self.WIDTH + self.velocity >= display_width:
                self.x = display_width - self.WIDTH
            else:
                self.x += self.velocity

        if self.inputLEFT == self.inputRIGHT:
            self.standing = True

    def generate_hitbox(self):
        self.hitbox = tuple(sum(element) for element in zip((self.x, self.y, self.WIDTH, self.HEIGHT), self.HITBOXCONST))

    def get_hit(self, damage):
        """Method called by class Enemy"""
        self.health -= damage

class Enemy(object):
    def __init__(self, x):
        #Constant attrubutes
        self.WALK_LEFT = [pygame.image.load(texture_location+'L1E.png'), pygame.image.load(texture_location+'L2E.png'), pygame.image.load(texture_location+'L3E.png'), pygame.image.load(texture_location+'L4E.png'), pygame.image.load(texture_location+'L5E.png'), pygame.image.load(texture_location+'L6E.png'), pygame.image.load(texture_location+'L7E.png'), pygame.image.load(texture_location+'L8E.png')]
        self.WALK_RIGHT = [flip_picture(self.WALK_LEFT[0]), flip_picture(self.WALK_LEFT[1]), flip_picture(self.WALK_LEFT[2]), flip_picture(self.WALK_LEFT[3]), flip_picture(self.WALK_LEFT[4]), flip_picture(self.WALK_LEFT[5]), flip_picture(self.WALK_LEFT[6]), flip_picture(self.WALK_LEFT[7])]
        self.ATTACK_LEFT = [pygame.image.load(texture_location+'L9E.png'), pygame.image.load(texture_location+'L10E.png'), pygame.image.load(texture_location+'L11E.png')]
        self.ATTACK_RIGHT = [flip_picture(self.ATTACK_LEFT[0]), flip_picture(self.ATTACK_LEFT[1]), flip_picture(self.ATTACK_LEFT[2])]
        self.WIDTH = self.WALK_LEFT[0].get_size()[0]
        self.HEIGHT = self.WALK_LEFT[0].get_size()[1]
        self.velocity = 2
        self.FALLCONST = 0.5
        self.LEFT_HITBOXCONST = (27, 8, -37, -9)
        self.RIGHT_HITBOXCONST = (10, 8, -37, -9)
        self.BETWEENATTACK = 10
        self.HITSOUND = pygame.mixer.Sound(sound_location+"hit.wav")
        self.DAMAGE = 10
        self.isJump = False

        #Variable attributes
        self.health = 100
        self.x = x
        self.y = -self.HEIGHT
        self.fall_count = 0
        self.ze_padel = False
        self.standing = False
        self.walk_count = 0
        self.isLeft = False
        self.closest_player = None
        self.inAttack = False
        self.attack_count = -1
        self.hitbox = None
        self.betweenAttackCount = self.BETWEENATTACK
        self.isColliding = False
        self.current_platform = None

    def draw(self):
        global window
        if self.hitbox != None and self.health != None:
            display_health_bar(self.hitbox, self.health)

        if self.walk_count >= 16:
            self.walk_count = 0

        if self.inAttack:
            if self.isLeft:
                window.blit(self.ATTACK_LEFT[self.attack_count], (self.x, self.y))
            else:
                window.blit(self.ATTACK_RIGHT[self.attack_count], (self.x, self.y))

        elif self.standing:
            if self.isLeft:
                window.blit(self.WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(self.WALK_RIGHT[0], (self.x, self.y))

        elif self.isLeft:
            window.blit(self.WALK_LEFT[self.walk_count//2], (self.x, self.y))
        else:
            window.blit(self.WALK_RIGHT[self.walk_count//2], (self.x, self.y))

    def exist(self):
        global players

        self.check_hit()
        check_fall(self)
        if self.find_closest_player():
            self.check_attack()
            if not self.inAttack:
                self.check_move()
        else:
            self.inAttack = False
            self.standing = True
        self.generate_hitbox()

        if self.health > 0:
            return True
        else:
            return False

    def fall(self):
        if self.closest_player != None and self.x < self.closest_player.hitbox[0] + (self.closest_player.hitbox[2]//2):
            self.isLeft = False
        else:
            self.isLeft = True

        if self.y + self.HEIGHT > display_height:
            self.y = display_height - self.HEIGHT
        elif self.y < display_height - self.HEIGHT:
            self.y += self.fall_count**2 *self.FALLCONST
            self.fall_count += 1
        else:
            self.ze_padel = True

    def check_move(self):
        x_collision = self.hitbox != None and self.hitbox[0] < self.closest_player.hitbox[0] + self.closest_player.hitbox[2] and self.closest_player.hitbox[0] < self.hitbox[0] + self.hitbox[2]
        if x_collision:
            self.standing = True
            pass

        elif self.x + (self.WIDTH//2) > self.closest_player.hitbox[0] + (self.closest_player.hitbox[2]//2):
            self.standing = False
            if self.isLeft:
                self.walk_count += 1
                self.x -= self.velocity
            else:
                self.isLeft = True
                self.walk_count = 0

        elif self.x + (self.WIDTH//2) < self.closest_player.hitbox[0] + (self.closest_player.hitbox[2]//2):
            self.standing = False
            if not self.isLeft:
                self.walk_count += 1
                self.x += self.velocity
            else:
                self.isLeft = False
                self.walk_count = 0
        else:
            pass

    def find_closest_player(self):
        if len(players) > 0:
            oddaljenosti = [abs(self.x - player.x) for player in players]
            self.closest_player = players[oddaljenosti.index(min(oddaljenosti))]
            return True
        else:
            return False

    def check_attack(self):
        if self.hitbox == None:
            return

        self.isColliding = check_collision(self.hitbox, self.closest_player.hitbox)
        if self.isColliding and self.betweenAttackCount == self.BETWEENATTACK:
            self.inAttack = True

            if self.attack_count < 2:
                self.attack_count += 1
            else:
                self.attack_count = -1
                self.closest_player.get_hit(self.DAMAGE)
                self.betweenAttackCount = 0

        else:
            self.inAttack = False
            if self.betweenAttackCount < self.BETWEENATTACK:
                self.betweenAttackCount += 1

    def generate_hitbox(self):
        if self.isLeft:
            self.hitbox = tuple(sum(element) for element in zip((self.x, self.y, self.WIDTH, self.HEIGHT), self.LEFT_HITBOXCONST))
        else:
            self.hitbox = tuple(sum(element) for element in zip((self.x, self.y, self.WIDTH, self.HEIGHT), self.RIGHT_HITBOXCONST))

    def check_hit(self):
        for projectile in projectiles:
            if projectile.hitbox != None and self.hitbox != None and check_collision(self.hitbox, projectile.hitbox) and projectile.isDangerous:
                projectile.make_hit()
                self.HITSOUND.play()
                self.health -= projectile.DAMAGE

class Projectile(object):
    def __init__(self, x, y, left):
        #Constant attributes
        self.TYPE = self.generate_type()
        self.y = y
        if left:
            self.DIRECTION_COEFFICIENT = -1
        else:
            self.DIRECTION_COEFFICIENT = 1

        if self.TYPE == bulletType.RED:
            self.COLOR = (255, 0, 0)
            self.DAMAGE = 100
            self.RADIUS = 9
            self.VELOCITY = 4
            self.MAXHITCOUNTDOWN = 1
            self.SOUND = pygame.mixer.Sound(sound_location+"bullet.wav")

        elif self.TYPE == bulletType.GREEN:
            self.COLOR = (0, 255, 0)
            self.DAMAGE = 10
            self.RADIUS = 5
            self.VELOCITY = 7
            self.MAXHITCOUNTDOWN = 1
            self.SOUND = pygame.mixer.Sound(sound_location+"bullet.wav")

        else:
            self.COLOR = (0, 0, 255)
            self.DAMAGE = 30
            self.RADIUS = 7
            self.VELOCITY = 16
            self.MAXHITCOUNTDOWN = 0
            self.SOUND = pygame.mixer.Sound(sound_location+"bullet.wav")

        self.HITBOXCONST = (-self.RADIUS, -self.RADIUS, 0, 0)

        #Variable attributes
        self.x = x
        self.hitbox = None
        self.hit_countdown = 0
        self.hit = False
        self.isDangerous = True

    def draw(self):
        global window
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.RADIUS)

    def exist(self):
        inside_screen = self.x + self.RADIUS*2 < display_width and self.x >= 0
        if inside_screen and self.execute_hit():
            self.x += self.VELOCITY * self.DIRECTION_COEFFICIENT
            self.hitbox = tuple(sum(element) for element in zip((self.x, self.y, self.RADIUS*2, self.RADIUS*2), self.HITBOXCONST))
            return True
        else:
            return False

    def generate_type(self):
        if calculate_possibility_result(20):
            return bulletType.RED
        elif calculate_possibility_result(50):
            return bulletType.GREEN
        else:
            return bulletType.BLUE

    def make_hit(self):
        """Method called only by other objects"""
        self.hit = True
        if not self.TYPE == bulletType.GREEN:
            self.isDangerous = False

    def execute_hit(self):
        if self.hit and not self.TYPE == bulletType.GREEN:
            if self.hit_countdown < self.MAXHITCOUNTDOWN:
                self.hit_countdown += 1
                return True
            else:
                return False
        else:
            return True

class Platform(object):
    def __init__(self, x, y, widthCount):
        #Constant attributes
        self.X = x
        self.Y = y
        self.WIDTHCOUNT = widthCount
        self.SURFACE = self.create_surface()
        self.hitbox = (self.X, self.Y, self.SURFACE.get_width(), self.SURFACE.get_height())

    def draw(self):
        global window
        window.blit(self.SURFACE, (self.X, self.Y))

    def exist(self):
        return True

    def create_surface(self):
        piece = pygame.image.load(texture_location+"plate.png")
        newSurface = pygame.Surface((piece.get_width()*self.WIDTHCOUNT, piece.get_height()), pygame.SRCALPHA)
        totalWidth = 0
        for x in range(self.WIDTHCOUNT):
            newSurface.blit(piece, (totalWidth, 0))
            totalWidth += piece.get_width()

        return newSurface

def draw_window():
    window.blit(bg, (0,0))

    for platform in platforms:
        platform.draw()

    for player in players:
        player.draw()

    for enemy in enemies:
        enemy.draw()

    for projectile in projectiles:
        projectile.draw()

    pygame.display.update()

def check_fall(object):
    if object.hitbox == None:
        return

    speed = round(object.fall_count**2 * object.FALLCONST + 0.5) #0.5 must be added in order to correctly round floats smaller than 1

    check_platform(object, speed)
    if object.current_platform == None and not object.isJump:
        object.y += speed
        object.fall_count += 1
    elif not object.isJump:
        object.fall_count = 0
        object.y = object.current_platform.hitbox[1] - object.HEIGHT

def check_platform(object, speed):
    if object.hitbox == None:
        return
    if speed == 0:
        coefficient = 1
    else:
        coefficient = 0

    for platform in platforms:
        x_collision = object.hitbox[0] > platform.hitbox[0] and object.hitbox[0] + object.hitbox[2] < platform.hitbox[0] + platform.hitbox[2]
        height_match = object.hitbox[1] + object.hitbox[3] + speed >= platform.hitbox[1] - coefficient and object.y + object.HEIGHT <= platform.hitbox[1]
        notJumping = not object.isJump or object.jump_count == 10 or object.jump_count < 0

        if x_collision and height_match and notJumping:
            object.current_platform = platform
            return

    object.current_platform = None

def flip_picture(picture):
    return pygame.transform.flip(picture, True, False)

def check_collision(first, second):
    """fuction checks collision of two given hitboxes"""
    x_collision = first[0] < second[0] + second[2] and second[0] < first[0] + first[2]
    y_collision = first[1] < second[1] + second[3] and second[1] < first[1] + first[3]

    if x_collision and y_collision:
        return True
    else:
        return False

def display_health(displayText):
    global window
    global displayTextStart

    text = font.render(displayText, True, (255, 255, 255))
    currentSize = text.get_size()[0]
    window.blit(text, (displayTextStart, 0))
    displayTextStart += currentSize + 20

def display_health_bar(hitbox, health):
    pygame.draw.rect(window, (255, 0, 0), (hitbox[0] - healthBarResize, hitbox[1] - 15, hitbox[2] + healthBarResize*2, 10))
    pygame.draw.rect(window, (0, 255, 0), (hitbox[0] - healthBarResize, hitbox[1] - 15, ((hitbox[2] + healthBarResize*2)*health)//100, 10))

def calculate_possibility_result(possibility):
    """function returns resoult with the given possibility"""
    if random.randint(1, 100) <= possibility:
        return True
    else:
        return False

def spawn_enemies(possibility):
    if calculate_possibility_result(possibility):
        enemies.append(Enemy(random.randint(0, display_width-64)))

def generate_platform(xMin, xMax, width, yFloor):
    """function for random platform generation"""
    if width == 0:
        return

    number_of_platforms = (xMax - xMin) // (width*singlePlatformWidth + spacingBetweenPlatforms)
    for n in range(1, number_of_platforms+1):
        xMin_current = xMin + (((xMax - xMin) // number_of_platforms)*(n-1))
        xMax_current =  xMin + ((xMax - xMin) // number_of_platforms)*n - spacingBetweenPlatforms

        x = random.randint(xMin_current, xMax_current - width*singlePlatformWidth)
        y = yFloor - maxPlatformHeight + random.randint(-50, 50)

        if y > biggestSpriteHeight and y < display_height - biggestSpriteHeight - singlePlatformHeight*2:
            platforms.append(Platform(x, y, width))
        generate_platform(xMin_current, xMax_current, width-1, y)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

display_width = 800
display_height = 500

sound_location = "sounds/"
texture_location = "textures/"

#Platform generation values
singlePlatformWidth = 100
singlePlatformHeight = 31
maxPlatformHeight = 130
spacingBetweenPlatforms = 10
biggestSpriteHeight = 64

window = pygame.display.set_mode((display_width, display_height))
#window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Creep")

clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri", 30)

bg = pygame.image.load(texture_location+"luna.png")
pygame.mixer.music.load(sound_location+"music.mp3")
pygame.mixer.music.play(-1)
game_run = True

healthBarResize = 10

players = []
enemies = []
projectiles = []
platforms = []
finalEnemyCount = 5
players.append(Player(inputType.KEYBOARD))
platforms.append(Platform(0, display_height - singlePlatformHeight, 8))

generate_platform(0, display_width, 3, display_height)

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    clock.tick(30)
    if len(enemies) < finalEnemyCount:
        spawn_enemies(1+(finalEnemyCount-len(enemies))*2)

    for player in players:
        if not player.exist():
            players.remove(player)

    for enemy in enemies:
        if not enemy.exist():
            enemies.remove(enemy)

    for projectile in projectiles:
        if not projectile.exist():
            projectiles.remove(projectile)

    displayTextStart = 0
    draw_window()

pygame.quit()
