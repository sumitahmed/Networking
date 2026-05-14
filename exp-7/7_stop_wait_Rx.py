import netpack as npk
import stop_wait as smn


# Settings:
PORT=9090
SERVER="127.0.0.1"
ADDR=(SERVER,PORT)

# Ste-1
rx=npk.create_udp_socket()

print('[=] Client is connecting to IP & PORT at Server side {}'.format(ADDR))

# Connect client socket object to PORT with hello message:
npk.send_data_to_udp_server(rx, "Hello", ADDR)

# Invoke reciever method:
smn.receiver(rx, ADDR)

# Close socket object:
npk.close_socket_connection(rx)




