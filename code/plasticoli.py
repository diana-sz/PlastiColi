# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 21:29:42 2022

@author: dajas
"""

import os
import pygame
import random
from itertools import compress
pygame.font.init()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PlastiColi")

BACKGROUND = (6, 63, 120)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BORDER = pygame.Rect(0, 0, WIDTH, HEIGHT//10)


FPS = 60  # frames per second for updating of screen
VEL = 4  # velocity
VIRUS_VEL = 6
PLASTIC_VEL = 5
PLASMID_VEL = 1
ECOLI_WIDTH, ECOLI_HEIGTH = 120, 50
VIRUS_WIDTH, VIRUS_HEIGTH = 35, 35

HEALTH_FONT = pygame.font.SysFont('arial', 40)
DEAD_FONT = pygame.font.SysFont('arial', 100)

# Define events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

ADDPLASTIC = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLASTIC, 500)

ADDPLASMID = pygame.USEREVENT + 3
pygame.time.set_timer(ADDPLASMID, 4000)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(
            os.path.join('media', 'ecoli.png'))
        self.surf = pygame.transform.scale(self.surf, 
                                           (ECOLI_WIDTH, ECOLI_HEIGTH))
        self.rect = self.surf.get_rect(topleft=(0, BORDER.height))
        self.health = 100
        self.plastic_eaten = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP] and self.rect.y - VEL > 0 + BORDER.height:
            self.rect.move_ip(0, -VEL)
        if pressed_keys[K_DOWN] and self.rect.y + VEL + self.rect.height < HEIGHT:
            self.rect.move_ip(0, VEL)
        if pressed_keys[K_LEFT] and self.rect.x - VEL > 0:
            self.rect.move_ip(-VEL, 0)
        if pressed_keys[K_RIGHT] and self.rect.x + VEL +  self.rect.width < WIDTH:
            self.rect.move_ip(VEL, 0) 
 
    def subtract_health(self):
        self.health -= 10
        
    def add_health(self, value):
        self.health += value
        
    def eat_plastic(self):
        self.plastic_eaten += 1
        self.add_health(1)
        
    def incorporate_plasmid(self):
        # random temporary advantage -- resistance to virus, double health, more plastic eaten...
        pass
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(
            os.path.join('media', 'virus.png'))
        self.surf = pygame.transform.scale(self.surf, 
                                           (VIRUS_WIDTH, VIRUS_HEIGTH))
        self.rect = self.surf.get_rect(
            topleft=(
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint(0 + BORDER.height, HEIGHT),
            )
        )
        self.speed = VIRUS_VEL

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# todo - enemy subclasses, plastic subclasses

class Plastic(pygame.sprite.Sprite):
    def __init__(self):
        super(Plastic, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((100, 150, 255))
        self.rect = self.surf.get_rect(
            topleft=(
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint(0 + BORDER.height, HEIGHT),
            )
        )
        self.speed = PLASTIC_VEL

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Plasmid(pygame.sprite.Sprite):
    def __init__(self):
        super(Plasmid, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((200, 150, 200))
        self.rect = self.surf.get_rect(
            topleft=(
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint(0 + BORDER.height, HEIGHT),
            )
        )
        self.speed = PLASMID_VEL

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()



def draw_window(player, all_sprites):
    WINDOW.fill(BACKGROUND)
    pygame.draw.rect(WINDOW, WHITE, BORDER)

    health_text = HEALTH_FONT.render(f"Health: {player.health}", 1, BLACK)
    WINDOW.blit(health_text, (WIDTH-health_text.get_width()-10, 0))

    
    # Draw all sprites
    for entity in all_sprites:
        WINDOW.blit(entity.surf, entity.rect)

    pygame.display.update()            




def ecoli_change_direction(keys_pressed, BASIC_ECOLI, angle=0):
    arrows_pressed_bool = [keys_pressed[K_LEFT], keys_pressed[K_RIGHT], 
                           keys_pressed[K_UP], keys_pressed[K_DOWN]]
    
    directions = [180, 0, 90, 270]
    if keys_pressed[K_DOWN]:
        directions = [180, 360, 90, 270]
    arrows_pressed = list(compress(directions, arrows_pressed_bool))
    
    if len(arrows_pressed) in [1,2]:
        angle = sum(arrows_pressed)/sum(arrows_pressed_bool)

    
    #angle = np.mean(arrows_pressed)
    
# if keys_pressed[K_LEFT] and keys_pressed[K_UP]:
# angle = 225
# elif keys_pressed[K_LEFT]:  # left
# angle = 180
# elif keys_pressed[K_UP]:  # up
# angle = 90 


# elif keys_pressed[K_RIGHT]:  # right
# angle = 0     

# if keys_pressed[K_DOWN]:  # down
# angle = 270 
        
    return pygame.transform.rotate(BASIC_ECOLI, angle)


def bacteria_is_dead(text):
    draw_text = DEAD_FONT.render(text, 1, BLACK)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, 
                            HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    player = Player()
    enemies = pygame.sprite.Group()
    plastics = pygame.sprite.Group()
    plasmids = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # control speed of while loop
        for event in pygame.event.get():
            
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    run = False
                    pygame.quit()
                        
            elif event.type == QUIT:
                run = False
                pygame.quit()
                
            if event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                
            if event.type == ADDPLASTIC:
                new_plastic = Plastic()
                plastics.add(new_plastic)
                all_sprites.add(new_plastic)

            if event.type == ADDPLASMID:
                new_plasmid = Plasmid()
                plasmids.add(new_plasmid)
                all_sprites.add(new_plasmid)
        
        if player.health <= 0:
            dead_text = "You are dead"
            bacteria_is_dead(dead_text)
            break


        keys_pressed = pygame.key.get_pressed()
    
        player.update(keys_pressed)
        enemies.update()
        plastics.update()
        plasmids.update()
        
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                player.subtract_health()
                enemy.kill()
                
        for plastic in plastics:
            if pygame.sprite.collide_rect(player, plastic):
                player.eat_plastic()
                plastic.kill()

        for plasmid in plasmids:
            if pygame.sprite.collide_rect(player, plasmid):
                player.incorporate_plasmid()
                plasmid.kill()

        draw_window(player, all_sprites)
    


    main()


if __name__ == "__main__":
    main()