
import socket
import sys
import struct
import _thread
blocks = "c0"
# convert the UDP DNS query to the TCP DNS query
def getTcpQuery(query):
    """print ( "query")
    print ( query)
    print (len(query))
    print (len(query).to_bytes(2, byteorder='big'))"""
    message = ((len(query)).to_bytes(2, byteorder='big')) + query
    """print ("msg=")
    print (message)"""
    return message

# send a TCP DNS query to the upstream DNS server
def sendTCP(DNSserverIP, query):
    server = (DNSserverIP, 53)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server)
    tcp_query = getTcpQuery(query)
    sock.send(tcp_query)  	
    data = sock.recv(1024)
    return data

# a new thread to handle the UPD DNS request to TCP DNS request
def handler(data, addr, socket, DNSserverIP):
    #print ("Request from client: ", data.encode("hex"), addr)
    TCPanswer = sendTCP(DNSserverIP, data)
    
    #print ("TCP Answer from server init: ", TCPanswer.hex())
    print (TCPanswer)
    """decoupe bastien"""
    chaine = TCPanswer.hex()
    i=0
    prefixe=""

    c = True
    tcp = []
    laliste=[]
    while (i<len(chaine)):
        x=chaine[i]+chaine[i+1]
        if(x!="c0"):
            if i == 18:
                x = "01"
            prefixe=prefixe + x
            
        else:
            #print (prefixe)
            tcp.append(prefixe+ "c0")
            prefixe=""
            
        #print(x)
        i=i+2
        
        


    #print (prefixe)
    prefixe=(prefixe[2:])
    prefixe = "0c" + prefixe
    print (prefixe)
    tcp.append(prefixe)
    laliste.append(tcp[0])
    laliste.append(tcp[-1])
    #print(laliste)
    final=''.join(laliste)
    str_val=final.encode("utf-8")
    print ("final= " , final)
    print()
    
    TCPanswer=bytes.fromhex(final)
    #print ("TCP Answer from server final: ", TCPanswer.hex())
    #print (TCPanswer[:6])
    print (TCPanswer)
    #print ((TCPanswer[11:])[:6])
    UDPanswer = (TCPanswer[2:])
    #print "UDP Answer: ", UDPanswer.encode("hex")
    socket.sendto(UDPanswer, addr)
    
    """if TCPanswer:
        rcode = TCPanswer[:6]
        rcode = rcode[11:]
        print ("RCODE: ", rcode)
        if (int(rcode, 16) == 1):
            print ("Request is not a DNS query. Format Error!")
        else:
            print ("Success!")
            UDPanswer = TCPanswer[2:]
            #print "UDP Answer: ", UDPanswer.encode("hex")
            socket.sendto(UDPanswer, addr)
    else:
        print ("Request is not a DNS query. Format Error!")"""

if __name__ == '__main__':
    DNSserverIP = sys.argv[1]
    port = int(sys.argv[2])
    host = '127.0.0.1'
    try:
        # setup a UDP server to get the UDP DNS request
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        while True:
            data, addr = sock.recvfrom(1024)
            _thread.start_new_thread(handler, (data, addr, sock, DNSserverIP))
    except Exception as e:
        print (e)
        sock.close()