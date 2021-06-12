import socket, cv2, pickle, struct

#creating socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip )
socket_address = ('', 1234)

#socket binding
server_socket.bind(socket_address)

#socket listening
server_socket.listen(5)
print("LISTENING AT:",socket_address)

#socket accept
while True:
    client_socket,addr = server_socket.accept()
    print('GOT CONNECTION FROM: ',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            img, frame = vid.read()#returns true or false if the frame is read correctly
            a = pickle.dumps(frame) #serialize the frame in bytes
            message = struct.pack("Q", len(a))+a  #packs message and returns in bytes according to string format 
            client_socket.sendall(message)#sendall send all data 
            cv2.imshow('TRASMITTING VIDEO', frame)#shows video
            key = cv2.waitKey(1) & 0xFF 
            if key == ord('q'):
                client_socket.close()     
                
