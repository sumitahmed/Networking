'''
This module contains stop & wait protocol methods
'''

import time
import netpack as npk

data='RCCIIT ECE'
frame_data=[i for i in data]
ack_data='ACK'

# Sender Method:
def sender(tx_socket,rx_addr):
    global frame_data
    global ack_data

    for msg in frame_data:
        time.sleep(1)
        # Tx frame :
        npk.send_data_to_udp_client(tx_socket, msg, rx_addr)
        print('[SENT] frame data - [{}]'.format(msg))

        # Wait to Rx ACK frame:
        while True:

            (msg_rx, addr)=npk.read_data_from_udp_client(tx_socket)
            if msg_rx==ack_data:
                print('[ACK] Recieved for - [{}]'.format(msg))
                break

    # Tx NULL character to end connection:
    npk.send_data_to_udp_client(tx_socket,'\0',rx_addr)

    print('Terminate communication.')
    return


# Receiver Method:
def receiver(rx_socket, tx_ADDR):
    global ack_data
    rx_frame=[]

    while True:
        # Rx frame :
        (msg_rx, ADDR)=npk.read_data_from_udp_server(rx_socket)
        
        if msg_rx=='\0':
            print('Communication terminated')
            break
        else:
            rx_frame.append(msg_rx)
        print('[RECV] frame data - [{}]'.format(msg_rx))

        # Tx ACK frame :
        npk.send_data_to_udp_server(rx_socket, ack_data, tx_ADDR)        
        print('[SENT] Ack frame')
    
    print("[=] Received Data :")
    for i in rx_frame:
        print('{}'.format(i),end='')
    print("\n")
    return









