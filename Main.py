import pygame
from pygame.locals import *
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        #? setup player sprite and speed and what not
        super().__init__(groups)
        self.image = pygame.image.load("Assets\Img\Player_Snowman.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (96,96))
        Window_Width, Window_Height = 1280, 768
        self.rect =  self.image.get_frect(center = (Window_Width / 2, Window_Height / 2))
        self.Player_Direction = pygame.math.Vector2(0,0)
        
        #? setup cooldown on snowball launcher
        self.can_shoot = True
        self.snowball_shoot_time = 0
        self.cooldown_duration = 300
        self.Facing_Direction = "Right"
        
    def update(self, dt):
        
        self.Player_Speed = 800
        
        #? get the keys that are being pressed 
        Movement_keys = pygame.key.get_pressed()
        self.Player_Direction.x = int(Movement_keys[pygame.K_d] or Movement_keys[pygame.K_RIGHT]) - int(Movement_keys[pygame.K_a] or Movement_keys[pygame.K_LEFT])
        self.Player_Direction.y = int(Movement_keys[pygame.K_s] or Movement_keys[pygame.K_DOWN]) - int(Movement_keys[pygame.K_w] or Movement_keys[pygame.K_UP] or Movement_keys[pygame.K_SPACE])
        
        self.Player_Direction = self.Player_Direction.normalize() if self.Player_Direction else self.Player_Direction #? makes the speed constant when you click 2 buttons at the same time
        self.rect.center += self.Player_Direction * self.Player_Speed * dt
        
        Shooting_keys = pygame.key.get_just_pressed()
        if Shooting_keys[pygame.K_q] and self.can_shoot:
            Snowball(Snowball_Surf, self.rect.midright, (all_sprites, snowball_sprites))
            self.can_shoot = False
            self.snowball_shoot_time = pygame.time.get_ticks()
               
        self.snowball_timer()
                
    def snowball_timer(self): 
        if self.can_shoot == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.snowball_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
class Snowball(pygame.sprite.Sprite):
    
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        
        self.image = surf
        self.image = pygame.transform.scale(self.image, (12,12))
        self.rect = self.image.get_frect(midleft = pos)
        
        
    def update(self,dt):
        self.rect.centerx += 400 * dt
        
        #? destroys itself if it leaves the screen
        if self.rect.right > 1280:
            self.kill()    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, (96,96))
        self.rect =  self.image.get_frect(center = pos)
 
def title_menu():
    global On_Title_Card
    
    title_card = pygame.image.load("Assets\Img\Title_Card1.png").convert_alpha()
    title_card = pygame.transform.scale(title_card,(768,768))
    title_card_rect  = title_card.get_frect(center = (Window_Width / 2, Window_Height / 2))

    title_card2 = pygame.image.load("Assets\Img\Title_Card2.png").convert_alpha()
    title_card2 = pygame.transform.scale(title_card2,(768,768))
    title_card_rect2  = title_card2.get_frect(center = (Window_Width / 2, Window_Height / 2))

    display_interval = 400  # 1 second interval for switching cards
    last_switch_time = pygame.time.get_ticks()
    show_title_card_2 = False

    while On_Title_Card:
        #? limits the frame rate to 60
        dt = clock.tick(60) / 1000
        screen.fill("#639bff")
    
         # Check if it's time to switch the displayed image
        screen.blit(title_card, title_card_rect)

        current_time = pygame.time.get_ticks()
        if current_time - last_switch_time >= display_interval:
            show_title_card_2 = not show_title_card_2  # Toggle title card
            last_switch_time = current_time

        # Draw the appropriate title card
        if show_title_card_2:
            screen.blit(title_card2, title_card_rect2)
        else:
            screen.blit(title_card, title_card_rect)  
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            elif event.type == pygame.KEYDOWN:
                On_Title_Card = False
        

        pygame.display.update() #* or .flip as flip does only a part of the display while .update does the entire display

def pause_menu():
    dt = clock.tick(60) / 1000
    global Game_Paused
    """Paused_Card = pygame.image.load("Assets\Img\Title_Card1.png").convert_alpha()
    Paused_Card = pygame.transform.scale(Paused_Card,(768,768))
    Paused_Card_rect  = Paused_Card.get_frect(center = (Window_Width / 2, Window_Height / 2))
    """

    while Game_Paused:
        
        font = pygame.font.Font("Assets\Fonts\\alagard.ttf", 75)
        text = font.render("PAUSED", None, (255, 255, 255))  
        text_rect = text.get_rect(center=(Window_Width // 2, Window_Height // 2))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()   
            elif event.type == KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_p]:
                    Game_Paused = False
            
        pygame.display.update() #* or .flip as flip does only a part of the display while .update does the entire display
        
def collisions():
    global Game_Running
    player_dies = pygame.sprite.spritecollide(player_sprite, enemy_sprites, False, pygame.sprite.collide_mask)
    
    if player_dies:
        Game_Running = False
    #? for each snowball if the snowball collides with an enemy sprite kill it
    for snowball in snowball_sprites:
       collided_sprites =  pygame.sprite.spritecollide(snowball, enemy_sprites, True)
       if collided_sprites:
           snowball.kill()

#? setup pygame
pygame.init()
Window_Width, Window_Height = 1280, 768

#? screen size and screen image and junk 
snowman_icon = pygame.image.load("Assets\Img\icons8-snowman-32.png")
pygame.display.set_caption("Summer In December!!!")
pygame.display.set_icon(snowman_icon)
screen = pygame.display.set_mode((Window_Width, Window_Height), pygame.SRCALPHA)

#? importing surface images
Snowball_Surf = pygame.image.load("Assets\Img\Snowball_Projectile.png")
Enemy_Surf = pygame.image.load("Assets\Img\Placeholder.png")
        
#? setting time for the framerate
clock = pygame.time.Clock()

On_Title_Card = True
Game_Running = True
Game_Paused = False
    
#? setting up groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
snowball_sprites = pygame.sprite.Group()
player_sprite = Player(all_sprites)
red_box_sprite = Enemy(Enemy_Surf,(1000, 384), (all_sprites, enemy_sprites))

#? Main Game loop
while Game_Running:
    title_menu()
    
    #? limits the frame rate to 60
    dt = clock.tick(60) / 1000
        
    for event in pygame.event.get():
        if event.type == QUIT:
            Game_Running = False   
        elif event.type == KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_p]:
                Game_Paused = not Game_Paused
                pause_menu()
            
    #? updating the screen
    all_sprites.update(dt)  
    collisions()
    
    #? wipes away last frame
    screen.fill('#639bff')
    all_sprites.draw(screen)
    pygame.display.update() #* or .flip as flip does only a part of the display while .update does the entire display
            
#? closes game properly
pygame.quit()
sys.exit()
        
        
#? groups of sprites so I don't have to do a bunch of shit yada yada read the docs again moron

#! when making multiple sprites that are the same import once and then use a for loop 

