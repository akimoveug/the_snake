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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Def class"""

    position = (GRID_SIZE * (GRID_WIDTH // 2), GRID_SIZE * (GRID_HEIGHT // 2))
    body_color = (128, 128, 128)

    def __init__(self):
        pass

    def draw(self):
        """Abstract method"""
        pass


class Apple(GameObject):
    """Apple class"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Randomize apple position"""
        position_x = GRID_SIZE * randint(1, GRID_WIDTH - 1)
        position_y = GRID_SIZE * randint(1, GRID_HEIGHT - 1)
        return (position_x, position_y)

    def draw(self, surface):
        """Draw apple"""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class WrongFood(Apple):
    """Wrong food class"""

    def __init__(self):
        super().__init__()
        self.body_color = (117, 78, 27)


class Snake(GameObject):
    """Snake class"""

    length = 1  # Snake lenght. Used in "move" method.
    positions: list = []
    direction = RIGHT
    next_direction = None
    last = None

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions.append(self.position)

    def update_direction(self):
        """Snake direction update"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Snake move by keyboard to right, left, up and down. Moving
        by inserting new coordinates to tail.
        """
        if self.direction == RIGHT:
            # If head is at the right edge.
            if self.positions[0][0] == SCREEN_WIDTH - GRID_SIZE:
                self.positions.insert(0, (0, self.positions[0][1]))
            else:
                self.positions.insert(0, (self.positions[0][0] + GRID_SIZE,
                                          self.positions[0][1]))

        elif self.direction == LEFT:
            # If head is at the left edge.
            if self.positions[0][0] == 0:
                self.positions.insert(0, (SCREEN_WIDTH - GRID_SIZE,
                                          self.positions[0][1]))
            else:
                self.positions.insert(0, (self.positions[0][0] - GRID_SIZE,
                                          self.positions[0][1]))

        elif self.direction == UP:
            # If head is at the top edge.
            if self.positions[0][1] == 0:
                self.positions.insert(0, (self.positions[0][0],
                                          SCREEN_HEIGHT - GRID_SIZE))
            else:
                self.positions.insert(0, (self.positions[0][0],
                                          self.positions[0][1] - GRID_SIZE))

        elif self.direction == DOWN:
            # If head is at the bottom edge.
            if self.positions[0][1] == SCREEN_HEIGHT - GRID_SIZE:
                self.positions.insert(0, (self.positions[0][0], 0))
            else:
                self.positions.insert(0, (self.positions[0][0],
                                          self.positions[0][1] + GRID_SIZE))
        # Checking if snake not ate apple (variable "lenght" increases if ate).
        # If not ate - delete tail. Variable 'last' store position for "erase"
        # in "draw" method
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self, surface):
        """Draw"""
        for position in self.positions[:-1]:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Draw snake's head
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Erase snake's tail
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
        pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Get snake's head position"""
        return self.positions[0]

    def reset(self, surface):
        """Reset snake to defaults and clear old snake on screen"""
        for position in self.positions:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """User action processing function"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main function"""
    apple = Apple()
    snake = Snake()
    potato = WrongFood()
    while True:
        clock.tick(SPEED)
        apple.draw(screen)
        potato.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)

        # If snake eat apple
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position()
            snake.length += 1

        # If snake eat himself
        if (snake.length > 4) and (snake.get_head_position()
                                   in snake.positions[4:]):
            snake.reset(screen)

        # If snake eat wrong food
        if snake.get_head_position() == potato.position:
            if snake.length > 1:
                potato.position = potato.randomize_position()
                snake.last = snake.positions.pop()
                snake.length -= 1
                snake.draw(screen)
            else:
                potato.position = potato.randomize_position()
                snake.reset(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
