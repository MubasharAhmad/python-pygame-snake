import pygame
import random
pygame.init()  # to initialize all the modules
pygame.mixer.init()  


# colours
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


screen_width = 900
screen_height = 600
# to set the screen window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# background image
image = pygame.image.load('img2.jpg')
image = pygame.transform.scale(image, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snake Game")  # game title
pygame.display.update()


# clock
clock = pygame.time.Clock()


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])



font = pygame.font.SysFont(None, 55)
# function to display text
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def welcome():
    is_playing = True
    while is_playing:
        gameWindow.fill(black)
        text_screen('Welcome to Snakes', white, 240, 200)
        text_screen('Press space bar to start', white, 210, 250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # to quit the game
                is_playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    game_loop()
        pygame.display.update()
        clock.tick(30)

def game_loop():
    with open('hs.txt', 'r') as f:
        hscore = f.read()
    # variables required
    is_playing = True
    game_over = False
    snake_x = 60
    snake_y = 60
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0
    snake_size = 10
    score = 0
    food_x = random.randint(0, screen_width)
    food_y = random.randint(0, screen_height)
    fps = 30  # frames
    
    snk_list = []
    snk_length = 1

    while is_playing:
        # for loop to get all the events in the game window
        if game_over:
            with open('hs.txt', 'w') as f:
                f.write(str(hscore))
            gameWindow.fill(black)
            text_screen('Game over! Press enter key to continue', white, 100, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # to quit the game
                    is_playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
    
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # to quit the game
                    is_playing = False
                


                if event.type == pygame.KEYDOWN:
                    # to move right
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    # to move up
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    # to move left
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    # to move down
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_y = snake_y + velocity_y
            snake_x = snake_x + velocity_x

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10
                # print('Score is: ', score)
                food_x = random.randint(0, screen_width)
                food_y = random.randint(0, screen_height)
                snk_length += 5
                if score > int(hscore):
                    hscore = score

            gameWindow.blit(image, (0, 0))
            text_screen('Score: '+str(score) + ' Hiscore: '+ str(hscore), white, 5, 5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]
                
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                pygame.mixer.music.stop()
                game_over = True

            if head in snk_list[:-1]:
                pygame.mixer.music.stop()
                game_over = True

            plot_snake(gameWindow, white, snk_list, snake_size)

            # head of snake
            # pygame.draw.rect(gameWindow, white, [snake_x, snake_y, snake_size, snake_size])
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
game_loop()