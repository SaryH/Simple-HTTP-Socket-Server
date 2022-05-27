import os.path
from socket import * #importing library
serverPort = 5000 #setting server port
serverSocket = socket(AF_INET,SOCK_STREAM) #creating socket
serverSocket.bind(('', serverPort)) #binding the socket
serverSocket.listen(1) #server is now ready to listen for 1 connection
print("Server is ready!")
counter = 0 #To skip first request, which is main.html
while True: #forever loop
    connectionSocket, addr = serverSocket.accept() #accepts the connection and creates a connection socket which is at the client's side
    state = connectionSocket.recv(1024).decode() #reads the request

    print("Connection established with: ")
    print(addr) #ip address of client
    print(state) #state of connection (displays http requests)

    x = state.split("/")
    fileName = x[1].split()[0] #gets requested file name
    print("Requesting file: "+fileName)
    flag = 0

    if not os.path.exists(fileName) and fileName != "index.html" and fileName !="HTTP" and fileName!="SortByName" and fileName!="SortByPrice": #if file is not in dir
        ftype = "Content-type: text/html\r\n"
        flag = 1 #flag used below for 404 error page
    elif (fileName == 'index.html' or fileName == "HTTP"): #skips the first request because it is http
        fileName = "main.html" #sends the main.html by default
        ftype = "Content-type: text/html\r\n"
    elif fileName == "SortByPrice":
        ftype = "Content-type: text/plain"
        fileName = "sortbyprice.txt"
    elif fileName == "SortByName":
        ftype = "Content-type: text/plain"
        fileName = "sortbyname.txt"
    elif fileName.split(".")[1] == "png": #checks the type of file requested so that an approprtiate response type is made
        ftype = "Content-type: image/png\r\n"
    elif fileName.split(".")[1] == "jpg":
        ftype = "Content-type: image/jpg\r\n"
    elif fileName.split(".")[1] == "css":
        ftype = "Content-type: text/css\r\n"
    else:
        ftype = "Content-type: text/html\r\n"
        fileName = "main.html"

    if flag == 0:
        connectionSocket.send("HTTP/1.1 200 OK\r\n") #http
        connectionSocket.send(ftype)  # declaring file type
        connectionSocket.send("\r\n")
        f = open(fileName, "rb")  # opening the file
        connectionSocket.send(f.read())  # sending the file
    elif flag == 1:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n")
        s = "<!DOCTYPE html><style>*{ transition: all 0.6s;}html { height: 100%;}body{ font-family: 'Lato', sans-serif; " \
          "color: #888; margin: 0;}#main{ display: table; width: 100%; height: 100vh; text-align: center;}.fof{ " \
          "display: table-cell; vertical-align: middle;}.fof h1{ font-size: 50px; display: inline-block; " \
          "padding-right: 12px; animation: type .5s alternate infinite;}@keyframes type{ from{box-shadow: inset -3px " \
          "0px 0px #888;} to{box-shadow: inset -3px 0px 0px transparent;}}p{text-align: center;font-weight: bold;}h2{" \
          "color: red;text-align: center;}</style><html><head><title>Error</title></head><body><div id='main'> <div " \
          "class='fof'> <h1>404! Not Found!</h1> </div></div><h2>The file is not found!</h2><p>Sary Hammad 1192698 & " \
          "Laith Sharia 1190651 from: "+str(addr)+"</p></body></html> "
        connectionSocket.send("\r\n")
        connectionSocket.send(s)
    connectionSocket.close()  # closing socket
