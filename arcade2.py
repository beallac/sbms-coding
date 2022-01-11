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


# #-----------------------------------------------------
# from pynput import keyboard

# def on_press(key):
#     global personX, personY

#     if key == keyboard.Key.up:
#         personY += 1

#     if key == keyboard.Key.down:
#         personY -= 1

#     if key == keyboard.Key.right:
#         personX += 1

#     if key == keyboard.Key.left:
#         personX -= 1

# listener = keyboard.Listener(on_press=on_press)
# listener.start()


