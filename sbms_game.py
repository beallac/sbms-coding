import arcade

class Grid():
    def __init__(self, filename, grid_size=100):

        self.maze = arcade.ShapeElementList()

        # x_inc = arcade.get_display_size()[0] / grid_size
        # y_inc = arcade.get_display_size()[0] / grid_size

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
                        shape = arcade.create_rectangle_filled(x, y, x_inc, y_inc, arcade.csscolor.BLACK)
                        self.maze.append(shape)
                
                x += x_inc

            x = 0 + x_inc / 2
            y -= y_inc

        # self.maze = arcade.ShapeElementList()

        # for i in range(10):
        #     s = arcade.create_rectangle_filled(i*10, i*10, 10, 10, arcade.csscolor.BLACK)
        #     self.maze.append(s)

        