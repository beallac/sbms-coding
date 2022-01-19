from pynput import keyboard


keepGoing = True

def on_press(key):
    global keepGoing

    if key == keyboard.Key.esc:
        keepGoing = False
        print('escape')

    if key == keyboard.Key.up:
        print('up')

    if key == keyboard.Key.down:
        print('down')

    if key == keyboard.Key.right:
        print('right')

    if key == keyboard.Key.left:
        print('left')


listener = keyboard.Listener(on_press=on_press)
listener.start()

while keepGoing:
    pass
