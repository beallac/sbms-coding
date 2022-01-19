# Import the "arcade" library
import arcade

personX = personY = 300

def draw_person(x, y):
    arcade.draw_circle_filled(x, y, 50, arcade.csscolor.WHITE)
    arcade.draw_arc_filled(x, y, 40, 40, arcade.csscolor.BLUE, 0, 180)

def on_draw(delta_time):
    # Get ready to draw
    arcade.start_render()

    # Draw a rectangle for ground
    # Left of 0, right of 599
    # Top of 300, bottom of 0
    arcade.draw_lrtb_rectangle_filled(0, 600, 300, 0, arcade.csscolor.GREEN)

    draw_person(personX, personY)

def main():
    arcade.open_window(600, 600, "The droid")
    arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    arcade.schedule(on_draw, 1/60)

    # Keep the window up until someone closes it.
    arcade.run()

main()
