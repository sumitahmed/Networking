import netpack as npk
import random 


PORT=9999
server_ip="127.0.0.1"
ADDR=(server_ip, PORT)

# Step-1
server_socket=npk.create_udp_socket()

# Step-2
npk.start_udp_server(server_socket, ADDR)

# Step-3
print("[WAIT] Server waits for client")
(data, addr)=npk.read_data_from_udp_client(server_socket)
print('[CONNECTED] Client with IP : {} & PORT : {}'.format(addr[0], addr[1]))

while True:
    val=random.randint(0,100)
    npk.send_data_to_udp_client(server_socket, val, addr)
    print("[SEND] Data {}".format(val))

    (data, addr)=npk.read_data_from_udp_client(server_socket)
    if data=="close":
        npk.close_socket_connection(server_socket)
        print("[=] UDP Client requesting to close connection")
        break
    else:
        print("[RECEV] {}".format(data))

