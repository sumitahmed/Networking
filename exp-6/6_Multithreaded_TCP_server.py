import netpack as npk
import random
import threading
import time

PORT=9999
server_ip="127.0.0.1"
ADDR=(server_ip, PORT)
client_details={}
client_id=1

def clientHandle(client_socket, addr, id):
    lock = threading.Lock()
    global client_details

    while True:
        try:
            lock.acquire()
            val=random.randint(0,100)
            npk.send_data_to_tcp_client(client_socket,val)
            print("[SEND] to client {} Data {}".format(addr, val))

            data=npk.read_data_from_tcp_client(client_socket)
            if data=="close":
                npk.close_socket_connection(client_socket)
                print("[=] TCP Client - {} requesting to close connection".format(addr))
                break
            else:
                print("[RECEV] {} from Client - {}".format(data, addr))
        except (ConnectionResetError,BrokenPipeError):
            print("[ERROR] Client - {} connection".format(addr))
            break
        finally:
            lock.release()

    client_details[id].append(time.ctime(time.time()))
    print("Closed Thread for client - {} & port - {}".format(addr[0], addr[1]))

# Step-1
server_socket=npk.create_tcp_socket()

# Step-2
npk.start_tcp_server(server_socket, ADDR)

# Step-3
print("[WAIT] Server waits for client")

while True:
    try:    
        (client_socket, addr)=npk.accept_tcp_client(server_socket)
        print('[CONNECTED] Client with IP : {} & PORT : {}'.format(addr[0], addr[1]))
        client_thread = threading.Thread(target=clientHandle, 
                                         args=(client_socket, addr, client_id), 
                                         daemon=True)
        client_thread.start()
        
        client_details[client_id]=[addr, time.ctime(time.time())]
        client_id +=1

        print("*"*100)
        for id, client_info in client_details.items():
            print(f"Client - {id} connection details - {client_info}")
        print("*"*100)
        
    except KeyboardInterrupt:
        break

print("*"*100)
for id, client_info in client_details.items():
    print(f"Client - {id} connection details - {client_info}")
print("*"*100)
npk.close_socket_connection(server_socket)