import random
import time
import selective_repeat_udp_module as udp
import netpack as npk

# Parameters:
m=3
N=int((2**m)/2)
R=0
count=0
print('Window size is considered as : {}'.format(N))

# Data:
data=[]
buffer=[0 for i in range(N)]

# ========================================================
# Generate rando flag: 0-Normal, 1-Frame lost, 2-ACK lost
# ========================================================
def generateFlag():
    val=random.randint(0,100)
    if val<30 and val>=0:
        return 0
    elif val<80 and val>=30:
        return 1
    else:
        return 2

# ========================================================
# Wait random time : Multiple of 100 ms 
# min 0 sec & max 1 sec
# ========================================================
def wait():
    cnt=random.randint(0,10)
    for _ in range(cnt):
        time.sleep(0.1)

# ========================================================
# Send ACK:
# ========================================================
def send_ack(i, client_socket, ADDR):
    # SEND MSG='ACK-'+str(i) to Socket
    msg='ACK-'+str(i)
    npk.send_data_to_udp_server(client_socket, msg, ADDR)
    print('SENT : {}'.format(msg))  
    
# ========================================================
# Send nACK:
# ========================================================
def send_nack(i,client_socket, ADDR):
    # SEND MSG='NACK-'+str(i) to Socket
    msg='NACK-'+str(i)
    npk.send_data_to_udp_server(client_socket, msg, ADDR)
    print('SENT : {}'.format(msg))  

# ========================================================
# Store received msg to data list:
# ========================================================
def storedata(value,i, client_socket, ADDR): # this is called only when valid frames are received
    global R, N
        
    # Modified part
    if R==i:
        data.append(value)
        R+=1
    elif R<i: # Frame gap means frame lost
        lost_frame_cnt=i-R # lost frame counts
        for id in range(lost_frame_cnt):
            send_nack(R+id, client_socket, ADDR)
            data.append('') 
        data.append(value)
        R=i+1
    else:
        data[i]=value
    
    print('[=] Received buffer : {}'.format(data))

# ========================================================
# Printing received data:
# ========================================================
def print_data():
    global data
    data_string=''
    print(data)
    for i in data:
        data_string+=i
    return data_string

# ========================================================
# Main section:
# ========================================================
if __name__=='__main__':

    # START CLIENT:
    client, ADDR = udp.client_method()
    time.sleep(5)
    
    while True:

        # -------------------------
        try:
            (msg, ADDR)=npk.read_data_from_udp_server(client)
        except:
            pass
        else:
                        
            # CLOSE SOCKET
            if msg=='QUIT':
                client.close()
                print('RECEIVED MESSAGE : {}'.format(print_data()))
                break

            msg_split=msg.split('-')
            print('-'*50)
            print('RECV : {}'.format(msg_split))        
            x=int(msg_split[-1])
            val=msg_split[0]

            # -------------------------
            flag=generateFlag()
            # flag=0
            # -------------------------

            # -------------------------
            if flag==0: # Normal case : ACK
                print('RECV OK')
                storedata(val,x, client, ADDR)
                send_ack(x, client, ADDR)
                wait()
            elif flag==2: # ACK lost
                print('ACK LOST')
                storedata(val,x, client, ADDR)
            else: # Frame lost case : NACK 
                print('FRAME LOST')
                
        finally:
            pass
        