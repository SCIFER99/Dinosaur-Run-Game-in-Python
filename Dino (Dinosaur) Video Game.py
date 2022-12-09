# By: Tim Tarver

# This script is a 2D Video Game called Dino Run! This script consists of adding
# modules such as Pygame, Mixer, Pytest, Display, Image and Transform to
# add effects to the game.

import random
import pygame

import time

# The line below initializes the module to implement the video game!

pygame.init()


# This class will construct the motion of the main character: DINO!

class Dino():
    
    def __init__(self):
        
        self.Img = pygame.image.load("sprites/dino_.png")
        self.WIDTH, self.HEIGHT = 44, 48
        self.Img = pygame.transform.scale(self.Img, (self.WIDTH, self.HEIGHT))
        self.image = self.Img
        self.x = 20
        self.y = 170
        self.g = -0.25 # Gravity
        self.up = 7 # Initial upward velocity
        self.t = 0 # time
        self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)


        self.runImg1 = pygame.image.load("sprites/dino_1.png")
        self.runImg2 = pygame.image.load("sprites/dino_2.png")
        self.runImg1 = pygame.transform.scale(self.runImg1, (self.WIDTH, self.HEIGHT))
        self.runImg2 = pygame.transform.scale(self.runImg2, (self.WIDTH, self.HEIGHT))

        self.duck1 = pygame.image.load("sprites/dino_ducking1.png")
        self.duck2 = pygame.image.load("sprites/dino_ducking2.png")
        self.duck1 = pygame.transform.scale(self.duck1, (self.WIDTH + 15, self.HEIGHT))
        self.duck2 = pygame.transform.scale(self.duck2, (self.WIDTH + 15, self.HEIGHT))
        self.is_ducking = False

        self.duckImgs = [self.duck1, self.duck2]

        self.runImgs = [self.runImg1, self.runImg2]

        self.jump_sound = pygame.mixer.Sound("jump.wav")
        self.count = 0
        self.jumping = False


    def jump(self):
        
        self.y -= self.up # Start jumping
        self.jumping = True
        self.jump_sound.play()

    def update(self):
        
        if self.y < 170: # check if jumping
            self.up = self.up + self.g * self.t # v = u + at
            self.y -= self.up
            self.t += 0.12 #  incrementing time

        if self.y > 170: # check if the jump is complete and resetting all variables
            self.y = 170
            self.t = 0
            self.up = 7
            self.jumping = False

        if self.is_ducking:
            
            self.hitbox = pygame.Rect(self.x + 5, self.y + 20, self.WIDTH + 12, self.HEIGHT - 20)
            self.image = self.duckImgs[int(self.count) % 2]
            self.count += 0.2
            
        elif self.jumping:
            
            self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)
            self.image = self.Img
            
        else:
            
            self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 17, self.HEIGHT - 5)
            self.image = self.runImgs[int(self.count) % 2]
            self.count += 0.15

    def draw(self, screen):
        
        screen.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2) # Comment out if you do not want to see hitbox

class Ptera():
    
    def __init__(self):
        
        self.width, self.height = 50, 40
        self.im1 = pygame.image.load("sprites/ptera1.png")
        self.im2 = pygame.image.load("sprites/ptera2.png")

        self.im1 = pygame.transform.scale(self.im1, (self.width, self.height))
        self.im2 = pygame.transform.scale(self.im2, (self.width, self.height))

        self.flaps = [self.im1, self.im2]

        self.image = self.im1

        self.altitudes = [175, 150, 110]
        self.x = random.randint(750, 1000) # generate a random position for ptera
        self.y = random.choice(self.altitudes)

        self.speed = 5
        self.count = 0
        self.is_ptera = True
        self.is_cactus = False

        self.hitbox = (self.x, self.y + 10, self.width, self.height - 12)


    def update(self):
        
        self.image = self.flaps[int(self.count) % 2] # Flapping mechanism
        self.count += 0.1

        self.x -= self.speed

        if self.x < 50:
            self.allowed = True

        self.hitbox = pygame.Rect(self.x, self.y + 10, self.width, self.height - 12)

    def draw(self, screen):
        
        screen.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2) # Comment out if you do not want the hitbox

class Cactus():
    
    def __init__(self):
        self.image0 = pygame.image.load("sprites/cacti-small.png")
        self.image1 = pygame.image.load("sprites/cacti-big.png")
        self.width0 = 45
        self.height = 44
        self.width1 = 65
        self.image0 = pygame.transform.scale(self.image0, (self.width0, self.height))
        self.image1 = pygame.transform.scale(self.image1, (self.width1, self.height))
        self.is_cactus = True
        self.is_ptera = False

        self.image, self.width = random.choice([[self.image0, self.width0], [self.image1, self.width1]])

        self.x = random.randint(720, 1000)
        self.y = 175
        self.speed = 4

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= self.speed

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Ground():
    
    def __init__(self):
        
        self.ground_length = 1202
        self.image1 = pygame.image.load("sprites/ground.png")
        self.image1_x = 0
        self.image1_y = 200

        #OK Now we need another image of groung as well
        # and this is because our ground will be continoulsy
        # moving towards the left side as we play the game..
        # Now how we gonna show this move to the user.
        # Well, the move will be actually the repitition of 2 images,
        # say it  as image 1 and image 2, so when
        # the first image move toward the left,
        # the other image will appear at its place
        # because we want a continous ground.
        # So let say when the first image will
        # move 10px towards the left then the 2nd image
        # should also move 10px towards the left,

        self.image2 = pygame.image.load("sprites/ground.png")
        self.image2_x = self.image1_x + self.ground_length
        self.image2_y = self.image1_y
        self.speed = 4


    def draw(self, screen):
        
        screen.blit(self.image1, (self.image1_x, self.image1_y))
        screen.blit(self.image2, (self.image2_x, self.image2_y))

    def update(self):
        
        self.image1_x -= self.speed
        self.image2_x -= self.speed

        if self.image1_x + self.ground_length < 0:
            self.image1_x = self.image2_x + self.ground_length
        elif self.image2_x + self.ground_length < 0:
            self.image2_x = self.image1_x + self.ground_length

class Cloud():

    def __init__(self):
        
        self.image = pygame.image.load("sprites/cloud.png")
        self.WIDTH, self.HEIGHT = 70, 40
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.speed = 1
        self.x = 600
        self.y = 50

    def update(self):
        
        self.x -= self.speed

        if self.x < -self.WIDTH:
            self.x = 600
            self.y = random.randint(10, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


def game():
    
    screen = pygame.display.set_mode((700, 250))
    #The first thing we need to do is to create a clock and
    #clock will help us to keep track of time
    #It's also a good idea to create a clock to make sure
    # our program updates at a fixed speed
    # (otherwise it would run at different speed depending
    # on how fast the computer is).
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 20)
    check_point = pygame.mixer.Sound("checkPoint.wav")
    death_sound = pygame.mixer.Sound("die.wav")
    pygame.display.set_caption("Dino Run")

    dino_icon = pygame.image.load("sprites/dino_.png")
    pygame.display.set_icon(dino_icon)

    game_over = pygame.image.load("sprites/game_over.png")
    replay_button = pygame.image.load("sprites/replay_button.png")
    logo = pygame.image.load("sprites/logo.png")
    GREY = (240, 240, 240)
    WHITE = (255, 255, 255)

    ground = Ground()
    dino = Dino()
    cloud = Cloud()

    obstacles = [Cactus()]
    obstacle_start = time.time()
    minimum_time = 1.5

    running = False
    play_game = True
    dead = False
    high_score_value = 0
    FPS = 85

    while play_game:
        
        if not dead:
            
            screen.fill(GREY)
            ground.draw(screen)
            screen.blit(dino.image, (dino.x, dino.y))
            screen.blit(logo, (200, 70))

        pygame.display.update()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()
                play_game = False
                
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    
                    running = True
                    ground = Ground()
                    dino = Dino()
                    obstacles = [Cactus()]
                    obstacle_start = time.time()
                    dead = False
                    running = True
                    score_value = 0


        while running:
            
            clock.tick(FPS) # Controlling Frames Per Second

            score = font.render("Score: " + str(int(score_value)), True, (200, 200, 200))
            score_value += 0.25
            high_score_value = max(high_score_value, score_value)
            high_score = font.render("High Score: " + str(int(high_score_value)), True, (200, 200, 200))
            screen.fill(GREY)

            # Event handling
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        
                        dino.jump()
                        
                    elif event.key == pygame.K_DOWN:
                        
                        dino.is_ducking = True
                        
                elif event.type == pygame.KEYUP:
                    
                    if event.key == pygame.K_DOWN:
                        
                        dino.is_ducking = False

            ground.update()
            ground.draw(screen)

            cloud.update()
            cloud.draw(screen)

            dino.update()
            dino.draw(screen)

            for obstacle in obstacles:
                
                if obstacle.is_cactus:
                    
                    obstacle.speed = ground.speed
                    
                elif obstacle.is_ptera:
                    
                    obstacle.speed = ground.speed + 1
                    
                obstacle.update()
                obstacle.draw(screen)

            screen.blit(score, (550, 30))
            screen.blit(high_score, (350, 30))

            # Add new obstacle
            
            if time.time() - obstacle_start > minimum_time + random.randrange(0, 30) / 10:
                print(time.time() - obstacle_start)


                obstacle_start = time.time()
                
                if score_value > 500.0:
                    ptera_probability = random.random() # Generate a random float from 0 to 1.0
                    if ptera_probability > 0.5: # 20% probability that ptera is spawned
                        obstacles.append(Ptera())
                        obstacles[-1].speed = ground.speed + 1
                    else:
                        obstacles.append(Cactus()) # 80% probability of a cactus (duh)
                        obstacles[-1].speed = ground.speed # Synchronise the speed
                else:
                    obstacles.append(Cactus())
                    obstacles[-1].speed = ground.speed

            if int(score_value) > 0 and int(score_value) % 100 == 0 and int(score_value) % 3 == 0: # Increase game speed after score crosses a multiple of 300

                ground.speed += 0.25
                for obstacle in obstacles:
                    if obstacle.is_cactus:
                        obstacle.speed = ground.speed
                    elif obstacle.is_ptera:
                        obstacle.speed = ground.speed + 1

            if score_value > 1 and score_value % 100 == 0: # Checkpoint sound after score crosses a multiple of 100

                check_point.play()

            if dino.hitbox.colliderect(obstacles[0].hitbox): # Collision detection with closest cactus

                death_sound.play()
                dead = True
                screen.blit(game_over, (170, 70))
                screen.blit(replay_button, (340, 100))

            #print(obstacles)
                
            if obstacles[0].x < -30:
                
                obstacles.pop(0)
                
                if obstacles == []:
                    
                    obstacles.append(Cactus())
                    obstacle_start = time.time()

            pygame.display.update()

            if dead:
                
                del dino
                del ground
                del obstacles
                running = False

game()
