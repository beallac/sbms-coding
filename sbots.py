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

