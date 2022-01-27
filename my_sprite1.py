# Import the "arcade" library
import arcade
import random
import math
import time

# from arcade.experimental.crt_filter import CRTFilter
# from pyglet.math import Vec2

class Person():
    def __init__(self):
        self.x = 300
        self.y = 300

        self.my_sprite = arcade.Sprite("char1.png", center_x = self.x, center_y = self.y)

    def draw_person(self):
        self.my_sprite.update()
        self.my_sprite.draw()
        return

class MyWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.person1 = Person()

        # # Create the crt filter
        # self.crt_filter = CRTFilter(1200, 1200,
        #                             resolution_down_scale=6.0,
        #                             hard_scan=-8.0,
        #                             hard_pix=-3.0,
        #                             display_warp = Vec2(1.0 / 32.0, 1.0 / 24.0),
        #                             mask_dark=0.5,
        #                             mask_light=1.5)
      
    def on_draw(self):
        # # Draw our stuff into the CRT filter instead of on screen
        # self.crt_filter.use()
        # self.crt_filter.clear()

        # Get ready to draw
        arcade.start_render()

        # Draw a rectangle for ground
        # Left of 0, right of 599
        # Top of 300, bottom of 0
        arcade.draw_lrtb_rectangle_filled(0, 600, 300, 0, arcade.csscolor.GREEN)

        self.person1.draw_person()

        # # Next, switch back to the screen and dump the contents of the CRT filter to it.
        # self.use()
        # self.clear()
        # self.crt_filter.draw()
        

    def on_key_press(self, symbol, modifier):

        if symbol == arcade.key.LEFT:
            print('left')
            self.person1.my_sprite.change_x = -1

        if symbol == arcade.key.RIGHT:
            pass


    def on_key_release(self, symbol, modifier):

        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.person1.my_sprite.change_x = 0

        

def main():
    MyWindow(600, 600, "The sprite")

    arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    # Keep the window up until someone closes it.
    arcade.run()

main()
