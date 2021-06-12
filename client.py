import socket , cv2, pickle, struct

#creating socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creates a socket object
host_ip = '192.168.1.7' #taking server ip
port = 1234 #taking serverside port

#connecting to the server
client_socket.connect((host_ip,port)) 

#Sending an empty message; the QOTD service works by sending arbitrary data to the socket
data = b"" 

#Return the size of the struct (and hence of the bytes object produced by pack corresponding to the format string format.
payload_size = struct.calcsize("Q") 

while True:
    while len(data) < payload_size :
        packet = client_socket.recv(4*1024) #will read at utmost 4*1024 bytes, blocking if no information is waiting to be read.
        if not packet : break
        data+=packet
    packed_msg_size = data[:payload_size] #setting limit to payload size
    data = data[payload_size:]

    #Unpack from the buffer according to the format string format. The result is a tuple 
    msg_size = struct.unpack("Q", packed_msg_size)[0] 
    
    while len(data) < msg_size :
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data) # converting to bytes
    cv2.imshow("Recieved",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
        
client_socket.close()
