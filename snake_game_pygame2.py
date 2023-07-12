import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

# Constants
GRID_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 30
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Snake class
class Snake:
    def __init__(self):
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT // 2
        self.direction = -1
        self.segments = [(self.x, self.y)]

    def change_direction(self, direction):
        if self.direction == Direction.UP and direction == Direction.DOWN:
            return
        if self.direction == Direction.DOWN and direction == Direction.UP:
            return
        if self.direction == Direction.LEFT and direction == Direction.RIGHT:
            return
        if self.direction == Direction.RIGHT and direction == Direction.LEFT:
            return
        self.direction = direction

    def move(self):

        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1

        if self.y <= -1 and self.direction == Direction.UP:
            self.y = GRID_HEIGHT - 1
        elif self.y >= GRID_HEIGHT and self.direction == Direction.DOWN:
            self.y = 0

        if self.x <= -1 and self.direction == Direction.LEFT:
            self.x = GRID_WIDTH - 1
        elif self.x >= GRID_WIDTH and self.direction == Direction.RIGHT:
            self.x = 0

        self.segments.insert(0, (self.x, self.y))
        self.segments.pop()

    def grow(self, ):
        if self.direction == Direction.RIGHT:
            self.segments.append((self.segments[-1][0] + 1, self.segments[-1][1]))
        elif self.direction == Direction.LEFT:
            self.segments.append((self.segments[-1][0] - 1, self.segments[-1][1]))
        elif self.direction == Direction.UP:
            self.segments.append((self.segments[-1][0], self.segments[-1][1] + 1))
        elif self.direction == Direction.DOWN:
            self.segments.append((self.segments[-1][0], self.segments[-1][1] - 1))

    def check_collision(self, food):
        return self.segments[0] == (food.x, food.y)

    def check_collision_self(self):
        for segment in self.segments[1:]:
            if self.segments[0] == segment:
                return True
        return False

    def draw_cube(self, win, segment, eyes=False, tail=False):
        pygame.draw.rect(win, BLUE if tail else GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        if eyes:
            centre = GRID_SIZE // 2
            radius = 3

            circleMiddle = (self.x * GRID_SIZE + centre - radius, self.y * GRID_SIZE + 8)
            circleMiddle2 = (self.x * GRID_SIZE + GRID_SIZE - radius * 2, self.y * GRID_SIZE + 8)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle2, radius)

        if tail:
            radius = 3
            circleMid = (segment[0] * GRID_SIZE + GRID_SIZE//2, segment[1] * GRID_SIZE + GRID_SIZE//2)
            pygame.draw.circle(win, (0, 0, 0), circleMid, radius)

    def draw(self, win):
        for index, segment in enumerate(self.segments):
            more_than_1 = self.get_segments() > 1
            self.draw_cube(win, segment, eyes=not bool(index), tail=(index == self.get_segments() - 1) and more_than_1)

    def get_segments(self):
        return len(self.segments)


# Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)

    def draw(self, win):
        pygame.draw.rect(win, RED, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Game class
class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.snake = Snake()
        self.food = Food()
        self.game_over = False

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle arrow key events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(Direction.RIGHT)

            if self.snake.check_collision_self():
                self.game_over = True

            if self.snake.check_collision(self.food):
                self.snake.grow()
                self.food = Food()

            self.snake.move()

            self.win.fill(BLACK)
            self.snake.draw(self.win)
            self.food.draw(self.win)

            score_text = self.font.render(f"Score: {self.snake.get_segments()}", True, WHITE)
            self.win.blit(score_text, (10, 10))

            pygame.display.update()
            self.clock.tick(5 + self.snake.get_segments() // 10)

        # Game over loop
        while True:
            self.win.fill(BLACK)
            game_over_text = self.font.render("Game Over", True, RED)
            restart_text = self.font.render("Press R to Restart", True, GREEN)
            self.win.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                           SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            self.win.blit(restart_text, (
                SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + restart_text.get_height() // 2))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()

    def restart_game(self):
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.run()


# Main driver code
if __name__ == '__main__':
    game = Game()
    game.run()
