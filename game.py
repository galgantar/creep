import pygame
import random
import enum
import os
import time

os.environ["SDL_VIDEO_CENTERED"] = "1" # Center a pygame window

display_width = 1200
display_height = 600

sound_location = "sounds/"
texture_location = "textures/"
player_texture_location = "textures/player/"
enemy_texture_location = "textures/skeleton/"
bullet_textures_location = "textures/ammunition/"

# Platform generation values
singlePlatformWidth = 100
singlePlatformHeight = 31
maxPlatformHeight = 130
spacingBetweenPlatforms = 10
biggestSpriteHeight = 64


pygame.mixer.pre_init(44100, -16, 2, 2048) # Put here because of sound preloading in Class attributes
pygame.init()


def starting_screen():
    window.blit(bg, (0,0))
    play_button = Button("Play", None, 250, centered_x=True)
    exit_button = Button("Exit", None, 300, centered_x=True)

    play_button.display()
    exit_button.display()

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                pygame.quit()
                quit()

def ending_screen(score):
    window.blit(bg, (0,0))

    caption = font.render("You died :-(", True, (0, 0, 0))
    points = font.render("Your score: {}".format(score), True, (0, 0, 0))
    window.blit(caption, (display_width//2 - caption.get_width()//2, 100))
    window.blit(points, (display_width//2 - caption.get_width()//2, 130))

    play_button = Button("Play again", None, 250, centered_x=True)
    exit_button = Button("Exit", None, 300, centered_x=True)

    play_button.display()
    exit_button.display()

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                pygame.quit()
                quit()

def draw_window():
    window.blit(bg, (0,0))
    display_elapsed_time()

    for platform in platforms:
        platform.draw()

    for player in players:
        player.draw()

    for enemy in enemies:
        enemy.draw()

    for projectile in projectiles:
        projectile.draw()

    pygame.display.update()

def flip_picture(picture):
    return pygame.transform.flip(picture, True, False)

def resize_picture(picture, ratio):
    relation_coefficient = picture.get_width() / picture.get_height()
    new_height = round(picture.get_height() * ratio)
    new_width = round(new_height * relation_coefficient)

    return pygame.transform.scale(picture, (new_width, new_height))

def create_sound(name):
    location = sound_location + name
    sound = pygame.mixer.Sound(location)
    sound.set_volume(0.1)
    return sound

def display_elapsed_time():
    global time_elapsed
    formatted_time = "Time: {}:{}".format(time_elapsed // 60, time_elapsed % 60)

    text = font.render(str(formatted_time), True, (0, 0, 0))
    window.blit(text, (30, 30))

def check_collision(first, second):
    """fuction checks collision of two given hitboxes"""
    x_collision = first[0] < second[0] + second[2] and second[0] < first[0] + first[2]
    y_collision = first[1] < second[1] + second[3] and second[1] < first[1] + first[3]

    if x_collision and y_collision:
        return True
    else:
        return False

def calculate_possibility_result(possibility):
    """function returns resoult with the given possibility"""
    possibility = round(possibility)
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
        y = yFloor - maxPlatformHeight + random.randint(-30, 30)

        if y > biggestSpriteHeight:
            platforms.append(Platform(x, y, width))
        generate_platform(xMin_current, xMax_current, width-1, y)


class bulletType(enum.Enum):
    RED = enum.auto()
    GREEN = enum.auto()
    BLUE = enum.auto()

class inputType(enum.Enum):
    KEYBOARD = enum.auto()


class Button(object):
    def __init__(self, text, x=None, y=None, **kwargs):
        self.surface = font.render(text, True, (0, 0, 0))
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if "centered_x" in kwargs and kwargs["centered_x"]:
            self.x = display_width//2 - self.WIDTH//2
        else:
            self.x = x

        if "centered_y" in kwargs and kwargs["centered_y"]:
            self.y = display_height//2 - self.HEIGHT//2
        else:
            self.y = y

    def display(self):
        window.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False

class Body(object):
    """parent class for everything with a human-like body (Enemy and Player classes)"""

    def check_platform(self, speed):
        if speed == 0:
            coefficient = 1
        else:
            coefficient = 0

        for platform in platforms:
            x_collision = self.hitbox[0] < platform.hitbox[0] + platform.hitbox[2] and self.hitbox[0] + self.hitbox[2] > platform.hitbox[0]
            height_match = self.hitbox[1] + self.hitbox[3] + speed >= platform.hitbox[1] - coefficient and self.y + self.HEIGHT <= platform.hitbox[1]
            notJumping = self.jump_count == 10 or self.jump_count < 0

            if x_collision and height_match and notJumping:
                self.current_platform = platform
                return

        self.current_platform = None

    def check_fall(self):
        speed = round(self.fall_count**2 * Player.FALLCONST)

        self.check_platform(speed)
        if self.current_platform == None and not self.isJump:
            self.y += speed
            self.fall_count += 1
        elif not self.isJump:
            self.fall_count = 0
            self.y = self.current_platform.hitbox[1] - self.HEIGHT

    def display_points(self, displayText):
        global window
        global displayTextStart

        text = font.render(displayText, True, (0, 0, 0))
        currentSize = text.get_width()
        window.blit(text, (30, displayTextStart))
        displayTextStart += currentSize + 30

    def display_players_health(self):
        global window
        global healtBarStart

        x = display_width - 20 - heart_icon.get_width()
        for i in range(self.health):
            window.blit(heart_icon, (x, healtBarStart))
            x -= heart_icon.get_width()


        healtBarStart = 0

    def display_health_bar(self):
        pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0] - healthBarResize, self.hitbox[1] - 10, self.hitbox[2] + healthBarResize*2, 5))
        pygame.draw.rect(window, (0, 255, 0), (self.hitbox[0] - healthBarResize, self.hitbox[1] - 10, ((self.hitbox[2] + healthBarResize*2)*self.health)//100, 5))


class Player(Body):
    WALK_LEFT = [pygame.image.load(player_texture_location+'L1.png'), pygame.image.load(player_texture_location+'L2.png'), pygame.image.load(player_texture_location+'L3.png'), pygame.image.load(player_texture_location+'L4.png'), pygame.image.load(player_texture_location+'L5.png'), pygame.image.load(player_texture_location+'L6.png'), pygame.image.load(player_texture_location+'L7.png'), pygame.image.load(player_texture_location+'L8.png'), pygame.image.load(player_texture_location+'L9.png')]
    WALK_RIGHT = list(map(lambda x: flip_picture(x), WALK_LEFT))
    JUMPCONST = 0.5
    FALLCONST = 0.5
    velocity = 5
    WIDTH = WALK_LEFT[0].get_width()
    HEIGHT = WALK_LEFT[0].get_height()
    HITBOXCONST = (22, 15, -44, -16) # Hitbox format: x, y, width, height
    MAXSHOOTCOUNT = 15

    def __init__(self, inputForm):
        # Constant attributes
        self.INPUTTYPE = inputForm

        # Variable attributes
        self.health = 7
        self.x = random.randint(0, display_width-Player.WIDTH)
        self.y = -Player.HEIGHT
        self.isJump = False
        self.standing = True
        self.isLeft = False
        self.jump_count = 10
        self.walk_count = 0
        self.fall_count = 0
        self.hitbox = None
        self.shoot_count = Player.MAXSHOOTCOUNT
        self.current_platform = None
        self.points = 0

        # Command attrubutes
        self.inputLEFT = None
        self.inputRIGHT = None
        self.inputUP = None
        self.inputFIRE = None

    def draw(self):
        global window
        self.display_players_health()
        self.display_points("Points: {}".format(self.points))

        if self.walk_count >= 18:
            self.walk_count = 0

        if self.standing:
            if self.isLeft:
                window.blit(Player.WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(Player.WALK_RIGHT[0], (self.x, self.y))

        elif self.isLeft:
            window.blit(Player.WALK_LEFT[self.walk_count//2], (self.x, self.y))
        else:
            window.blit(Player.WALK_RIGHT[self. walk_count//2], (self.x, self.y))

    def exist(self):
        if not self.hitbox:
            self.generate_hitbox()

        self.get_input_vaues()
        self.check_fire()
        self.check_fall()
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
        if self.shoot_count < Player.MAXSHOOTCOUNT:
            self.shoot_count += 1
        if self.inputFIRE and self.shoot_count == Player.MAXSHOOTCOUNT:
            if len(projectiles) <= 10:
                self.shoot_count = 0
                projectile = Projectile(self.x + Player.WIDTH//2, int(self.y + Player.HEIGHT/2), self.isLeft, self)
                projectiles.append(projectile)
                projectile.SOUND.play()

    def check_jump(self):
        if not self.isJump:
            if self.inputUP and self.current_platform != None:
                self.isJump = True
        else:
            if self.jump_count >= 0:
                speed = round(self.jump_count**2 * Player.JUMPCONST)
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

            if self.hitbox[0] - Player.velocity <= 0:
                self.x = -Player.HITBOXCONST[0]
            else:
                self.x -= Player.velocity

        if self.inputRIGHT:
            if self.isLeft:
                self.walk_count = 0
                self.isLeft = False
            self.standing = False
            self.walk_count += 1

            if self.hitbox[0] + self.hitbox[2] + Player.velocity >= display_width:
                self.x = display_width + Player.HITBOXCONST[2] # third value in hitboxconst is negative
            else:
                self.x += Player.velocity

        if self.inputLEFT == self.inputRIGHT:
            self.standing = True

    def generate_hitbox(self):
        self.hitbox = tuple(sum(element) for element in zip((self.x, self.y, Player.WIDTH, Player.HEIGHT), Player.HITBOXCONST))

    def get_hit(self, damage):
        """Method called by class Enemy"""
        self.health -= damage

class Enemy(Body):
    WALK_RIGHT_ICONS = [pygame.image.load(enemy_texture_location+'Skeleton-Walk_01.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_02.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_03.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_04.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_05.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_06.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_07.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_08.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_09.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_10.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_11.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_12.png'), pygame.image.load(enemy_texture_location+'Skeleton-Walk_13.png')]
    WALK_RIGHT = list(map(lambda x: resize_picture(x, 2), WALK_RIGHT_ICONS))
    WALK_LEFT = list(map(lambda x: flip_picture(x), WALK_RIGHT))

    ATTACK_RIGHT_ICONS = [pygame.image.load(enemy_texture_location+'Skeleton-Attack_01.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_02.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_03.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_04.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_05.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_06.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_07.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_08.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_09.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_10.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_11.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_12.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_13.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_14.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_15.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_16.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_17.png'), pygame.image.load(enemy_texture_location+'Skeleton-Attack_18.png'),]
    ATTACK_RIGHT = list(map(lambda x: resize_picture(x, 2), ATTACK_RIGHT_ICONS))
    ATTACK_LEFT = list(map(lambda x: flip_picture(x), ATTACK_RIGHT))

    WIDTH = WALK_LEFT[0].get_width()
    HEIGHT = WALK_LEFT[0].get_height()
    velocity = 3
    FALLCONST = 0.5
    HITBOXCONST = (51, 20, -103, -20)
    BETWEENATTACK = 10
    HITSOUND = create_sound("hit.wav")
    DAMAGE = 1
    MAXJUMPCOUNT = 10
    JUMPCONST = 0.5

    JUMPHEIGHT = 0
    for n in range(MAXJUMPCOUNT+1): # Unable to use comperhensions because of 'class body' scope of class attributes
        JUMPHEIGHT += round(n**2 * JUMPCONST)

    def __init__(self, x):
        # Variable attributes
        self.health = 100
        self.x = x
        self.y = -Enemy.HEIGHT
        self.fall_count = 0
        self.standing = False
        self.walk_count = 0
        self.isLeft = False
        self.closest_player = None
        self.inAttack = False
        self.attack_count = 0
        self.hitbox = None
        self.betweenAttackCount = Enemy.BETWEENATTACK
        self.isColliding = False
        self.current_platform = None
        self.target_platform = None
        self.heading_left = None
        self.isJump = False
        self.jump_count = Enemy.MAXJUMPCOUNT
        self.last_damager = None

    def draw(self):
        global window
        if self.hitbox != None and self.health:
            self.display_health_bar()

        if self.walk_count > 18:
            self.walk_count = 0

        if self.inAttack:
            if self.isLeft:
                window.blit(Enemy.ATTACK_LEFT[self.attack_count], (self.x, self.y))
            else:
                window.blit(Enemy.ATTACK_RIGHT[self.attack_count], (self.x, self.y))

        elif self.standing:
            if self.isLeft:
                window.blit(Enemy.WALK_LEFT[0], (self.x, self.y))
            else:
                window.blit(Enemy.WALK_LEFT[0], (self.x, self.y))

        elif self.isLeft:
            window.blit(Enemy.WALK_LEFT[self.walk_count//2], (self.x, self.y))
        else:
            window.blit(Enemy.WALK_RIGHT[self.walk_count//2], (self.x, self.y))

    def exist(self):
        if not self.hitbox:
            self.generate_hitbox()

        self.check_hit()
        self.check_fall()
        self.check_jump()
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
            self.last_damager.points += 10
            return False

    def check_move(self):
        if self.current_platform == None or self.isJump or self.fall_count != 0:
            self.target_platform = None
            return # Enemy doesn't move if in jump or falling

        elif self.current_platform == self.closest_player.current_platform:
            if self.x + (Enemy.WIDTH//2) > self.closest_player.hitbox[0] + (self.closest_player.hitbox[2]//2):
                self.standing = False
                if self.isLeft:
                    self.walk_count += 1
                    self.x -= Enemy.velocity
                else:
                    self.isLeft = True
                    self.walk_count = 0

            elif self.x + (Enemy.WIDTH//2) < self.closest_player.hitbox[0] + (self.closest_player.hitbox[2]//2):
                self.standing = False
                if not self.isLeft:
                    self.walk_count += 1
                    self.x += Enemy.velocity
                else:
                    self.isLeft = False
                    self.walk_count = 0
            return

        elif not self.standing and self.heading_left != None:
            if self.heading_left:
                self.isLeft = True
                self.walk_count += 1
                self.x -= Enemy.velocity
            else:
                self.isLeft = False
                self.walk_count += 1
                self.x += Enemy.velocity

        if self.target_platform and self.target_platform.hitbox[0] + self.target_platform.hitbox[2] > self.hitbox[0] and self.hitbox[0] + self.hitbox[2] > self.target_platform.hitbox[0]: # X collision between enemy and its target platform
            possibility_percentage = (self.y/display_height)*5
            if not self.isJump and calculate_possibility_result(possibility_percentage):
                self.isJump = True # Beginning of a jump
                self.jump_count = Enemy.MAXJUMPCOUNT

        if self.heading_left == None:
            self.heading_left = random.choice([True, False])

        else:
            possibility_percentage = (100 - ((self.y/display_height)*100))/4
            if self.current_platform and self.hitbox[0] + self.hitbox[2] + self.velocity > self.current_platform.hitbox[0] + self.current_platform.hitbox[2] and calculate_possibility_result(possibility_percentage):
                self.heading_left = True

            elif self.current_platform and self.hitbox[0] - self.velocity < self.current_platform.hitbox[0] and calculate_possibility_result(possibility_percentage):
                self.heading_left = False

        if self.hitbox[0] - self.velocity < 0:
            self.heading_left = False
        elif self.hitbox[0] + self.hitbox[2] + self.velocity > display_width:
            self.heading_left = True

        if not self.target_platform and self.current_platform:
            self.get_target_platform()

    def get_target_platform(self):
        avalible_platforms = []
        for platform in platforms:
            platform_x_collision = self.current_platform.hitbox[0] < platform.hitbox[0] + platform.hitbox[2] and self.current_platform.hitbox[0] + self.current_platform.hitbox[2] > platform.hitbox[0]

            if self.current_platform != platform and platform_x_collision and platform.Y > self.y + Enemy.HEIGHT - Enemy.JUMPHEIGHT and platform.Y < self.y + Enemy.HEIGHT:
                avalible_platforms.append(platform)

        if avalible_platforms:
            self.target_platform = random.choice(avalible_platforms)

    def check_jump(self):
        if self.isJump:
            self.y -= round(self.jump_count**2 * Enemy.JUMPCONST)
            self.jump_count -= 1

        if self.jump_count == 1:
            self.jump_count = Enemy.MAXJUMPCOUNT
            self.isJump = False

    def find_closest_player(self):
        if players:
            oddaljenosti = [abs(self.x - player.x) for player in players]
            self.closest_player = players[oddaljenosti.index(min(oddaljenosti))]
            return True
        else:
            return False

    def check_attack(self):
        self.isColliding = check_collision(self.hitbox, self.closest_player.hitbox)
        if self.isColliding and self.betweenAttackCount == Enemy.BETWEENATTACK:
            self.inAttack = True

            if self.attack_count < 9:
                self.attack_count += 1
            else:
                self.attack_count = 0
                self.closest_player.get_hit(Enemy.DAMAGE)
                self.betweenAttackCount = 0

        elif self.isColliding:
            self.betweenAttackCount += 1

        else:
            self.inAttack = False
            self.attack_count = 0
            if self.betweenAttackCount < Enemy.BETWEENATTACK:
                self.betweenAttackCount += 1

    def generate_hitbox(self):
        self.hitbox = tuple(sum(element) for element in zip((self.x, self.y, Enemy.WIDTH, Enemy.HEIGHT), Enemy.HITBOXCONST))

    def check_hit(self):
        for projectile in projectiles:
            if projectile.hitbox != None and self.hitbox != None and check_collision(self.hitbox, projectile.hitbox) and projectile.isDangerous:
                projectile.make_hit()
                Enemy.HITSOUND.play()
                self.health -= projectile.DAMAGE
                self.last_damager = projectile.owner

class Projectile(object):
    BLUE_ICON = resize_picture(pygame.image.load(bullet_textures_location + "b2.png"), 0.4)
    GREEN_ICON = resize_picture(pygame.image.load(bullet_textures_location + "b3.png"), 0.5)
    RED_ICON = resize_picture(pygame.image.load(bullet_textures_location + "b1.png"), 0.5)

    def __init__(self, x, y, left, owner):
        # Constant attributes
        self.TYPE = self.generate_type()

        if self.TYPE == bulletType.RED:
            self.DAMAGE = 100
            self.VELOCITY = 4
            self.MAXHITCOUNTDOWN = 1
            self.SOUND = create_sound("bullet.wav")
            self.ICON = Projectile.RED_ICON
            self.HITBOXCONST = (5,15,-5,-30)

        elif self.TYPE == bulletType.GREEN:
            self.DAMAGE = 10
            self.VELOCITY = 7
            self.MAXHITCOUNTDOWN = 1
            self.SOUND = create_sound("bullet.wav")
            self.ICON = Projectile.GREEN_ICON
            self.HITBOXCONST = (15,22,-15,-44)

        else:
            self.DAMAGE = 30
            self.VELOCITY = 16
            self.MAXHITCOUNTDOWN = 0
            self.SOUND = create_sound("bullet.wav")
            self.ICON = Projectile.BLUE_ICON
            self.HITBOXCONST = (5,15,-5,-30)

        if left:
            self.DIRECTION_COEFFICIENT = -1
            self.ICON = flip_picture(self.ICON)
        else:
            self.DIRECTION_COEFFICIENT = 1

        # Variable attributes
        self.WIDTH = self.ICON.get_width() # Depends on projectile type
        self.HEIGHT = self.ICON.get_height() # Depends on projectile type
        self.x = x
        self.y = y - self.HEIGHT // 2
        self.hitbox = None
        self.hit_countdown = 0
        self.hit = False
        self.isDangerous = True
        self.owner = owner

    def draw(self):
        global window
        window.blit(self.ICON, (self.x, self.y))

    def exist(self):
        inside_screen = self.x + self.WIDTH < display_width and self.x >= 0
        if inside_screen and self.execute_hit():
            self.x += self.VELOCITY * self.DIRECTION_COEFFICIENT
            self.generate_hitbox()
            return True
        else:
            return False

    def generate_type(self):
        if calculate_possibility_result(5):
            return bulletType.RED
        elif calculate_possibility_result(15):
            return bulletType.GREEN
        else:
            return bulletType.BLUE

    def generate_hitbox(self):
        self.hitbox = tuple(sum(element) for element in zip((self.x, self.y, self.WIDTH, self.HEIGHT), self.HITBOXCONST))

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
        # Constant attributes
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

window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Creep")

clock = pygame.time.Clock()
font = pygame.font.Font("fonts/04b03.ttf", 30)

bg = pygame.image.load(texture_location+"background.jpg")
heart_icon = resize_picture(pygame.image.load(texture_location+"heart.png"), 0.5)
pygame.mixer.music.load(sound_location+"music.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
game_run = True

healthBarResize = 10

players = []
enemies = []
projectiles = []
platforms = []

finalEnemyCount = 7
starting_time = int(time.time())
time_elapsed = 0
finalScore = 0

players.append(Player(inputType.KEYBOARD))
platforms.append(Platform(0, display_height - singlePlatformHeight, 12))
enemies.append(Enemy(100))

generate_platform(0, display_width, 3, display_height)

starting_screen()

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    clock.tick(30)
    time_elapsed = int(time.time()) - starting_time
    finalEnemyCount = 7 + time_elapsed // 15

    if len(enemies) < finalEnemyCount:
        spawn_enemies(1+(finalEnemyCount-len(enemies))*2)

    for player in players:
        if not player.exist():
            finalScore += player.points
            players.remove(player)


    for enemy in enemies:
        if not enemy.exist():
            enemies.remove(enemy)

    for projectile in projectiles:
        if not projectile.exist():
            projectiles.remove(projectile)

    displayTextStart = 90
    healtBarStart = 30
    draw_window()
    if not players:
        ending_screen(finalScore)

pygame.quit()
quit()
