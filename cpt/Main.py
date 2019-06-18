import pygame, sys, random                              # Import pygame, random, and sys
pygame.init()                                           # Initialize pygame

screen = pygame.display.set_mode((800, 600))            # Screen of 800 x 600 px
pygame.display.set_caption("Hit The Frogs")             # Caption for the window
clock = pygame.time.Clock()                             # Clock for FPS
frog_img = pygame.image.load("frog_2x_1.png")           # Load in images for sprites
reinhardt_l = pygame.image.load("ban.png")
reinhardt_r = pygame.transform.flip(reinhardt_l, True, False)
idle_l = pygame.image.load("d_idle.png")
idle_r = pygame.transform.flip(idle_l, True, False)
hit_l = pygame.image.load("d_hit.png")
hit_r = pygame.transform.flip(hit_l, True, False)
frog_stuff = pygame.image.load("chunk.png")
eyeball = pygame.image.load("eye.png")
dock = pygame.image.load("dock.png")
mr_sun = pygame.transform.scale(pygame.image.load("sun.png"), (200, 200))
blood_stain = pygame.image.load("stain.png")

death_sound = pygame.mixer.Sound("frog_die.wav")
frog_sound = pygame.mixer.Sound("sound.wav")

banner_font = pygame.font.SysFont("Verdana", 80)        # Set font for main banner
stat_font = pygame.font.SysFont("AvantGarde", 30)       # Set font for score and timer
display_font = pygame.font.SysFont("AvantGarde", 60)    # Set font for display text
clicky_font = pygame.font.SysFont("Times", 40)          # Set font for clickys
mono_font = pygame.font.SysFont("CourierNew", 48)       # Set font for highscores

score_file = open("Highscore.txt", "r")                 # Opens the file with high scores
high_score = []                                         # Reads the scores in the file into a list for use later
for entry in score_file:
    high_score.append(int(entry))
score_file.close()

WHITE = (255, 255, 255)                                 # Make some RGB colours easier to call
BLACK = (000, 000, 000)
RED   = (255, 000, 000)
GREEN = (000, 255, 000)
WATER = ( 60, 100, 255)
B2    = (150, 150, 255)
WALL  = (150, 150, 150)
SKY   = (130, 200, 255)

settings = {1: (10, 450), 2: (10, 500), 3: (15, 550)}   # Settings for 3 levels
# Index 0 is the min score required to pass the level, index 1 is the position of the frogs on the map

active_list = pygame.sprite.Group()                     # List of sprites on the game board
blood_list = pygame.sprite.Group()                      # List of retards on the game board
sprite_list = []                                        # List of all sprites


class Frog(pygame.sprite.Sprite):                       # Class for frogs
    """ Class for the 3 frogs that are on the screen -
    Frogs jump around randomly and die when hit and then come back after some time
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = frog_img                           # Set image to default frog image
        self.face = -1                                  # Set direction to left by default
        self.rect = self.image.get_rect()               # Rect object for frog positioning
        self.rect.center = (x, y)                       # Frog position is set to given parameters
        self.death_timer = 120                          # Timer for the frog to come back after dying
        self.jump_timer = random.randrange(30, 151)     # Timer for the delay between jumps
        self.jump_sequence = 1                          # Tracks the frame of the jump animation the frog is on
        self.airborne = False                           # This one is self explanatory
        self.jump_distance = 0                          # How long the frog will jump per frame
        self.pos = y                                    # Y value that the frog operates on

    def move_abs(self, x, y):                           # Moves the frog to an absolute value
        self.rect.center = (x, y)                       # Moves the frog rect centre to the given value

    def move_rel(self, x, y):                           # Moves the frog by a relative value
        self.rect = self.rect.move(x, y)                # Moves the frog rect by the given value

    def reset(self):                                    # Resets the frog after it dies
        self.airborne = False                           # Frog is put on the ground
        self.jump_timer = random.randrange(150, 181)    # Jump is put back on a timer
        self.jump_sequence = 1                          # Resets the jump animation
        self.prep_jump()                                # Prepares a new jump
        self.move_abs(850, self.pos)                    # Frog is placed randomly on the ground

    def prep_jump(self):
        destination = random.randrange(50, 750)         # Gets random destination
        dist_per_frame = (destination - self.rect.left) // 59
        self.jump_distance = dist_per_frame             # Calculate and set the jump distance per frame
        if self.face * dist_per_frame < 0:              # Flips the image if jumping in other direction
            self.image = pygame.transform.flip(self.image, True, False)
            self.face = -self.face

    def hop(self, seq, distance):                       # Changes jump distance based on which frame the jump is on
        if seq < 30:
            if seq < 16:
                self.move_rel(distance, -15)
            else:
                self.move_rel(distance, -10)
        elif seq < 59:
            if seq < 44:
                self.move_rel(distance, 10)
            else:
                self.move_rel(distance, 15)
        else:                                           # Resets the jump related values
            self.jump_sequence = 0
            self.airborne = False
            self.jump_timer = random.randrange(30, 151)
            self.prep_jump()

    def update(self):                                   # Update function ran every frame
        if self not in active_list:                     # If the frog is not on the map
            if self.death_timer > 0:                    # If frog is dead and timer is counting down ticks the timer
                self.death_timer -= 1
            else:                                       # If the timer is at 0 then it is reset and the frog is revived
                active_list.add(self)
                self.death_timer = 120
        if self.airborne:                               # If frog is airborne calls the hop function
            self.hop(self.jump_sequence, self.jump_distance)
            self.jump_sequence += 1
        else:                                           # If frog is on the map
            if self.jump_timer == 0:                    # If the timer tracking the frog jump is 0 makes the frog jump
                self.airborne = True
                pygame.mixer.Sound.play(frog_sound)
            else:
                self.jump_timer -= 1                    # Otherwise the timer for the frog jump is ticked


class Player(pygame.sprite.Sprite):                     # Class for the player character
    """ Class for the player character -
    Player moves around and attempts to hit frogs
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = idle_l                             # Default image is set the idle image
        self.pos = self.image.get_rect()                # Position of the player
        self.pos.center = (x, y)                        # Centres the player on the given parameters
        self.rect = pygame.Rect(self.pos.left, self.pos.top + 35, 30, 30)
        # The rect attribute is set to a rectangle- this specific attribute is used in the built in collision detection
        # system, which allows it to act as the hitbox for the hammer.
        self.acceleration = 0                           # "Acceleration" of the player
        self.landed = True                              # Variable tracking if player in on the ground or not
        self.jump_timer = 1                             # Tracks the frame the player is in during a jump
        self.cooldown = 0                               # Tracks the amount of time since the last hit command
        self.hit_out = False                            # Tracks whether the player in during the hit animation
        self.facing = -1                                # Tracks which way the player in facing
        self.animation = 0                              # Tracks the frame the player is in during a hit

    def move(self, x, y):                               # Function for moving the player sprite
        self.pos = self.pos.move(x, y)                  # Moves the player's rect by the given parameters
        self.rect = self.rect.move(x, y)                # Moves the player's hitbox by the given parameters
        rs = self.pos.right                             # Tracks the right edge of the player
        ls = self.pos.left                              # Tracks the left edge of the player
        if ls < 0:                                      # If the left edge is off the screen puts the player back on it
            self.pos = self.pos.move(-ls, 0)
            self.rect = self.rect.move(-ls, 0)
        if rs > 800:                                    # If the right edge is off the screen puts the player back on it
            self.pos = self.pos.move((-rs + 800), 0)
            self.rect = self.rect.move((-rs + 800), 0)

    def accelerate(self, acel):                         # Changes the players acceleration
        if abs(self.acceleration) < 10:                 # If the players acceleration is not greater than absolute 10
            self.acceleration += acel                   # Changes the acceleration by the given parameters

    def jump(self, jump_timer):                         # Function for making the player jump
        if jump_timer < 30:                             # If the frame of jump is less than 30
            if jump_timer < 15:                         # If during the first half of jump, player is moved up
                self.move(0, -10)
            if jump_timer > 15:                         # If during the last half of the jump, player is moved down
                self.move(0, 10)
        else:                                           # If the frame of the jump is 30 player is landed
            self.landed = True
            self.jump_timer = 0

    def turn(self, direction):                          # Changes the image of the player to match its direction
        if direction == -1:                             # If the intended direction is left
            self.image = idle_l                         # Sets image to the left facing idle
            self.rect.left = self.pos.left              # Moves hitbox to the left of the player
            self.facing = -1                            # Sets the player to facing left
        else:                                           # If the intended direction is right
            self.image = idle_r                         # Sets image to the right facing idle
            self.rect.right = self.pos.right            # Moves hitbox to the right of the player
            self.facing = 1                             # Sets the player to facing right

    def set_idle(self):                                 # Sets the player image back to idle after hit animation
        if self.facing == 1:                            # If the player is facing left the image is the left idle
            self.image = idle_r
        else:                                           # If the player is facing right the image is the right idle
            self.image = idle_l

    def update(self):                                   # Update function run every frame
        if self.acceleration != 0:                      # If the players acceleration is not 0
            self.move(self.acceleration, 0)             # The player is moved by the acceleration value
            if self.acceleration < 0:                   # If the acceleration is negative
                self.acceleration += 1                  # Acceleration is set 1 closer to 0
            else:                                       # If the acceleration is positive
                self.acceleration -= 1                  # Acceleration is set 1 closer to 0
        if not self.landed:                             # If player is in the air
            self.jump(self.jump_timer)                  # Calls the jump function
            self.jump_timer += 1                        # Increases the jump timer by 1
        if not self.hit_out and self.cooldown > 0:      # If the player is not hitting and the cooldown is not at 0
            self.cooldown -= 1                          # Lowers the cooldown by 1
        if self.animation != 0:                         # If the hit animation is not at frame 0
            if self.animation == 10:                    # If the hit animation is at frame 10
                self.set_idle()                         # Set idle function is called
                self.animation = 0                      # Animation frame is set to 0
            else:                                       # If the hit animation not at frame 10
                self.animation += 1                     # The hit animation is increased by 1


class Organ(pygame.sprite.Sprite):
    """ Class for the bits of frog that appear after a frog is killed
    The pieces of frog fly out in a random direction and disappear off the screen
    """
    def __init__(self, x, y):
        super().__init__()
        self.x_mov = random.randrange(-13, 14)          # X velocity
        self.y_mov = random.randrange(-20, 1)           # Y velocity
        self.y_acc = 1                                  # Y acceleration
        self.image = pygame.transform.rotate(frog_stuff, random.randrange(0, 360))  # Randomly rotate the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def update(self):
        if self.rect.top < 650:                         # If the object in on the screen move it accordingly
            self.move(self.x_mov, self.y_mov)
            self.y_mov += self.y_acc
            self.y_acc += 0
        else:                                           # If the object is not on screen kills it
            self.kill()


class EyeBall(Organ):
    """ Subclass of the organ class
    Functions the same way except eyeballs fly higher and less far outward
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.rotate(eyeball, random.randrange(0, 360))
        self.y_mov -= 15
        self.x_mov //= 3


def play_game(lvl):                                     # Function to play the game
    """ Function that plays the game -
    Takes the level as a parameter and returns the score of the player and the next level if the player passed
    """
    timer = 5400                                        # Timer for the game is set to 90 secs (90 * 60)
    frog_height = settings[level][1]
    char = Player(400, 300)                             # Character sprite is initialised
    frog_list = []                                      # List of frogs is set to empty list
    for x in range(3):                                  # Initialises 3 frogs and adds it the frog list
        frog_list.append(Frog(850, frog_height))   		# Y position of the frog is set to setting for the current level
    for frog in frog_list:                              # Adds all the frogs to the list of active frogs
        active_list.add(frog)

    hit_q = False
    score = 0                                           # Score is set to 0
    screen_txt("LEVEL " + str(lvl), 310)                # Displays the current level on the screen

    while timer > 0:                                    # Plays the game while the timer is not 0
        for event in pygame.event.get():                # Checks if the user closes the window
            if event.type == pygame.QUIT:               # If user kills then quits pygame and exits the program
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()                 # Gets a list of all the keys pressed by the user
        if keys[pygame.K_LEFT]:                         # If left arrow is pressed
            char.accelerate(-2)                         # Accelerates the player by 2[left]
            if char.facing == 1 and char.animation == 0:    # If player is facing the other way and not in an animation
                char.turn(-1)                           # Turns the player around
        if keys[pygame.K_RIGHT]:                        # If right arrow is pressed
            char.accelerate(2)                          # Accelerates the player by 2[right]
            if char.facing == -1 and char.animation == 0:   # If player is facing the other way and not in an animation
                char.turn(1)                            # Turns the player around
        if keys[pygame.K_UP]:                           # If up arrow is pressed
            if char.landed:                             # If player is on the ground
                char.landed = False                     # Player is now jumping
        if keys[pygame.K_SPACE]:                        # If spacebar is pressed
            if char.cooldown == 0:                      # If the cooldown for hitting is at 0
                hit_q = True                            # Queues a hit for later
                char.cooldown = 60                      # Sets the cooldown to 60 frames
                if char.facing == 1:                    # If player is facing right
                    char.image = hit_r                  # Sets image to right facing hit
                else:                                   # If player is facing left
                    char.image = hit_l                  # Sets image to left facing hit
        char.update()                                   # Calls the update function for the player
        for frog in frog_list:                          # Calls the update function for all the frogs
            frog.update()
        blood_list.update()
        if hit_q:                                       # If a hit was queued
            char.animation = 1                          # Sets the player to frame 1 of the hit animation
            hit = pygame.sprite.spritecollide(char, active_list, True)  # Checks for collisions with any active frogs
            for a in hit:                               # For every frog that is hit
                pygame.mixer.Sound.play(death_sound)
                score += 1                              # Increases score by 1
                for x in range(random.randrange(2, 4)):
                    blood_list.add(Organ(a.rect.center[0], a.rect.center[1]))
                for x in range(random.randrange(0, 3)):
                    blood_list.add(EyeBall(a.rect.center[0], a.rect.center[1]))
                a.reset()

            hit_q = False                               # Hit queue is set back to false
        score_txt = stat_font.render("Score: " + str(score), False, BLACK)  # Renders the score display
        timer_txt = stat_font.render("Time: " + str(timer // 60), False, BLACK) # Renders the timer display
        level_txt = stat_font.render("Level: " + str(level), False, BLACK)  # Renders the level display
        screen.fill(SKY)                              # Fills the screen in white
        screen.blit(mr_sun, (600, 15))
        screen.blit(char.image, char.pos)               # Draws the player on the screen
        screen.blit(dock, (0, 332))
        pygame.draw.rect(screen, WATER, (0, frog_height, 800, 150))
        active_list.draw(screen)                        # Draws all active frogs on the screen
        blood_list.draw(screen)
        screen.blit(level_txt, (20, 20))               # Blits the level display onto the screen
        screen.blit(score_txt, (120, 20))               # Blits the score display onto the screen
        screen.blit(timer_txt, (220, 20))               # Blits the timer display onto the screen
        pygame.display.flip()                           # Updates the screen
        timer -= 1                                      # Ticks the timer
        clock.tick(60)                                  # Runs the game at 60 FPS
    active_list.empty()                                 # After game empties the list of active frogs
    blood_list.empty()                                  # After game empties the list of dead frogs
    if score >= settings[lvl][0]:                       # If the score is better than the needed score to beat the level
        return score, lvl + 1                           # Returns the score and indication the player has beat the level
    else:                                               # If the score is not enough
        return 0, lvl                                   # Returns no score and indication the player has failed


def screen_txt(txt, x, score=0):
    """ Function that displays some text on the screen for 2 secs
    Takes the text and x value
    Optional score value can be given to display an extra line for the user's total score
    """
    screen.fill(WHITE)                                  # Fills the screen in white
    screen.blit(display_font.render(txt, True, BLACK), (x, 250))    # Blits the given text onto the screen
    if score != 0:
        screen.blit(stat_font.render("Total Score: " + str(score), True, BLACK), (x + 5, 300))
        # If the score parameter is given, then an extra line displaying the players total score is displayed
        # Allows the function to be used in multiple displays
    pygame.display.flip()                               # Updates the screen
    pygame.time.wait(2000)                              # Waits 2 seconds


def rank(score):                                        # Ranks the player's score among the high scores
    """ Function that ranks the users score among the top highscores
    Takes the given score and ranks it accordingly with the score in the highscore list
    Returns the ranked position adjusted for
    """
    placement = -1                                      # Placement is -1
    for x in range(9, -1, -1):                          # Runs through the high score list and ranks the player's score
        if score > high_score[x]:                       # For every score that is lower than the player's
            placement = x                               # The players score is set to that rank
            high_score[x] = high_score[x - 1]           # The other score is moved down
    if placement > -1:                                  # If the player's score is ranked on the high scores
        high_score[placement] = score                   # Places the player's score in its position
        overwrite = open("Highscore.txt", "w")          # Opens the highscore file to record the new score
        for num in high_score:                          # Writes all the scores onto a line
            overwrite.write(str(num) + "\n")
        overwrite.close()                               # Closes highscore file
        return placement + 1                            # Returns the player's ranked position, adjusted for index 0


def opening_seq():                                      # Function to display the opening screen
    """ Function that displays the screen at the start of the program -
    Takes no parameters and returns nothing
    """
    opening = True                                      # Opening is set to true
    while opening:                                      # While the game is in the opening screen
        for event in pygame.event.get():                # Checks for events
            if event.type == pygame.QUIT:               # If user quits, exit the program
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:      # If user clicks
                pos = pygame.mouse.get_pos()            # Gets mouse position
                if 90 < pos[0] < 230 and 300 < pos[1] < 346:    # If mouse is over the start button
                    opening = False                     # Ends the opening sequence
                if 90 < pos[0] < 207 and 375 < pos[1] < 421:
                    instructions()
                if 90 < pos[0] < 335 and 450 < pos[1] < 496:    # If mouse if over the highscore button
                    display_score()                     # Calls the display score function
        screen.fill(WHITE)                              # Fills the screen with white
        pygame.draw.rect(screen, B2, pygame.Rect(90, 300, 140, 46))     # Draws a rect for start button
        pygame.draw.rect(screen, B2, pygame.Rect(90, 450, 245, 46))     # Draws a rect for highscore button
        pygame.draw.rect(screen, B2, pygame.Rect(90, 375, 117, 46))
        screen.blit(clicky_font.render("START", True, BLACK), (100, 300))
        screen.blit(clicky_font.render("HIGHSCORE", True, BLACK), (100, 450))
        screen.blit(clicky_font.render("HELP", True, BLACK), (100, 375))
        screen.blit(banner_font.render("HIT THE FROGS", True, RED), (80, 100))
        # Blits all the text onto the screen
        screen.blit(pygame.transform.scale(frog_img, (215, 215)), (490, 295))   # Draws the frog picture
        pygame.display.flip()                           # Updates the screen
        clock.tick(5)                                   # Runs a 5 fps


def ending_seq(final):                                  # Function for displaying the final result
    """ Function that displays the screen after the player finishes a game -
    Takes the final result of the player as a parameter and displays it
    """
    screen.fill(WHITE)                                  # Fills the screen with white
    if final == 0:                                      # Display for if the player did not rank on the highscore list
        screen.blit(display_font.render("You did not rank on the leaderboard", True, BLACK), (40, 250))
        screen.blit(mr_sun, (280, 330))
    else:                                               # Display for if the player ranked on the highscore list
        screen.blit(display_font.render("You got rank " + str(final) + " on the leaderboard", True, BLACK), (50, 250))
        screen.blit(stat_font.render("Good Job", True, BLACK), (635, 230))
        screen.blit(blood_stain, (150, 450))
        screen.blit(pygame.transform.rotate(pygame.transform.scale(eyeball, (75, 75)), 195), (200, 460))
        screen.blit(pygame.transform.rotate(pygame.transform.scale(frog_stuff, (90, 90)), -35), (330, 420))
    pygame.display.flip()                               # Updates the screen
    pygame.time.wait(2000)                              # Waits 2 seconds
    screen.blit(stat_font.render("Press Any Key To Continue", True, BLACK), (55, 300))    # Writes the text for continue
    pygame.display.flip()                               # Updates the screen
    while True:                                         # While loop
        for event in pygame.event.get():                # Check events
            if event.type == pygame.QUIT:               # If user kills then exit the program
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:      # If user clicks screen
                return


def display_score():                                    # Function for displaying the list of highscores
    """ Function that displays the list of highscores -
    Takes no parameters and returns nothing
    """
    screen.fill(WHITE)                                  # Fills the screen with white
    screen.blit(banner_font.render("HIGH SCORES", True, BLACK), (25, 15))
    screen.blit(display_font.render("BACK", True, RED), (645, 50))
    # Renders the text onto the screen
    for x in range(9):                                  # Renders all the highscores onto the screen
        screen.blit(mono_font.render(str(x + 1) + ".       " + str(high_score[x]), True, BLACK), (50, 125 + 45 * x))
    screen.blit(mono_font.render("10.      " + str(high_score[9]), True, BLACK), (50, 530))
    screen.blit(frog_img, (450, 131))                   # Draws the frogs onto the screen
    screen.blit(pygame.transform.scale(frog_img, (134, 134)), (450, 180))
    screen.blit(pygame.transform.scale(frog_img, (316, 316)), (450, 294))
    pygame.display.flip()                               # Updates the screen
    while True:                                         # While loop
        for event in pygame.event.get():                # Check events
            if event.type == pygame.QUIT:               # If user kills then exit program
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:      # If user clicks screen
                pos = pygame.mouse.get_pos()            # Get mouse position
                if 645 < pos[0] < 765 and 50 < pos[1] < 85:    # If mouse is over back button exits function
                    return


def instructions():                                     # Function for displaying instructions
    """ Function that displays the instructions for playing the game -
    Takes no parameters and returns nothing
    """
    screen.fill(WHITE)                                  # Writes a bunch of stuff on the screen
    screen.blit(banner_font.render("HOW TO PLAY", True, BLACK), (25, 50))
    screen.blit(display_font.render("BACK", True, RED), (630, 85))
    screen.blit(mono_font.render("Your job is to hit frogs", True, BLACK), (25, 170))
    screen.blit(mono_font.render("Use the arrow keys to move", True, BLACK), (25, 230))
    screen.blit(mono_font.render("Press spacebar to hit", True, BLACK), (25, 290))
    screen.blit(mono_font.render("+1 score by killing frog", True, BLACK), (25, 350))
    screen.blit(mono_font.render("Try to earn highest score", True, BLACK), (25, 410))
    screen.blit(mono_font.render("10/10/15 pts to pass 1/2/3", True, BLACK), (25, 470))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # If user kills exit the program
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:      # If user clicks back button returns
                pos = pygame.mouse.get_pos()
                if 630 < pos[0] < 750 and 85 < pos[1] < 120:
                    return


while __name__ == "__main__":                           # Main game loop
    level = 1                                           # Level starts at 1
    total_score = 0                                     # Total score starts at 0
    done_round = False                                  # Round is not done
    board_rank = -1                                     # Player is not currently ranked on the leaderboard
    opening_seq()                                       # Displays the opening screen
    while not done_round:                               # While the current round is being played
        result = play_game(level)                       # Plays the game and takes the result of it
        if result[1] != level:                          # If the player passed the level
            total_score += result[0]                    # Adds player's score to the total score
            if result[1] == 4:                          # If player passed level 3
                done_round = True                       # Round is finished
                board_rank = rank(total_score)          # Player's total score is ranked
            else:                                       # If player was not on level 3
                level += 1                              # Player advances to next level
                screen_txt("LEVEL PASSED", 245, total_score)    # Displays level passed on the screen
        else:                                           # If player failed the level
            screen_txt("LEVEL FAILED", 245)             # Displays level failed on the screen
    screen_txt("YOU WIN", 300, total_score)             # After round loop exits display win text
    pygame.time.wait(2000)                              # Wait 2 seconds
    ending_seq(board_rank)                              # Display ending screen
