from random import randint
import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (125, 125, 125)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WRONG_FOOD_COLOR = (117, 78, 27)
speed = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Base class"""

    def __init__(self, position=(GRID_SIZE * (GRID_WIDTH // 2),
                 GRID_SIZE * (GRID_HEIGHT // 2)), body_color=(128, 128, 138)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Base class draw method"""
        rect = pg.Rect(
            (self.position),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        if hasattr(self, 'last') and self.last is not None:
            last_rect = pg.Rect((self.last), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Apple class"""

    def __init__(self, positions=[], color=APPLE_COLOR):
        super().__init__()
        self.body_color = color
        self.position = self.randomize_position(positions)

    def randomize_position(self, positions):
        """Randomize apple position"""
        self.position = (GRID_SIZE * randint(1, GRID_WIDTH - 1),
                         GRID_SIZE * randint(1, GRID_HEIGHT - 1))
        while self.position in positions:
            self.position = (GRID_SIZE * randint(1, GRID_WIDTH - 1),
                             GRID_SIZE * randint(1, GRID_HEIGHT - 1))
        return self.position


class Snake(GameObject):
    """Snake class"""

    def __init__(self, color=SNAKE_COLOR):
        super().__init__()
        self.length = 1
        self.positions = []
        self.direction = LEFT
        self.last = None
        self.body_color = color
        self.positions.append(self.position)

    def update_direction(self, next_direction=RIGHT):
        """Snake direction update"""
        self.direction = next_direction

    def move(self):
        """Snake move by keyboard to right, left, up and down."""
        head_position = self.get_head_position()
        head_new_position = (head_position[0] + self.direction[0] * GRID_SIZE,
                             head_position[1] + self.direction[1] * GRID_SIZE)

        # If head is at the right edge.
        if head_new_position[0] == SCREEN_WIDTH:
            head_new_position = (0, head_new_position[1])
        # If head is at the left edge.
        if head_new_position[0] == -GRID_SIZE:
            head_new_position = (SCREEN_WIDTH - GRID_SIZE,
                                 head_new_position[1])
        # If head is at the bottom edge.
        if head_new_position[1] == SCREEN_HEIGHT:
            head_new_position = (head_new_position[0], 0)
        # If head is at the top edge.
        if head_new_position[1] == -GRID_SIZE:
            head_new_position = (head_new_position[0],
                                 SCREEN_HEIGHT - GRID_SIZE)

        self.positions.insert(0, head_new_position)

        # Checking if snake not ate apple (variable "lenght" increases if ate).
        # If not ate - delete tail. Variable 'last' store position for "erase"
        # in "draw" method
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self):
        """Draw"""
        self.position = self.get_head_position()
        super().draw()

    def get_head_position(self):
        """Get snake's head position"""
        return self.positions[0]

    def reset(self):
        """Reset snake to defaults and clear old snake on screen"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.__init__(self.body_color)


def handle_keys(game_object):
    """User action processing function"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            elif event.key == pg.K_KP_MINUS or pg.K_KP_PLUS:
                game_speed(event.key)


def update_caption(max_snake_length=1):
    """Update caption (game speed and max snake lenght)"""
    pg.display.set_caption(f'''Змейка. Esc - выход. +/- - скорость.
 Скорость змейки: {speed}. Максимальная длина: {max_snake_length}''')


def game_speed(value):
    """Game speed updater. Used to prevent changing
    game speed less or equal 0
    """
    global speed
    if value == 1073741911:
        speed += 5
    else:
        speed -= 5
    if speed == 0:
        speed = 5  # Defaul min speed


def main():
    """Main function"""
    snake = Snake(SNAKE_COLOR)
    apple = Apple(snake.positions, APPLE_COLOR)
    potato = Apple(snake.positions, WRONG_FOOD_COLOR)
    screen.fill(BOARD_BACKGROUND_COLOR)
    max_snake_length = 1
    while True:

        handle_keys(snake)
        snake.move()

        # If snake eat apple
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1
            if max_snake_length < snake.length:
                max_snake_length = snake.length

        # Else if snake eat himself
        elif (snake.length > 4) and (snake.get_head_position()
                                     in snake.positions[4:]):
            max_snake_length = snake.length
            snake.reset()

        # Else if snake eat wrong food
        elif snake.get_head_position() == potato.position:
            if snake.length > 1:
                snake.draw()  # Redraw snake to delete tail on screen
                snake.last = snake.positions.pop()
                snake.length -= 1
            else:
                snake.reset()
            potato.randomize_position(snake.positions)
        apple.draw()
        potato.draw()
        snake.draw()
        update_caption(max_snake_length)
        pg.display.update()
        clock.tick(speed)


if __name__ == '__main__':
    main()
