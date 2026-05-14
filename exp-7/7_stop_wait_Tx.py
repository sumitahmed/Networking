import netpack as npk
import stop_wait as smn

# Settings:
PORT=9090
SERVER="127.0.0.1"
ADDR=(SERVER,PORT)


# Step-1:
tx=npk.create_udp_socket()

# Step-2:
npk.start_udp_server(tx, ADDR)

# Waiting for Rx to connect:
print('-'*50+'\n Tx is ready to accept client ...')

# Capture "Hello" message from client:
while True:
    (msg, addr)=npk.read_data_from_udp_client(tx)
    if msg=='Hello':
        print('[Connected] Client : {}'.format(addr))
        break

# Invoke sender method:
smn.sender(tx, addr)

# Close socket object:
npk.close_socket_connection(tx)
print('[SENDER] Process is finished')
