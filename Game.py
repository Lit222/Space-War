import pygame as pg
import random as rand

pg.init()

size = screen_width, screen_height = 900, 497
screen = pg.display.set_mode(size)

pg.display.set_caption("Space War")
pg.display.set_icon(pg.image.load('static/img/icon.png'))
clock = pg.time.Clock()

boom_sound = pg.mixer.Sound('static/sound/boom.mp3')
button_sound = pg.mixer.Sound('static/sound/button.mp3')
wow_sound = pg.mixer.Sound('static/sound/wow.mp3')
arm_sound = pg.mixer.Sound('static/sound/arm.mp3')

meteor_img = [pg.image.load('static/img/meteor1.png'), pg.image.load('static/img/meteor2.png'), pg.image.load('static/img/meteor3.png'), pg.image.load('static/img/meteor4.png')]
meteor_options = [48, 42, 55, 52, 30, 31, 18, 26]

arm_img = pg.image.load('static/img/arm.png')
enemy_arm_img = pg.image.load('static/img/enemy_arm.png')

enemy1_img = pg.image.load('static/img/enemy1.png')
enemy2_img = pg.image.load('static/img/enemy2.png')
enemy3_img = pg.image.load('static/img/enemy3.png')
enemy4_img = pg.image.load('static/img/enemy4.png')
enemy5_img = pg.image.load('static/img/enemy5.png')

boss1_img = pg.image.load('static/img/boss1.png')
boss2_img = pg.image.load('static/img/boss2.png')

planet1_img = pg.image.load('static/img/planet_1.png')
planet2_img = pg.image.load('static/img/planet_2.png')
planet3_img = pg.image.load('static/img/planet_3.png')
planet4_img = pg.image.load('static/img/planet_4.png')
planet5_img = pg.image.load('static/img/planet_5.png')
planet6_img = pg.image.load('static/img/planet_6.png')
planet7_img = pg.image.load('static/img/planet_7.png')
planet8_img = pg.image.load('static/img/planet_8.png')
planet9_img = pg.image.load('static/img/planet_9.png')

player_img = [pg.image.load('static/img/up_player.png'), pg.image.load('static/img/player.png'), pg.image.load('static/img/down_player.png')]
player_width = 36
player_height = 39
player_x = 32
player_y = 384
speed = 4
player_up = False
player_down = False

cooldown = 0
level_time = 0
meteor_fly = False

class Arm:
        def __init__(self, x, y, image):
                self.image = image
                self.x = x
                self.y = y
                self.speed = 3
        
        def arm_move(self):
                self.x += self.speed
                if self.x <= screen_width:
                        screen.blit(self.image, (self.x, self.y))
                        return True
                else:
                        return False

class Enemy_arm():
        def __init__(self, x, y, image):
                self.image = image
                self.x = x
                self.y = y
                self.speed = 3
        
        def enemy_arm_move(self):
                self.x -= self.speed

                if self.x >= 0:
                        screen.blit(self.image, (self.x, self.y))
                        return True
                else:
                        return False

class Button:
        def __init__(self, width, height):
                self.width = width
                self.height = height

        def draw(self, x, y, message, sound, action = None, font_size = 30, font_color = (255, 0, 255)):
                mouse = pg.mouse.get_pos()
                click = pg.mouse.get_pressed()

                if x < mouse[0] < x + self.width and y < mouse[1] < y + self. height:
                        if click[0] == 1:
                                pg.mixer.Sound.play(sound)
                                pg.time.delay(300)
                                if action is not None:
                                        if action == quit:
                                                pg.quit()
                                        else:
                                                action()
                
                print_text(message = message, x = x + 10, y = y + 10, font_size = font_size, font_color = font_color)

class Star:
    def __init__(self):
        self.x = rand.randrange(screen_width)
        self.y = rand.randrange(screen_height)
        self.s_color = (rand.randrange(255), rand.randrange(255), rand.randrange(255))
        self.flag = rand.choice([True, False])
 
    def draw(self):
        pg.draw.circle(screen, self.s_color, [self.x, self.y], 1)
 
    def blinking(self):
        if self.flag:
            self.s_color = (rand.randrange(255), rand.randrange(255), rand.randrange(255))

class Meteor:
        def __init__(self, x, y, width, height, image, speed):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.image = image
                self.speed = speed
        
        def move(self):
                if self.x >= -self.width:
                        screen.blit(self.image, (self.x, self.y))
                        self.x -= self.speed
                        return True
                else:
                        return False

        def return_self(self, radius, y, width, height, image):
                self.x = radius
                self.y = y
                self.width = width
                self.height = height
                self.image = image
                screen.blit(self.image, (self.x, self.y))

class Enemy:
        def __init__(self, away_y, image, width, height, speed, shoot_speed, health, boss = False):
                self.image = image
                self.width = width
                self.height = height
                self.x = rand.randrange(550, 850)
                self.y = away_y
                self.away_y = away_y
                self.speed = speed
                self.dest_y = 3 * rand.randrange(30, 150)
                self.cd_hide = 0
                self.come = True
                self.destroy = False
                self.cd_shoot = 0
                self.all_arms = []
                self.shoot_speed = shoot_speed
                self.boss = boss
                
                if self.boss:
                        self.dest_y = 80
                        self.x = 600

                self.health = health
                self.health_rerun = 0
                self.health_weak = 1
                self.health_medium = 2
                self.health_strong = 5
                self.health_boss = 100
                self.health_big_boss = 1000

                if self.health == 1:
                        self.health_rerun = self.health_weak
                elif self.health == 2:
                        self.health_rerun = self.health_medium
                elif self.health == 3:
                        self.health_rerun = self.health_strong
                elif self.health == 4:
                        self.health_rerun = self.health_boss
                elif self.health == 5:
                        self.health_rerun = self.health_big_boss

        def draw(self):
                
                screen.blit(self.image, (self.x, self.y))
                
                if self.come and self.cd_hide == 0:
                        return 1
                elif self.destroy:
                        return 2
                elif self.cd_hide > 0:
                        self.cd_hide -= 1

                return 0

        def show(self):
                if self.y < self.dest_y:
                        self.y += self.speed
                else:
                        self.come = False
                        self.dest_y = self.away_y

        def dest(self):
                self.y = -100
                self.come = True
                self.destroy = False
                self.x = rand.randrange(550, 850)
                self.dest_y = 3 * rand.randrange(30, 150)
                self.cd_hide = 80
                if self.boss:
                        self.y = -900
                        self.come = False

        def check_dmg(self, arm):
                if self.health == 1:
                        if self.x <= arm.x <= self.x + self.width:
                                if self.y <= arm.y <= self.y + self.height:
                                        self.health_weak -= 1

                        if self.health_weak == 0:  
                                self.destroy = True
                                self.health_weak = self.health_rerun
                        elif self.health_weak > 0: 
                                self.destroy = False
                elif self.health == 2:
                        if self.x <= arm.x <= self.x + self.width:
                                if self.y <= arm.y <= self.y + self.height:
                                        self.health_medium -= 1

                        if self.health_medium == 0:  
                                self.destroy = True
                                self.health_medium = self.health_rerun
                        elif self.health_medium > 0: 
                                self.destroy = False

                elif self.health == 3:
                        if self.x <= arm.x <= self.x + self.width:
                                if self.y <= arm.y <= self.y + self.height:
                                        self.health_strong -= 1

                        if self.health_strong == 0:  
                                self.destroy = True
                                self.health_strong = self.health_rerun
                        elif self.health_strong > 0: 
                                self.destroy = False

                elif self.health == 4:
                        if self.x <= arm.x <= self.x + self.width:
                                if self.y <= arm.y <= self.y + self.height:
                                        self.health_boss -= 1

                        if self.health_boss > 0: 
                                self.destroy = False
                        elif self.health_boss == 0:
                                self.destroy = True
                                self.health_boss = self.health_rerun
                
                elif self.health == 5:
                        if self.x <= arm.x <= self.x + self.width:
                                if self.y <= arm.y <= self.y + self.height:
                                        self.health_big_boss -= 1

                        if self.health_big_boss == 0:  
                                self.destroy = True
                                self.health_big_boss = self.health_rerun
                        elif self.health_big_boss > 0: 
                                self.destroy = False

                if self.boss:
                        if self.destroy:
                                return True

        def shoot(self):
                if not self.cd_shoot:
                        new_arm = Enemy_arm(self.x, self.y, enemy_arm_img)
                        
                        self.all_arms.append(new_arm)
                        self.cd_shoot = 200 - self.shoot_speed
                else:
                        self.cd_shoot -= 1

                for arm in self.all_arms:
                        if not arm.enemy_arm_move():
                                self.all_arms.remove(arm)

        def player_shoot(self):
                for arm in self.all_arms:
                        if player_x <= arm.x <= player_x + player_width:
                                if player_y <= arm.y <= player_y + player_height:
                                        return True
                return False

def create_meteors(array):
        choice = rand.randrange(0, 4)
        img = meteor_img[choice]
        width = meteor_options[choice * 2]
        y = meteor_options[choice * 2 + 1]
        height = rand.randrange(35, 450)
        array.append(Meteor(screen_width + 20, height, width, y, img, 4))

        choice = rand.randrange(0, 4)
        img = meteor_img[choice]
        width = meteor_options[choice * 2]
        y = meteor_options[choice * 2 + 1]
        height = rand.randrange(35, 450)
        array.append(Meteor(screen_width + 300, height, width, y, img, 4))

        choice = rand.randrange(0, 4)
        img = meteor_img[choice]
        width = meteor_options[choice * 2]
        y = meteor_options[choice * 2 + 1]
        height = rand.randrange(35, 450)
        array.append(Meteor(screen_width + 600, height, width, y, img, 4))

        choice = rand.randrange(0, 4)
        img = meteor_img[choice]
        width = meteor_options[choice * 2]
        y = meteor_options[choice * 2 + 1]
        height = rand.randrange(35, 450)
        array.append(Meteor(screen_width + 900, height, width, y, img, 4))

def find_radius(array): 
        maximum = max(array[0].x, array[1].x, array[2].x, array[3].x)
        if maximum < screen_width:
                radius = screen_width
                if radius - maximum < 50:
                        radius += 150
        else:
                radius = maximum
        choise = rand.randrange(0, 5)
        if choise == 0:
                radius += rand.randrange(10,15)
        else:
                radius += rand.randrange(200, 350)

        return radius

def draw_array(array):
        for meteor in array:
                check = meteor.move()
                if not check:
                        radius = find_radius(array)

                        choice = rand.randrange(0, 4)
                        img = meteor_img[choice]
                        width = meteor_options[choice * 2]
                        height = meteor_options[choice * 2 + 1]
                        y = rand.randrange(35, 450)
                        meteor.return_self(radius, y, width, height, img)

def check_collision(barriers):
        for barrier in barriers:
                if barrier.y <= player_y <= barrier.y + barrier.height:
                        if barrier.x <= player_x <= barrier.x + barrier.width:
                                return True
                        elif barrier.x <= player_x + player_width <= barrier.x + barrier.width:
                                return True
                elif barrier.y <= player_y + player_height <= barrier.y + barrier.height:
                        if barrier.x <= player_x <= barrier.x + barrier.width:
                                return True
                        elif barrier.x <= player_x + player_width <= barrier.x + barrier.width:
                                return True
        return False

def draw_enemy(enemys):
        for enemy in enemys:
                action = enemy.draw()
                if action == 1:
                        enemy.show()
                elif action == 2:
                        enemy.dest()
                else:
                        enemy.shoot()

def check_enemy_dmg(arms, enemys):
        for arm in arms:
                for enemy in enemys:
                        enemy.check_dmg(arm)
                        if enemy.check_dmg(arm):
                                return True
        return False

def check_player_dmg(enemys):
        for enemy in enemys:
                if enemy.player_shoot():
                        return True
        return False

def print_text(message, x, y, font_color = (192, 192, 192), font_type = 'static/ttf/pobeda-bold1.ttf', font_size = 30):
        font_type = pg.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color)
        screen.blit(text, (x, y))

def count_time(meteors):
        global level_time, meteor_fly

        if not meteor_fly:
                for meteor in meteors:
                        if meteor.x <= player_x + player_width / 2 <= player_x + player_width:
                                
                                        meteor_fly = True
                                        break
        else:
                level_time += 1
                meteor_fly = False
                                

def show_menu():
        menu_bg = pg.image.load('static/img/space war.png')

        start_btn = Button(300,70)
        quit_btn = Button(300, 90)

        pg.mixer.music.load('static/sound/Kudinov Dmitry - Sempai.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        show = True
        while show:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                show = False
                                pg.quit()

                screen.blit(menu_bg, (0, 0))

                start_btn.draw(150,200, 'Start game', button_sound, maps_menu, font_size = 50, font_color = (0, 246, 255))
                quit_btn.draw(150, 300, 'Quit game', button_sound, quit, font_size = 50, font_color = (0, 246, 255))

                pg.display.update()
                clock.tick(60)

def maps_menu():
        maps_bg = pg.image.load('static/img/maps.png')

        start_btn = Button(180,70)
        start1_btn = Button(190,70)
        start2_btn = Button(200, 70)
        start3_btn = Button(210, 70)
        start4_btn = Button(180, 90)
        start5_btn = Button(190, 90)
        start6_btn = Button(200, 90)
        start7_btn = Button(210, 90)

        show = True
        while show:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                show = False
                                pg.quit()

                screen.blit(maps_bg, (0, 0))

                start_btn.draw(100,200, 'Level 1', button_sound, level_1, font_size = 50, font_color = (0, 246, 255))
                start1_btn.draw(300,200, 'Level 2', button_sound, level_2, font_size = 50, font_color = (0, 246, 255))
                start2_btn.draw(500,200, 'Level 3', button_sound, level_3, font_size = 50, font_color = (0, 246, 255))
                start3_btn.draw(700,200, 'Level 4', button_sound, level_4, font_size = 50, font_color = (0, 246, 255))
                start4_btn.draw(100,300, 'Level 5', button_sound, level_5, font_size = 50, font_color = (0, 246, 255))
                start5_btn.draw(300,300, 'Level 6', button_sound, level_6, font_size = 50, font_color = (0, 246, 255))
                start6_btn.draw(500,300, 'Level 7', button_sound, level_7, font_size = 50, font_color = (0, 246, 255))
                start7_btn.draw(700,300, 'Level 8', button_sound, level_8, font_size = 50, font_color = (0, 246, 255))

                keys = pg.key.get_pressed()

                if keys[pg.K_ESCAPE]:
                        show_menu()

                pg.display.update()
                clock.tick(60)

def pause():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_1, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_1, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_1():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown, level_time

        level_time = 0

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())

        meteors = []
        create_meteors(meteors)

        pg.mixer.music.load('static/sound/Kudin.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

                if level_time >= 900:
                        level_2()

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                screen.blit(planet3_img, (246, 150))

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                draw_array(meteors)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        level_time = 0
                        game = False

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over()

def pause2():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_2, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over2():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_2, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_2():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown, level_time

        level_time = 0

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())
        
        meteors = []
        create_meteors(meteors)

        enemy1 = Enemy(-80, enemy1_img, width = 42, height = 41, speed = 3, shoot_speed = 0, health = 1)
        enemy2 = Enemy(-80, enemy1_img, width = 42, height = 41, speed = 3, shoot_speed = 0, health = 1)
        enemy3 = Enemy(-22000, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 100, health = 1)
        all_enemys = [enemy1, enemy2, enemy3]



        if level_time > 100:
                enemy3 = Enemy(-80, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 50)

        pg.mixer.music.load('static/sound/ZxA - Lo-Fi bit 1 exp.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause2()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

                if level_time >= 900:
                        level_3()

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                screen.blit(planet1_img, (246, 150))

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                draw_array(meteors)

                draw_enemy(all_enemys)
                check_enemy_dmg(all_btn_arm, all_enemys)

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        level_time = 0
                        game = False

                if check_player_dmg(all_enemys):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over2()

def pause3():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_3, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over3():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_3, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_3():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown, level_time

        level_time = 0

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())
        
        meteors = []
        create_meteors(meteors)

        enemy1 = Enemy(-80, enemy1_img, width = 42, height = 41, speed = 3, shoot_speed = 0, health = 1)
        enemy2 = Enemy(-80, enemy1_img, width = 42, height = 41, speed = 3, shoot_speed = 0, health = 1)
        enemy3 = Enemy(-1000, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 100, health = 1)
        enemy4 = Enemy(-10000, enemy3_img, width = 47, height = 47, speed = 3, shoot_speed = 20, health = 2)
        all_enemys = [enemy1, enemy2, enemy3, enemy4]


        pg.mixer.music.load('static/sound/ZxA - exp bit 808.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause3()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

                if level_time >= 1200:
                        level_4

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        level_time = 0
                        game = False

                if check_player_dmg(all_enemys):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                draw_array(meteors)

                draw_enemy(all_enemys)
                check_enemy_dmg(all_btn_arm, all_enemys)

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over3()

def pause4():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_4, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over4():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_4, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_4():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())
        
        meteors = []
        create_meteors(meteors)

        enemy1 = Enemy(-80, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 100, health = 1)
        enemy2 = Enemy(-80, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 100, health = 1)
        enemy3 = Enemy(-1000, enemy3_img, width = 47, height = 47, speed = 3, shoot_speed = 20, health = 2)
        enemy4 = Enemy(-1000, enemy3_img, width = 47, height = 47, speed = 3, shoot_speed = 20, health = 2)
        boss = Enemy(-10000, boss1_img, width = 295, height = 311, speed = 3, shoot_speed = 100, health = 4, boss = True)
        all_enemys = [enemy1, enemy2, enemy3, enemy4, boss]


        pg.mixer.music.load('static/sound/ZxA - Зарисовочка №6.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause4()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                screen.blit(planet2_img, (146, 150))
                screen.blit(planet4_img, (446, 100))

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                if check_player_dmg(all_enemys):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                if check_enemy_dmg(all_btn_arm, all_enemys):
                        level_5()

                draw_array(meteors)

                draw_enemy(all_enemys)
                check_enemy_dmg(all_btn_arm, all_enemys)

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over4()

def pause5():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_5, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over5():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_5, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_5():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown, level_time

        level_time = 0

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())
        
        meteors = []
        create_meteors(meteors)

        enemy1 = Enemy(-80, enemy3_img, width = 47, height = 47, speed = 3, shoot_speed = 20, health = 2)
        enemy2 = Enemy(-80, enemy3_img, width = 47, height = 47, speed = 3, shoot_speed = 20, health = 2)
        enemy3 = Enemy(-100, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 100, health = 1)
        enemy4 = Enemy(-1000, enemy4_img, width = 39, height = 50, speed = 5, shoot_speed = 100, health = 2)
        enemy5 = Enemy(-10000, enemy4_img, width = 39, height = 50, speed = 5, shoot_speed = 100, health = 2)
        all_enemys = [enemy1, enemy2, enemy3, enemy4, enemy5]


        pg.mixer.music.load('static/sound/zxa - Waltz 2var.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause5()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

                if level_time >= 900:
                        level_6()

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        level_time = 0
                        game = False

                if check_player_dmg(all_enemys):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                draw_array(meteors)

                draw_enemy(all_enemys)
                check_enemy_dmg(all_btn_arm, all_enemys)

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over5()

def pause6():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_6, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over6():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_6, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_6():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown, level_time

        level_time = 0

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())
        
        meteors = []
        create_meteors(meteors)

        enemy1 = Enemy(-80, enemy4_img, width = 39, height = 50, speed = 5, shoot_speed = 100, health = 2)
        enemy2 = Enemy(-80, enemy4_img, width = 39, height = 50, speed = 5, shoot_speed = 100, health = 2)
        enemy3 = Enemy(-100, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 100, health = 1)
        enemy4 = Enemy(-1000, enemy4_img, width = 39, height = 50, speed = 5, shoot_speed = 100, health = 2)
        enemy5 = Enemy(-10000, enemy5_img, width = 58, height = 69, speed = 10, shoot_speed = 150, health = 3)
        all_enemys = [enemy1, enemy2, enemy3, enemy4, enemy5]


        pg.mixer.music.load('static/sound/ZxA - exp bit xz.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause5()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

                if level_time >= 1300:
                        level_7()

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                screen.blit(planet5_img, (146, 150))
                screen.blit(planet8_img, (446, 100))
                screen.blit(planet7_img, (746, 50))

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        level_time = 0
                        game = False

                if check_player_dmg(all_enemys):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                draw_array(meteors)

                draw_enemy(all_enemys)
                check_enemy_dmg(all_btn_arm, all_enemys)

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over6()

def pause7():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)                        

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_7, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over7():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_7, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_7():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown, level_time

        level_time = 0

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())
        
        meteors = []
        create_meteors(meteors)

        enemy1 = Enemy(-80, enemy4_img, width = 39, height = 50, speed = 5, shoot_speed = 100, health = 2)
        enemy2 = Enemy(-80, enemy4_img, width = 39, height = 50, speed = 5, shoot_speed = 100, health = 2)
        enemy3 = Enemy(-100, enemy2_img, width = 33, height = 34, speed = 5, shoot_speed = 100, health = 1)
        enemy4 = Enemy(-1000, enemy5_img, width = 58, height = 69, speed = 10, shoot_speed = 150, health = 3)
        enemy5 = Enemy(-10000, enemy5_img, width = 58, height = 69, speed = 10, shoot_speed = 150, health = 3)
        enemy6 = Enemy(-20000, enemy5_img, width = 58, height = 69, speed = 10, shoot_speed = 150, health = 3)
        all_enemys = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6]


        pg.mixer.music.load('static/sound/ZxA - Lo-Fi bit 3 exp 2.0.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause7()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

                if level_time >= 1200:
                        level_8()

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                screen.blit(planet6_img, (150, 150))

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        level_time = 0
                        game = False

                if check_player_dmg(all_enemys):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                draw_array(meteors)

                draw_enemy(all_enemys)
                check_enemy_dmg(all_btn_arm, all_enemys)

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over7()

def pause8():
        paused = True

        restart_btn = Button(300,40)
        mainmenu_btn = Button(300, 90)

        pg.mixer.music.pause()

        button = Button(100, 50)

        while paused:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Paused', 160, 200)
                        print_text('Press w to go up', 360, 200)
                        print_text('Press s to go down', 360, 230)
                        print_text('Press SPACE to shoot', 360, 260)
                        print_text('Press Escape or Enter to continue game', 360, 290)

                        koys = pg.key.get_pressed()
                        if koys[pg.K_RETURN] or koys[pg.K_ESCAPE]:
                                paused = False
                
                button.draw(160, 160, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                restart_btn.draw(120,240, 'Restart game', button_sound, level_8, font_size = 30, font_color = (192, 192, 192))
                mainmenu_btn.draw(110, 280, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                pg.display.update()
                clock.tick(15)

        pg.mixer.music.unpause()

def game_over8():

        restart_btn = Button(300,20)
        mainmenu_btn = Button(300, 30)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()
                        
                        print_text('Game Over', 450, 200)

                        restart_btn.draw(430,225, 'Restart game', button_sound, level_8, font_size = 30, font_color = (192, 192, 192))
                        mainmenu_btn.draw(420, 250, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_RETURN]:
                                return True
                        if k[pg.K_ESCAPE]:
                                return False
                pg.display.update()
                clock.tick(15)

def level_8():
        global player_up, player_down, player_x, player_y, player_width, player_height, cooldown

        STARS_COUNT = 200
        star_list = []
        for _ in range(STARS_COUNT):
                star_list.append(Star())
        
        meteors = []
        create_meteors(meteors)

        enemy1 = Enemy(-100, enemy5_img, width = 58, height = 69, speed = 10, shoot_speed = 150, health = 3)
        enemy2 = Enemy(-100, enemy5_img, width = 58, height = 69, speed = 10, shoot_speed = 150, health = 3)
        enemy3 = Enemy(-100, enemy5_img, width = 58, height = 69, speed = 10, shoot_speed = 150, health = 3)
        boss = Enemy(-10000, boss2_img, width = 295, height = 311, speed = 3, shoot_speed = 100, health = 5, boss = True)
        all_enemys = [enemy1, enemy2, enemy3, boss]


        pg.mixer.music.load('static/sound/Кудинов Дмитрий - song 1.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        all_btn_arm = []

        game = True
        while game:

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                game = False
                                pg.quit()

                keys = pg.key.get_pressed()

                if (keys[pg.K_UP] or keys[pg.K_w]) and player_y > 0:
                        player_y -= speed
                        player_up = True
                        player_down = False
                elif (keys[pg.K_DOWN] or keys[pg.K_s]) and player_y < 497 - player_height:
                        player_y += speed
                        player_up = False
                        player_down = True
                else: 
                        player_up = False
                        player_down = False

                if keys[pg.K_ESCAPE]:
                        pause8()

                if not cooldown:
                        if keys[pg.K_SPACE]:
                                all_btn_arm.append(Arm(player_x + player_width, player_y, arm_img))
                                cooldown = 50
                else:
                        cooldown -= 1

                count_time(meteors)

##############################################################################################

                screen.fill((0,0,0))  

                for st in star_list:
                        st.draw()
                        st.blinking()

                screen.blit(planet9_img, (150, 150))

                if player_up:
                        screen.blit(player_img[0], (player_x, player_y))
                elif player_down:
                        screen.blit(player_img[2], (player_x, player_y))
                else:
                        screen.blit(player_img[1], (player_x, player_y))

                for arm in all_btn_arm:
                        if not arm.arm_move():
                                all_btn_arm.remove(arm)

                if check_collision(meteors):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                if check_player_dmg(all_enemys):
                        pg.mixer.music.stop()
                        pg.mixer.Sound.play(boom_sound)
                        game = False

                if check_enemy_dmg(all_btn_arm, all_enemys):
                        show_titers()

                draw_array(meteors)

                draw_enemy(all_enemys)
                check_enemy_dmg(all_btn_arm, all_enemys)

                pg.display.update()
                clock.tick(80)

##############################################################################################

        return game_over8()

def show_titers():
        
        mainmenu_btn = Button(300, 30)

        button = Button(100, 50)

        pg.mixer.music.load('static/sound/Metal Gear Rising Revengeance - Metal Gear Rising Revengeance OST It Has To Be This Way Extended.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        stopped = True
        while stopped:
                for event in pg.event.get():
                        if event.type == pg.QUIT:
                                pg.quit()

                        button.draw(410, 150, 'WOW', wow_sound, font_size=30, font_color=(192, 192, 192))
                        print_text('Game End', 400, 200)
                        print_text('Thank you for playing!', 340, 250)
                        print_text('Game made by Tereburke Daniil', 300, 300)
                        print_text('Supported by Dmitry Obolonski', 300, 350)

                        mainmenu_btn.draw(350, 400, 'Main Menu game', button_sound, show_menu, font_size = 30, font_color = (192, 192, 192))

                        k = pg.key.get_pressed()
                        if k[pg.K_ESCAPE]:
                                show_menu()

                pg.display.update()
                clock.tick(15)

def run_game():

        show_menu()

while run_game():
        pass

pg.quit()
