import arcade

# --- Constants ---
SPRITE_SCALING = 0.5
TILE_SCALING = .5
GRID_PIXEL_SIZE = 128
GRAVITY = 0.25

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Go SBMS!"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 10

LAYER_NAME_WALLS = "Walls"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_REWARDS = "Rewards"
LAYER_NAME_LADDERS = "Ladders"

MAP_NAME = "level1.json"


class GameIntroView(arcade.View):
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        view = GamePlayView()
        self.window.show_view(view)

class GamePlayView(arcade.View):
    """ View to show when game is over """

    def on_show(self):

        # Set up the player
        self.player_sprite = None

        # Physics engine so we don't run into walls.
        self.physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Store our tile map
        self.tile_map = None
        self.scene = None


        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Sprite lists
        # self.player_list = arcade.SpriteList()
        # self.wall_list = arcade.SpriteList()
        # self.object_list = arcade.SpriteList()


        # --- Load our map

        # Read in the tiled map

        layer_options = {
            "Walls": {
                "use_spatial_hash": True,
            },
            "Rewards": {
                "use_spatial_hash": True,
            },
            "Ladders": {
                "use_spatial_hash": True,
            },
            "Platforms": {
                "use_spatial_hash": False,
            },
        }

        # Read in the tiled map
        try:
            self.tile_map = arcade.load_tilemap(MAP_NAME, TILE_SCALING, layer_options)
        except:
            print("\n\n\n***** Tilemap does not exist ******\n\n\n")
    
        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           scale=0.4)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.scene.add_sprite("Player", self.player_sprite)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep player from running through the wall_list layer
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_NAME_PLATFORMS],
            walls=self.scene[LAYER_NAME_WALLS],
            # ladders=self.scene[LAYER_NAME_LADDERS],
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.scene.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the GUI
        arcade.draw_rectangle_filled(self.window.width // 2,
                                     20,
                                     self.window.width,
                                     40,
                                     arcade.color.ALMOND)
        text = f"Scroll value: ({self.camera_sprites.position[0]:5.1f}, " \
               f"{self.camera_sprites.position[1]:5.1f})"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

        elif key == arcade.key.E:
            view = GameEndView()
            self.window.show_view(view)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0

        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        # self.player_sprite.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()


        # # See if we hit any rewards
        # reward_hit_list = arcade.check_for_collision_with_list(
        #     self.player_sprite, self.scene[LAYER_NAME_REWARDS]
        # )

        # # Loop through each reward we hit (if any) and remove it
        # for reward in reward_hit_list:

        #     # Figure out how many points this reward is worth
        #     if "Points" not in reward.properties:
        #         print("Warning, collected a reward without a Points property.")
        #     else:
        #         points = int(reward.properties["Points"])
        #         self.score += points

        #     # Remove the reward
        #     reward.remove_from_sprite_lists()


        # Scroll the screen to the player
        self.scroll_to_player()
        
    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a
        smoother pan.
        """

        position = self.player_sprite.center_x - self.window.width / 2, \
            self.player_sprite.center_y - self.window.height / 2
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))

class GameEndView(arcade.View):
    """ Our custom Window Class"""

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """ Draw this view """
        self.window.clear()
        arcade.draw_text("GAME OVER Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        view = GameIntroView()
        self.window.show_view(view)


def main():
    """ Main function """
    window = arcade.Window(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    view = GameIntroView()
    window.show_view(view)
    arcade.run()

main()