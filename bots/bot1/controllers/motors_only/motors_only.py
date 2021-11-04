"""motors_only controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

import socket, select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10020)

server_socket.bind(server_address)

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)


TIME_STEP = 64

MAX_SPEED = 6.28


# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

#rLED = robot.getDevice('led0')
#rLED.set(1)

# set up the motor speeds at 10% of the MAX_SPEED.
#leftMotor.setVelocity(0.1 * MAX_SPEED)
#rightMotor.setVelocity(0.1 * MAX_SPEED)
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

server_socket.listen(1)



read_list = [server_socket]

while robot.step(TIME_STEP) != -1:

    readable, writable, errored = select.select(read_list, [], [], .01)
    for s in readable:
        if s is server_socket:
            client_socket, address = server_socket.accept()
            read_list.append(client_socket)
            print ("Connection from", address)
        else:
            data = s.recv(1024)
            if data:
                print(data)
                s = data.split()

                if s[0] == b'D':
                    print('setting speed')

                    #leftMotor.setVelocity(0.1 * MAX_SPEED)
                    #rightMotor.setVelocity(0.1 * MAX_SPEED)

                    leftMotor.setVelocity(float(s[1]))
                    rightMotor.setVelocity(float(s[2]))
            else:
                s.close()
                read_list.remove(s)




# Enter here exit cleanup code.
