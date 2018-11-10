import pygame

class Player():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.x = int(display_width/2 - self.width/2)
        self.y = display_height - self.height
        self.velocity = 5
        self.jump = False
        self.left = False
        self.right = False
        self.jump_count = 10
        self.JUMPCONST = 0.5
        self.walk_count = 0

    def draw(self, window):
        if self.walk_count >= 18:
            self.walk_count = 0

        if self.left == self.right:
            window.blit(standing, (self.x, self.y))
        elif self.left:
            window.blit(WALK_LEFT[self.walk_count//2], (self.x, self.y))
        elif self.right:
            window.blit(WALK_RIGHT[self. walk_count//2], (self.x, self.y))

    def exist(self):
        if not self.jump:
            if keys[pygame.K_SPACE]:
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
            self.right = True
            self.walk_count += 1

            if self.x + self.width + self.velocity >= display_width:
                self.x = display_width - self.width
            else:
                self.x += self.velocity
        
        if keys[pygame.K_LEFT] == keys[pygame.K_RIGHT]:
            self.left = False
            self.right = False


def draw_window():
    window.blit(bg, (0,0))
    
    player1.draw(window)

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

player1 = Player(64, 64)

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    clock.tick(27)
    keys = pygame.key.get_pressed()
    player1.exist()
    draw_window()

pygame.quit()