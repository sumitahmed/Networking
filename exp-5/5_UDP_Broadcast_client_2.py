import netpack as npk
import random
import time

client_port=10999

# Step-1
client_socket=npk.create_udp_broadcast_client_timeoutsocket(client_port)


T1=time.time()
while True:
    try:
        (data, ADDR)=npk.read_data_from_udp_server(client_socket)
        print('[=] Message from server : {}'.format(data))
    except KeyboardInterrupt:
        print('Program Interrupted')
        npk.close_socket_connection(client_socket)
        break
    except:
        pass
    else:
        if data=='close':
            print('Server Closed')
            npk.close_socket_connection(client_socket)
            break   
    
    # if (time.time()-T1)>20:
    #     print('Elapsed 20 s, now close client')
    #     npk.close_socket_connection(client_socket)
    #     break



