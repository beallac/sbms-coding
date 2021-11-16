"""motors_only controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, DistanceSensor

from controller import Supervisor
import sys, math
supervisor = Supervisor()
# do this once only
robot_node = supervisor.getFromDef("MY_ROBOT")
if robot_node is None:
    sys.stderr.write("No DEF MY_ROBOT node found in the current world file\n")
    sys.exit(1)
else:
    print("Supervisor activated!!!")
trans_field = robot_node.getField("translation")

import socket, select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10020)

server_socket.bind(server_address)

# create the Robot instance.
# robot = Robot()
robot = supervisor

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

d0 = robot.getDevice('ds0')
d0.enable(TIME_STEP)

d1 = robot.getDevice('ds1')
d1.enable(TIME_STEP)

d2 = robot.getDevice('ds2')
d2.enable(TIME_STEP)

d3 = robot.getDevice('ds3')
d3.enable(TIME_STEP)

d4 = robot.getDevice('ds4')
d4.enable(TIME_STEP)

d5 = robot.getDevice('ds5')
d5.enable(TIME_STEP)

d6 = robot.getDevice('ds6')
d6.enable(TIME_STEP)

d7 = robot.getDevice('ds7')
d7.enable(TIME_STEP)

sensors = [d0, d1, d2, d3, d4, d5, d6, d7]

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

    # # print(robot_node.getPosition())
    R = robot_node.getOrientation()
    # # y = (m02 - m20)/√((m21 - m12)2+(m02 - m20)2+(m10 - m01)2)
    y = (R[2]-R[6]) / math.sqrt((R[7]-R[5])**2 + (R[2]-R[6])**2 + (R[3]-R[1])**2)
    # # angle = acos(( m00 + m11 + m22 - 1)/2)
    angle = math.acos(( R[0] + R[4] + R[8] - 1)/2) / math.pi * 180
    angle *= -y
    
    m = ""
    for sensor in sensors:
        reading = sensor.getValue()
        m += ( "{:6.1f} ".format(reading) )
    m += ( "{:6.1f} ".format(angle) )
    print(m)
    # print('d: ', d0.getValue(), d1.getValue(), d2.getValue(), d3.getValue(), d4.getValue(), d5.getValue(), d6.getValue(), d7.getValue() )

    readable, writable, errored = select.select(read_list, [], [], .01)
    for s in readable:
        if s is server_socket:
            client_socket, address = server_socket.accept()
            read_list.append(client_socket)
            print ("Connection from", address)
        else:
            data = s.recv(1024)
            if data:
                # print(data)
                sp = data.split()

                if sp[0] == b'D' and len(sp) == 3:
                    # print('setting speed')

                    #leftMotor.setVelocity(0.1 * MAX_SPEED)
                    #rightMotor.setVelocity(0.1 * MAX_SPEED)
                    
                    try:
                        leftM = float(sp[1])
                        rightM = float(sp[2])
                        
                        leftMotor.setVelocity(leftM)
                        rightMotor.setVelocity(rightM)
                        
                    except:
                        pass
                    
                if sp[0] == b'S':
                
                    m = 'S '
                    
                    for sensor in sensors:
                        reading = sensor.getValue()
                        m += ( "{:.2f} ".format(reading) )
                        b = bytes(m, 'utf-8')
                    s.send(b)
                
                if sp[0] == b'C':
                
                    m = 'C '                    
                    m += ( "{:.2f} ".format(angle) )
                    b = bytes(m, 'utf-8')
                    s.send(b)
                  
                                    
            else:
                s.close()
                read_list.remove(s)




# Enter here exit cleanup code.
