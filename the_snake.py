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
DEFAULT_COLOR = (10, 10, 10)

speed = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Base class"""

    def __init__(self, body_color=DEFAULT_COLOR):
        self.position = (
            GRID_SIZE * (GRID_WIDTH // 2), GRID_SIZE * (GRID_HEIGHT // 2)
        )
        self.body_color = body_color

    def draw(self):
        """Base class draw method"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Apple class"""

    def __init__(self, *occupied_positions, body_color=APPLE_COLOR,):
        super().__init__(body_color=body_color)
        self.randomize_position(*occupied_positions)

    def randomize_position(self, *occupied_positions):
        """Randomize apple position"""
        positions = []
        for arg in occupied_positions:
            (positions.append(arg) if type(arg) is
             tuple else positions.extend(arg))
            positions.append(self.position)
        while self.position in positions:
            self.position = (
                GRID_SIZE * randint(1, GRID_WIDTH - 1),
                GRID_SIZE * randint(1, GRID_HEIGHT - 1)
            )


class Snake(GameObject):
    """Snake class"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.length = 1
        self.positions = []
        self.direction = RIGHT
        self.last = []
        self.positions.append(self.position)
        self.reset()

    def update_direction(self, next_direction=RIGHT):
        """Snake direction update"""
        self.direction = next_direction

    def move(self):
        """Snake move by keyboard to right, left, up and down."""
        head_position = (
            (self.get_head_position()[0] + self.direction[0] * GRID_SIZE)
            % SCREEN_WIDTH,
            (self.get_head_position()[1] + self.direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT
        )
        self.positions.insert(0, head_position)

        # Checking if snake not ate apple (variable "lenght" increases if ate).
        # If not ate - delete tail. Variable 'last' store position for "erase"
        # in "draw" method
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self):
        """Draw"""
        self.position = self.get_head_position()
        super().draw()
        last_rect = pg.Rect((self.last), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Get snake's head position"""
        return self.positions[0]

    def reset(self):
        """Reset snake to defaults"""
        self.length = 1
        self.position = (
            GRID_SIZE * (GRID_WIDTH // 2), GRID_SIZE * (GRID_HEIGHT // 2)
        )
        self.positions = []
        self.direction = RIGHT
        self.positions.append(self.position)


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
            elif event.key == pg.K_q or event.key == pg.K_a:
                game_speed(event.key)


def update_caption(max_snake_length=1):
    """Update caption (game speed and max snake lenght)"""
    pg.display.set_caption(
        'Змейка. Esc - выход. Q/A - скорость.'
        f'Скорость змейки: {speed}. Максимальная длина: {max_snake_length}'
    )


def game_speed(value):
    """Game speed updater"""
    global speed
    if value == pg.K_q:
        speed += 5
    else:
        speed -= 5
    if speed == 0:
        speed = 5  # Defaul min speed


def main():
    """Main function"""
    snake = Snake()
    apple = Apple(snake.positions)
    potato = Apple(
        snake.positions, apple.position,
        body_color=WRONG_FOOD_COLOR
    )
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
                '''To prevent max_snake_length from updating in new round,
                until snake reach new max length.'''
                max_snake_length = snake.length

        # Else if snake eat himself
        elif (snake.length > 4) and (snake.get_head_position()
                                     in snake.positions[4:]):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Else if snake eat wrong food
        elif snake.get_head_position() == potato.position:
            if snake.length > 1:
                snake.draw()  # Redraw snake to delete tail on screen
                snake.last = snake.positions.pop()
                snake.length -= 1
            else:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
            potato.randomize_position(snake.positions, apple.position)
        apple.draw()
        potato.draw()
        snake.draw()
        update_caption(max_snake_length)
        pg.display.update()
        clock.tick(speed)


if __name__ == '__main__':
    main()
