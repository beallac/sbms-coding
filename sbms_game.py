import arcade

class Grid():
    def __init__(self, filename, grid_size=100):

        self.maze = arcade.ShapeElementList()

        x_inc = arcade.get_window().width / grid_size
        y_inc = arcade.get_window().height / grid_size

        print('Increments: ', y_inc, y_inc)

        f = open(filename, 'r')
        allLines = f.readlines()
        f.close()

        x = 0 + x_inc/2
        y = arcade.get_window().height - y_inc/2

        for line in allLines:
            ss = line.split(',')
            for s in ss:
                if s:
                    if s[0] == '1':
                        # shape = arcade.create_rectangle_filled(x, y, x_inc, y_inc, arcade.csscolor.BLACK)
                        shape = arcade.create_rectangle_filled(x, y, x_inc, y_inc, (0, 0, 0))
                        self.maze.append(shape)
                    elif s[0] == '2':   # Use for horizontal surfaces
                        # shape = arcade.create_rectangle_filled(x, y, x_inc, y_inc, arcade.csscolor.BLACK)
                        shape = arcade.create_rectangle_filled(x, y, x_inc, y_inc, (0, 0, 2))
                        self.maze.append(shape)
                    elif s[0] == '3':   # Use for vertical surfaces
                        # shape = arcade.create_rectangle_filled(x, y, x_inc, y_inc, arcade.csscolor.BLACK)
                        shape = arcade.create_rectangle_filled(x, y, x_inc, y_inc, (0, 0, 3))
                        self.maze.append(shape)
                
                x += x_inc

            x = 0 + x_inc / 2
            y -= y_inc



EXPLOSION_TEXTURE_COUNT = 60

class Explosion(arcade.Sprite):
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

    @classmethod
    def draw(cls):
        cls.explosions_list.update()
        cls.explosions_list.draw()
    
    @classmethod
    def hit(cls, location):
        # Make an explosion
        explosion = Explosion(cls.explosion_texture_list)

        # Move it to the location of the coin
        explosion.center_x = location[0]
        explosion.center_y = location[1]

        # Call update() because it sets which image we start on
        explosion.update()

        # Add to a list of sprites that are explosions
        cls.explosions_list.append(explosion)

        # Hit Sound
        arcade.sound.play_sound(cls.hit_sound)

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



class SpriteAnimated(arcade.Sprite):

    def __init__(self, spritesheet, columns, grid_size, count):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.count = count
        self.textures = arcade.load_spritesheet(spritesheet, grid_size, grid_size, columns, count)
        self.set_texture(self.current_texture)

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        self.set_texture(self.current_texture % self.count)



        # enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]
        # for my_object in enemies_layer:
        #     cartesian = self.tile_map.get_cartesian(my_object.shape[0], my_object.shape[1])
        #     enemy_type = my_object.properties['type']
        #     if enemy_type == "zombie":
        #         enemy = arcade.Sprite("resources/tank.png", scale = SPRITE_SCALING)
        #     if enemy_type == "robot":
        #         enemy = arcade.Sprite("resources/tank.png", scale = SPRITE_SCALING)
        #     enemy.center_x = cartesian[0] * TILE_SCALING * self.tile_map.tile_width
        #     enemy.center_y = (cartesian[1] + 1) * TILE_SCALING * self.tile_map.tile_height
        #     if "boundary_left" in my_object.properties:
        #         enemy.boundary_left = my_object.properties["boundary_left"]
        #     if "boundary_right" in my_object.properties:
        #         enemy.boundary_right = my_object.properties["boundary_right"]
        #     if "change_x" in my_object.properties:
        #         enemy.change_x = my_object.properties["change_x"]
        #     self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)



        # self.scene.update(
        #     [LAYER_NAME_ENEMIES],
        # )

        # # See if the enemy hit a boundary and needs to reverse direction.
        # for enemy in self.scene[LAYER_NAME_ENEMIES]:
        #     if (
        #         enemy.boundary_right
        #         and enemy.right > enemy.boundary_right
        #         and enemy.change_x > 0
        #     ):
        #         enemy.change_x *= -1
        #     if (
        #         enemy.boundary_left
        #         and enemy.left < enemy.boundary_left
        #         and enemy.change_x < 0
        #     ):
        #         enemy.change_x *= -1
