import pygame
import math
import random
import threading
from datetime import datetime
import glob
import re

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Main():
    def __init__(self, Dimensions = 1000):
        self.Dimensions = Dimensions
        self.display = pygame.display.set_mode((self.Dimensions, self.Dimensions))
        pygame.font.init()
        self.font = pygame.font.SysFont("calibri", 30)
        pygame.display.set_caption("Asteroid Game ")
        self.fps = 60
        self.clock = pygame.time.Clock()
        pygame.init()

    def start(self):
        Scorescreen = True
        running = True
        self.character = Player()
        self.handler = EventHandler()
        self.scoreboard = Scoreboard()

        self.display = pygame.display.set_mode((self.Dimensions, self.Dimensions))
        pygame.event.set_blocked(1024) # mouse movement
        pygame.event.set_blocked(1025) # mouse movement
        pygame.event.set_blocked((32784)) # mouse out of window

        while running:
            self.event_list = pygame.event.get()
            for self.event in self.event_list:
                if self.event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_ESCAPE:
                        Scorescreen = True
            white = [255, 255, 255]
            self.display.fill(white)
            self.clock.tick(self.fps)
            while Scorescreen:
                self.display.fill(white)
                self.event_list = pygame.event.get()
                for self.event in self.event_list:
                    if self.event.type == pygame.QUIT:
                        pygame.display.quit()
                        pygame.quit()
                        quit()

                    if self.event.type == pygame.KEYDOWN:
                        if self.event.key == pygame.K_RETURN:
                            Scorescreen = False

                self.scoreboard.show_past_scores()
                pygame.display.flip()

                self.clock.tick(self.fps)

            ####Character Updates
            self.display_sprite(self.character.image, self.character.x, self.character.y,
                                self.character.looking_directions, 100)
            self.character.detect_events()

            ####Bullet Updates
            self.character.move_bullets()
            self.character.reduce_countdown()
            self.display_bullets()

            ####Asteroid Updates
            self.handler.spawn()
            self.handler.update()
            self.detect_asteroid_death()
            self.detect_player_death()

            ####Displays Data
            self.display_fps()
            self.display_asteroid_count()
            self.display_bullets_count()
            self.display_score()

            pygame.display.flip()

    def display_asteroid_count(self):
        asteroids = (str(len(self.handler.asteroid_list)) + " Asteroids roaming around")
        count_text = self.font.render(asteroids, True, pygame.Color("coral"))
        self.display.blit(count_text, (360, 0))

    def display_bullets_count(self):
        bullets = (str(len(self.character.bullets_list)) + " Bullets in play")
        bullets_text = self.font.render(bullets, True, pygame.Color("coral"))
        self.display.blit(bullets_text, (10, 0))

    def get_hitbox_list(self, x, y, length):
        # x is centre of hitbox of asteroid
        # y is centre of hitbox of asteroid
        # range is whole size of hitbox as a square
        x_range = []
        y_range = []
        x = round(x)
        y = round(y)
        length = round(length*0.5) # 0.4 seems to be perfect amount for a decent hitbox
        low_x = x - length
        low_y = y - length
        high_y = y + length
        high_x = x + length

        if low_x < 0:
            x_range.extend(list(range(0, high_x)))
            x_range.extend(list(range(low_x + Game.Dimensions, Game.Dimensions)))
        elif high_x > Game.Dimensions:
            x_range.extend(list(range(low_x, Game.Dimensions)))
            x_range.extend(list(range(0, high_x - Game.Dimensions)))
        else:
            x_range.extend(list(range(low_x, high_x)))

        if low_y < 0:
            y_range.extend(list(range(0, high_y)))
            y_range.extend(list(range(low_y + Game.Dimensions, Game.Dimensions)))
        elif high_y > Game.Dimensions:
            y_range.extend(list(range(low_y, Game.Dimensions)))
            y_range.extend(list(range(0, high_y - Game.Dimensions)))
        else:
            y_range.extend(list(range(low_y, high_y)))
        return (list(x_range), list(y_range))


    def detect_player_death(self):

        for asteroid in range(0, len(self.handler.asteroid_list)):
            try:
                asteroid_hitbox = self.get_hitbox_list(self.handler.asteroid_list[asteroid].x,
                                               self.handler.asteroid_list[asteroid].y,
                                               self.handler.asteroid_list[asteroid].size / 2)
                hitbox_of_asteroid_x, hitbox_of_asteroid_y = asteroid_hitbox[0], asteroid_hitbox[1]
                character_hitbox = self.get_hitbox_list(self.character.x, self.character.y, self.character.size)
                char_x, char_y = character_hitbox[0], character_hitbox[1]
            except:
                pass



            if any(y in hitbox_of_asteroid_y for y in char_y):
                if any(x in hitbox_of_asteroid_x for x in char_x):
                    if self.scoreboard.get_score() > 100:
                        self.scoreboard.text_score()
                        self.scoreboard.remove_score(100)
                        self.restart = False
                    else:
                        self.scoreboard.text_score()
                        self.lose_screen()




    def detect_asteroid_death(self):
        try:
            for asteroid in range(len(self.handler.asteroid_list)):
                for bullet in range(len(self.character.bullets_list)):

                    asteroid_hitbox = self.get_hitbox_list(self.handler.asteroid_list[asteroid].x, self.handler.asteroid_list[asteroid].y, self.handler.asteroid_list[asteroid].size/2)
                    hitbox_of_asteroid_x, hitbox_of_asteroid_y = asteroid_hitbox[0], asteroid_hitbox[1]
                    bullet_hitbox = self.get_hitbox_list(self.character.bullets_list[bullet].x, self.character.bullets_list[bullet].y, self.character.bullets_list[bullet].size/2)
                    hitbox_of_bullet_x, hitbox_of_bullet_y = bullet_hitbox[0], bullet_hitbox[1]


                    #print((hitbox_of_bullet_x, hitbox_of_bullet_y))
                    #print((self.handler.asteroid_list[asteroid].x, self.handler.asteroid_list[asteroid].y))
                    ### x and y are both matching. Issue is with the "any()" function.

                    if any(y in hitbox_of_bullet_y for y in hitbox_of_asteroid_y):
                        if any(x in hitbox_of_bullet_x for x in hitbox_of_asteroid_x):
                            del self.handler.asteroid_list[asteroid]
                            del self.character.bullets_list[bullet]
                            self.scoreboard.add_score(15)
                            break
        except Exception as E:

            print(E)
            print("yer")

    def display_fps(self):  # Displays current FPS
        fps_counter = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps_counter, True, pygame.Color("coral"))
        self.display.blit(fps_text, (965, 0))

    def display_sprite(self, picture, x, y, orientation, size):
        image = pygame.image.load(picture)
        image.convert_alpha()
        image = pygame.transform.scale(image, (size, size))
        image = rot_center(image, orientation)
        self.display.blit(image, (x, y))

    def display_bullets(self):
        for bullet in self.character.bullets_list:
            self.display.blit(bullet.image, (bullet.x, bullet.y))

    def display_score(self):
        score_text = (str(self.scoreboard.get_score()) + " Points")
        score_text = self.font.render(score_text, True, pygame.Color("coral"))
        self.display.blit(score_text, (750, 0))


class Player:
    def __init__(self):
        self.size = 100
        self.Dimensions = Game.Dimensions
        self.x = self.Dimensions / 2
        self.y = self.Dimensions / 2
        self.looking_directions = 0
        self.velocity = 0
        self.image = "Pictures/Player.png"
        self.bullet_countdown = 0
        self.left_button_down = False
        self.right_button_down = False
        self.button_down = False
        self.moving = False
        self.bullets_list = []

    def stop(self):
        self.velocity *= 0.97


    def move(self):
        bearing = 360 - self.looking_directions
        bearing = bearing % 360
        if self.velocity >= 4:
            pass
        elif self.moving:
            self.velocity += 0.05

        if 0 <= bearing <= 90:
            self.x += self.velocity * math.sin(math.radians(bearing))
            self.y -= self.velocity * math.cos(math.radians(bearing))
        elif 90 <= bearing <= 180:
            self.x += self.velocity * math.sin(math.radians(bearing))
            self.y -= self.velocity * math.cos(math.radians(bearing) * -1)
        elif 180 <= bearing <= 270:
            bearing -= 180
            self.x -= self.velocity * math.sin(math.radians(bearing))
            self.y += self.velocity * math.cos(math.radians(bearing))
        elif 270 <= bearing <= 360:
            bearing -= 180
            self.x -= self.velocity * math.sin(math.radians(bearing))
            self.y += self.velocity * math.cos(math.radians(bearing) * -1)

        if self.x > Game.Dimensions:
            self.x = 0
        if self.x < 0:
            self.x = Game.Dimensions

        if self.y > Game.Dimensions:
            self.y = 0
        if self.y < 0:
            self.y = Game.Dimensions

    def reduce_countdown(self):
        self.bullet_countdown -= 1

    def shoot(self):
        if len(self.bullets_list) < 4:
            if self.bullet_countdown <= 0:
                self.new_bullet = bullet(self)
                self.bullets_list.append(self.new_bullet)
                self.bullet_countdown = 30
                print("shot a bullet")
            else:
                self.bullet_countdown -= 1
        else:
            print("max bullets")

    def detect_events(self): #### all movements
        if self.left_button_down == True:
            self.turn_left()
        if self.right_button_down == True:
            self.turn_right()
        if self.button_down == True:
            self.stop()
        if self.moving == True:
            self.move()

        else:
            pass
            self.velocity *= 0.99
            if self.velocity < 0.1:
                self.velocity = 0
            self.move()

        self.event_list = Game.event_list
        for self.event in self.event_list:
            if self.event.type == pygame.KEYUP :
                if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                    self.left_button_down = False
                if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                    self.right_button_down = False
                if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                    self.moving = False
                if self.event.key == pygame.K_s or self.event.key == pygame.K_DOWN:
                    self.button_down = False

                if self.event.key == pygame.K_SPACE:
                    self.shoot()


            elif self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                    x = threading.Thread(target=self.turn_left)
                    x.start()
                    self.left_button_down = True
                if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                    y = threading.Thread(target=self.turn_right)
                    y.start()
                    self.right_button_down = True
                if self.event.key == pygame.K_DOWN or self.event.key == pygame.K_s:
                    s = threading.Thread(target = self.stop)
                    s.start()
                    self.button_down = True
                if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                    z = threading.Thread(target=self.move)
                    z.start()
                    self.moving = True
        try:
            x.join()
            y.join()
            z.join()
        except:
            pass



    def turn_left(self):
        self.looking_directions += 2

    def turn_right(self):
        self.looking_directions -= 2

    def move_bullets(self):
        for bullet in self.bullets_list:
            bullet.move()

class Asteroids():
    def __init__(self):
        self.size = random.randint(90, 110)
        self.x = random.choice(list(range(0, int(Game.Dimensions / 4))) + list(range(int(Game.Dimensions * (3 / 4)), Game.Dimensions)))
        self.y = random.choice(list(range(0, int(Game.Dimensions / 4))) + list(range(int(Game.Dimensions * (3 / 4)), Game.Dimensions)))
        self.velocity = random.choice([0.9,1,1.1,1.2])
        self.looking_direction = random.randrange(0, 360)
        self.picture = "Pictures/Asteroids.png"
        size = 75
        self.image = pygame.image.load(self.picture)
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = rot_center(self.image, self.looking_direction)

    def get_orientation(self):
        return self.looking_direction

    def get_size(self):
        return self.size

    def get_pic(self):
        return self.picture

    def get_xy(self):
        return self.x, self.y

    def Update(self):
        Game.display.blit(self.image, (self.x, self.y))

    def Drift(self):
        bearing = 360 - self.looking_direction
        bearing = bearing % 360

        if 0 <= bearing <= 90:
            self.x += self.velocity * math.sin(math.radians(bearing))

            self.y -= self.velocity * math.cos(math.radians(bearing))

        elif 90 <= bearing <= 180:
            self.x += self.velocity * math.sin(math.radians(bearing))

            self.y -= self.velocity * math.cos(math.radians(bearing) * -1)
        elif 180 <= bearing <= 270:
            bearing -= 180
            self.x -= self.velocity * math.sin(math.radians(bearing))

            self.y += self.velocity * math.cos(math.radians(bearing))
        elif 270 <= bearing <= 360:
            bearing -= 180
            self.x -= self.velocity * math.sin(math.radians(bearing))

            self.y += self.velocity * math.cos(math.radians(bearing) * -1)#

        if self.x < 0 - self.size:
            self.x += Game.Dimensions
        if self.x > Game.Dimensions:
            self.x -= Game.Dimensions

        if self.y < 0:
            self.y += Game.Dimensions
        if self.y > Game.Dimensions:
            self.y -= Game.Dimensions

class EventHandler():
    def __init__(self):
        self.asteroid_list = []
        self.tick = 0
        self.asteroid_cap = 15

    def spawn(self):
        self.tick += 1
        if len(self.asteroid_list) >= self.asteroid_cap:
            self.tick -= 1
        elif self.tick >= 60:
            temp_asteroid = Asteroids()
            self.asteroid_list.append(temp_asteroid)
            #print("Asteroid created: " + str(len(self.asteroid_list)) + " currently alive")
            self.tick = 0
            del temp_asteroid

    def update(self):
        for current in self.asteroid_list:
            current.Drift()
            current.Update()

class Scoreboard():
    def __init__(self):
        self.score = 0
        time = datetime.now()
        time = time.strftime("%d.%m.%Y_%H%M%S")
        self.filename = "Scores/" + str(time) + ".txt"
        print("Creating " + self.filename)
        self.score_file = open(self.filename, "w+")

    def remove_score(self, removing):
        self.score -= removing

    def get_score_file(self):
        return self.score_file

    def get_score(self):
        return self.score

    def add_score(self, added):
        self.score += added

    # create function to get all data from file
    def get_data(self):
        all = []
        for i in range(0, len(glob.glob("Scores/*.txt"))):
            self.score_file = open(glob.glob("Scores/*.txt")[i], "r")
            temp = self.score_file.read()
            print(temp)
            all.append(temp)
        if len(all) == 0:
            return False
        return all

    #create function to get only integers from function get_data
    def get_integers(self):
        all = self.get_data()
        if all == False:
            return False

        integers = []
        for i in range(0, len(all)):
            if all[i].isdigit():
                integers.append(all[i])
        return integers

    #create function to get only last three letters from function get_data
    def get_last_3_letters(self):
        all = self.get_data()
        if all == False:
            return False
        letters = []
        for i in range(0, len(all)):
            if all[i].isalpha():
                letters.append(all[i])

        return letters[-3:]

    def show_past_scores(self):
        points = self.get_integers()
        name = self.get_last_3_letters()
        if points == False:
            text = "No scores yet"
            Game.display.blit(text, (400, 500))
            return
        if name == False:
            text = Game.font.render("No scores yet", True, (pygame.color("coral")))
            Game.display.blit(text, (400, 500))
            return
        for i in range(0, len(points)):
                current_points = Game.font.render(points[i], True, pygame.Color("coral"))
                current_name = Game.font.render(name[i], True, pygame.Color("coral"))
                Game.display.blit(current_points, (300, 500 + (i * 50)))
                Game.display.blit(current_name, (500, 500 + (i * 50)))



class bullet(Player):
    def __init__(self, character):

        self.looking_directions = character.looking_directions
        picture = "Pictures/bullet.png"
        self.size = 15
        self.x = character.x
        self.y = character.y
        self.image = pygame.image.load(picture)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = rot_center(self.image, self.looking_directions)
        self.velocity = 6


    def update(self):
        pygame.blit(self.image)

    def move(self):
        bearing = 360 - self.looking_directions
        bearing = bearing % 360

        if 0 <= bearing <= 90:
            self.x += self.velocity * math.sin(math.radians(bearing))

            self.y -= self.velocity * math.cos(math.radians(bearing))

        elif 90 <= bearing <= 180:
            self.x += self.velocity * math.sin(math.radians(bearing))

            self.y -= self.velocity * math.cos(math.radians(bearing) * -1)
        elif 180 <= bearing <= 270:
            bearing -= 180
            self.x -= self.velocity * math.sin(math.radians(bearing))

            self.y += self.velocity * math.cos(math.radians(bearing))
        elif 270 <= bearing <= 360:
            bearing -= 180
            self.x -= self.velocity * math.sin(math.radians(bearing))

            self.y += self.velocity * math.cos(math.radians(bearing) * -1)

        if self.x > Game.Dimensions:
            self.x = 0
        if self.x < 0:
            self.x = Game.Dimensions

        if self.y > Game.Dimensions:
            self.y = 0
        if self.y < 0:
            self.y = Game.Dimensions

if __name__ == "__main__":
    Game = Main()
    Game.start()
