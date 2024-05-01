from random import choice, randint

import pygame

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

# Цвет камня
ROCK_COLOR = (211, 211, 211)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, body_color=None):
        """
        Инициализация базовых атрибутов объекта,]
        таких как его позиция и цвет.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        Этот метод должен определять,
        как объект будет отрисовываться на экране..
        """
        pass


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    Яблоко должно отображаться
    в случайных клетках игрового поля.
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация объекта-яблоко и его цвета."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """
        Метод для установки позиции яблока
        случайным образом на игрвом поле.
        """
        x = GRID_SIZE * randint(0, GRID_WIDTH - 1)
        y = GRID_SIZE * randint(0, GRID_HEIGHT - 1)
        self.position = (x, y)

    def draw(self):
        """Метод отрисовывает объект-камень на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Rock(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий камень и действия с ним.
    Камень отображается в случайной клетке игрового поля при запуске игры.
    """

    def __init__(self, body_color=ROCK_COLOR):
        """Инициализация объекта-камня"""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """
        Метод для установки позиции камня
        случайным образом на игрвом поле.
        """
        x = GRID_SIZE * randint(0, GRID_WIDTH - 1)
        y = GRID_SIZE * randint(0, GRID_HEIGHT - 1)
        self.position = (x, y)

    def draw(self):
        """Метод отрисовывает объект-камень на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject, описывающий змейку и её поведение.
    Этот класс управляет её движением, отрисовкой, а также
    обрабатывает действия пользователя.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация начальногоё состояние змейки."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [(self.position)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        head_coord = self.get_head_position()
        coord_x = head_coord[0] + self.direction[0] * GRID_SIZE
        coord_y = head_coord[1] + self.direction[1] * GRID_SIZE

        if coord_x > SCREEN_WIDTH:
            coord_x = 0
        elif coord_x < 0:
            coord_x = SCREEN_WIDTH

        if coord_y > SCREEN_HEIGHT:
            coord_y = 0
        elif coord_y < 0:
            coord_y = SCREEN_HEIGHT

        print(self.positions)
        print(self.length)
        if self.length == len(self.positions):
            self.last = self.positions.pop()

        # Добавление координаты головы
        self.positions.insert(0, (coord_x, coord_y))

    def draw(self):
        """Метод для отрисовки змейки и затирания следа."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """
        Метод обновляет игрвоое поле, сбрасывая змейку в начальное состояние.
        Вызывается при столкновении с самой собой или с камнем.
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice((UP, RIGHT, DOWN, LEFT))


def handle_keys(game_object):
    """
    Функция обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        # print("event loop!")
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Точка входа в программу.
    Инициализация игры и запуск основного игрового цикла.
    """
    pygame.init()

    apple = Apple()
    snake = Snake()
    rock = Rock()

    while apple.position in snake.positions:
        apple.randomize_position()

    while rock.position in (snake.position, apple.position):
        rock.randomize_position()

    apple.draw()
    snake.draw()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if (
            snake.get_head_position() in snake.positions[2:]
            or snake.get_head_position() == rock.position
        ):
            snake.reset()
            apple.randomize_position()
            rock.randomize_position()

        elif snake.get_head_position() == apple.position:
            while apple.position in snake.positions:
                apple.randomize_position()
            snake.length += 1

        snake.draw()
        apple.draw()
        rock.draw()

        pygame.display.update()


if __name__ == "__main__":
    """
    Точка входа в программу.
    Вызывается при запуске файла напрямую.
    """
    main()
