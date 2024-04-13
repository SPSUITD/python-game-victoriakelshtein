"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Космические приключения"


# Constants used to scale our sprites from their original size

CHARACTER_SCALING = 1

TILE_SCALING = 0.5



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        # These are 'lists' that keep track of our sprites. Each sprite should

        # go into a list.

        self.wall_list = None

        self.player_list = None


        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.color.BUBBLE_GUM)


    def setup(self):

        """Set up the game here. Call this function to restart the game."""

        # Create the Sprite lists

        self.player_list = arcade.SpriteList()

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)



        # Set up the player, specifically placing it at these coordinates.

        image_source = "img/cat.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        self.player_sprite.center_x = 100

        self.player_sprite.center_y = 180

        self.player_list.append(self.player_sprite)



        # Create the ground

        # This shows using a loop to place multiple sprites horizontally




        # Put some crates on the ground

        # This shows using a coordinate list to place sprites

        coordinate_list = [[420, 50], [100, 90], [400, 400], [500, 250], [290, 180], [110, 340], [220, 500]]



        for coordinate in coordinate_list:

            # Add a crate on the ground

            wall = arcade.Sprite(

                "img/fon.png", TILE_SCALING

            )

            wall.position = coordinate

            self.wall_list.append(wall)


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()


        # Draw our sprites

        self.wall_list.draw()

        self.player_list.draw()



def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()