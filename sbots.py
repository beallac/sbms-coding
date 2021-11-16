import socket, time

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

def pollSensors():
    m = "S "
    b = bytes(m, 'utf-8')
    sock.sendall(b)

    # Add sleep here
    time.sleep(0.05)

    d = sock.recv(1024)
    # print("Data", d)
    
    s = d.split()
    # print('len', len(s))
    if len(s) != 9:
        return 0

    return [ float(s[1]), float(s[2]), float(s[3]), float(s[4]), float(s[5]), float(s[6]), float(s[7]), float(s[8]) ]

def pollCompass():
    m = "C "
    b = bytes(m, 'utf-8')
    sock.sendall(b)

    # Add sleep here
    time.sleep(0.05)

    d = sock.recv(1024)
    # print("Data", d)
    
    s = d.split()
    # print('len', len(s))
    if len(s) != 2:
        return 0

    return float(s[1])


if __name__ == "__main__":

    while True:
        motorPair(5.0, 5.0)
        time.sleep(.25)
        dist = pollSensors()
        print('-------------', dist)
        time.sleep(.25)

else:
    time.sleep(.25)



