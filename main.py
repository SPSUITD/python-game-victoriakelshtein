"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000 #размер окна
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Космические приключения"


# Константы, используемые для масштабирования наших спрайтов по сравнению с их первоначальным размером

CHARACTER_SCALING = 1 # размер персонажа
TILE_SCALING = 0.5

JUMP_MAX_HEIGHT = 100

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Вызовите родительский класс и настройте окно
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Это "списки", которые отслеживают наши спрайты. Каждый спрайт должен быть помещен в список

        self.wall_list = None
        self.player_list = None


        # Отдельная переменная, содержащая спрайт игрока
        self.player_sprite = None

        self.camera = None

        self.player_jump = False
        self.jump_start = None
        self.camera_max = 0

        arcade.set_background_color(arcade.color.BUBBLE_GUM)


    def setup(self):

        """Set up the game here. Call this function to restart the game."""

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Создайте списки спрайтов

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Настройте проигрыватель, специально разместив его по этим координатам

        image_source = "img/cat.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 180
        self.player_list.append(self.player_sprite) # расположение кота


        coordinate_list = [[420, 50], [100, 90], [400, 400], [500, 250], [290, 180], [110, 340], [220, 500]] #координаты платформ

        for coordinate in coordinate_list:
            # Поставьте ящик на землю
            wall = arcade.Sprite(

                "img/fon.png", TILE_SCALING 

            )

            wall.position = coordinate
            self.wall_list.append(wall)


    def on_draw(self):
        """Render the screen."""

        # Очистите экран до цвета фона
        self.clear()

        # Нарисуем наших спрайтов
        self.wall_list.draw()
        self.player_list.draw()

        # Activate our Camera
        self.camera.use()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        if self.player_sprite.center_y - ( self.camera.viewport_height / 2) >= self.camera_max:
            screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
            self.camera_max = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        else:
            screen_center_y = self.camera_max


        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""
        #self.player_sprite.center_y += 1
        #self.player_sprite.center_x += 1
       
        if self.player_jump:
            self.player_sprite.center_y += 2
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIGHT:
                self.player_jump = False
        else:
            self.player_sprite.center_y -= 2

        # Position the camera
        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_jump == True
            self.jump_start = self.player_sprite.center_y
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.center_y -= 15
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.center_x -= 15
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.center_x += 15 
            # управление котом

    


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()