import arcade
import random

# Константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Космические приключения"

# Константы, используемые для масштабирования наших спрайтов по сравнению с их первоначальным размером
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
JUMP_MAX_HEIGHT = 150
GRAVITY = 2
MAX_JUMPS = 2  # Максимальное количество прыжков
LOSS_HEIGHT = 300  # Высота, на которую игрок должен упасть, чтобы проиграть

class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.BUBBLE_GUM)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Конец игры", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                        arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text(f"Ваш рекорд: {int(self.game_view.high_score)}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Нажмите, чтобы начать заново", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                        arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.game_view.restart_game()
        self.window.show_view(self.game_view)

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Вызовите родительский класс и настройте окно
        super().__init__()

        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.camera = None
        self.player_jump = False
        self.jump_start = None
        self.player_y = 0  # Переменная для отслеживания текущей высоты игрока
        self.score = 0
        self.moving_left = False
        self.moving_right = False
        self.jump_count = 0  # Счетчик количества прыжков
        self.high_score = 0  # Самый высокий результат в текущей сессии

        self.game_over_view = None

        arcade.set_background_color(arcade.color.BUBBLE_GUM)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Set up the Camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Создаем основную платформу в нижней части экрана
        main_platform = arcade.Sprite("img/fon.png", TILE_SCALING)
        main_platform.position = SCREEN_WIDTH / 2, 50
        main_platform.width = 100
        main_platform.height = 20
        self.wall_list.append(main_platform)

        # Настройте проигрыватель, специально разместив его на верхней платформе
        image_source = "img/cat.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = main_platform.top + self.player_sprite.height / 2 + 1  # Увеличиваем высоту, чтобы игрок не подтягивался
        self.player_list.append(self.player_sprite)

        # Создаем остальные случайные платформы
        for i in range(8):
            wall = arcade.Sprite("img/fon.png", TILE_SCALING)
            wall.position = random.randrange(SCREEN_WIDTH), i * 80 + main_platform.top + 80
            wall.width = 100
            wall.height = 20
            wall.center_y += 10
            self.wall_list.append(wall)

        self.game_over_view = GameOverView(self)

    def restart_game(self):
        """Restart the game"""
        self.setup()
        self.player_y = 0  # Сбросить рекорд
        self.jump_count = 0  # Сбросить счетчик прыжков
        # Обновляем самый высокий результат
        self.high_score = max(self.high_score, self.player_y)
        self.center_camera_to_player()  # Установить камеру на игрока
        self.window.show_view(self.game_over_view)
        # Опустить камеру вниз после перезапуска игры
        self.camera.move_to((0, 0))
        self.camera.use()
        self.camera.update()

    def on_draw(self):
        """Render the screen."""
        self.clear()

        self.wall_list.draw()
        self.player_list.draw()

        text = f"рекорд: {int(self.player_y)}"
        arcade.draw_text(text, 10 + self.camera.position[0], SCREEN_HEIGHT - 30 + self.camera.position[1],
                        arcade.color.BLACK, 14)

        self.camera.use()
        self.camera.update()

    def center_camera_to_player(self):
        """Center the camera on the player"""
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        
        # Ограничение камеры по горизонтали
        if screen_center_x < 0:
            screen_center_x = 0
        elif screen_center_x > SCREEN_WIDTH - self.camera.viewport_width:
            screen_center_x = SCREEN_WIDTH - self.camera.viewport_width
        
        # Ограничение камеры по вертикали
        if screen_center_y < 0:
            screen_center_y = 0
        
        self.camera.move_to((screen_center_x, screen_center_y))


    def on_update(self, delta_time):
        """Movement and game logic"""
        if self.player_jump and self.jump_start is not None:
            self.player_sprite.center_y += 6
            self.player_y = max(self.player_y, self.player_sprite.center_y)
            if self.player_sprite.center_y >= self.jump_start + JUMP_MAX_HEIGHT:
                self.player_jump = False
                self.player_y = self.player_sprite.center_y
        else:
            if self.jump_start is not None:
                self.player_sprite.center_y -= 6

        on_platform = False
        for wall in self.wall_list:
            if arcade.check_for_collision(self.player_sprite, wall):
                if self.player_sprite.bottom <= wall.top and self.player_sprite.bottom + 6 >= wall.top:  # Изменяем условие проверки столкновения
                    self.player_sprite.center_y += (wall.top - self.player_sprite.bottom)
                    on_platform = True
                    self.player_jump = False
                    self.jump_count = 0  # Сбросить счетчик прыжков
                    break

        if not on_platform:
            self.player_sprite.center_y -= GRAVITY

        if self.player_sprite.center_y < self.player_y - LOSS_HEIGHT:  # Игрок упал на 300 пунктов от достигнутой высоты
            self.restart_game()

        if self.player_sprite.center_x - self.player_sprite.width / 2 <= 0:
            self.player_sprite.center_x = self.player_sprite.width / 2
        elif self.player_sprite.center_x + self.player_sprite.width / 2 >= SCREEN_WIDTH:
            self.player_sprite.center_x = SCREEN_WIDTH - self.player_sprite.width / 2

        self.center_camera_to_player()

        if self.moving_right:
            self.player_sprite.change_x = 4
        elif self.moving_left:
            self.player_sprite.change_x = -4
        else:
            self.player_sprite.change_x = 0

        self.player_sprite.update()

        self.create_random_platforms()
        self.center_camera_to_player()

        # Обновляем самый высокий результат
        self.high_score = max(self.high_score, self.player_y)

    def create_random_platforms(self):
        top_platform = max([wall.top for wall in self.wall_list])
        while top_platform < self.player_sprite.top + SCREEN_HEIGHT:
            x = random.randrange(0, SCREEN_WIDTH)
            y = top_platform + random.randint(80, 200)
            wall = arcade.Sprite("img/fon.png", TILE_SCALING)
            wall.position = x, y
            wall.width = 100
            wall.height = 20
            wall.center_y += 10
            if wall.top < self.camera.position[1] - SCREEN_HEIGHT / 2:
                wall.remove_from_sprite_lists()  # Удаляем нижние платформы, которые за пределами камеры
            else:
                self.wall_list.append(wall)
            top_platform = y


    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.moving_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.moving_right = True
        elif key == arcade.key.UP or key == arcade.key.SPACE:
            if self.jump_count < MAX_JUMPS:  # Проверяем количество совершенных прыжков
                self.player_jump = True
                self.jump_start = self.player_sprite.center_y
                self.jump_count += 1  # Увеличиваем счетчик прыжков

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.moving_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.moving_right = False

class MyGameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_view = MyGame()
        self.game_view.setup()
        self.show_view(self.game_view)

def main():
    """Main function"""
    window = MyGameWindow()
    arcade.run()

if __name__ == "__main__":
    main()
