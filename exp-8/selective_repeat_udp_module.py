'''
[This module used to setup UDP Server & Client sockets]
-------------------------------------------------------
Methods:
[1] server_method()
[2] client_method()
'''
import netpack as npk

# Global Parameters:
SERVER_PORT=9090
SERVER_IP="127.0.0.1"
ADDR=(SERVER_IP, SERVER_PORT)
timeout_val=0.1

# ========================================================
# Server Connection setup
# ========================================================
def server_method():
    '''
    --------------------------
    server_method() returns - 
    --------------------------
    [1] Server socket
    [2] ADDR : (server_ip, server_port)
    [3] addr : (client_ip, client_port)
    '''
    global ADDR, timeout_val

    server_socket=npk.create_udp_timeoutsocket(timeout_val)
    
    npk.start_udp_server(server_socket, ADDR)
    print('[=] UDP Server is starting at : {}'.format(ADDR))

    print('-'*50)
    print('[=] Server waits for connection ...')

    while True:
        try:
            (msg, addr)=npk.read_data_from_udp_client(server_socket)
        except:
            pass
        else:
            npk.send_data_to_udp_client(server_socket, "OK", addr)
            print('[CONNECTED] Client {}'.format(addr))        
            break
        finally:
            pass

    return server_socket, ADDR, addr
        
    
# ========================================================
# Client Connection setup
# ========================================================
def client_method():
    '''
    --------------------------
    client_method() returns - 
    --------------------------
    [1] Client socket
    [2] ADDR : (server_ip, server_port)
    '''
    global ADDR, timeout_val

    client_socket=npk.create_udp_timeoutsocket(timeout_val)
    
    npk.send_data_to_udp_server(client_socket, "HELLO", ADDR)
    # print('[=] Client is connecting to Server {}'.format(ADDR))

    while True:
        try:
            (msg, ADDR) = npk.read_data_from_udp_server(client_socket)
        except:
            pass
        else:
            if msg=='OK':
                print('[CONNECTED] Server : {}'.format(ADDR))
                break
        finally:
            pass

    return client_socket, ADDR
