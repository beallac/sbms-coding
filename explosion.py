"""
Sprite Explosion

Simple program to show how to make explosions with a series of bitmaps.

Artwork from https://kenney.nl
Explosion graphics from https://www.explosiongenerator.com/

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_explosion_bitmapped
"""
import random
import arcade
import os


EXPLOSION_TEXTURE_COUNT = 60

class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


# Variables that will hold sprite lists
explosions_list = None


# Pre-load the animation frames. We don't do this in the __init__
# of the explosion sprite because it
# takes too long and would cause the game to pause.
explosion_texture_list = []

columns = 16
count = 60
sprite_width = 256
sprite_height = 256
file_name = ":resources:images/spritesheets/explosion.png"

# Load the explosions from a sprite sheet
explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

# Load sounds. Sounds from kenney.nl
hit_sound = arcade.sound.load_sound(":resources:sounds/explosion2.wav")

explosions_list = arcade.SpriteList()


def on_draw():
    explosions_list.draw()


def on_update():
    explosions_list.update()


def hit(location):
    # Make an explosion
    explosion = Explosion(explosion_texture_list)

    # Move it to the location of the coin
    explosion.center_x = location[0]
    explosion.center_y = location[1]

    # Call update() because it sets which image we start on
    explosion.update()

    # Add to a list of sprites that are explosions
    explosions_list.append(explosion)

    # Hit Sound
    arcade.sound.play_sound(hit_sound)
