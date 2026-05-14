
import time
import selective_repeat_udp_module as udp
import netpack as npk


# Parameters:
m=3
N=int((2**m)/2)
SF=0
SL=SF+N-1
S=SF
frame_timeout_val=5
print('Window size is considered as : {}'.format(N))


# Data:
data_string='RCCIIT ECE@SMN'
data=[val for val in data_string]
# print(data)

# timer & ack_frame:
timer=[]
ack_frame=[]



# ========================================================
# New frame Tx method:
# ========================================================
def tx_frame(server_socket, addr):
    global data, timer, ack_frame, S
    

    ack_frame.append(0)
    # SEND data[S] via socket:
    msg=data[S]+'-'+str(S)
    npk.send_data_to_udp_client(server_socket, msg, addr)
    timer.append(time.time())
    S+=1
    print('SENT : {}'.format(msg))        

# ========================================================
# Re-Tx frame method:
# ========================================================
def retx_frame(i,server_socket, addr):
    global data, timer, ack_frame
    # global socket, addr

    ack_frame[i]=0
    # SEND data[i] via socket:
    msg=data[i]+'-'+str(i)
    npk.send_data_to_udp_client(server_socket, msg, addr)
    timer[i]=time.time()
    print('[Re-Tx] frame : {}'.format(i))
    

# ========================================================
# Main section:
# ========================================================
if __name__=='__main__':

    # START SERVER:
    server, ADDR, addr = udp.server_method()
    time.sleep(5)
    
    while True:

        if S==len(data) and sum(ack_frame)==len(data):
            # CLOSE SOCKET:
            npk.send_data_to_udp_client(server, "QUIT", addr)
            npk.close_socket_connection(server)
            print('SENDER MESSAGE : {}'.format(data_string))
            break

        # ----------------------------------
        # TX new frame section:
        if S<=SL:
            tx_frame(server, addr)
            time.sleep(1) # To creat a delay of atlest 1 sec between two succesive frames
        
        
        # Look at ACK Rx: check received msg
        # msg format : ACK-X / NACK-X
        # msg='ACK-10' means frame 10 is good and received correctly by receiver
        # msg='NACK-10' means frame 10 having trouble need retrnasmission
        
        # ----------------------------------
        try:
            (msg, addr)=npk.read_data_from_udp_client(server)
            
        except:
            pass
        else:
            msg_split=msg.split('-')
            x=int(msg_split[-1])
            print('RECV : {}'.format(msg_split))        

            if msg_split[0]=='ACK':
                # for i in range(SF,S):
                #     ack_frame[i]=1
                #     timer[i]=-1
                ack_frame[x]=1
                timer[x]=-1

                # update window position:
                for id in range(SF,len(ack_frame)):
                    if ack_frame[id]==1:
                        SF=id+1
                        SL=min(SF+N-1,len(data)-1) # Must not exceed last valid index of data
                    elif ack_frame[id]==0:
                        # print('S:{},SF:{},SL:{}'.format(S,SF,SL))
                        break
            elif msg_split[0]=='NACK':
                retx_frame(x,server, addr)

        finally:
            pass
                                    

        # ----------------------------------
        # Look at timer:
        T=time.time()
        # print('Timer Checking')
        for i in range(SF,S):
            if ack_frame[i]==0 and round((T-timer[i])>frame_timeout_val):
                print('[TIMER EXPIRES FOR FRAME : {}]'.format(i))
                retx_frame(i,server, addr)
