import pygame
from gui import button
import snake, agent
import utils
import sys

# Graphics
WHITE = (255, 255, 255)
GREEN = (0, 201, 87)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

LOW = 8
MID = 25
HIGH = 999999999999999999999999999999

width, height = 560, 560

pygame.init()
game_display = pygame.display.set_mode((width, height + 40), pygame.RESIZABLE)
pygame.display.set_caption("Reinforcement Learning Snake Game")

message_font = pygame.font.SysFont('Times New Roman', 40)   # font for the game title
options_font = pygame.font.SysFont('Times New Roman', 25)
score_font = pygame.font.SysFont('ubuntu', 15)              # Font for the score
BG = pygame.image.load("images/BG.jpg")                     # Background of the game window

game = snake.SnakeEnv(game_display, width, height)
snake_agent = agent.Agent(game)


def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        game_display.blit(BG, (0, 0))

        mousePosition = pygame.mouse.get_pos()

        menuText = utils.get_font(45).render("SNAKE AI", True, "#FFFFFF")
        menuRect = menuText.get_rect(center=(280, 50))

        player_btn = button.Button(image=pygame.image.load("images/Button.png"), pos=(280, 150),
                                   text_input="PLAYER", font=utils.get_font(40), base_color="#d7fcd4",
                                   hovering_color="White")
        agent_btn = button.Button(image=pygame.image.load("images/Button.png"), pos=(280, 300),
                                     text_input="AGENT", font=utils.get_font(40), base_color="#d7fcd4",
                                     hovering_color="White")
        quit_btn = button.Button(image=pygame.image.load("images/Button.png"), pos=(280, 450),
                                   text_input="QUIT", font=utils.get_font(40), base_color="#d7fcd4",
                                   hovering_color="White")

        game_display.blit(menuText, menuRect)

        for bt in [player_btn, agent_btn, quit_btn]:
            bt.changeColor(mousePosition)
            bt.update(game_display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_btn.checkForInput(mousePosition):
                    return "player"
                if agent_btn.checkForInput(mousePosition):
                    return "agent"
                if quit_btn.checkForInput(mousePosition):
                    pygame.quit()
                    sys.exit(0)

        pygame.display.update()


def game_rules(mode):
    pygame.display.set_caption("Options")

    while True:
        game_display.blit(BG, (0, 0))
        mousePosition = pygame.mouse.get_pos()
        menuText = utils.get_font(30).render("OPTIONS", True, WHITE)
        menuRect = menuText.get_rect(center=(280, 50))
        wallsText = utils.get_font(30).render("Walls ", True, WHITE)
        wallsRect = wallsText.get_rect(center=(200, 150))
        bordersText = utils.get_font(30).render("Borders ", True, WHITE)
        bordersRect = bordersText.get_rect(center=(200, 210))
        growthText = utils.get_font(30).render("Growth ", True, WHITE)
        growthRect = growthText.get_rect(center=(200, 270))

        on_img = pygame.image.load("images/on.png")
        off_img = pygame.image.load("images/off.png")

        if mode == "agent":
            trainText = utils.get_font(30).render("Train ", True, WHITE)
            trainRect = trainText.get_rect(center=(200, 330))
            game_display.blit(trainText, trainRect)

            speedText = utils.get_font(30).render("Speed ", True, WHITE)
            speedRect = speedText.get_rect(center=(200, 390))
            game_display.blit(speedText, speedRect)

            if snake_agent.train_agent:
                train_btn = button.Button(image=pygame.transform.scale(on_img, (89, 50)), pos=(400, 330), text_input="",
                                          font=utils.get_font(20), base_color="#d7fcd4", hovering_color="White")
            else:
                train_btn = button.Button(image=pygame.transform.scale(off_img, (89, 50)), pos=(400, 330), text_input="",
                                          font=utils.get_font(20), base_color="#d7fcd4", hovering_color="White")

        game_display.blit(wallsText, wallsRect)
        game_display.blit(menuText, menuRect)
        game_display.blit(bordersText, bordersRect)
        game_display.blit(growthText, growthRect)

        # speed buttons
        if mode == 'agent' and game.snake_speed == LOW:
            speed_btn = button.Button(image=None, pos=(400, 390), text_input="LOW", font=utils.get_font(30), base_color="#d7fcd4",
                                     hovering_color="White")
        elif mode == 'agent' and game.snake_speed == MID:
            speed_btn = button.Button(image=None, pos=(400, 390), text_input="MID", font=utils.get_font(30),
                                      base_color="#d7fcd4",
                                      hovering_color="White")
        elif mode == 'agent' and game.snake_speed == HIGH:
            speed_btn = button.Button(image=None, pos=(400, 390), text_input="HIGH", font=utils.get_font(30),
                                      base_color="#d7fcd4",
                                      hovering_color="White")

        # rules buttons
        if 'walls' in game.rules:
            wall_btn = button.Button(image=pygame.transform.scale(on_img, (89, 50)), pos=(400, 150),
                                     text_input="", font=utils.get_font(10), base_color="#d7fcd4",
                                     hovering_color="White")
        else:
            wall_btn = button.Button(image=pygame.transform.scale(off_img, (89, 50)), pos=(400, 150),
                            text_input="", font=utils.get_font(20), base_color="#d7fcd4", hovering_color="White")

        if 'borders' in game.rules:
            borders_btn = button.Button(image=pygame.transform.scale(on_img, (89, 50)), pos=(400, 210),
                                        text_input="", font=utils.get_font(20), base_color="#d7fcd4",
                                        hovering_color="White")
        else:
            borders_btn = button.Button(image=pygame.transform.scale(off_img, (89, 50)), pos=(400, 210),
                                        text_input="", font=utils.get_font(20), base_color="#d7fcd4",
                                        hovering_color="White")

        if 'growth' in game.rules:
            growth_btn = button.Button(image=None, pos=(400, 270), text_input="FRONT", font=utils.get_font(30), base_color="#d7fcd4",
                                     hovering_color="White")
        else:
            growth_btn = button.Button(image=None, pos=(400, 270), text_input="BACK", font=utils.get_font(30), base_color="#d7fcd4",
                                     hovering_color="White")

        scoreboard_btn = button.Button(image=None, pos=(280, 510), text_input="Scoreboard", font=utils.get_font(20),
                                   base_color="#d7fcd4",
                                   hovering_color="White")


        # go back, play buttons
        back_btn = button.Button(image=pygame.image.load("images/back.jpg"), pos=(60, 510),
                            text_input="", font=utils.get_font(30), base_color="Black", hovering_color="Green")
        forward_btn = button.Button(image=pygame.image.load("images/forward.jpg"), pos=(500, 510),
                               text_input="", font=utils.get_font(30), base_color="Black", hovering_color="Green")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:  # if a button is pressed
                if back_btn.checkForInput(mousePosition):  # back button leads you back to menu
                    return True
                elif forward_btn.checkForInput(mousePosition) and mode == "player":  # forward button allows you to play
                    return False
                elif forward_btn.checkForInput(mousePosition) and mode == "agent":
                    return False
                elif wall_btn.checkForInput(mousePosition):
                    if 'walls' in game.rules:
                        game.rules.remove('walls')
                    else:
                        game.rules.append('walls')
                elif borders_btn.checkForInput(mousePosition):
                    if 'borders' in game.rules:
                        game.rules.remove('borders')
                    else:
                        game.rules.append('borders')
                elif growth_btn.checkForInput(mousePosition):
                    if 'growth' in game.rules:
                        game.rules.remove('growth')
                    else:
                        game.rules.append('growth')
                elif scoreboard_btn.checkForInput(mousePosition):
                    show_scoreboard()
                elif mode == "agent" and train_btn.checkForInput(mousePosition):
                    snake_agent.train_agent = not snake_agent.train_agent
                elif mode == "agent" and speed_btn.checkForInput(mousePosition):
                    game.set_speed()

        buttons_list = [back_btn, forward_btn, wall_btn, borders_btn, growth_btn, scoreboard_btn]

        if mode == "agent":
            buttons_list.append(train_btn)
            buttons_list.append(speed_btn)

        for bt in buttons_list:
            bt.changeColor(mousePosition)
            bt.update(game_display)

        pygame.display.update()


# start game
def game_loop():
    pygame.display.set_caption("Snake AI")
    # game loop
    while True:
        game.player_move()

        # condition if the snake dies
        if game.game_closed:
            break


def gameClosedMenu(mode):
    pygame.display.set_caption("Snake AI")

    while True:
        game_display.blit(BG, (0, 0))  # Background
        mousePosition = pygame.mouse.get_pos()  # position of the mouse
        menuText = utils.get_font(45).render("Hard Luck", True, "#FFFFFF")
        menuRect = menuText.get_rect(center=(280, 50))

        score = utils.get_font(30).render("Your score is " + str(game.snake_length - 1), True, WHITE)
        scoreRect = score.get_rect(center=(280, 100))

        replayButton = button.Button(image=pygame.image.load("images/Button.png"), pos=(280, 190),
                              text_input="PLAY AGAIN", font=utils.get_font(36), base_color="#d7fcd4", hovering_color="White")
        menuButton = button.Button(image=pygame.image.load("images/Button.png"), pos=(280, 340),
                            text_input="MENU", font=utils.get_font(40), base_color="#d7fcd4", hovering_color="White")
        quitButton = button.Button(image=pygame.image.load("images/Button.png"), pos=(280, 490),
                            text_input="QUIT", font=utils.get_font(40), base_color="#d7fcd4", hovering_color="White")

        game_display.blit(menuText, menuRect)
        game_display.blit(score, scoreRect)

        for bt in [replayButton, menuButton, quitButton]:
            bt.changeColor(mousePosition)
            bt.update(game_display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if replayButton.checkForInput(mousePosition) and mode == "player":
                    return False
                elif replayButton.checkForInput(mousePosition) and mode == "agent":
                    return False
                elif menuButton.checkForInput(mousePosition):
                    return True
                elif quitButton.checkForInput(mousePosition):
                    pygame.quit()
                    sys.exit(0)

        pygame.display.update()


def show_scoreboard():
    pygame.display.set_caption("Scoreboard")

    while True:
        game_display.blit(BG, (0, 0))  # Background
        mousePosition = pygame.mouse.get_pos()  # position of the mouse
        rulesText = utils.get_font(20).render(" ".join(game.rules), True, "#FFFFFF")
        rulesRect = rulesText.get_rect(center=(280, 50))

        game_display.blit(rulesText, rulesRect)

        key_board = '-'.join(game.rules)

        start_x = 280
        start_y = 100
        i = 1
        for score in game.scoreboard[key_board]:
            scoreText = utils.get_font(15).render(str(i) + ".  " + str(score[1]) + "  " + str(score[0]), True, "#FFFFFF")
            scoreRect = scoreText.get_rect(center=(start_x, start_y))
            game_display.blit(scoreText, scoreRect)

            start_y += 30
            i += 1

        # go back, play buttons
        back_btn = button.Button(image=pygame.image.load("images/back.jpg"), pos=(60, 510),
                                 text_input="", font=utils.get_font(30), base_color="Black", hovering_color="Green")

        for bt in [back_btn]:
            bt.changeColor(mousePosition)
            bt.update(game_display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:  # if a button is pressed
                if back_btn.checkForInput(mousePosition):  # back button leads you back to menu
                    return True

        pygame.display.update()


if __name__ == '__main__':
    while True:
        mode = main_menu()

        while True:
            # select game rules
            if game_rules(mode):
                break

            game.rules.sort()
            game.load_max_score()

            # human player plays
            if mode == "player":
                game.snake_speed = LOW
                game.reset()
                game_loop()
            else:
                # agent plays
                snake_agent.run_agent()

            # update scoreboard
            game.save_scoreboard()

            if gameClosedMenu(mode):
                break
