import netpack as npk
import random 


PORT=9999
client_ip="127.0.0.1"

server_ip=client_ip
ADDR=(server_ip, PORT)

# Step-1
client_socket=npk.create_udp_socket()

# Step-2
npk.send_data_to_udp_server(client_socket, "Hello", ADDR)
print('[CONNECTED] Server with IP : {} & PORT : {}'.format(ADDR[0], ADDR[1]))

while True:
    (data, ADDR)=npk.read_data_from_udp_server(client_socket)
    print('[=] Message from server : {}'.format(data))

    flag=input('Close connection y/n : ')
    if flag=='y' or flag=='Y':
        npk.send_data_to_udp_server(client_socket, "close", ADDR)
        npk.close_socket_connection(client_socket)
        print("[=] Requested for closing connection")
        break
    else:
        npk.send_data_to_udp_server(client_socket, "+ACK", ADDR)

    

