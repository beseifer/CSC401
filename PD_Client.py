from socket import *
import sys

serverIP = sys.argv[-2]
serverPort = int(sys.argv[-1])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))

print("Connected to the Prisoners Interrogation")

welcome = clientSocket.recv(1024).decode()

if welcome == "Server is busy with an interrogation. Try to connect again later.":
    clientSocket.close()
    print(welcome)
    exit()
else:
    print(welcome)

begin = clientSocket.recv(1024).decode()
print(begin)

response = None
while response != 'C' and response != 'B':
    response = input('Enter Cooperate(C) or Betray(B): ').strip()

clientSocket.send(response.encode())

verdict = clientSocket.recv(1024).decode()

print(verdict)

clientSocket.close()

print("Disconnecting from the Jailer server. Interrogation is over!")
