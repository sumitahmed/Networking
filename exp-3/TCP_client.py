import netpack as npk

PORT=9999
client_ip="127.0.0.1"

server_ip=client_ip
ADDR=(server_ip, PORT)


# Step-1
client_socket=npk.create_tcp_socket()

# Step-2
npk.connect_to_tcp_server(client_socket, ADDR)
print('[CONNECTED] Server with IP : {} & PORT : {}'.format(ADDR[0], ADDR[1]))

while True:
    data=npk.read_data_from_tcp_server(client_socket)
    print('[=] Message from server : {}'.format(data))

    flag=input('Close connection y/n : ')
    if flag=='y' or flag=='Y':
        npk.send_data_to_tcp_server(client_socket,"close")
        npk.close_socket_connection(client_socket)
        print("[=] Requested for closing connection")
        break
    else:
        npk.send_data_to_tcp_server(client_socket,"+ACK")


