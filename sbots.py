import socket, time, select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10020)
print('made sock')

# sock.bind(server_address)
sock.connect(server_address)
print('made connection')

def motorPair(left, right):
    m = "D " + str(round(left, 1)) + " " + str(round(right, 1))
    b = bytes(m, 'utf-8')
    sock.sendall(b)
    # Add sleep here
    time.sleep(0.05)


lastSensorReading = False

def pollSensors():
    global lastSensorReading

    m = "S "
    b = bytes(m, 'utf-8')
    sock.sendall(b)

    # Add sleep here
    time.sleep(0.05)

    readable, writable, errored = select.select([sock], [], [], .01)

    if not readable:
        return lastSensorReading

    d = sock.recv(1024)
    # print("Data", d)
    
    s = d.split()
    # print('len', len(s))
    if len(s) != 9:
        return lastSensorReading

    lastSensorReading = [ float(s[1]), float(s[2]), float(s[3]), float(s[4]), float(s[5]), float(s[6]), float(s[7]), float(s[8]) ]

    return lastSensorReading


lastCompassReading = False

def pollCompass():
    global lastCompassReading

    m = "C "
    b = bytes(m, 'utf-8')
    sock.sendall(b)

    # Add sleep here
    time.sleep(0.05)

    readable, writable, errored = select.select([sock], [], [], .01)

    if not readable:
        return lastCompassReading

    d = sock.recv(1024)
    # print("Data", d)
    
    s = d.split()
    # print('len', len(s))
    if len(s) != 2:
        return lastCompassReading

    lastCompassReading = float(s[1])
    return lastCompassReading


if __name__ == "__main__":

    while True:
        motorPair(1.0, -1.0)
        time.sleep(.25)
        dist = pollSensors()
        print('-------------', dist)
        comp = pollCompass()
        print('.............' ,comp)
        time.sleep(.25)

else:
    time.sleep(.25)



